from partner.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from partner.seedwork.aplicacion.queries import ejecutar_query as query
from partner.modulos.dominio.entidades import Partner

from .base import ObtenerPartnerBaseHandler
from partner.modulos.infraestructura.repositorios import RepositorioPartners
from partner.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from partner.config.uow import UnidadTrabajoSQLAlchemy
import uuid

class ObtenerTodosPartners(Query):
    ...

class ObtenerTodosPartnersHandler(ObtenerPartnerBaseHandler):

    def handle(self, query) -> QueryResultado:
        partners_dto = []
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioPartners.__class__)
        
        uow = UnidadTrabajoSQLAlchemy()
        UnidadTrabajoPuerto.set_uow(uow)

        partners = repositorio.obtener_todos()
        
        partners_dicts = [partner_a_dict(c) for c in partners]

        return QueryResultado(resultado=partners_dicts)
    
@query.register(ObtenerTodosPartners)
def ejecutar_query_obtener_partners(query: ObtenerTodosPartners):
    handler = ObtenerTodosPartnersHandler()
    return handler.handle(query)

def partner_a_dict(partner):
    return {
        "id": str(getattr(partner, "id", "")),
        "id_campaign": str(getattr(partner, "id_campaign", "")),
        "nombre": getattr(partner, "nombre", ""),
        "tipo": getattr(partner, "tipo", ""),
        "informacion_perfil": getattr(partner, "informacion_perfil", "")
    }