from partner.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from partner.seedwork.aplicacion.queries import ejecutar_query as query
from partner.modulos.dominio.entidades import Partner

from .base import ObtenerPartnerBaseHandler
from partner.modulos.infraestructura.repositorios import RepositorioPartners
from partner.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from partner.config.uow import UnidadTrabajoSQLAlchemy
import uuid
from dataclasses import dataclass

@dataclass
class ObtenerPartner(Query):
    id: str

class ObtenerPartnerHandler(ObtenerPartnerBaseHandler):

    def handle(self, query) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioPartners.__class__)
        
        uow = UnidadTrabajoSQLAlchemy()
        UnidadTrabajoPuerto.set_uow(uow)

        partners = repositorio.obtener_por_id(query.id)

        return QueryResultado(resultado=partner_a_dict(partners))
    
@query.register(ObtenerPartner)
def ejecutar_query_obtener_partner(query: ObtenerPartner):
    handler = ObtenerPartnerHandler()
    return handler.handle(query)

def partner_a_dict(partner):
    return {
        "id": str(partner.id),
        "id_campaign": str(getattr(partner, "id_campaign", "")),
        "nombre": getattr(partner, "nombre", ""),
        "tipo": getattr(partner, "tipo", ""),
        "informacion_perfil": getattr(partner, "informacion_perfil", "")
    }