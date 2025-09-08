from alpespartners.seedwork.aplicacion.comandos import Comando
from alpespartners.modulos.campañas.aplicacion.dto import CampañaDTO, ParticipanteDTO
from .base import CrearCampañaBaseHandler
from dataclasses import dataclass, field
from alpespartners.seedwork.aplicacion.comandos import ejecutar_commando as comando

from alpespartners.modulos.campañas.dominio.entidades import Campaña
from alpespartners.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from alpespartners.modulos.campañas.aplicacion.mapeadores import MapeadorCampaña
from alpespartners.modulos.campañas.infraestructura.repositorios import RepositorioCampañas

@dataclass
class CrearCampaña(Comando):
    id: str
    nombre: str
    tipo: str
    estado: str
    fecha_inicio: str
    fecha_fin: str
    presupuesto: float
    divisa: str
    marca_id: str
    participantes: list[ParticipanteDTO]


class CrearCampañaHandler(CrearCampañaBaseHandler):
    
    def handle(self, comando: CrearCampaña):
        campaña_dto = CampañaDTO(
                id=comando.id
            ,   nombre=comando.nombre
            ,   tipo=comando.tipo
            ,   estado=comando.estado
            ,   fecha_inicio=comando.fecha_inicio
            ,   fecha_fin=comando.fecha_fin
            ,   presupuesto=comando.presupuesto
            ,   divisa=comando.divisa
            ,   marca_id=comando.marca_id
            ,   participantes=comando.participantes)

        campaña: Campaña = self.fabrica_campañas.crear_objeto(campaña_dto, MapeadorCampaña())
        campaña.crear_campaña(campaña)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioCampañas.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, campaña)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(CrearCampaña)
def ejecutar_comando_crear_campaña(comando: CrearCampaña):
    handler = CrearCampañaHandler()
    handler.handle(comando)
    