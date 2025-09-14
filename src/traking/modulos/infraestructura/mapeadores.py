from traking.seedwork.dominio.repositorios import Mapeador
from traking.modulos.dominio.entidades import Evento
from .dto import Evento as EventoDTO

from typing import Union, Optional
from datetime import datetime
from enum import Enum


class MapeadorEvento(Mapeador):
    
    def entidad_a_dto(self, entidad: Evento):
        return EventoDTO(
            id_partner=entidad.id_partner,
            id_campana=entidad.id_campana,
            fecha=entidad.fecha
        )

    def dto_a_entidad(self, dto: EventoDTO):
        return Evento(
            id_partner=dto.id_partner,
            id_campana=dto.id_campana,
            fecha=dto.fecha
        )
        
    def entidad_a_externo(self, entidad: Evento) -> dict:
        return entidad.__dict__
        
    def obtener_tipo(self) -> type:
        return Evento.__class__