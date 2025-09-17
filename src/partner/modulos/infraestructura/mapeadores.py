from ...seedwork.dominio.repositorios import Mapeador
from ...modulos.dominio.entidades import Partner, Affiliate, Influencer
# from partner.modulos.dominio.objetos_valor import (
#     Codigo, Nombre, TipoCampaña, EstadoCampaña, Dinero, TipoParticipante
# )
from .dto import TipoPartner, Partner as PartnerDTO

from typing import Union, Optional
from datetime import datetime
from enum import Enum


class MapeadorPartner(Mapeador):
    
    def entidad_a_dto(self, entidad: Partner):
        tipo = TipoPartner.influencer if isinstance(entidad, Influencer) else TipoPartner.affiliate
        return PartnerDTO(
            nombre=entidad.nombre,
            tipo=tipo,
            informacion_perfil=entidad.informacion_perfil
        )

    def dto_a_entidad(self, dto: PartnerDTO):
        return Partner(
            nombre=dto.nombre,
            tipo=dto.tipo,
            informacion_perfil=dto.informacion_perfil
        )
        
    def entidad_a_externo(self, entidad: Partner) -> dict:
        return entidad.__dict__
        
    def obtener_tipo(self) -> type:
        return Partner.__class__