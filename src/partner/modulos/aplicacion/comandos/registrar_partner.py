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
from partner.modulos.infraestructura.despachadores import Despachador
from partner.modulos.infraestructura.v1.comandos import ComandoRegistrarEvento, RegistrarEvento
from partner.seedwork.infraestructura import utils

@dataclass
class ComandoRegistrarPartner(Comando):
    id_campaign: str
    nombre: str
    tipo: str
    informacion_perfil: str

class RegistrarPartnerHandler(RegistrarPartnerBaseHandler):

    def a_entidad(self, comando: ComandoRegistrarPartner) -> Partner:
        params = dict(
            id_campaign=comando.id_campaign,
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
        
        #UnidadTrabajoPuerto.registrar_failure(partner)
        
        comando_registrar_eventos(partner)
        
        

@comando.register(ComandoRegistrarPartner)
def ejecutar_comando_registrar_partner(comando: ComandoRegistrarPartner):
    handler = RegistrarPartnerHandler()
    handler.handle(comando)
    
def comando_registrar_eventos(data):
    print(data)
    
    payload = RegistrarEvento(
        id_partner = str(data.id),
        id_campana = str(data.id_campaign),
        fecha = utils.time_millis()
    )

    comando = ComandoRegistrarEvento(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=RegistrarEvento.__name__,
        data = payload
    )
    
    despachador = Despachador()
    despachador.publicar_mensaje(comando, "comando-registrar-evento-conversion")