from ...seedwork.dominio.repositorios import Mapeador
from ...modulos.dominio.entidades import Campaign, Participante
from .dto import Campaign as CampaignDTO

from typing import Union, Optional
from datetime import datetime
from enum import Enum


class MapeadorCampaign(Mapeador):
    
    def entidad_a_dto(self, entidad: Campaign):
        
        participantes_list = [
            {
                "id": p.id,
                "tipo": p.tipo,
                "nombre": p.nombre,
                "informacion_perfil": p.informacion_perfil
            } for p in entidad.participantes
        ]
        
        return CampaignDTO(
            nombre=entidad.nombre,
            presupuesto=entidad.presupuesto,
            divisa=entidad.divisa,
            marca_id=entidad.marca_id,
            participantes=participantes_list
        )

    def dto_a_entidad(self, dto: CampaignDTO):
        return Campaign(
            nombre=dto.nombre,
            presupuesto=dto.presupuesto,
            divisa=dto.divisa,
            marca_id=dto.marca_id,
            participantes=[
                Participante(
                    id=p.id,
                    tipo=p.tipo,
                    nombre=p.nombre,
                    informacion_perfil=p.informacion_perfil
                )
                for p in dto.participantes
            ]
        )
        
    def entidad_a_externo(self, entidad: Campaign) -> dict:
        return entidad.__dict__
        
    def obtener_tipo(self) -> type:
        return Campaign.__class__