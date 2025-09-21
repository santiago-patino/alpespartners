from campaign.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from campaign.seedwork.aplicacion.queries import ejecutar_query as query
from campaign.modulos.dominio.entidades import Campaign
from campaign.modulos.infraestructura.dto import Campaign as CampaignDTO
from .base import ObtenerCampaignBaseHandler
from campaign.modulos.infraestructura.repositorios import RepositorioCampaigns
from campaign.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from campaign.config.uow import UnidadTrabajoSQLAlchemy
import uuid
from dataclasses import dataclass

@dataclass
class ObtenerCampaign(Query):
    id: str

class ObtenerCampaignHandler(ObtenerCampaignBaseHandler):

    def handle(self, query) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioCampaigns.__class__)
        
        uow = UnidadTrabajoSQLAlchemy()
        UnidadTrabajoPuerto.set_uow(uow)

        campaigns = repositorio.obtener_por_id(query.id)

        return QueryResultado(resultado=campaign_a_dict(campaigns))
    
@query.register(ObtenerCampaign)
def ejecutar_query_obtener_campaign(query: ObtenerCampaign):
    handler = ObtenerCampaignHandler()
    return handler.handle(query)

def campaign_a_dict(campaign):
    return {
        "id": str(campaign.id),
        "nombre": campaign.nombre,
        "presupuesto": campaign.presupuesto,
        "divisa": campaign.divisa,
        "marca_id": campaign.marca_id,
        "participantes": [
            {
                "id": str(p.id),
                "tipo": p.tipo,
                "nombre": p.nombre,
                "informacion_perfil": p.informacion_perfil
            }
            for p in getattr(campaign, "participantes", [])  # evita error si no tiene participantes
        ]
    }