from traking.seedwork.aplicacion.comandos import Comando, ComandoHandler
from traking.seedwork.aplicacion.comandos import ejecutar_commando as comando
from traking.modulos.dominio.entidades import Evento 
from traking.modulos.infraestructura.repositorios import RepositorioEventos
from traking.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from traking.config.uow import UnidadTrabajoSQLAlchemy
from traking.modulos.infraestructura.mapeadores import MapeadorEvento
from .base import RegistrarEventoBaseHandler
from dataclasses import dataclass
import datetime
import time

@dataclass
class ComandoRegistrarEvento(Comando):
    id_partner: str
    id_campana: str
    fecha: str

class RegistrarEventoHandler(RegistrarEventoBaseHandler):

    def a_entidad(self, comando: ComandoRegistrarEvento) -> Evento:
        params = dict(
            id_partner=comando.id_partner,
            id_campana=comando.id_campana,
            fecha=comando.fecha,
        )
        
        partner = Evento(**params)

        return partner
        
    def handle(self, comando: ComandoRegistrarEvento):
        evento = self.a_entidad(comando)
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioEventos.__class__)
        #repositorio.agregar(evento)
        
        uow = UnidadTrabajoSQLAlchemy()
        UnidadTrabajoPuerto.set_uow(uow)
        
        # Registrar batch y commit
        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, evento)
        UnidadTrabajoPuerto.commit()

@comando.register(ComandoRegistrarEvento)
def ejecutar_comando_registrar_evento(comando: ComandoRegistrarEvento):
    handler = RegistrarEventoHandler()
    handler.handle(comando)