from dataclasses import dataclass, field
from typing import Optional
from alpespartners.seedwork.aplicacion.dto import DTO


@dataclass(frozen=True)
class DineroDTO(DTO):
    monto: float
    divisa: str


@dataclass(frozen=True)
class ParticipanteDTO(DTO):
    id: str
    tipo: str
    nombre: Optional[str] = None
    informacion_perfil: Optional[str] = None


@dataclass(frozen=True)
class CampañaDTO(DTO):
    id: str
    nombre: str
    tipo: str
    estado: str
    fecha_inicio: str
    fecha_fin: str
    presupuesto: float
    divisa: str
    marca_id: Optional[str] = None
    participantes: list[ParticipanteDTO] = field(default_factory=list)