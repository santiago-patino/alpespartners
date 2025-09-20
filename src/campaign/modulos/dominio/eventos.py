from pulsar.schema import *
from dataclasses import dataclass, field
from campaign.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime
import uuid

class EventoCampaign(EventoDominio):
    ...

class Participante(Record):
    id = String()
    tipo = String()
    nombre = String()
    informacion_perfil = String()

class CampaignRegistrada(Record, EventoCampaign):
    id = String()
    nombre = String()
    presupuesto = Float()
    divisa = String()
    marca_id = String()
    participantes = String()
    
class RegistroCampaignFallido(Record, EventoCampaign):
    id = String()
    nombre = String()
    presupuesto = Float()
    divisa = String()
    marca_id = String()
    participantes = String()