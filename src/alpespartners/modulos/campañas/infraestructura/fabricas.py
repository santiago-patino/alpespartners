""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de campañas

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de campañas

"""

from dataclasses import dataclass

from alpespartners.modulos.campañas.dominio.repositorios import RepositorioCampañas
from alpespartners.seedwork.dominio.fabricas import Fabrica
from alpespartners.seedwork.dominio.repositorios import Repositorio

from .excepciones import ExcepcionFabrica
from .repositorios import RepositorioCampañasSQLite


@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioCampañas.__class__:
            return RepositorioCampañasSQLite()
        else:
            raise ExcepcionFabrica()