from pulsar.schema import *
from dataclasses import dataclass, field
from ....seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)
from ....seedwork.infraestructura.utils import time_millis
import uuid

class Participante(Record):
    id = String()
    tipo = String()
    nombre = String()
    informacion_perfil = String()

class RegistrarCampaign(Record):
    nombre = String()
    presupuesto = Float()
    divisa = String()
    marca_id = String()
    participantes = String()
    #participantes = Array(Participante)

class ComandoRegistrarCampaign(ComandoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="RegistrarCampaign")
    datacontenttype = String()
    service_name = String(default="campaign.aeroalpes")
    data = RegistrarCampaign

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)