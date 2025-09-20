from campaign.seedwork.dominio.repositorios import Mapeador
from campaign.modulos.dominio.entidades import Campaign, Participante
from campaign.modulos.dominio.eventos import CampaignRegistrada, EventoCampaign
from .dto import Campaign as CampaignDTO

from typing import Union, Optional
from datetime import datetime
from enum import Enum
from campaign.seedwork.infraestructura import utils
from .excepciones import NoExisteImplementacionParaTipoFabricaExcepcion


class MapadeadorEventosCampaign(Mapeador):

    # Versiones aceptadas
    versions = ('v1',)

    LATEST_VERSION = versions[0]

    def __init__(self):
        self.router = {
            CampaignRegistrada: self._entidad_a_reserva_creada,
            # ReservaAprobada: self._entidad_a_reserva_aprobada,
            # ReservaCancelada: self._entidad_a_reserva_cancelada,
            # ReservaPagada: self._entidad_a_reserva_pagada
        }

    def obtener_tipo(self) -> type:
        return EventoReserva.__class__

    def es_version_valida(self, version):
        for v in self.versions:
            if v == version:
                return True
        return False

    def _entidad_a_reserva_creada(self, entidad: CampaignRegistrada, version=LATEST_VERSION):
        def v1(evento):
            from .v1.eventos import CampaignRegistrada, EventoCampaign

            payload = CampaignRegistrada(
                id=str(evento.id),
                nombre=str(evento.nombre), 
                presupuesto=evento.presupuesto, 
                divisa=str(evento.divisa),
                marca_id=str(evento.marca_id),
                participantes=str(evento.participantes), 
            )
            evento_integracion = EventoCampaign(id=str(evento.id))
            evento_integracion.id = str(evento.id)
            evento_integracion.time = int(utils.time_millis())
            evento_integracion.specversion = str(version)
            evento_integracion.type = 'CampaignCreada'
            evento_integracion.datacontenttype = 'AVRO'
            evento_integracion.service_name = 'alpespartners'
            evento_integracion.campaign_registrada = payload

            return evento_integracion
                    
        if not self.es_version_valida(version):
            raise Exception(f'No se sabe procesar la version {version}')

        if version == 'v1':
            return v1(entidad)       

    def entidad_a_dto(self, entidad: EventoCampaign, version=LATEST_VERSION) -> CampaignDTO:
        if not entidad:
            raise NoExisteImplementacionParaTipoFabricaExcepcion
        func = self.router.get(entidad.__class__, None)

        if not func:
            raise NoExisteImplementacionParaTipoFabricaExcepcion

        return func(entidad, version=version)
    
    def dto_a_entidad(self, dto: CampaignDTO, version=LATEST_VERSION) -> Campaign:
        raise NotImplementedError

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
            id=entidad.id,
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