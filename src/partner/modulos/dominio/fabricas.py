""" Fábricas para la creación de objetos del dominio de campañas

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de campañas

"""

from .entidades import Partner
from .excepciones import TipoObjetoNoExisteEnDominioPartnersExcepcion
from ...seedwork.dominio.repositorios import Mapeador
from ...seedwork.dominio.fabricas import Fabrica
from ...seedwork.dominio.entidades import Entidad
from dataclasses import dataclass

@dataclass
class _FabricaPartners(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            # Dominio → DTO
            return mapeador.entidad_a_dto(obj)
        else:
            # DTO → Dominio
            partner: Partner = mapeador.dto_a_entidad(obj)

            return partner


@dataclass
class FabricaPartners(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Partner.__class__:
            fabrica_partner = _FabricaPartners()
            return fabrica_partner.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioPartnersExcepcion()

