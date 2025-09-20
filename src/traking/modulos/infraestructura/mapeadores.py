from traking.seedwork.dominio.repositorios import Mapeador
from traking.modulos.dominio.entidades import Evento
from .dto import Evento as EventoDTO
from traking.modulos.dominio.eventos import EventoRegistrado, RegistroEventoFallido, EventoTraking
from partner.seedwork.infraestructura import utils

from typing import Union, Optional
from datetime import datetime
from enum import Enum

class MapadeadorEventos(Mapeador):

    # Versiones aceptadas
    versions = ('v1',)

    LATEST_VERSION = versions[0]

    def __init__(self):
        self.router = {
            EventoRegistrado: self._entidad_a_evento_creado,
            RegistroEventoFallido: self._entidad_a_evento_fallido,
        }

    def obtener_tipo(self) -> type:
        return EventoReserva.__class__

    def es_version_valida(self, version):
        for v in self.versions:
            if v == version:
                return True
        return False

    def _entidad_a_evento_creado(self, entidad: EventoRegistrado, version=LATEST_VERSION):
        def v1(evento):
            from .v1.eventos import EventoRegistrado, EventoTraking
            
            payload = EventoRegistrado(
                id=str(evento.id),
                id_partner=str(evento.id_partner),
                id_campana=str(evento.id_campana), 
                fecha=evento.fecha,
            )
            evento_integracion = EventoTraking(id=str(evento.id))
            evento_integracion.id = str(evento.id)
            evento_integracion.time = int(utils.time_millis())
            evento_integracion.specversion = str(version)
            evento_integracion.type = 'evento_registrado'
            evento_integracion.datacontenttype = 'AVRO'
            evento_integracion.service_name = 'alpespartners'
            evento_integracion.evento_registrado = payload

            return evento_integracion
                    
        if not self.es_version_valida(version):
            raise Exception(f'No se sabe procesar la version {version}')

        if version == 'v1':
            return v1(entidad) 
    
    def _entidad_a_evento_fallido(self, entidad: RegistroEventoFallido, version=LATEST_VERSION):
        def v1(evento):
            from .v1.eventos import RegistroEventoFallido, EventoTraking
            
            payload = RegistroEventoFallido(
                id=str(evento.id),
                id_partner=str(evento.id_partner),
                id_campana=str(evento.id_campana), 
                fecha=evento.fecha,
            )
            evento_integracion = EventoTraking(id=str(evento.id))
            evento_integracion.id = str(evento.id)
            evento_integracion.time = int(utils.time_millis())
            evento_integracion.specversion = str(version)
            evento_integracion.type = 'evento_fallido'
            evento_integracion.datacontenttype = 'AVRO'
            evento_integracion.service_name = 'alpespartners'
            evento_integracion.evento_fallido = payload

            return evento_integracion
                    
        if not self.es_version_valida(version):
            raise Exception(f'No se sabe procesar la version {version}')

        if version == 'v1':
            return v1(entidad)       

    def entidad_a_dto(self, entidad: EventoTraking, version=LATEST_VERSION) -> EventoDTO:
        if not entidad:
            raise NoExisteImplementacionParaTipoFabricaExcepcion
        func = self.router.get(entidad.__class__, None)

        if not func:
            raise NoExisteImplementacionParaTipoFabricaExcepcion

        return func(entidad, version=version)
    
    def dto_a_entidad(self, dto: EventoDTO, version=LATEST_VERSION) -> Evento:
        raise NotImplementedError

class MapeadorEvento(Mapeador):
    
    def entidad_a_dto(self, entidad: Evento):
        return EventoDTO(
            id_partner=entidad.id_partner,
            id_campana=entidad.id_campana,
            fecha=entidad.fecha
        )

    def dto_a_entidad(self, dto: EventoDTO):
        return Evento(
            id=dto.id,
            id_partner=dto.id_partner,
            id_campana=dto.id_campana,
            fecha=dto.fecha
        )
        
    def entidad_a_externo(self, entidad: Evento) -> dict:
        return entidad.__dict__
        
    def obtener_tipo(self) -> type:
        return Evento.__class__