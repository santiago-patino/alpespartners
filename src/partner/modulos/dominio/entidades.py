"""Entidades del dominio de cliente

En este archivo usted encontrará las entidades del dominio de cliente

"""

from datetime import datetime
from partner.seedwork.dominio.entidades import Entidad, AgregacionRaiz
from partner.modulos.dominio.eventos import PartnerRegistrado
from dataclasses import dataclass, field

# from .objetos_valor import Nombre, Email, Cedula, Rut

@dataclass
class Partner(AgregacionRaiz):
    nombre: str = ""
    informacion_perfil: str = ""
    tipo: str = ""
    
    def crear_partner(self, partner: "Partner"):
        self.nombre = partner.nombre
        self.informacion_perfil = partner.informacion_perfil
        self.tipo = partner.tipo
        
        self.agregar_evento(
            PartnerRegistrado(
                id=str(self.id),
                nombre=self.nombre,
                tipo=self.tipo,
                informacion_perfil=self.informacion_perfil
            )
        )

@dataclass
class Affiliate(Partner, AgregacionRaiz):
    pass

@dataclass
class Influencer(Partner, AgregacionRaiz):
    pass
   
