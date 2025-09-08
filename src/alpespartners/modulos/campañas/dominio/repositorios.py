""" Interfaces para los repositorios del dominio de campañas

En este archivo usted encontrará las diferentes interfaces para repositorios
del dominio de campañas

"""

from abc import ABC
from alpespartners.seedwork.dominio.repositorios import Repositorio

class RepositorioCampañas(Repositorio, ABC):
    ...

class RepositorioMarcas(Repositorio, ABC):
    ...