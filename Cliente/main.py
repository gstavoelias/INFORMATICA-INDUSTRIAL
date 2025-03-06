from datetime import datetime
from pyModbusTCP.client import ModbusClient
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
from pymodbus.constants import Endian
import json

class MainWidget():
    def __init__(self, server_ip, porta):
        self._cliente = ModbusClient(host=server_ip,port = porta)
        self.modbus_addrs =  {
            "tit02": 1218,
            "tit01": 1220,
            "pit02": 1222,
            "pit01": 1224,
            "pit03": 1226,
            "temperatura": 710,
            "velocidade": 712,
            "vazao": 714
        }
        self.tags = { key: {"addr": value, "color": None} for key, value in self.modbus_addrs.items()}
        self.measures = {"timestamp": None, "values": {}}
        
    def readData(self):
        self.measures["timestamp"] = datetime.now().isoformat()
        for key, value in self.tags.items():
            self.measures["values"][key] = self.readFloat(value["addr"])

    def readFloat(self, addr):
        result = self._cliente.read_holding_registers(addr, 2)
        decoder = BinaryPayloadDecoder.fromRegisters(result, byteorder=Endian.BIG, wordorder=Endian.BIG)
        return decoder.decode_32bit_float()

    def displayData(self):
        with open("results.txt", "w") as f:
            json.dump(self.measures, f, indent=4)
    

app = MainWidget("localhost", 502)
app.readData()
app.displayData()
