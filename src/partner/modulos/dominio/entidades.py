"""Entidades del dominio de cliente

En este archivo usted encontrará las entidades del dominio de cliente

"""

from datetime import datetime
from partner.seedwork.dominio.entidades import Entidad, AgregacionRaiz
from partner.modulos.dominio.eventos import PartnerRegistrado, RegistroPartnerFallido
from dataclasses import dataclass, field
from partner.modulos.infraestructura.v1 import TipoPartner
from typing import Optional
# from .objetos_valor import Nombre, Email, Cedula, Rut

@dataclass
class Partner(AgregacionRaiz):
    id: Optional[str] = None
    id_campaign: str = ""
    nombre: str = ""
    informacion_perfil: str = ""
    tipo: str = ""
    
    def crear_partner(self, partner: "Partner"):
        self.id_campaign = partner.id_campaign
        self.nombre = partner.nombre
        self.informacion_perfil = partner.informacion_perfil
        self.tipo = partner.tipo
        
        self.agregar_evento(
            PartnerRegistrado(
                id=str(self.id),
                id_campaign=str(self.id_campaign),
                nombre=self.nombre,
                tipo=TipoPartner.influencer,
                informacion_perfil=self.informacion_perfil
            ),
            RegistroPartnerFallido(
                id=str(self.id),
                id_campaign=str(self.id_campaign),
                nombre=self.nombre,
                tipo=TipoPartner.influencer,
                informacion_perfil=self.informacion_perfil
            )
        )

@dataclass
class Affiliate(Partner, AgregacionRaiz):
    pass

@dataclass
class Influencer(Partner, AgregacionRaiz):
    pass
   
