from ....seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from ....seedwork.aplicacion.queries import ejecutar_query as query
from dataclasses import dataclass
from .base import ObtenerCampaignBaseHandler
from ....modulos.infraestructura.repositorios import RepositorioCampaigns
from ....modulos.infraestructura.mapeadores import MapeadorCampaign
import uuid

@dataclass
class QueryObtenerCampaign(Query):
    id: str

class ObtenerCampaignHandler(ObtenerCampaignBaseHandler):

    def handle(self, query: QueryObtenerCampaign) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioCampaigns.__class__)
        campaign = self.fabrica_campaigns.crear_objeto(repositorio.obtener_por_id(query.id), MapeadorCampaign())
        return QueryResultado(resultado=campaign)

@query.register(QueryObtenerCampaign)
def ejecutar_query_obtener_campaign(query: QueryObtenerCampaign):
    handler = ObtenerCampaignHandler()
    return handler.handle(query)