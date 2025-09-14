from campaign.seedwork.aplicacion.queries import Query, QueryHandler, ResultadoQuery
import uuid

class ObtenerTodosPartners(Query):
    ...

class ObtenerTodosPartnersHandler(QueryHandler):

    def handle() -> ResultadoQuery:
        ...