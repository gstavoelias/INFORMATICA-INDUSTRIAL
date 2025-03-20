from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from timeseriesgraph import TimeSeriesGraph
from kivy_garden.graph import LinePlot

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

class MonitoraCompressor(MonitoramentoPopup):
    """
    Popup da janela de monitoramento da tensão
    """
    pass

class DataGraphPopup(Popup):
    def __init__(self, xmax, plot_color, **kwargs):
        super().__init__(**kwargs)
        self.plot = LinePlot(line_width=1.5, color=plot_color)
        self.ids.graph.add_plot(self.plot)
        self.ids.graph.xmax = xmax

class LabeledCheckBoxDataGraph(BoxLayout):
    pass


class HistGraphPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__()
        
        # Criar CheckBoxes para os sensores dentro do ScrollView
        for key, value in kwargs.get("tags", {}).items():
            cb = LabeledCheckBoxHistGraph()
            cb.ids.label.text = key
            cb.ids.label.color = (1, 0, 0, 1)
            cb.id = key
            self.ids.sensores.add_widget(cb)

    def confirmar_selecao(self):
        """
        Função chamada ao clicar no botão 'Confirmar Seleção'.
        Aqui você pode capturar quais sensores foram selecionados.
        """
        sensores_selecionados = []
        for checkbox in self.ids.sensores.children:
            if checkbox.ids.checkbox.active:  # Se o CheckBox estiver marcado
                sensores_selecionados.append(checkbox.ids.label.text)

        print("Sensores selecionados:", sensores_selecionados)
        # Aqui você pode atualizar o gráfico com base na seleção


class LabeledCheckBoxHistGraph(BoxLayout):
    pass

#COMANDO PARA O MOTOR
class ComandoPopup(Popup):
    pass

#COMANDO PARA O COMPRESSOR
class ComandoCOPopup(Popup):
    pass