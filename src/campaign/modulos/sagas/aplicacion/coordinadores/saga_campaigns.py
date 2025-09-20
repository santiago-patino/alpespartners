from campaign.seedwork.aplicacion.sagas import CoordinadorOrquestacion, Transaccion, Inicio, Fin
from campaign.seedwork.aplicacion.comandos import Comando
from campaign.seedwork.dominio.eventos import EventoDominio
import uuid
from campaign.seedwork.infraestructura import utils

# from campaign.modulos.sagas.aplicacion.comandos.cliente import RegistrarUsuario, ValidarUsuario
# from campaign.modulos.sagas.aplicacion.comandos.pagos import PagarReserva, RevertirPago
# from campaign.modulos.sagas.aplicacion.comandos.gds import ConfirmarReserva, RevertirConfirmacion

from campaign.modulos.aplicacion.comandos.registrar_campaign import ComandoRegistrarCampaign
# from campaign.modulos.aplicacion.comandos.cancelar_campaign import ComandoCancelarCampaign
from campaign.modulos.dominio.eventos import RegistroCampaignFallido, CampaignRegistrada

# from campaign.modulos.sagas.dominio.eventos.partner import PartnerRegistrado, RegistroPartnerFallido
# from campaign.modulos.sagas.aplicacion.comandos.partner import ComandoRegistrarPartner
from campaign.modulos.infraestructura.v1.eventos import PartnerRegistrado, RegistroPartnerFallido, EventoRegistrado, RegistroEventoFallido
from campaign.modulos.infraestructura.v1.comandos import ComandoRegistrarPartner, RegistrarPartner, ComandoRegistrarCampaign as ComandoRegistrarCampaignV1, RegistrarCampaign, CancelarCampaign, ComandoCancelarCampaign, ComandoCancelarPartner, CancelarPartner, ComandoRegistrarEvento, RegistrarEvento, ComandoCancelarEvento, CancelarEvento


from campaign.seedwork.infraestructura import utils
from campaign.modulos.infraestructura.v1 import TipoPartner

from campaign.modulos.infraestructura.despachadores import Despachador
import json

# from aeroalpes.modulos.vuelos.aplicacion.comandos.aprobar_reserva import AprobarReserva
# from aeroalpes.modulos.vuelos.aplicacion.comandos.cancelar_reserva import CancelarReserva
# from aeroalpes.modulos.vuelos.dominio.eventos.reservas import ReservaCreada, ReservaCancelada, ReservaAprobada, CreacionReservaFallida, AprobacionReservaFallida
# from aeroalpes.modulos.sagas.dominio.eventos.pagos import ReservaPagada, PagoRevertido, PagoFallido
# from aeroalpes.modulos.sagas.dominio.eventos.gds import ReservaGDSConfirmada, ConfirmacionGDSRevertida, ConfirmacionFallida

# from campaign.modulos.sagas.dominio.eventos.campaign import CampaignRegistrada


