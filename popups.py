from kivy.uix.popup import Popup
from kivy.uix.label import Label


class ModbusPopup(Popup):
    _info_lb = None
    def __init__(self, server_ip, server_port, **kwargs):
        super().__init__(**kwargs)
        self.ids.txt_ip.text = str(server_ip)
        self.ids.txt_porta.text = str(server_port)

    def setInfo(self, message):
        self._info_lb = Label(text=message)
        self.ids.layout.add_widget(self._info_lb)

    def clearInfo(self):
        if self._info_lb is not None:
            self.ids.layout.remove_widget(self._info_lb)

class ScanPopup(Popup):
    def __init__(self, scantime, **kwargs):
        super().__init__(**kwargs)
        self.ids.txt_st.text = str(scantime)

class ComandoPopup(Popup):
    """
    Popup da janela dos comandos da planta
    """
    popup = Popup()

    popup.open()


class MonitoramentoPopup(Popup):
    """
    Popup da janela de monitoramento da planta
    """
    popup = Popup()

    popup.open()

class MonitoraTemperatura(MonitoramentoPopup):
    """
    Popup da janela de monitoramento da tensão
    """
    pass

class MonitoraTensao(MonitoramentoPopup):
    """
    Popup da janela de monitoramento da tensão
    """
    pass

class MonitoraCorrente(MonitoramentoPopup):
    """
    Popup da janela de monitoramento da tensão
    """
    pass

class MonitoraPotencias(MonitoramentoPopup):
    """
    Popup da janela de monitoramento da tensão
    """
    pass