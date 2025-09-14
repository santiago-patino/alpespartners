from pulsar.schema import *
from dataclasses import dataclass, field
from traking.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)
from traking.seedwork.infraestructura.utils import time_millis
import uuid


class RegistrarEvento(Record):
    id_partner = String()
    id_campana = String()
    fecha = Long()

class ComandoRegistrarEvento(ComandoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="RegistrarEvento")
    datacontenttype = String()
    service_name = String(default="traking.aeroalpes")
    data = RegistrarEvento

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)