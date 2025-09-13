from pydispatch import dispatcher

from .handlers import HandlerCampañaIntegracion

from alpespartners.modulos.campañas.dominio.eventos import CampañaCreada

dispatcher.connect(HandlerCampañaIntegracion.handle_campaña_creada, signal=f'{CampañaCreada.__name__}Integracion')