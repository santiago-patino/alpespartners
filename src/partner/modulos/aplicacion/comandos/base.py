from ....seedwork.aplicacion.comandos import ComandoHandler
from ....modulos.infraestructura.fabricas import FabricaRepositorio
from ....modulos.dominio.fabricas import FabricaPartners

class RegistrarPartnerBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_partners: FabricaPartners = FabricaPartners()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_partners(self):
        return self._fabrica_partners
    