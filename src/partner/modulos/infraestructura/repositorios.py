from ...modulos.dominio.entidades import Partner
from ...modulos.dominio.repositorios import RepositorioPartners
from ...modulos.dominio.fabricas import FabricaPartners
from ...config.db import get_db, SessionLocal

from .mapeadores import MapeadorPartner
from .dto import Partner as PartnerDTO

from uuid import UUID

class RepositorioPartnersSQLAlchemy(RepositorioPartners):

    def __init__(self):
        self._fabrica_partners: FabricaPartners = FabricaPartners()
        
    @property
    def db(self):
        from ...seedwork.infraestructura.uow import UnidadTrabajoPuerto
        return UnidadTrabajoPuerto.get_uow().db

    @property
    def fabrica_partners(self):
        return self._fabrica_partners

    def obtener_por_id(self, id: UUID) -> Partner:
        with SessionLocal() as db:
            partner_dto = db.query(PartnerDTO).filter_by(id=str(id)).one()
            return self.fabrica_partners.crear_objeto(partner_dto, MapeadorPartner())

    def obtener_todos(self) -> list[Partner]:
        # TODO
        raise NotImplementedError

    def agregar(self, partner: Partner):
        partner_dto = self.fabrica_partners.crear_objeto(partner, MapeadorPartner())
        self.db.add(partner_dto)

    def actualizar(self, partner: Partner):
        # TODO
        raise NotImplementedError

    def eliminar(self, reserva_id: UUID):
        # TODO
        raise NotImplementedError