class CoordinadorCampañas(CoordinadorOrquestacion):
    
    # def __init__(self):
    #     print(CampaignRegistrada.__class__)
        # super().__init__()
        # self.id_correlacion = uuid.uuid4()

    def inicializar_pasos(self):
        self.pasos = [
            Inicio(index=0),
            Transaccion(index=1, comando=ComandoRegistrarCampaign, evento=CampaignRegistrada, error=RegistroCampaignFallido, compensacion=ComandoCancelarCampaign),
            Transaccion(index=2, comando=ComandoRegistrarPartner, evento=PartnerRegistrado, error=RegistroPartnerFallido, compensacion=ComandoCancelarPartner),
            Transaccion(index=3, comando=ComandoRegistrarEvento, evento=EventoRegistrado, error=RegistroEventoFallido, compensacion=ComandoCancelarEvento),
            Fin(index=4)
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
        evento_nombre = type(evento).__name__ if not isinstance(evento, type) else evento.__name__
        print(f'[COMPENSACION] Evento Origen: {evento_nombre}, Comando Destino: {type(tipo_comando).__name__ if tipo_comando else "None"}')
        # print(f'[COMPENSACION] Evento Origen: {type(evento).__name__}, Comando Destino: {tipo_comando.__name__ if tipo_comando else "None"}')
        despachador = Despachador()
        if tipo_comando == ComandoRegistrarCampaign:
            print("HERE")
            # print(evento)
            # payload = RegistrarCampaign(
            #     nombre = evento.nombre,
            #     presupuesto = evento.presupuesto,
            #     divisa = evento.divisa,
            #     marca_id = evento.marca_id,
            #     participantes=json.dumps(evento.participantes)
            # )

            # comando = ComandoRegistrarCampaignV1(
            #     time=utils.time_millis(),
            #     ingestion=utils.time_millis(),
            #     datacontenttype=RegistrarCampaign.__name__,
            #     data = payload
            # )
            # despachador.publicar_mensaje(comando, "comando-registrar-campaign")
        elif tipo_comando == ComandoRegistrarPartner:
            participantes = json.loads(evento.participantes)
            for p in participantes:
                payload = RegistrarPartner(
                    id_campaign=str(evento.id),
                    nombre=p['nombre'],
                    tipo=TipoPartner[p['tipo'].lower()],  
                    informacion_perfil=p['informacion_perfil'],
                    fecha_creacion=utils.time_millis()
                )
                comando = ComandoRegistrarPartner(
                    time=utils.time_millis(),
                    ingestion=utils.time_millis(),
                    datacontenttype=RegistrarPartner.__name__,
                    data=payload
                )
            
                despachador.publicar_mensaje(comando, "comando-registrar-partner")
        elif tipo_comando == ComandoRegistrarEvento:
            payload = RegistrarEvento(
                id_partner = str(evento.id),
                id_campana = str(evento.id_campaign),
                fecha = utils.time_millis()
            )
        
            comando = ComandoRegistrarEvento(
                time=utils.time_millis(),
                ingestion=utils.time_millis(),
                datacontenttype=RegistrarEvento.__name__,
                data = payload
            )
            
            despachador.publicar_mensaje(comando, "comando-registrar-evento-conversion")
            
        elif tipo_comando == ComandoCancelarCampaign:
            payload = CancelarCampaign(
                id = evento.id_campaign
            )
        
            comando = ComandoCancelarCampaign(
                time=utils.time_millis(),
                ingestion=utils.time_millis(),
                datacontenttype=CancelarCampaign.__name__,
                data = payload
            )
            despachador.publicar_mensaje(comando, "comando-cancelar-campaign")
            
        elif tipo_comando == ComandoCancelarPartner:
            print(evento)
            payload = CancelarPartner(
                id = evento.id_partner
            )
        
            comando = ComandoCancelarPartner(
                time=utils.time_millis(),
                ingestion=utils.time_millis(),
                datacontenttype=CancelarPartner.__name__,
                data = payload
            )
            despachador.publicar_mensaje(comando, "comando-cancelar-partner")
            
            
        elif tipo_comando == ComandoCancelarEvento:
            payload = CancelarEvento(
                id = "06f4addd-4601-4c20-95cf-3b1596014284"
            )
        
            comando = ComandoCancelarEvento(
                time=utils.time_millis(),
                ingestion=utils.time_millis(),
                datacontenttype=CancelarEvento.__name__,
                data = payload
            )
            despachador.publicar_mensaje(comando, "comando-cancelar-evento")
        
       
# Listener/Handler para redireccionar eventos de dominio a la saga
def oir_mensaje(signal, sender, **kwargs):
    mensaje = kwargs.get("evento")

    coordinador = CoordinadorCampañas()
    coordinador.inicializar_pasos()
    coordinador.procesar_evento(mensaje)
   
