"""Entidades del dominio de cliente

En este archivo usted encontrará las entidades del dominio de cliente

"""

from datetime import datetime
from traking.seedwork.dominio.entidades import Entidad, AgregacionRaiz
from dataclasses import dataclass, field

@dataclass
class Evento(Entidad):
    id_partner: str = ""
    id_campana: str = ""
    fecha: datetime = field(default_factory=datetime.utcnow)
   
