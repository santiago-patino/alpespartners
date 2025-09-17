"""Entidades del dominio de cliente

En este archivo usted encontrará las entidades del dominio de cliente

"""

from datetime import datetime
from ...seedwork.dominio.entidades import Entidad, AgregacionRaiz
from dataclasses import dataclass, field

# from .objetos_valor import Nombre, Email, Cedula, Rut

@dataclass
class Partner(Entidad):
    nombre: str = ""
    informacion_perfil: str = ""
    tipo: str = ""

@dataclass
class Affiliate(Partner, AgregacionRaiz):
    pass

@dataclass
class Influencer(Partner, AgregacionRaiz):
    pass
   
