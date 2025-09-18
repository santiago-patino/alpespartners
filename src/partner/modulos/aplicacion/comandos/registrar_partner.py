from partner.seedwork.aplicacion.comandos import Comando, ComandoHandler
from partner.seedwork.aplicacion.comandos import ejecutar_commando as comando
from partner.modulos.dominio.entidades import Partner, Affiliate, Influencer
from partner.modulos.dominio.objetos_valor import Cedula, Email, Nombre, Rut 
from partner.modulos.infraestructura.repositorios import RepositorioPartners
from partner.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from partner.config.uow import UnidadTrabajoSQLAlchemy
from partner.modulos.infraestructura.mapeadores import MapeadorPartner
from .base import RegistrarPartnerBaseHandler
from dataclasses import dataclass
import datetime
import time

@dataclass
class ComandoRegistrarPartner(Comando):
    nombre: str
    tipo: str
    informacion_perfil: str

class RegistrarPartnerHandler(RegistrarPartnerBaseHandler):

    def a_entidad(self, comando: ComandoRegistrarPartner) -> Partner:
        params = dict(
            nombre=comando.nombre,
            tipo=comando.tipo,
            informacion_perfil=comando.informacion_perfil,
            fecha_creacion = datetime.datetime.now(),
            fecha_actualizacion = datetime.datetime.now()
        )
        
        partner = Partner(**params)

        # if comando.tipo == 'Influencer':
        #     partner = Influencer(**params)
        # else:
        #     partner = Affiliate(**params)

        return partner
        
    def handle(self, comando: ComandoRegistrarPartner):
        partner = self.a_entidad(comando)
        partner.crear_partner(partner)
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioPartners.__class__)
        
        uow = UnidadTrabajoSQLAlchemy()
        UnidadTrabajoPuerto.set_uow(uow)
        
        # Registrar batch y commit
        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, partner)
        UnidadTrabajoPuerto.commit()
        
        

@comando.register(ComandoRegistrarPartner)
def ejecutar_comando_registrar_partner(comando: ComandoRegistrarPartner):
    handler = RegistrarPartnerHandler()
    handler.handle(comando)