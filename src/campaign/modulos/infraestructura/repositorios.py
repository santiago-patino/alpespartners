from campaign.modulos.dominio.entidades import Campaign
from campaign.modulos.dominio.repositorios import RepositorioCampaigns
from campaign.modulos.dominio.fabricas import FabricaCampaigns
from campaign.config.db import get_db, SessionLocal

from .mapeadores import MapeadorCampaign
from .dto import Campaign as CampaignDTO

from uuid import UUID

class RepositorioCampaignsSQLAlchemy(RepositorioCampaigns):

    def __init__(self):
        self._fabrica_campaigns: FabricaCampaigns = FabricaCampaigns()
        
    @property
    def db(self):
        from campaign.seedwork.infraestructura.uow import UnidadTrabajoPuerto
        return UnidadTrabajoPuerto.get_uow().db

    @property
    def fabrica_campaigns(self):
        return self._fabrica_campaigns

    def obtener_por_id(self, id: UUID) -> Campaign:
        with SessionLocal() as db:
            campaign_dto = db.query(CampaignDTO).filter_by(id=str(id)).one()
            return self.fabrica_campaigns.crear_objeto(campaign_dto, MapeadorCampaign())

    def obtener_todos(self) -> list[Campaign]:
        # TODO
        raise NotImplementedError

    def agregar(self, campaign: Campaign):
        campaign_dto = self.fabrica_campaigns.crear_objeto(campaign, MapeadorCampaign())
        self.db.add(campaign_dto)

    def actualizar(self, campaign: Campaign):
        # TODO
        raise NotImplementedError

    def eliminar(self, reserva_id: UUID):
        # TODO
        raise NotImplementedError