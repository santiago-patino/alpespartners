from partner.seedwork.dominio.repositorios import Mapeador
from partner.modulos.campañas.dominio.entidades import Campaña, Participante
from partner.modulos.campañas.dominio.objetos_valor import (
    Codigo, Nombre, TipoCampaña, EstadoCampaña, Dinero, TipoParticipante
)
from .dto import Partner as PartnerDTO

from typing import Union, Optional
from datetime import datetime
from enum import Enum


class MapeadorPartner(Mapeador):

    def entidad_a_dto(self, entidad: Campaña) -> CampañaDTO:
        return PartnerDTO(
            nombre=entidad.nombre,
            tipo=entidad.tipo,
            informacion_perfil=entidad.informacion_perfil,
        )

    def dto_a_entidad(self, dto: CampañaDTO) -> Campaña:
        participantes = [
            Participante(
                id=Codigo(p.id),
                tipo=TipoParticipante(p.tipo),
                nombre=Nombre(p.nombre),
                informacion_perfil=p.informacion_perfil,
            )
            for p in dto.participantes
        ]

        return Campaña(
            id=Codigo(dto.id),
            nombre=Nombre(dto.nombre),
            tipo=TipoCampaña(dto.tipo),
            estado=EstadoCampaña(dto.estado),
            fecha_inicio=self._parse_fecha(dto.fecha_inicio),
            fecha_fin=self._parse_fecha(dto.fecha_fin),
            presupuesto=Dinero(monto=dto.presupuesto, divisa=dto.divisa),
            marca_id=Codigo(dto.marca_id) if dto.marca_id else None,
            participantes=participantes,
        )

    def obtener_tipo(self) -> type:
        return Campaña.__class__