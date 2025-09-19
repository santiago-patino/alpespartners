from pydispatch import dispatcher
from .handlers import HandlerPartnerDominio

dispatcher.connect(HandlerPartnerDominio.handle_partner_creado, signal='PartnerRegistradoDominio')
dispatcher.connect(HandlerPartnerDominio.handle_partner_fallido, signal='RegistroPartnerFallidoIntegracion')
