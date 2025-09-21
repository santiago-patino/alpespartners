from pulsar.schema import *
from dataclasses import dataclass, field
from partner.seedwork.dominio.eventos import (EventoDominio)

class EventoTraking(EventoDominio):
    ...

class EventoRegistrado(Record, EventoTraking):
    id = String()
    id_partner = String()
    id_campana = String()
    fecha = Long()
    
class RegistroEventoFallido(Record, EventoTraking):
    id = String()
    id_partner = String()
    id_campana = String()
    fecha = Long()