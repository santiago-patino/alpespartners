from pydispatch import dispatcher

from .coordinadores.saga_campaigns import oir_mensaje

# Conectar listeners de eventos de dominio para la saga
# from campaign.modulos.vuelos.dominio.eventos.reservas import ReservaCreada, ReservaCancelada, ReservaAprobada, CreacionReservaFallida, AprobacionReservaFallida
# from aeroalpes.modulos.sagas.dominio.eventos.pagos import ReservaPagada, PagoRevertido, PagoFallido
# from aeroalpes.modulos.sagas.dominio.eventos.gds import ReservaGDSConfirmada, ConfirmacionGDSRevertida, ConfirmacionFallida

from campaign.modulos.dominio.eventos import CampaignRegistrada, RegistroCampaignFallido
from campaign.modulos.infraestructura.v1.eventos import RegistroPartnerFallido, PartnerRegistrado, RegistroEventoFallido, EventoRegistrado
# from partner.modulos.dominio.eventos import RegistroPartnerFallido

# Conectar eventos de vuelos
dispatcher.connect(oir_mensaje, signal=f'{CampaignRegistrada.__name__}Integracion')
dispatcher.connect(oir_mensaje, signal=f'{RegistroCampaignFallido.__name__}Integracion')

dispatcher.connect(oir_mensaje, signal=f'{PartnerRegistrado.__name__}Integracion')
dispatcher.connect(oir_mensaje, signal=f'{RegistroPartnerFallido.__name__}Integracion')

dispatcher.connect(oir_mensaje, signal=f'{EventoRegistrado.__name__}Integracion')
dispatcher.connect(oir_mensaje, signal=f'{RegistroEventoFallido.__name__}Integracion')
# dispatcher.connect(oir_mensaje, signal=f'RegistroPartnerFallidoIntegracion')

