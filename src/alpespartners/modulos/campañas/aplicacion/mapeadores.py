from alpespartners.seedwork.aplicacion.dto import Mapeador as AppMap
from alpespartners.seedwork.dominio.repositorios import Mapeador as RepMap
from alpespartners.modulos.campañas.dominio.entidades import Campaña, Participante
from alpespartners.modulos.campañas.dominio.objetos_valor import Dinero
from .dto import CampañaDTO, ParticipanteDTO, DineroDTO

from datetime import datetime
from enum import Enum

class MapeadorCampañaDTOJson(AppMap):
    
    def _procesar_participante(self, participante: dict) -> ParticipanteDTO:
        return ParticipanteDTO(
            id=participante.get("id", ""),
            tipo=participante.get("tipo", ""),
            nombre=participante.get("nombre", ""),
            informacion_perfil=participante.get("informacion_perfil", "")
        )

    def externo_a_dto(self, externo: dict) -> CampañaDTO:
        # Budget
        budget_raw = externo.get("presupuesto", {})
        budget_dto = None
        if budget_raw:
            budget_dto = DineroDTO(
                monto=float(budget_raw.get("monto", 0.0)),
                divisa=budget_raw.get("divisa", "USD")
            )

        # Participantes
        participantes_dto: list[ParticipantesDTO] = []
        for part in externo.get("participantes", []):
            participantes_dto.append(self._procesar_participante(part))
        
        # Campaña
        return CampañaDTO(
            id=externo.get("id", ""),
            nombre=externo.get("nombre", ""),
            tipo=externo.get("tipo", ""),
            estado=externo.get("estado", ""),
            fecha_inicio=externo.get("fecha_inicio", ""),
            fecha_fin=externo.get("fecha_fin", ""),
            presupuesto=budget_dto,
            divisa=externo.get("divisa", ""),
            marca_id=externo.get("marca_id", ""),
            participantes=participantes_dto
        )

    def dto_a_externo(self, dto: CampañaDTO) -> dict:
        return dto.__dict__

class MapeadorCampaña(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'
    
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
    
    def entidad_a_dto(self, entidad: Campaña) -> CampañaDTO:
        return CampañaDTO(
            id=str(entidad.id),
            nombre=entidad.nombre,
            tipo=entidad.tipo.value if isinstance(entidad.tipo, Enum) else entidad.tipo,
            estado=entidad.estado.value if isinstance(entidad.estado, Enum) else entidad.estado,
            fecha_inicio=entidad.fecha_inicio,
            fecha_fin=entidad.fecha_fin,
            presupuesto=entidad.presupuesto.monto,
            divisa=entidad.presupuesto.divisa,
            marca_id=str(entidad.marca_id) if entidad.marca_id else None,
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
        
    def dto_a_entidad(self, dto: CampañaDTO) -> Campaña:
        participantes = []
        if dto.participantes:
            for p in dto.participantes:
                participantes.append(
                    Participante(
                        id=p.id,
                        tipo=p.tipo,
                        nombre=p.nombre,
                        informacion_perfil=p.informacion_perfil,
                    )
                )
        
        return Campaña(
            id=dto.id,
            nombre=dto.nombre,
            tipo=dto.tipo,
            estado=dto.estado,
            fecha_inicio=dto.fecha_inicio,
            fecha_fin=dto.fecha_fin,
            presupuesto=Dinero(monto=dto.presupuesto.monto, divisa=dto.presupuesto.divisa),
            marca_id=dto.marca_id,
            participantes=participantes
        )
        
    def obtener_tipo(self) -> type:
        return Campaña.__class__



