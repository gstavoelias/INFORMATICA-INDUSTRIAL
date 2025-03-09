from kivy.uix.boxlayout import BoxLayout
from popups import ModbusPopup, ScanPopup
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
from pymodbus.constants import Endian
from pyModbusTCP.client import ModbusClient
from kivy.core.window import Window
from threading import Thread
from time import sleep
from datetime import datetime
import random

class MainWidget(BoxLayout):

    _updateThread = None
    _updateWidgets = True
    _tags = {}
    def __init__(self, **kwargs):
        super().__init__()
        self._scan_time = kwargs.get('scan_time')
        self._serverIP = kwargs.get("server_ip")
        self._serverPort = kwargs.get("server_port")
        self._modbusPopup = ModbusPopup(self._serverIP, self._serverPort)
        self._scanPopup = ScanPopup(scantime=self._scan_time)
        self._modbusClient = ModbusClient(host=self._serverIP, port=self._serverPort)
        self._meas = {}
        self._meas["timestamp"] = None
        self._meas["values"] = {}
        for key, value in kwargs.get("modbus_addrs").items():
            if key == "encoder_axial":
                unit = " RPM"
            elif key == "torque_axial":
                unit = " N.m"
            elif str(key).startswith("pit"):
                unit = " psi"
            elif str(key).startswith("tit") or key == "temperatura":
                unit = " °C"
            elif key == "vazao":
                unit = " m³/h"
            elif key == "velocidade":
                unit = " m/s"
            else:
                unit = " ?"
            plot_color = (random.random(), random.random(), random.random(), 1)
            self._tags[key] = {"addr": value, "color": plot_color, "unit": unit}

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
                print("a")
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
                sleep(self._scan_time/1000)
        except Exception as e:
            self._modbusClient.close()
            print("Erro: ", e.args)


    def readData(self):
        self._meas["timestamp"] = datetime.now()
        for key, value in self._tags.items():
            self._meas["values"][key] = self.readFloat(value["addr"])

    def readFloat(self, addr):
        result = self._modbusClient.read_holding_registers(addr, 2)
        decoder = BinaryPayloadDecoder.fromRegisters(result, byteorder=Endian.BIG, wordorder=Endian.BIG)
        return decoder.decode_32bit_float()

    def updateGUI(self):
        for key, value in self._tags.items():
            self.ids[key].text = "{:.2f}".format(self._meas["values"][key]) + value["unit"]
