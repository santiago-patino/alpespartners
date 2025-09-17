""" Fábricas para la creación de objetos del dominio de campañas

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de campañas

"""

from .entidades import Campaign
from .excepciones import TipoObjetoNoExisteEnDominioCampaignsExcepcion
from ...seedwork.dominio.repositorios import Mapeador
from ...seedwork.dominio.fabricas import Fabrica
from ...seedwork.dominio.entidades import Entidad
from dataclasses import dataclass

@dataclass
class _FabricaCampaigns(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            # Dominio → DTO
            return mapeador.entidad_a_dto(obj)
        else:
            # DTO → Dominio
            campaign: Campaign = mapeador.dto_a_entidad(obj)

            return campaign


@dataclass
class FabricaCampaigns(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Campaign.__class__:
            fabrica_campaign = _FabricaCampaigns()
            return fabrica_campaign.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioCampaignsExcepcion()

