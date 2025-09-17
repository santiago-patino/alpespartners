""" Fábricas para la creación de objetos del dominio de campañas

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de campañas

"""

from .entidades import Evento
from .excepciones import TipoObjetoNoExisteEnDominioEventosExcepcion
from ...seedwork.dominio.repositorios import Mapeador
from ...seedwork.dominio.fabricas import Fabrica
from ...seedwork.dominio.entidades import Entidad
from dataclasses import dataclass

@dataclass
class _FabricaEventos(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            # Dominio → DTO
            return mapeador.entidad_a_dto(obj)
        else:
            # DTO → Dominio
            evento: Evento = mapeador.dto_a_entidad(obj)

            return evento


@dataclass
class FabricaEventos(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Evento.__class__:
            fabrica_evento = _FabricaEventos()
            return fabrica_evento.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioEventosExcepcion()

