from partner.modulos.dominio.eventos import PartnerRegistrado
from partner.seedwork.aplicacion.handlers import Handler
from partner.modulos.infraestructura.despachadores import Despachador

class HandlerPartnerDominio(Handler):

    @staticmethod
    def handle_partner_creado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'evento-partners')
        print('================ PARTNER CREADO ===========')
        

    