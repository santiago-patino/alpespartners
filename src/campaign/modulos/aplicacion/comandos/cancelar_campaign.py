from campaign.seedwork.aplicacion.comandos import Comando, ComandoHandler
from campaign.seedwork.aplicacion.comandos import ejecutar_commando as comando
from campaign.modulos.dominio.entidades import Campaign, Participante
from campaign.modulos.infraestructura.repositorios import RepositorioCampaigns
from campaign.seedwork.infraestructura.uow import UnidadTrabajoPuerto, UnidadTrabajo
from campaign.config.uow import UnidadTrabajoSQLAlchemy
from campaign.modulos.infraestructura.mapeadores import MapeadorCampaign
from .base import RegistrarCampaignBaseHandler
from dataclasses import dataclass
import datetime 
import time
import json

@dataclass
class ComandoCancelarCampaign(Comando):
    id: str

class CancelarCampaignHandler(RegistrarCampaignBaseHandler):

    def a_entidad(self, comando: ComandoCancelarCampaign) -> Campaign:
        
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
        
    def handle(self, comando: ComandoCancelarCampaign):
        # campaign = self.a_entidad(comando)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioCampaigns.__class__)
        
        uow = UnidadTrabajoSQLAlchemy()
        UnidadTrabajoPuerto.set_uow(uow)
        
        # Registrar batch y commit
        UnidadTrabajoPuerto.registrar_batch(repositorio.eliminar, comando.id)
        UnidadTrabajoPuerto.commit()

@comando.register(ComandoCancelarCampaign)
def ejecutar_comando_cancelar_campaign(comando: ComandoCancelarCampaign):
    handler = CancelarCampaignHandler()
    handler.handle(comando)