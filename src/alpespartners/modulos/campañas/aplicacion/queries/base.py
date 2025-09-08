from alpespartners.seedwork.aplicacion.queries import QueryHandler
from alpespartners.modulos.campañas.infraestructura.fabricas import FabricaRepositorio
from alpespartners.modulos.campañas.dominio.fabricas import FabricaCampañas

class CampañaQueryBaseHandler(QueryHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_campañas: FabricaCampañas = FabricaCampañas()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_campañas(self):
        return self._fabrica_campañas    