from traking.seedwork.aplicacion.comandos import Comando, ComandoHandler
from traking.seedwork.aplicacion.comandos import ejecutar_commando as comando
from traking.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from traking.modulos.infraestructura.repositorios import RepositorioEventos
from traking.config.uow import UnidadTrabajoSQLAlchemy
from .base import RegistrarEventoBaseHandler
from dataclasses import dataclass
import datetime 
import time
import json

@dataclass
class ComandoCancelarEvento(Comando):
    id: str

class CancelarPartnerHandler(RegistrarEventoBaseHandler):
        
    def handle(self, comando: ComandoCancelarEvento):
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioEventos.__class__)
        
        uow = UnidadTrabajoSQLAlchemy()
        UnidadTrabajoPuerto.set_uow(uow)
        
        # Registrar batch y commit
        UnidadTrabajoPuerto.registrar_batch(repositorio.eliminar, comando.id)
        UnidadTrabajoPuerto.commit()

@comando.register(ComandoCancelarEvento)
def ejecutar_comando_cancelar_evento(comando: ComandoCancelarEvento):
    handler = CancelarPartnerHandler()
    handler.handle(comando)