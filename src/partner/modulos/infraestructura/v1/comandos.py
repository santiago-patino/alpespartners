from pulsar.schema import *
from dataclasses import dataclass, field
from partner.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)
from partner.seedwork.infraestructura.utils import time_millis
from partner.modulos.infraestructura.v1 import TipoPartner
import uuid


class RegistrarPartner(Record):
    id_campaign = String()
    nombre = String()
    tipo = TipoPartner
    informacion_perfil = String()
    fecha_creacion = Long()

class ComandoRegistrarPartner(ComandoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="RegistrarPartner")
    datacontenttype = String()
    service_name = String(default="partner.aeroalpes")
    data = RegistrarPartner

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
class CancelarPartner(Record):
    id = String()

class ComandoCancelarPartner(ComandoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="CancelarPartner")
    datacontenttype = String()
    service_name = String(default="partner.aeroalpes")
    data = CancelarPartner

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)