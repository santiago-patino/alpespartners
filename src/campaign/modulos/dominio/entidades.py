"""Entidades del dominio de cliente

En este archivo usted encontrará las entidades del dominio de cliente

"""

from datetime import datetime
from campaign.seedwork.dominio.entidades import Entidad, AgregacionRaiz
from dataclasses import dataclass, field


@dataclass
class Participante(Entidad):
    id: str = ""
    tipo: str = ""
    nombre: str = ""
    informacion_perfil: str = ""

@dataclass
class Campaign(Entidad):
    nombre: str = ""
    presupuesto: float = ""
    divisa: str = ""
    marca_id: str = ""
    participantes: list[Participante] = field(default_factory=list)

   
