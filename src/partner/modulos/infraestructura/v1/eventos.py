from pulsar.schema import *
from partner.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion
from partner.seedwork.infraestructura.utils import time_millis
from partner.modulos.infraestructura.v1 import TipoPartner
import uuid


class PartnerRegistrado(Record):
    id = String()
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)