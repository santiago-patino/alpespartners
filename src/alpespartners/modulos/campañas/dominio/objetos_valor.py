"""Objetos valor del dominio de vuelos

En este archivo usted encontrará los objetos valor del dominio de vuelos

"""

from __future__ import annotations

from dataclasses import dataclass, field
from alpespartners.seedwork.dominio.objetos_valor import ObjetoValor, Codigo, Ruta, Locacion
# from datetime import datetime
from enum import Enum

# -------------------------
# Identidad y nombres
# -------------------------

@dataclass(frozen=True)
class Nombre(ObjetoValor):
    valor: str


# -------------------------
# Dinero y presupuesto
# -------------------------

@dataclass(frozen=True)
class Dinero(ObjetoValor):
    monto: float
    divisa: str


# -------------------------
# Estado de campaña
# -------------------------

class EstadoCampaña(Enum):
    DRAFT = "draft"
    ACTIVA = "active"
    FINALIZADA = "finished"
    PAUSADA = "paused"


# -------------------------
# Tipos de campañas
# -------------------------

class TipoCampaña(Enum):
    INFLUENCER = "Influencer"
    AFFILIATE = "Affiliate"
    MIXTA = "Mixed"


# -------------------------
# Tipos de participantes
# -------------------------

class TipoParticipante(Enum):
    INFLUENCER = "Influencer"
    AFFILIATE = "Affiliate"