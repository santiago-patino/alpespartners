from pulsar.schema import *
from campaign.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion
from campaign.seedwork.infraestructura.utils import time_millis
import uuid
from campaign.modulos.infraestructura.v1 import TipoPartner
from campaign.seedwork.dominio.eventos import (EventoDominio)
from dataclasses import dataclass, field
    
class Participante(Record):
    id = String()
    tipo = String()
    nombre = String()
    informacion_perfil = String()

class CampaignRegistradaPayload(Record):
    id = String()
    nombre = String()
    presupuesto = String()
    divisa = String()
    marca_id = String()
    participantes = String()

class EventoCampaign(EventoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="EventoCampaign")
    datacontenttype = String()
    service_name = String(default="campaign.aeroalpes")
    campaign_registrada = CampaignRegistradaPayload

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
class PartnerRegistrado(Record):
    id = String()
    id_campaign = String()
    nombre = String()
    tipo = TipoPartner
    informacion_perfil = String()
    fecha_creacion = Long()

class RegistroPartnerFallido(Record, EventoDominio):
    id = String()
    id_campaign = String()
    nombre = String()
    tipo = TipoPartner
    informacion_perfil = String()
    fecha_creacion = Long()
        
class EventoPartner(EventoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="EventoPartner")
    datacontenttype = String()
    service_name = String(default="partner.aeroalpes")
    partner_registrado = PartnerRegistrado
    partner_fallido = RegistroPartnerFallido

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
class EventoRegistrado(Record):
    id = String()
    id_partner = String()
    id_campana = String()
    fecha = Long()
        
class RegistroEventoFallido(Record, EventoDominio):
    id = String()
    id_partner = String()
    id_campana = String()
    fecha = Long()
        
class EventoTraking(EventoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="EventoTraking")
    datacontenttype = String()
    service_name = String(default="traking.aeroalpes")
    evento_registrado = EventoRegistrado
    evento_fallido = RegistroEventoFallido

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)