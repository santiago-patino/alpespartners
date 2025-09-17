from ..seedwork.infraestructura.uow import UnidadTrabajo, Batch
from pydispatch import dispatcher
from ..config.db import SessionLocal

import logging
import traceback

class ExcepcionUoW(Exception):
    ...

class UnidadTrabajoSQLAlchemy(UnidadTrabajo):

    def __init__(self):
        self._batches: list[Batch] = list()
        self.db = SessionLocal()  # Creamos la sesión de SQLAlchemy

    def __enter__(self) -> UnidadTrabajo:
        return super().__enter__()

    def __exit__(self, *args):
        self.rollback()
        self.db.close()

    def _limpiar_batches(self):
        self._batches = list()

    @property
    def savepoints(self) -> list:
        # TODO: implementar savepoints si lo necesitas
        return []

    @property
    def batches(self) -> list[Batch]:
        return self._batches             

    def commit(self):
        try:
            for batch in self.batches:
                batch.operacion(*batch.args, **batch.kwargs)  # solo args originales
            self.db.commit()  # commit de la sesión SQLAlchemy
            super().commit()
        except Exception as e:
            self.db.rollback()
            raise ExcepcionUoW(f"Error al hacer commit: {str(e)}")

    def rollback(self, savepoint=None):
        if savepoint:
            # TODO: implementar rollback a savepoint
            savepoint.rollback()
        else:
            self.db.rollback()
        super().rollback()
    
    def savepoint(self):
        # TODO: implementar savepoint usando self.db.begin_nested()
        ...

