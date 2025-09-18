from pydispatch import dispatcher
from .handlers import HandlerCampaignDominio
from campaign.modulos.dominio.eventos import CampaignRegistrada

dispatcher.connect(HandlerCampaignDominio.handle_campaign_creado, signal='CampaignRegistradaDominio')
