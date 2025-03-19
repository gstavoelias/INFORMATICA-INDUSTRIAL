from kivy.app import App
from mainwidget import MainWidget
from kivy.lang.builder import Builder
from utils import Units, ModbusType
from popups import *

class Tag:
    def __init__(self, addr : int, modbus_type: str, unit: str, divisor : int = 1, root_widget: type = MainWidget) -> None:
        self.addr = addr
        self.modbus_type = modbus_type
        self.unit = unit.value
        self.divisor = divisor
        self.root_widget= root_widget

class MainApp(App):
    def build(self) -> None:
        
        self._widget = MainWidget(
            scan_time=1000,
            server_ip="127.0.0.1", 
            server_port=502, 
            modbus_addrs = {
                "encoder_axial": Tag(addr=884, modbus_type=ModbusType.FP, unit=Units.ROTATION),
                "torque_axial": Tag(addr=1424, modbus_type=ModbusType.FP, unit=Units.TORQUE),
                "tit02": Tag(addr=1218, modbus_type=ModbusType.FP, unit=Units.TEMPERATURE, divisor=10),
                "tit01": Tag(addr=1220, modbus_type=ModbusType.FP, unit=Units.TEMPERATURE, divisor=10),
                "pit02": Tag(addr=1222, modbus_type=ModbusType.FP, unit=Units.PRESSURE, divisor=10),
                "pit01": Tag(addr=1224, modbus_type=ModbusType.FP, unit=Units.PRESSURE, divisor=10),
                "pit03": Tag(addr=1226, modbus_type=ModbusType.FP, unit=Units.PRESSURE, divisor=10),
                "temperatura": Tag(addr=710, modbus_type=ModbusType.FP, unit=Units.TEMPERATURE),
                "velocidade": Tag(addr=712, modbus_type=ModbusType.FP, unit=Units.SPEED),
                "vazao": Tag(addr=714, modbus_type=ModbusType.FP, unit=Units.FLOW),
                "temp_r": Tag(addr=700, modbus_type=ModbusType.FP, unit=Units.TEMPERATURE, divisor=10, root_widget=MonitoraTemperatura),
                "temp_s": Tag(addr=702, modbus_type=ModbusType.FP, unit=Units.TEMPERATURE, divisor=10, root_widget=MonitoraTemperatura),
                "temp_t": Tag(addr=704, modbus_type=ModbusType.FP, unit=Units.TEMPERATURE, divisor=10, root_widget=MonitoraTemperatura),
                "temp_carc": Tag(addr=706, modbus_type=ModbusType.FP, unit=Units.TEMPERATURE, divisor=10, root_widget=MonitoraTemperatura),
                "tensao_rs_co": Tag(addr=732, modbus_type=ModbusType.HOLDING_REGISTER, unit=Units.VOLTAGE, divisor=10, root_widget=MonitoraCompressor),
                "tensao_st_co": Tag(addr=733, modbus_type=ModbusType.HOLDING_REGISTER, unit=Units.VOLTAGE, divisor=10, root_widget=MonitoraCompressor),
                "tensao_tr_co": Tag(addr=734, modbus_type=ModbusType.HOLDING_REGISTER, unit=Units.VOLTAGE, divisor=10, root_widget=MonitoraCompressor),
                "corrente_r_co": Tag(addr=726, modbus_type=ModbusType.HOLDING_REGISTER, unit=Units.CURRENT, divisor=10, root_widget=MonitoraCompressor),
                "corrente_s_co": Tag(addr=727, modbus_type=ModbusType.HOLDING_REGISTER, unit=Units.CURRENT, divisor=10, root_widget=MonitoraCompressor),
                "corrente_t_co": Tag(addr=728, modbus_type=ModbusType.HOLDING_REGISTER, unit=Units.CURRENT, divisor=10, root_widget=MonitoraCompressor),
                "corrente_n_co": Tag(addr=729, modbus_type=ModbusType.HOLDING_REGISTER, unit=Units.CURRENT, divisor=10, root_widget=MonitoraCompressor),
                "corrente_media_co": Tag(addr=731, modbus_type=ModbusType.HOLDING_REGISTER, unit=Units.CURRENT, divisor=10, root_widget=MonitoraCompressor),
                "ativa_r_co": Tag(addr=735, modbus_type=ModbusType.HOLDING_REGISTER, unit=Units.POWER, root_widget=MonitoraCompressor),
                "ativa_s_co": Tag(addr=736, modbus_type=ModbusType.HOLDING_REGISTER, unit=Units.POWER, root_widget=MonitoraCompressor),
                "ativa_t_co": Tag(addr=737, modbus_type=ModbusType.HOLDING_REGISTER, unit=Units.POWER, root_widget=MonitoraCompressor),
                "ativa_total_co": Tag(addr=738, modbus_type=ModbusType.HOLDING_REGISTER, unit=Units.POWER, root_widget=MonitoraCompressor),
                "reativa_r_co": Tag(addr=739, modbus_type=ModbusType.INT_16, unit=Units.POWER,root_widget=MonitoraCompressor),
                "reativa_s_co": Tag(addr=740, modbus_type=ModbusType.INT_16, unit=Units.POWER, root_widget=MonitoraCompressor),
                "reativa_t_co": Tag(addr=741, modbus_type=ModbusType.INT_16, unit=Units.POWER, root_widget=MonitoraCompressor),
                "reativa_total_co": Tag(addr=742, modbus_type=ModbusType.INT_16, unit=Units.POWER, root_widget=MonitoraCompressor),
                "aparente_r_co": Tag(addr=743, modbus_type=ModbusType.HOLDING_REGISTER, unit=Units.POWER, root_widget=MonitoraCompressor),
                "aparente_s_co": Tag(addr=744, modbus_type=ModbusType.HOLDING_REGISTER, unit=Units.POWER, root_widget=MonitoraCompressor),
                "aparente_t_co": Tag(addr=745, modbus_type=ModbusType.HOLDING_REGISTER, unit=Units.POWER,root_widget=MonitoraCompressor),
                "aparente_total_co": Tag(addr=746, modbus_type=ModbusType.HOLDING_REGISTER, unit=Units.POWER, root_widget=MonitoraCompressor)
            })
        return self._widget
    

    def on_stop(self):
        self._widget.stopRefresh()
    


if __name__ == "__main__":
    Builder.load_string(open("mainwidget.kv", encoding="utf-8").read(), rulesonly=True)
    Builder.load_string(open("popups.kv", encoding="utf-8").read(), rulesonly=True)
    MainApp().run()