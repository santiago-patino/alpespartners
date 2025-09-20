from partner.seedwork.dominio.repositorios import Mapeador
from partner.modulos.dominio.entidades import Partner, Affiliate, Influencer
from partner.modulos.dominio.eventos import PartnerRegistrado, EventoPartner, RegistroPartnerFallido
from .dto import TipoPartner, Partner as PartnerDTO

from typing import Union, Optional
from datetime import datetime
from enum import Enum
from campaign.seedwork.infraestructura import utils
from .excepciones import NoExisteImplementacionParaTipoFabricaExcepcion

class MapadeadorEventosPartner(Mapeador):

    # Versiones aceptadas
    versions = ('v1',)

    LATEST_VERSION = versions[0]

    def __init__(self):
        self.router = {
            PartnerRegistrado: self._entidad_a_partner_creado,
            RegistroPartnerFallido: self._entidad_a_partner_fallido,
        }

    def obtener_tipo(self) -> type:
        return EventoReserva.__class__

    def es_version_valida(self, version):
        for v in self.versions:
            if v == version:
                return True
        return False

    def _entidad_a_partner_creado(self, entidad: PartnerRegistrado, version=LATEST_VERSION):
        def v1(evento):
            from .v1.eventos import PartnerRegistrado, EventoPartner
            
            payload = PartnerRegistrado(
                id=str(evento.id),
                id_campaign=str(evento.id_campaign),
                nombre=str(evento.nombre), 
                tipo=evento.tipo,
                informacion_perfil=str(evento.informacion_perfil),
                fecha_creacion=evento.fecha_creacion,
            )
            evento_integracion = EventoPartner(id=str(evento.id))
            evento_integracion.id = str(evento.id)
            evento_integracion.time = int(utils.time_millis())
            evento_integracion.specversion = str(version)
            evento_integracion.type = 'partner_registrado'
            evento_integracion.datacontenttype = 'AVRO'
            evento_integracion.service_name = 'alpespartners'
            evento_integracion.partner_registrado = payload
            
            print(evento_integracion.__class__)

            return evento_integracion
                    
        if not self.es_version_valida(version):
            raise Exception(f'No se sabe procesar la version {version}')

        if version == 'v1':
            return v1(entidad) 
    
    def _entidad_a_partner_fallido(self, entidad: RegistroPartnerFallido, version=LATEST_VERSION):
        def v1(evento):
            from .v1.eventos import RegistroPartnerFallido, EventoPartner
            
            payload = RegistroPartnerFallido(
                id=str(evento.id), 
                id_campaign=str(evento.id_campaign),
                nombre=str(evento.nombre), 
                tipo=evento.tipo,
                informacion_perfil=str(evento.informacion_perfil),
                fecha_creacion=evento.fecha_creacion,
            )
            evento_integracion = EventoPartner(id=str(evento.id))
            evento_integracion.id = str(evento.id)
            evento_integracion.time = int(utils.time_millis())
            evento_integracion.specversion = str(version)
            evento_integracion.type = 'partner_fallido'
            evento_integracion.datacontenttype = 'AVRO'
            evento_integracion.service_name = 'alpespartners'
            evento_integracion.partner_fallido = payload

            return evento_integracion
                    
        if not self.es_version_valida(version):
            raise Exception(f'No se sabe procesar la version {version}')

        if version == 'v1':
            return v1(entidad)       

    def entidad_a_dto(self, entidad: EventoPartner, version=LATEST_VERSION) -> PartnerDTO:
        if not entidad:
            raise NoExisteImplementacionParaTipoFabricaExcepcion
        func = self.router.get(entidad.__class__, None)

        if not func:
            raise NoExisteImplementacionParaTipoFabricaExcepcion

        return func(entidad, version=version)
    
    def dto_a_entidad(self, dto: PartnerDTO, version=LATEST_VERSION) -> Partner:
        raise NotImplementedError


class MapeadorPartner(Mapeador):
    
    def entidad_a_dto(self, entidad: Partner):
        tipo = TipoPartner.influencer if isinstance(entidad, Influencer) else TipoPartner.affiliate
        return PartnerDTO(
            id=entidad.id,
            id_campaign=entidad.id_campaign,
            nombre=entidad.nombre,
            tipo=tipo,
            informacion_perfil=entidad.informacion_perfil
        )

    def dto_a_entidad(self, dto: PartnerDTO):
        return Partner(
            id_campaign=dto.id_campaign,
            nombre=dto.nombre,
            tipo=dto.tipo,
            informacion_perfil=dto.informacion_perfil
        )
        
    def entidad_a_externo(self, entidad: Partner) -> dict:
        return entidad.__dict__
        
    def obtener_tipo(self) -> type:
        return Partner.__class__