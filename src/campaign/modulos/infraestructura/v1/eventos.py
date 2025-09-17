from pulsar.schema import *
from ....seedwork.infraestructura.schema.v1.eventos import EventoIntegracion
from ....seedwork.infraestructura.utils import time_millis
import uuid

class Participante(Record):
    id = String()
    tipo = String()
    nombre = String()
    informacion_perfil = String()

class CampaignRegistrado(Record):
    id = String()
    nombre = String()
    presupuesto = String()
    divisa = String()
    marca_id = String()
    participantes = Array(Participante())

class EventoCampaign(EventoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="EventoCampaign")
    datacontenttype = String()
    service_name = String(default="campaign.aeroalpes")
    campaign_registrado = CampaignRegistrado

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)