from kivy.uix.boxlayout import BoxLayout
from popups import ModbusPopup, ScanPopup, MonitoramentoPopup, MonitoraTemperatura, MonitoraCompressor, DataGraphPopup, HistGraphPopup
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
from pymodbus.constants import Endian
from pyModbusTCP.client import ModbusClient
from kivy.core.window import Window
from threading import Thread
from time import sleep
from utils import Units, ModbusType
from datetime import datetime
import random
from models import DadoVentilador
from db import Session, Base, engine

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
        self._meas = {}
        self._meas["timestamp"] = None
        self._meas["values"] = {}
        Base.metadata.create_all(engine)
        self._session = Session()

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
            else:
                self._meas["values"][key] = self._modbusClient.read_holding_registers(value.addr,1)[0]/value.divisor

                


    def readFloat(self, addr):
        result = self._modbusClient.read_holding_registers(addr, 2)
        decoder = BinaryPayloadDecoder.fromRegisters(result, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
        return decoder.decode_32bit_float()

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
            data = DadoVentilador(**self._meas["values"])
            self._session.add(data)
            self._session.commit()
        except Exception as e:
            print(e)