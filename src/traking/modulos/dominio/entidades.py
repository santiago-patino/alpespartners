"""Entidades del dominio de cliente

En este archivo usted encontrará las entidades del dominio de cliente

"""

from datetime import datetime
from traking.seedwork.dominio.entidades import Entidad, AgregacionRaiz
from dataclasses import dataclass, field
from traking.modulos.dominio.eventos import EventoRegistrado, RegistroEventoFallido

@dataclass
class Evento(AgregacionRaiz):
    id_partner: str = ""
    id_campana: str = ""
    fecha: datetime = field(default_factory=datetime.utcnow)
    
    def crear_evento(self, event: "Event"):
        self.id_partner = event.id_partner
        self.id_campana = event.id_campana
        self.fecha = event.fecha
        
        self.agregar_evento(
            EventoRegistrado(
                id=str(self.id),
                id_partner=str(self.id_partner),
                id_campana=self.id_campana,
                fecha=self.fecha,
            ),
            RegistroEventoFallido(
                id=str(self.id),
                id_partner=str(self.id_partner),
                id_campana=self.id_campana,
                fecha=self.fecha,
            )
        )
   
