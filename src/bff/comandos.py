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
        
class CancelarCampaign(Record):
    id = String()

class ComandoCancelarCampaign(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="CancelarCampaign")
    datacontenttype = String()
    service_name = String(default="campaign.aeroalpes")
    data = CancelarCampaign

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
        
class CancelarPartner(Record):
    id = String()

class ComandoCancelarPartner(Record):
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
        
class RegistrarEvento(Record):
    id_partner = String()
    id_campana = String()
    fecha = Long()

class ComandoRegistrarEvento(Record):
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
        
class CancelarEvento(Record):
    id = String()

class ComandoCancelarEvento(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="CancelarEvento")
    datacontenttype = String()
    service_name = String(default="partner.aeroalpes")
    data = CancelarEvento

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)