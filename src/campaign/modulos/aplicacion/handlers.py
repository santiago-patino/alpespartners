from campaign.modulos.dominio.eventos import CampaignRegistrada
from campaign.seedwork.aplicacion.handlers import Handler
from campaign.modulos.infraestructura.despachadores import Despachador

class HandlerCampaignDominio(Handler):

    @staticmethod
    def handle_campaign_creado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'evento-campaigns')
        print('================ CAMPANA CREADA ===========')
        
    # @staticmethod
    # def handle_creacion_campaign_fallido(evento):
    #     despachador = Despachador()
    #     despachador.publicar_evento(evento, 'evento-campaigns')
    #     print('================ CAMPANA FALLIDA ===========')
        

    