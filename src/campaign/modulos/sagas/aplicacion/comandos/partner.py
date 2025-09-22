from pulsar.schema import *
from dataclasses import dataclass, field
from campaign.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)
from campaign.seedwork.infraestructura.utils import time_millis
from campaign.modulos.infraestructura.v1 import TipoPartner
from campaign.seedwork.aplicacion.comandos import Comando
import uuid


class RegistrarPartner(Record):
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

@dataclass
class ComandoCancelarPartner(Comando):
    id: str
    # def __init__(self, id):
    #     self.id = id

# class ComandoCancelarPartner(Comando):
#     id = String(default=str(uuid.uuid4()))
#     time = Long()
#     ingestion = Long(default=time_millis())
#     specversion = String(default="v1")
#     type = String(default="CancelarPartner")
#     datacontenttype = String()
#     service_name = String(default="partner.aeroalpes")
#     data = CancelarPartner

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)