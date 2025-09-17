from ....seedwork.aplicacion.comandos import ComandoHandler
from ....modulos.infraestructura.fabricas import FabricaRepositorio
from ....modulos.dominio.fabricas import FabricaCampaigns

class RegistrarCampaignBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_campaigns: FabricaCampaigns = FabricaCampaigns()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_campaigns(self):
        return self._fabrica_campaigns
    