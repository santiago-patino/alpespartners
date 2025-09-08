from alpespartners.modulos.campañas.dominio.entidades import Campaña
from alpespartners.modulos.campañas.dominio.fabricas import FabricaCampañas
from alpespartners.modulos.campañas.infraestructura.fabricas import \
    FabricaRepositorio
from alpespartners.modulos.campañas.infraestructura.repositorios import \
    RepositorioCampañas
from alpespartners.seedwork.aplicacion.servicios import Servicio

from .dto import CampañaDTO
from .mapeadores import MapeadorCampaña


class ServicioCampaña(Servicio):

    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_campañas: FabricaCampañas = FabricaCampañas()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_campañas(self):
        return self._fabrica_campañas

    def crear_campaña(self, campaña_dto: CampañaDTO) -> CampañaDTO:
        campaña: Campaña = self.fabrica_campañas.crear_objeto(campaña_dto, MapeadorCampaña())

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioCampañas)
        repositorio.agregar(campaña)

        return self.fabrica_campañas.crear_objeto(campaña, MapeadorCampaña())

    def obtener_campaña_por_id(self, id) -> CampañaDTO:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioCampañas)
        return repositorio.obtener_por_id(id).__dict__

