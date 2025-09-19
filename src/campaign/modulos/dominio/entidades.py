"""Entidades del dominio de cliente

En este archivo usted encontrará las entidades del dominio de cliente

"""

from datetime import datetime
from campaign.seedwork.dominio.entidades import Entidad, AgregacionRaiz
from dataclasses import dataclass, field
from campaign.modulos.dominio.eventos import CampaignRegistrada, Participante, RegistroCampaignFallido
import json
from campaign.seedwork.infraestructura import utils


@dataclass
class Participante(Entidad):
    id: str = ""
    tipo: str = ""
    nombre: str = ""
    informacion_perfil: str = ""

@dataclass
class Campaign(AgregacionRaiz):
    nombre: str = ""
    presupuesto: float = ""
    divisa: str = ""
    marca_id: str = ""
    participantes: list[Participante] = field(default_factory=list)
    
    def crear_campaign(self, campaign: "Campaign"):
        self.nombre = campaign.nombre
        self.presupuesto = campaign.presupuesto
        self.divisa = campaign.divisa
        self.marca_id = campaign.marca_id
        self.participantes = campaign.participantes
        
        lista_participantes = [
            {
                "id": p.id,
                "tipo": p.tipo,
                "nombre": p.nombre,
                "informacion_perfil": p.informacion_perfil
            } 
            for p in self.participantes
        ]
        
        # payload = id=str(self.id),
        #         nombre=self.nombre,
        #         presupuesto=self.presupuesto,
        #         divisa=self.divisa,
        #         marca_id=self.marca_id,
        #         participantes=json.dumps(lista_participantes)
        
        self.agregar_evento(
            CampaignRegistrada(
                id=str(self.id),
                nombre=self.nombre,
                presupuesto=self.presupuesto,
                divisa=self.divisa,
                marca_id=self.marca_id,
                participantes=json.dumps(lista_participantes)
            ),
            RegistroCampaignFallido(
                id=str(self.id),
                nombre=self.nombre,
                presupuesto=self.presupuesto,
                divisa=self.divisa,
                marca_id=self.marca_id,
                participantes=json.dumps(lista_participantes)
            ),
        )

   
