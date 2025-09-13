from partner.modulos.dominio.entidades import Partner
from partner.modulos.dominio.repositorios import RepositorioPartners
from partner.modulos.dominio.fabricas import FabricaPartners

# from .mapeadores import MapeadorCampaña

from uuid import UUID

class RepositorioPartnersSQLAlchemy(RepositorioPartners):

    def __init__(self):
        self._fabrica_partners: FabricaVuelos = FabricaPartners()

    @property
    def fabrica_partners(self):
        return self._fabrica_partners

    def obtener_por_id(self, id: UUID) -> Partner:
        reserva_dto = db.session.query(ReservaDTO).filter_by(id=str(id)).one()
        return self.fabrica_vuelos.crear_objeto(reserva_dto, MapeadorReserva())

    def obtener_todos(self) -> list[Partner]:
        # TODO
        raise NotImplementedError

    def agregar(self, partner: Partner):
        # partner_dto = self.fabrica_partners.crear_objeto(partner, MapeadorReserva())
        db.session.add(partner)

    def actualizar(self, partner: Partner):
        # TODO
        raise NotImplementedError

    def eliminar(self, reserva_id: UUID):
        # TODO
        raise NotImplementedError