from traking.seedwork.aplicacion.comandos import ComandoHandler
from traking.modulos.infraestructura.fabricas import FabricaRepositorio
from traking.modulos.dominio.fabricas import FabricaEventos

class RegistrarEventoBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_eventos: FabricaEventos = FabricaEventos()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_eventos(self):
        return self._fabrica_eventos
    