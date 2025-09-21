from pulsar.schema import *
from traking.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion
from traking.seedwork.infraestructura.utils import time_millis
import uuid


class EventoRegistrado(Record):
    id = String()
    id_partner = String()
    id_campana = String()
    fecha = Long()
    
class RegistroEventoFallido(Record):
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