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
            "vazao": 714,
            "temp_r": 700,
            "temp_s": 702,
            "temp_t": 704,
            "temp_carc": 706,
            "tensao_rs_co": 732,
            "tensao_st_co": 733,
            "tensao_tr_co": 734,
            "corrente_r_co": 726,
            "corrente_s_co": 727,
            "corrente_t_co": 728,
            "corrente_n_co": 729,
            "corrente_media_co": 731,
            "ativa_r_co": 735,
            "ativa_s_co": 736,
            "ativa_t_co": 737,
            "ativa_total_co": 738,
            "reativa_r_co": 739,
            "reativa_s_co": 740,
            "reativa_t_co": 741,
            "reativa_total_co": 742,
            "aparente_r_co": 743,
            "aparente_s_co": 744,
            "aparente_t_co": 745,
            "aparente_total_co": 746
        })
        
        return self._widget
    


if __name__ == "__main__":
    Builder.load_string(open("mainwidget.kv", encoding="utf-8").read(), rulesonly=True)
    Builder.load_string(open("popups.kv", encoding="utf-8").read(), rulesonly=True)
    MainApp().run()