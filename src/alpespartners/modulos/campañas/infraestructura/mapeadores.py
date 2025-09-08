""" Mapeadores para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from alpespartners.seedwork.dominio.repositorios import Mapeador
from alpespartners.modulos.campañas.dominio.entidades import Campaña, Participante
from alpespartners.modulos.campañas.dominio.objetos_valor import (
    Codigo, Nombre, TipoCampaña, EstadoCampaña, Dinero, TipoParticipante
)
from .dto import Campaña, Participante
from alpespartners.modulos.campañas.aplicacion.dto import CampañaDTO, ParticipanteDTO

from typing import Union, Optional
from datetime import datetime
from enum import Enum


class MapeadorCampaña(Mapeador):
    _FORMATO_FECHA = "%Y-%m-%dT%H:%M:%SZ"
    
    def orm_a_dto(self, orm: Campaña) -> CampañaDTO:
        # Extraemos solo los campos relevantes del ORM
        return CampañaDTO(
            id=orm.id,
            nombre=orm.nombre,
            tipo=orm.tipo,
            estado=orm.estado,
            fecha_inicio=orm.fecha_inicio.isoformat() if orm.fecha_inicio else None,
            fecha_fin=orm.fecha_fin.isoformat() if orm.fecha_fin else None,
            presupuesto=float(orm.presupuesto),
            divisa=orm.divisa,
            marca_id=orm.marca_id,
            participantes=[
                ParticipanteDTO(
                    id=p.id,
                    tipo=p.tipo,
                    nombre=p.nombre,
                    informacion_perfil=getattr(p, "informacion_perfil", None)
                )
                for p in getattr(orm, "participantes", [])
            ]
        )

    def entidad_a_dto(self, entidad: Campaña) -> CampañaDTO:
        return CampañaDTO(
            id=str(entidad.id),
            nombre=entidad.nombre,
            tipo=entidad.tipo.value if isinstance(entidad.tipo, Enum) else entidad.tipo,
            estado=entidad.estado.value if isinstance(entidad.estado, Enum) else entidad.estado,
            fecha_inicio=self._parse_fecha(entidad.fecha_inicio),
            fecha_fin=self._parse_fecha(entidad.fecha_fin),
            presupuesto=entidad.presupuesto.monto,
            divisa=entidad.presupuesto.divisa,
            marca_id=entidad.marca_id,
            participantes=[
                ParticipanteDTO(
                    id=str(p.id),
                    tipo=p.tipo.value if isinstance(p.tipo, Enum) else p.tipo,
                    nombre=p.nombre,
                    informacion_perfil=getattr(p, "informacion_perfil", None),
                )
                for p in entidad.participantes
            ],
        )
        
    def _parse_fecha(self, valor):
        if isinstance(valor, datetime):
            return valor
        if isinstance(valor, str) and valor:
            try:
                return datetime.strptime(valor, self._FORMATO_FECHA)
            except ValueError:
                # fallback si viene con timezone "Z" mal interpretado
                return datetime.fromisoformat(valor.replace("Z", "+00:00"))
        return None


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