from partner.seedwork.aplicacion.queries import Query, QueryHandler, ResultadoQuery
import uuid

class ObtenerPartner(Query):
    listing_id: uuid.UUID

class ObtenerPartnerHandler(QueryHandler):

    def handle() -> ResultadoQuery:
        ...