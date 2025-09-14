from campaign.modulos.vuelos.dominio.eventos.reservas import CampaignRegistrada
from campaign.seedwork.aplicacion.handlers import Handler
from campaign.modulos.infraestructura.despachadores import Despachador

class HandlerCampaignDominio(Handler):

    @staticmethod
    def handle_campaign_creado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'evento-campaign')
        print('================ CAMPANA CREADA ===========')
        

    