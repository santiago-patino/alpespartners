""" Fábricas para la creación de objetos del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de vuelos

"""

from .entidades import Campaña
from .excepciones import TipoObjetoNoExisteEnDominioCampañasExcepcion
from alpespartners.seedwork.dominio.repositorios import Mapeador
from alpespartners.seedwork.dominio.fabricas import Fabrica
from alpespartners.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass

@dataclass
class _FabricaCampaña(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            # Dominio → DTO
            return mapeador.entidad_a_dto(obj)
        else:
            # DTO → Dominio
            campaña: Campaña = mapeador.dto_a_entidad(obj)
            
            # Aquí podrías agregar validaciones de reglas de negocio
            # Ejemplo:
            # self.validar_regla(FechasValidas(campaña.fecha_inicio, campaña.fecha_fin))
            # self.validar_regla(PresupuestoPositivo(campaña.presupuesto))

            return campaña


@dataclass
class FabricaCampañas(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Campaña.__class__:
            fabrica_campaña = _FabricaCampaña()
            return fabrica_campaña.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioCampañasExcepcion()

