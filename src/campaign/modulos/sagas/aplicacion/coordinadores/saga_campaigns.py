from campaign.seedwork.aplicacion.sagas import CoordinadorOrquestacion, Transaccion, Inicio, Fin
from campaign.seedwork.aplicacion.comandos import Comando
from campaign.seedwork.dominio.eventos import EventoDominio
import uuid
from campaign.seedwork.infraestructura import utils

# from campaign.modulos.sagas.aplicacion.comandos.cliente import RegistrarUsuario, ValidarUsuario
# from campaign.modulos.sagas.aplicacion.comandos.pagos import PagarReserva, RevertirPago
# from campaign.modulos.sagas.aplicacion.comandos.gds import ConfirmarReserva, RevertirConfirmacion

from campaign.modulos.aplicacion.comandos.registrar_campaign import ComandoRegistrarCampaign
from campaign.modulos.aplicacion.comandos.cancelar_campaign import ComandoCancelarCampaign
from campaign.modulos.dominio.eventos import CampaignRegistrada, RegistroCampaignFallido

# from campaign.modulos.sagas.dominio.eventos.partner import PartnerRegistrado, RegistroPartnerFallido
from campaign.modulos.infraestructura.v1.eventos import PartnerRegistrado, RegistroPartnerFallido
from campaign.modulos.sagas.aplicacion.comandos.partner import ComandoRegistrarPartner, ComandoCancelarPartner

# from aeroalpes.modulos.vuelos.aplicacion.comandos.aprobar_reserva import AprobarReserva
# from aeroalpes.modulos.vuelos.aplicacion.comandos.cancelar_reserva import CancelarReserva
# from aeroalpes.modulos.vuelos.dominio.eventos.reservas import ReservaCreada, ReservaCancelada, ReservaAprobada, CreacionReservaFallida, AprobacionReservaFallida
# from aeroalpes.modulos.sagas.dominio.eventos.pagos import ReservaPagada, PagoRevertido, PagoFallido
# from aeroalpes.modulos.sagas.dominio.eventos.gds import ReservaGDSConfirmada, ConfirmacionGDSRevertida, ConfirmacionFallida


class CoordinadorCampañas(CoordinadorOrquestacion):
    
    # def __init__(self):
    #     super().__init__()
    #     self.id_correlacion = uuid.uuid4()

    def inicializar_pasos(self):
        self.pasos = [
            # Inicio(index=0),
            Transaccion(index=0, comando=ComandoRegistrarCampaign, evento=CampaignRegistrada, error=RegistroCampaignFallido, compensacion=ComandoCancelarCampaign),
            Transaccion(index=1, comando=ComandoRegistrarPartner, evento=PartnerRegistrado, error=RegistroPartnerFallido, compensacion=ComandoCancelarPartner),
            # Fin(index=3)
        ]

    def iniciar(self):
        self.persistir_en_saga_log(self.pasos[0])
    
    def terminar(self):
        self.persistir_en_saga_log(self.pasos[-1])

    def persistir_en_saga_log(self, mensaje):
        # TODO Persistir estado en DB
        # Probablemente usted podría usar un repositorio para ello
        print(f"[SAGA LOG] {type(mensaje).__name__}: {mensaje}")
        # En una implementación real, aquí se guardaría en base de datos

    def construir_comando(self, evento: EventoDominio, tipo_comando: type) -> Comando:
        # Transforma un evento en la entrada de un comando
        print(f'[COMPENSACION] Evento Origen: {type(evento).__name__}, Comando Destino: {tipo_comando.__name__ if tipo_comando else "None"}')

        if tipo_comando == ComandoCancelarCampaign:
            return ComandoCancelarCampaign(
                id = "05247050-6112-4851-9e1d-1502eed40213"
            )
        
        

# Listener/Handler para redireccionar eventos de dominio a la saga
def oir_mensaje(signal, sender, **kwargs):
    mensaje = kwargs.get("evento")
    print(mensaje.__class__)
    if isinstance(mensaje, EventoDominio):
        coordinador = CoordinadorCampañas()
        coordinador.inicializar_pasos()
        coordinador.procesar_evento(mensaje)
    else:
        raise NotImplementedError("El mensaje no es evento de Dominio")
