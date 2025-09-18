from pulsar.schema import *
from dataclasses import dataclass, field
from campaign.seedwork.dominio.eventos import (EventoDominio)

class EventoCampaign(EventoDominio):
    ...

class Participante(Record):
    id = String()
    tipo = String()
    nombre = String()
    informacion_perfil = String()

class CampaignRegistrada(Record):
    id = String()
    nombre = String()
    presupuesto = Float()
    divisa = String()
    marca_id = String()
    participantes = String()