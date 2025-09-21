from __future__ import annotations
from dataclasses import dataclass, field
from campaign.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime
from pulsar.schema import *

class EventoCampaign(EventoDominio):
    ...


@dataclass
class CampaignRegistrada(EventoCampaign):
    id = String()
    nombre = String()
    presupuesto = Float()
    divisa = String()
    marca_id = String()
    participantes = String()
    # id: str = None
    # nombre: str
    # presupuesto: float
    # divisa: str
    # marca_id: str
    # participantes: str


