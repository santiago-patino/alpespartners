from campaign.seedwork.aplicacion.comandos import Comando, ComandoHandler
from campaign.seedwork.aplicacion.comandos import ejecutar_commando as comando
from campaign.modulos.dominio.entidades import Campaign, Participante
from campaign.modulos.infraestructura.repositorios import RepositorioCampaigns
from campaign.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from campaign.config.uow import UnidadTrabajoSQLAlchemy
from campaign.modulos.infraestructura.mapeadores import MapeadorCampaign
from .base import RegistrarCampaignBaseHandler
from dataclasses import dataclass
import datetime 
import time
import json

from campaign.modulos.infraestructura.despachadores import Despachador
from campaign.modulos.infraestructura.v1.comandos import ComandoRegistrarPartner, RegistrarPartner
from campaign.modulos.infraestructura.v1 import TipoPartner
from campaign.seedwork.infraestructura import utils

@dataclass
class ComandoRegistrarCampaign(Comando):
    nombre: str
    presupuesto: float
    divisa: str
    marca_id: str
    participantes: list[Participante]

class RegistrarCampaignHandler(RegistrarCampaignBaseHandler):

    def a_entidad(self, comando: ComandoRegistrarCampaign) -> Campaign:
        
        participantes_list = json.loads(comando.participantes) if comando.participantes else []
        
        params = dict(
            nombre=comando.nombre,
            presupuesto=comando.presupuesto,
            divisa=comando.divisa,
            marca_id=comando.marca_id,
            participantes=[
                Participante(
                    id=p["id"],
                    tipo=p["tipo"],
                    nombre=p["nombre"],
                    informacion_perfil=p["informacion_perfil"]
                )
                for p in participantes_list
            ]
        )
        
        campaign = Campaign(**params)

        return campaign
        
    def handle(self, comando: ComandoRegistrarCampaign):
        campaign = self.a_entidad(comando)
        campaign.crear_campaign(campaign)
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioCampaigns.__class__)
        
        uow = UnidadTrabajoSQLAlchemy()
        UnidadTrabajoPuerto.set_uow(uow)
        
        # Registrar batch y commit
        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, campaign)
        UnidadTrabajoPuerto.commit()
        
        # UnidadTrabajoPuerto.registrar_failure(campaign)
        
        comando_registrar_partners(campaign)
        
        

@comando.register(ComandoRegistrarCampaign)
def ejecutar_comando_registrar_campaign(comando: ComandoRegistrarCampaign):
    handler = RegistrarCampaignHandler()
    handler.handle(comando)
    
def comando_registrar_partners(data):
    participantes = data.participantes
    
    despachador = Despachador()
    
    for p in participantes:
        print(p)
        payload = RegistrarPartner(
            id_campaign=str(data.id),
            nombre=p.nombre,
            tipo=TipoPartner[p.tipo.lower()],  
            informacion_perfil=p.informacion_perfil,
            fecha_creacion=utils.time_millis()
        )
        comando = ComandoRegistrarPartner(
            time=utils.time_millis(),
            ingestion=utils.time_millis(),
            datacontenttype=RegistrarPartner.__name__,
            data=payload
        )
      
        despachador.publicar_mensaje(comando, "comando-registrar-partner")