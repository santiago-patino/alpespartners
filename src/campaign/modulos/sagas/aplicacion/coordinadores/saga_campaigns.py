from campaign.seedwork.aplicacion.sagas import CoordinadorOrquestacion, Transaccion, Inicio, Fin
from campaign.seedwork.aplicacion.comandos import Comando
from campaign.seedwork.dominio.eventos import EventoDominio
import uuid
from campaign.seedwork.infraestructura import utils


from campaign.modulos.aplicacion.comandos.registrar_campaign import ComandoRegistrarCampaign
from campaign.modulos.dominio.eventos import RegistroCampaignFallido, CampaignRegistrada

from campaign.modulos.infraestructura.v1.eventos import PartnerRegistrado, RegistroPartnerFallido, EventoRegistrado, RegistroEventoFallido
from campaign.modulos.infraestructura.v1.comandos import ComandoRegistrarPartner, RegistrarPartner, ComandoRegistrarCampaign as ComandoRegistrarCampaignV1, RegistrarCampaign, CancelarCampaign, ComandoCancelarCampaign, ComandoCancelarPartner, CancelarPartner, ComandoRegistrarEvento, RegistrarEvento, ComandoCancelarEvento, CancelarEvento


from campaign.seedwork.infraestructura import utils
from campaign.modulos.infraestructura.v1 import TipoPartner

from campaign.modulos.infraestructura.despachadores import Despachador
import json


class CoordinadorCampañas(CoordinadorOrquestacion):

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
        print(f"[SAGA LOG] {type(mensaje).__name__}: {mensaje}")

    def construir_comando(self, evento: EventoDominio, tipo_comando: type) -> Comando:
        # Transforma un evento en la entrada de un comando
        # print(evento)
        evento_nombre = type(evento).__name__ if not isinstance(evento, type) else evento.__name__
        print(f'[COMPENSACION] Evento Origen: {evento_nombre}, Comando Destino: {type(tipo_comando).__name__ if tipo_comando else "None"}')
        despachador = Despachador()
        if tipo_comando == ComandoRegistrarPartner:
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
   
