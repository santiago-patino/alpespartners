from pulsar.schema import *
from campaign.seedwork.dominio.eventos import (EventoDominio)
from . import TipoPartner

# class EventoPartner(EventoDominio):
#     ...

class PartnerRegistrado(Record):
    id = String()
    nombre = String()
    tipo = TipoPartner
    informacion_perfil = String()
    fecha_creacion = Long()

class RegistroPartnerFallido(Record):
    id = String()
    nombre = String()
    tipo = TipoPartner
    informacion_perfil = String()
    fecha_creacion = Long()