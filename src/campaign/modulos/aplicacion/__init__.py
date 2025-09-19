from pydispatch import dispatcher
from .handlers import HandlerCampaignDominio
from campaign.modulos.dominio.eventos import CampaignRegistrada, RegistroCampaignFallido

# dispatcher.connect(HandlerCampaignDominio.handle_campaign_creado, signal='CampaignRegistradaDominio')
dispatcher.connect(HandlerCampaignDominio.handle_campaign_creado, signal=f'{CampaignRegistrada.__name__}Integracion')
