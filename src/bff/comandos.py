from pulsar.schema import *

from enum import Enum
import uuid

from .utils import time_millis


class RegistrarCampaignPayload(Record):
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
    data = RegistrarCampaignPayload

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TipoPartner(Enum):
    afiliado = "Affiliate"
    influencer = "Influencer"


class RegistrarPartnerPayload(Record):
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
    data = RegistrarPartnerPayload

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)