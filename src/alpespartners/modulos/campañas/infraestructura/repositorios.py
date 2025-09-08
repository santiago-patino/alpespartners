""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de vuelos

"""

from alpespartners.config.db import db
from alpespartners.modulos.campañas.dominio.repositorios import RepositorioCampañas, RepositorioMarcas
from alpespartners.modulos.campañas.dominio.objetos_valor import Nombre, Dinero, EstadoCampaña, TipoCampaña, TipoParticipante
from alpespartners.modulos.campañas.dominio.entidades import Campaña, Marca, Participante
from alpespartners.modulos.campañas.dominio.fabricas import FabricaCampañas
from alpespartners.seedwork.dominio.entidades import Entidad

from .dto import Campaña as CampañaDTO
from .mapeadores import MapeadorCampaña
from alpespartners.modulos.campañas.aplicacion.mapeadores import MapeadorCampañaDTOJson, MapeadorCampaña as MapeadorCampañaApp

from uuid import UUID

class RepositorioMarcasSQLite(RepositorioMarcas):

    def obtener_por_id(self, id: UUID) -> Marca:
        # TODO
        raise NotImplementedError

    def obtener_todos(self) -> list[Marca]:
        # TODO
        raise NotImplementedError

    def agregar(self, entity: Marca):
        # TODO
        raise NotImplementedError

    def actualizar(self, entity: Marca):
        # TODO
        raise NotImplementedError

    def eliminar(self, entity_id: UUID):
        # TODO
        raise NotImplementedError


class RepositorioCampañasSQLite(RepositorioCampañas):

    def __init__(self):
        self._fabrica_campañas: FabricaCampañas = FabricaCampañas()

    @property
    def fabrica_campañas(self):
        return self._fabrica_campañas

    def obtener_por_id(self, id: UUID) -> Campaña:
        campaña_orm = db.session.query(CampañaDTO).filter_by(id=str(id)).one()
        map_campaña = MapeadorCampaña()
        campaña_dto = map_campaña.orm_a_dto(campaña_orm)
        return campaña_dto

    def obtener_todos(self) -> list[Campaña]:
        # TODO
        raise NotImplementedError

    def agregar(self, campaña: Campaña):
        campaña_dto = self.fabrica_campañas.crear_objeto(campaña, MapeadorCampaña())
        db.session.add(campaña_dto)
        db.session.commit()

    def actualizar(self, campaña: Campaña):
        # TODO
        raise NotImplementedError

    def eliminar(self, campaña_id: UUID):
        # TODO
        raise NotImplementedError