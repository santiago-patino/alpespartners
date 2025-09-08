"""Objetos valor del dominio de campañas

En este archivo usted encontrará los objetos valor del dominio de campañas

"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
import alpespartners.modulos.campañas.dominio.objetos_valor as ov
from alpespartners.seedwork.dominio.entidades import Locacion, AgregacionRaiz, Entidad
from datetime import datetime
from decimal import Decimal
from enum import Enum
import uuid

@dataclass
class Participante(Entidad):
    id: ov.Codigo = field(default_factory=ov.Codigo)
    tipo: ov.TipoParticipante = field(default_factory=ov.TipoParticipante)
    nombre: ov.Nombre = field(default_factory=ov.Nombre)
    informacion_perfil: str | None = None

@dataclass
class Marca(Entidad):
    id: ov.Codigo = field(default_factory=ov.Codigo)
    nombre: ov.Nombre = field(default_factory=ov.Nombre)
    industria: ov.Industria | None = None
    informacion_contacto: ov.InformacionContacto | None = None

@dataclass
class Campaña(AgregacionRaiz):
    id: ov.Codigo = field(default_factory=ov.Codigo)
    nombre: ov.Nombre = field(default_factory=ov.Nombre)
    tipo: ov.TipoCampaña = field(default_factory=ov.TipoCampaña)
    estado: ov.EstadoCampaña = field(default_factory=ov.EstadoCampaña)
    fecha_inicio: datetime | None = None
    fecha_fin: datetime | None = None
    presupuesto: ov.Dinero | None = None
    marca_id: ov.Codigo = field(default_factory=ov.Codigo)
    participantes: list[Participante] = field(default_factory=list)
