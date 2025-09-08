from __future__ import annotations
from dataclasses import dataclass, field
from alpespartners.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime

@dataclass
class CampañaCreada(EventoDominio):
    id_campaña: uuid.UUID = None
    id_marca: uuid.UUID = None
    estado: str = None
    fecha_inicio: datetime = None