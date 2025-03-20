from kivy.uix.boxlayout import BoxLayout
from popups import ModbusPopup, ScanPopup, MonitoramentoPopup, MonitoraTemperatura, MonitoraCompressor, DataGraphPopup, HistGraphPopup, ComandoPopup, ComandoCOPopup
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
from pymodbus.constants import Endian
from pyModbusTCP.client import ModbusClient
from kivy.core.window import Window
from threading import Thread, Lock
from time import sleep
from utils import Units, ModbusType
from datetime import datetime
from kivy_garden.graph import LinePlot
import random
from models import DadoVentilador
from db import Session, Base, engine
import time

class MainWidget(BoxLayout):

    _updateThread = None
    _updateWidgets = True
    _tags = {}
    max_points = 20

    def __init__(self, **kwargs):
        super().__init__()
        self._scan_time = kwargs.get('scan_time')
        self._serverIP = kwargs.get("server_ip")
        self._serverPort = kwargs.get("server_port")
        self._tags = kwargs.get("modbus_addrs")
        self._modbusPopup = ModbusPopup(self._serverIP, self._serverPort)
        self._scanPopup = ScanPopup(scantime=self._scan_time)
        self._modbusClient = ModbusClient(host=self._serverIP, port=self._serverPort)
        self._monitoramentoPopup = MonitoramentoPopup()
        self._monitoraTemperatura = MonitoraTemperatura()
        self._monitoraCompressor = MonitoraCompressor()
        self._graph = DataGraphPopup(self.max_points, (1,0,0,1))
        self._hgraph = HistGraphPopup(tags=self._tags)
        self._co_motor = ComandoPopup()
        self._co_compressor = ComandoCOPopup()
        self._meas = {}
        self._meas["timestamp"] = None
        self._meas["values"] = {}
        Base.metadata.create_all(engine)
        self._session = Session()
        self._tipo_partida = None
        self.lock = Lock()


    def startDataRead(self, ip, port):
        self._serverIP = ip
        self._serverPort = port
        self._modbusClient.host = self._serverIP
        self._modbusClient.port = self._serverPort 
        try:
            Window.set_system_cursor("wait")
            self._modbusClient.open()
            Window.set_system_cursor("arrow")
            if self._modbusClient.is_open:
                self._updateThread = Thread(target=self.updater)
                self._updateThread.start()
                self.ids.img_con.source = "assets/conectado.png"
                self._modbusPopup.dismiss()
            else:
                self._modbusPopup.setInfo("Falha na conexão com o servidor.")
        except Exception as e:
            print("Erro: ", e.args)


    def updater(self):
        try:
            while self._updateWidgets:
                self.readData()
                self.updateGUI()
                self.updateDB()
                sleep(self._scan_time/1000)
        except Exception as e:
            self._modbusClient.close()
            print("Erro: ", e.args)


    def readData(self):
        self._meas["timestamp"] = datetime.now()
        for key, value in self._tags.items():
            if value.modbus_type == ModbusType.FP:
                self._meas["values"][key] = self.readFloat(value.addr)/value.divisor
            elif value.modbus_type == ModbusType.INT_16:
                self._meas["values"][key] = self.readInt(value.addr)/value.divisor
            else:
                self._meas["values"][key] = self._modbusClient.read_holding_registers(value.addr,1)[0]/value.divisor

                


    def readFloat(self, addr):
        result = self._modbusClient.read_holding_registers(addr, 2)
        decoder = BinaryPayloadDecoder.fromRegisters(result, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
        return decoder.decode_32bit_float()
    
    def readInt(self, addr):
        result = self._modbusClient.read_holding_registers(addr, 1)
        decoder = BinaryPayloadDecoder.fromRegisters(result, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
        return decoder.decode_16bit_int()
    
    def writeHoldingRegister(self, addr, value):
        self._modbusClient.write_single_register(addr, value)

    def writeSingleCoil(self, addr, value):
        self._modbusClient.write_single_coil(addr, value)

    def open_graph(self, variable_name="temperatura"):
        """Abre o gráfico correspondente à variável clicada."""
        try:
            if variable_name in self._meas["values"]:
                self._graph.ids.graph.clearPlots()
                plot_color = (1, 0, 0, 1)  # Define uma cor (vermelho, por exemplo)

                # Criando o gráfico para a variável correspondente
                p = LinePlot(line_width=1.5, color=plot_color)
                timestamps = [self._meas["timestamp"]]
                valores = [self._meas["values"][variable_name]]

                p.points = [(i, val) for i, val in enumerate(valores)]
                self._graph.ids.graph.add_plot(p)

                # Atualiza e exibe o gráfico
                self._graph.ids.graph.xmax = len(valores)
                self._graph.ids.graph.update_x_labels(timestamps)
                self._graph.open()
            else:
                print(f"Variável '{variable_name}' não encontrada nos dados.")
        except Exception as e:
            print(f"Erro ao abrir o gráfico: {e}")



    def tipoPartida(self, tipo_partida):
        try:
            comando = 2 if tipo_partida == "INVERSOR" else 1 if tipo_partida == "SOFT-START" else 3
            self.writeHoldingRegister(1324, comando)
            self.tipo_partida = tipo_partida

        except Exception as e:
            print(f"aqui: {e}")

    def acionaMotor(self, comando):
        addr = 1312 if self.tipo_partida == "INVERSOR" else 1316 if self.tipo_partida == "SOFT-START" else 1319
        self.writeHoldingRegister(addr, int(comando))
    
    def setRampa(self, value):
        self.writeHoldingRegister(1314, int(value)*10)
        time.sleep(0.5)
        self.writeHoldingRegister(1315, int(value)*10)

    #TENTATIVA DE ACIONAMENTO DOS COMPRESSORES#

    def tipoPartidaCO(self, tipo_partida):
        try:
            comando = 1 if tipo_partida == "HERMÉTICO" else 0 
            self.writeHoldingRegister(1328, comando)
            self.tipo_partida = tipo_partida
        except Exception as e:
            print(f"aqui: {e}")

    def acionaCompressor(self, comando):
        addr = 1328 
        self.writeHoldingRegister(addr, int(comando))

    def setRampaCO(self, value):
        self.writeHoldingRegister(1236, int(value)*10)
        time.sleep(0.5)
        self.writeHoldingRegister(1236, int(value)*10)
                
    #FIM DA TENTATIVA#



    def updateGUI(self):
        
        for key, value in self._tags.items():
            for widget in [self, self._monitoraTemperatura, self._monitoraCompressor, self._monitoramentoPopup]:
                if isinstance(widget, value.root_widget):
                    widget.ids[key].text = "{:.2f}".format(self._meas["values"][key]) + value.unit
                    break 
        
        self._graph.ids.graph.updateGraph((self._meas["timestamp"], self._meas["values"]["temperatura"]), 0)

    def stopRefresh(self):
        self._updateWidgets = False


    def updateDB(self):
        try:
            self._meas["values"]["timestamp"] = self._meas["timestamp"]
            data = DadoVentilador(**self._meas["values"])
            self._session.add(data)
            self._session.commit()
        except Exception as e:
            print(e)



    def getDataDB(self):
        init_t = self.parseDTString(self._hgraph.ids.txt_init_time.text)
        final_t = self.parseDTString(self._hgraph.ids.txt_final_time.text)
        cols = []
        for sensor in self._hgraph.ids.sensores.children:
            if sensor.ids.checkbox.active:
                cols.append(sensor.id)
        if init_t is None or final_t is None or len(cols)==0:
            return 
        cols.append("timestamp")
        
        try:
            dados = self.acesso_dados_historicos(init_t, final_t)
            print(dados)
            
            if not dados or len(dados) == 0:
                return

            self._hgraph.ids.graph.clearPlots()
            
            # Garante que 'timestamp' está presente
            if "timestamp" not in dados[0]:
                print("Erro: 'timestamp' não encontrado nos dados.")
                return

            # Converte timestamps
            # timestamps = [datetime.strptime(item["timestamp"], "%Y-%m-%d %H:%M:%S.%f") for item in dados]
            timestamps = [item["timestamp"] for item in dados]
            for key in dados[0].keys():
                if key not in cols or key == "timestamp":
                    continue

                plot_color = (random.random(), random.random(), random.random(), 1)
                p = LinePlot(line_width=1.5, color=plot_color)

                # Mapeia os valores da chave `key` em relação aos índices dos timestamps
                p.points = [(i, item[key]) for i, item in enumerate(dados) if key in item]

                self._hgraph.ids.graph.add_plot(p)

            self._hgraph.ids.graph.xmax = len(timestamps)
            self._hgraph.ids.graph.update_x_labels(timestamps)

        except Exception as e:
            print(f"Erro ao carregar gráfico: {e}")

    
    def parseDTString(self, datetime_str):
        try:
            print(datetime_str)
            d = datetime.strptime(datetime_str, '%d/%m/%Y %H:%M:%S')
            return d.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            print("aqui")
            print("Erro: ", e.args)

    def acesso_dados_historicos(self,init_t, final_t): 
        # with self.lock:
        try:
            result = self._session.query(DadoVentilador).filter(DadoVentilador.timestamp.between(init_t,final_t)).all()
            return [col.get_attr_printable_dict() for col in result]
        except Exception as e:
            print("Erro: ", e.args)




