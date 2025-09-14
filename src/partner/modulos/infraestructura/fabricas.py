""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de campañas

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de campañas

"""

from dataclasses import dataclass

from partner.modulos.dominio.repositorios import RepositorioPartners
from partner.seedwork.dominio.fabricas import Fabrica
from partner.seedwork.dominio.repositorios import Repositorio

from .excepciones import ExcepcionFabrica
from .repositorios import RepositorioPartnersSQLAlchemy


@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioPartners.__class__:
            return RepositorioPartnersSQLAlchemy()
        else:
            raise ExcepcionFabrica()