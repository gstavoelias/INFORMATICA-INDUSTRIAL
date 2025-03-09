from kivy.app import App
from mainwidget import MainWidget
from kivy.lang.builder import Builder

class MainApp(App):

    def build(self):
        self._widget = MainWidget(scan_time=1000, server_ip="127.0.0.1", server_port=502, 
        modbus_addrs = {
            "encoder_axial": 884,
            "torque_axial": 1424,
            "tit02": 1218,
            "tit01": 1220,
            "pit02": 1222,
            "pit01": 1224,
            "pit03": 1226,
            "temperatura": 710,
            "velocidade": 712,
            "vazao": 714
        })
        
        return self._widget
    


if __name__ == "__main__":
    Builder.load_string(open("mainwidget.kv", encoding="utf-8").read(), rulesonly=True)
    Builder.load_string(open("popups.kv", encoding="utf-8").read(), rulesonly=True)
    MainApp().run()