from sqlalchemy import Column, Integer, DateTime, Float
from db import Base

class DadoVentilador(Base):
    __tablename__ = 'dado_ventilador'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    encoder_axial = Column(Float)
    torque_axial = Column(Float)
    tit02 = Column(Float)
    tit01 = Column(Float)
    pit02 = Column(Float)
    pit01 = Column(Float)
    pit03 = Column(Float)
    temperatura = Column(Float)
    velocidade = Column(Float)
    vazao = Column(Float)
    temp_r = Column(Float)
    temp_s = Column(Float)
    temp_t = Column(Float)
    temp_carc = Column(Float)
    tensao_rs_co = Column(Float)
    tensao_st_co = Column(Float)
    tensao_tr_co = Column(Float)
    corrente_r_co = Column(Float)
    corrente_s_co = Column(Float)
    corrente_t_co = Column(Float)
    corrente_n_co = Column(Float)
    corrente_media_co = Column(Float)
    ativa_r_co = Column(Float)
    ativa_s_co = Column(Float)
    ativa_t_co = Column(Float)
    ativa_total_co = Column(Float)
    reativa_r_co = Column(Float)
    reativa_s_co = Column(Float)
    reativa_t_co = Column(Float)
    reativa_total_co = Column(Float)
    aparente_r_co = Column(Float)
    aparente_s_co = Column(Float)
    aparente_t_co = Column(Float)
    aparente_total_co = Column(Float)

    def get_attr_printable_list(self):
        """
        Retorna uma lista dos atributos formatados para exibição.
        """
        return [
            self.id,
            self.timestamp.strftime('%d/%m/%Y %H:%M:%S'),
            self.encoder_axial,
            self.torque_axial,
            self.tit02,
            self.tit01,
            self.pit02,
            self.pit01,
            self.pit03,
            self.temperatura,
            self.velocidade,
            self.vazao,
            self.temp_r,
            self.temp_s,
            self.temp_t,
            self.temp_carc,
            self.tensao_rs_co,
            self.tensao_st_co,
            self.tensao_tr_co,
            self.corrente_r_co,
            self.corrente_s_co,
            self.corrente_t_co,
            self.corrente_n_co,
            self.corrente_media_co,
            self.ativa_r_co,
            self.ativa_s_co,
            self.ativa_t_co,
            self.ativa_total_co,
            self.reativa_r_co,
            self.reativa_s_co,
            self.reativa_t_co,
            self.reativa_total_co,
            self.aparente_r_co,
            self.aparente_s_co,
            self.aparente_t_co,
            self.aparente_total_co
        ]
