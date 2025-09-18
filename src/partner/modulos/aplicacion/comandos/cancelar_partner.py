from partner.seedwork.aplicacion.comandos import Comando, ComandoHandler
from partner.seedwork.aplicacion.comandos import ejecutar_commando as comando
from partner.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from partner.modulos.infraestructura.repositorios import RepositorioPartners
from partner.config.uow import UnidadTrabajoSQLAlchemy
from .base import RegistrarPartnerBaseHandler
from dataclasses import dataclass
import datetime 
import time
import json

@dataclass
class ComandoCancelarPartner(Comando):
    id: str

class CancelarPartnerHandler(RegistrarPartnerBaseHandler):
        
    def handle(self, comando: ComandoCancelarPartner):
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioPartners.__class__)
        
        uow = UnidadTrabajoSQLAlchemy()
        UnidadTrabajoPuerto.set_uow(uow)
        
        # Registrar batch y commit
        UnidadTrabajoPuerto.registrar_batch(repositorio.eliminar, comando.id)
        UnidadTrabajoPuerto.commit()

@comando.register(ComandoCancelarPartner)
def ejecutar_comando_cancelar_partner(comando: ComandoCancelarPartner):
    handler = CancelarPartnerHandler()
    handler.handle(comando)