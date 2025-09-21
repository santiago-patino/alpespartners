from campaign.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from campaign.seedwork.aplicacion.queries import ejecutar_query as query
from campaign.modulos.dominio.entidades import Campaign
from campaign.modulos.infraestructura.dto import Campaign as CampaignDTO
from .base import ObtenerCampaignBaseHandler
from campaign.modulos.infraestructura.repositorios import RepositorioCampaigns
from campaign.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from campaign.config.uow import UnidadTrabajoSQLAlchemy
import uuid

class ObtenerTodosCampaigns(Query):
    ...

class ObtenerTodosCampaignsHandler(ObtenerCampaignBaseHandler):

    def handle(self, query) -> QueryResultado:
        campaigns_dto = []
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioCampaigns.__class__)
        
        uow = UnidadTrabajoSQLAlchemy()
        UnidadTrabajoPuerto.set_uow(uow)

        campaigns = repositorio.obtener_todos()
        
        campaigns_dicts = [campaign_a_dict(c) for c in campaigns]

        return QueryResultado(resultado=campaigns_dicts)
    
@query.register(ObtenerTodosCampaigns)
def ejecutar_query_obtener_campaigns(query: ObtenerTodosCampaigns):
    handler = ObtenerTodosCampaignsHandler()
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