from pydispatch import dispatcher
from .handlers import HandlerEventoDominio
from traking.modulos.dominio.eventos import EventoRegistrado, RegistroEventoFallido

dispatcher.connect(HandlerEventoDominio.handle_evento_creado, signal=f'{EventoRegistrado.__name__}Dominio')
dispatcher.connect(HandlerEventoDominio.handle_evento_fallido, signal=f'{RegistroEventoFallido.__name__}Integracion')