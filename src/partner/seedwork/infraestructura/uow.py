from abc import ABC, abstractmethod
from enum import Enum
from ...seedwork.dominio.entidades import AgregacionRaiz
from pydispatch import dispatcher
import logging
import traceback


class Lock(Enum):
    OPTIMISTA = 1
    PESIMISTA = 2


class Batch:
    def __init__(self, operacion, lock: Lock, *args, **kwargs):
        self.operacion = operacion
        self.args = args
        self.lock = lock
        self.kwargs = kwargs


class UnidadTrabajo(ABC):
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    def _obtener_eventos_rollback(self, batches=None):
        batches = self.batches if batches is None else batches
        eventos = []
        for batch in batches:
            for arg in batch.args:
                if isinstance(arg, AgregacionRaiz):
                    eventos += arg.eventos_compensacion
                    break
        return eventos

    def _obtener_eventos(self, batches=None):
        batches = self.batches if batches is None else batches
        eventos = []
        for batch in batches:
            for arg in batch.args:
                if isinstance(arg, AgregacionRaiz):
                    eventos += arg.eventos
                    break
        return eventos

    @abstractmethod
    def _limpiar_batches(self):
        raise NotImplementedError

    @abstractmethod
    def batches(self) -> list[Batch]:
        raise NotImplementedError

    @abstractmethod
    def savepoints(self) -> list:
        raise NotImplementedError                    

    def commit(self):
        self._publicar_eventos_post_commit()
        self._limpiar_batches()

    @abstractmethod
    def rollback(self, savepoint=None):
        self._limpiar_batches()
    
    @abstractmethod
    def savepoint(self):
        raise NotImplementedError

    def registrar_batch(self, operacion, *args, lock=Lock.PESIMISTA, repositorio_eventos_func=None, **kwargs):
        batch = Batch(operacion, lock, *args, **kwargs)
        self.batches.append(batch)
        self._publicar_eventos_dominio(batch, repositorio_eventos_func)

    def _publicar_eventos_dominio(self, batch, repositorio_eventos_func):
        for evento in self._obtener_eventos(batches=[batch]):
            if repositorio_eventos_func:
                repositorio_eventos_func(evento)
            dispatcher.send(signal=f'{type(evento).__name__}Dominio', evento=evento)

    def _publicar_eventos_post_commit(self):
        try:
            for evento in self._obtener_eventos():
                dispatcher.send(signal=f'{type(evento).__name__}Integracion', evento=evento)
        except:
            logging.error('ERROR: Suscribiendose al tópico de eventos!')
            traceback.print_exc()


# ---- Unidad de Trabajo Puerto sin Flask ----
class UnidadTrabajoPuerto:
    _uow: UnidadTrabajo = None  # Singleton para la sesión actual

    @staticmethod
    def set_uow(uow: UnidadTrabajo):
        UnidadTrabajoPuerto._uow = uow

    @staticmethod
    def get_uow() -> UnidadTrabajo:
        if UnidadTrabajoPuerto._uow is None:
            raise Exception("No hay Unidad de Trabajo inicializada")
        return UnidadTrabajoPuerto._uow

    @staticmethod
    def commit():
        uow = UnidadTrabajoPuerto.get_uow()
        uow.commit()

    @staticmethod
    def rollback(savepoint=None):
        uow = UnidadTrabajoPuerto.get_uow()
        uow.rollback(savepoint=savepoint)

    @staticmethod
    def savepoint():
        uow = UnidadTrabajoPuerto.get_uow()
        uow.savepoint()

    @staticmethod
    def dar_savepoints():
        uow = UnidadTrabajoPuerto.get_uow()
        return uow.savepoints()

    @staticmethod
    def registrar_batch(operacion, *args, lock=Lock.PESIMISTA, **kwargs):
        uow = UnidadTrabajoPuerto.get_uow()
        uow.registrar_batch(operacion, *args, lock=lock, **kwargs)
