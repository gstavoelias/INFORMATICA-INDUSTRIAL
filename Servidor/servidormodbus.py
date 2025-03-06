from pyModbusTCP.server import DataBank, ModbusServer
from time import sleep
import random
from pymodbus.payload import BinaryPayloadBuilder
import struct

class ServidorMODBUS():
    """
    Classe Servidor MODBUS
    """
    def __init__(self, host_ip, port):
        self._server = ModbusServer(host=host_ip, port=port, no_block=True)
    
    def float_to_payload(self, value):
        builder = BinaryPayloadBuilder(byteorder="big", wordorder="big")
        builder.add_32bit_float(value)
        return builder.to_registers()

    def run(self):
        self._server.start()
        print("Servidor em execução")
        while True:
            tit01 = self.float_to_payload(random.uniform(18.0, 30.0))
            tit02 = self.float_to_payload(random.uniform(18.0, 30.0))
            pit01 = self.float_to_payload(random.uniform(-5.0, 5.0))
            pit02 = self.float_to_payload(random.uniform(-5.0, 5.0))
            pit03 = self.float_to_payload(random.uniform(-5.0, 5.0))
            temperatura = self.float_to_payload(random.uniform(18.0, 30.0))
            velocidade = self.float_to_payload(random.uniform(0.0, 50.0))
            vazao = self.float_to_payload(random.uniform(0.0, 100.0))

            self._server.data_bank.set_holding_registers(1220, tit01) 
            self._server.data_bank.set_holding_registers(1218, tit02)  
            self._server.data_bank.set_holding_registers(1224, pit01)  
            self._server.data_bank.set_holding_registers(1222, pit02)  
            self._server.data_bank.set_holding_registers(1226, pit03)  
            self._server.data_bank.set_holding_registers(710, temperatura)  
            self._server.data_bank.set_holding_registers(712, velocidade)  
            self._server.data_bank.set_holding_registers(714, vazao)  

            sleep(1)

# Exemplo de uso
if __name__ == "__main__":
    servidor = ServidorMODBUS('127.0.0.1', 502)
    servidor.run()
