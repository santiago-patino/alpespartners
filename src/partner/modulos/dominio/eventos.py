from pulsar.schema import *
from dataclasses import dataclass, field
from partner.seedwork.dominio.eventos import (EventoDominio)
from partner.modulos.infraestructura.v1 import TipoPartner

class EventoPartner(EventoDominio):
    ...
    
class PartnerRegistrado(Record, EventoPartner):
    id = String()
    nombre = String()
    tipo = TipoPartner
    informacion_perfil = String()
    fecha_creacion = Long()
    
class RegistroPartnerFallido(Record, EventoPartner):
    id = String()
    nombre = String()
    tipo = TipoPartner
    informacion_perfil = String()
    fecha_creacion = Long() 