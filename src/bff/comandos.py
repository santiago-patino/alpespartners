from pulsar.schema import *
from .utils import time_millis
from enum import Enum
import uuid


class RegistrarCampaign(Record):
    nombre = String()
    presupuesto = Float()
    divisa = String()
    marca_id = String()
    participantes = String()


class ComandoRegistrarCampaign(Record):
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


class TipoPartner(Enum):
    afiliado = "Affiliate"
    influencer = "Influencer"


class RegistrarPartner(Record):
    id_campaign = String()
    nombre = String()
    tipo = TipoPartner
    informacion_perfil = String()
    fecha_creacion = Long()


class ComandoRegistrarPartner(Record):
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