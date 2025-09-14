""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de campañas

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de campañas

"""

from dataclasses import dataclass

from campaign.modulos.dominio.repositorios import RepositorioCampaigns
from campaign.seedwork.dominio.fabricas import Fabrica
from campaign.seedwork.dominio.repositorios import Repositorio

from .excepciones import ExcepcionFabrica
from .repositorios import RepositorioCampaignsSQLAlchemy


@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioCampaigns.__class__:
            return RepositorioCampaignsSQLAlchemy()
        else:
            raise ExcepcionFabrica()