from partner.modulos.dominio.entidades import Partner
from partner.modulos.dominio.repositorios import RepositorioPartners
from partner.modulos.dominio.fabricas import FabricaPartners
from partner.config.db import get_db, SessionLocal

from .mapeadores import MapeadorPartner
from .dto import Partner as PartnerDTO

from uuid import UUID

class RepositorioPartnersSQLAlchemy(RepositorioPartners):

    def __init__(self):
        self._fabrica_partners: FabricaPartners = FabricaPartners()
        
    @property
    def db(self):
        from partner.seedwork.infraestructura.uow import UnidadTrabajoPuerto
        return UnidadTrabajoPuerto.get_uow().db

    @property
    def fabrica_partners(self):
        return self._fabrica_partners

    def obtener_por_id(self, partner_id: UUID) -> Partner:
        partner_dto = self.db.query(PartnerDTO).filter(PartnerDTO.id == partner_id).first()
        if partner_dto:
            return self.fabrica_partners.crear_objeto(partner_dto, MapeadorPartner())
        return None
        # partner_dto = self.db.query(PartnerDTO).filter(PartnerDTO.id == partner_id).one()
        # if partner_dto:
        #     return self.fabrica_partners.crear_objeto(partner_dto, MapeadorPartner())
        # return None  # o lanzar excepción si no existe
        # with SessionLocal() as db:
        #     partner_dto = db.query(PartnerDTO).filter_by(id=str(id)).one()
        #     return self.fabrica_partners.crear_objeto(partner_dto, MapeadorPartner())

    def obtener_todos(self) -> list[Partner]:
        # TODO
        raise NotImplementedError

    def agregar(self, partner: Partner):
        partner_dto = self.fabrica_partners.crear_objeto(partner, MapeadorPartner())
        self.db.add(partner_dto)

    def actualizar(self, partner: Partner):
        # TODO
        raise NotImplementedError

    def eliminar(self, partner_id: UUID):
        partner_dto = self.db.query(PartnerDTO).filter(PartnerDTO.id == partner_id).first()
        if partner_dto:
            eliminado = self.fabrica_partners.crear_objeto(partner_dto, MapeadorPartner())
            self.db.delete(partner_dto)
            return eliminado