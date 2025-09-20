from traking.modulos.dominio.entidades import Evento
from traking.modulos.dominio.repositorios import RepositorioEventos
from traking.modulos.dominio.fabricas import FabricaEventos
from traking.config.db import get_db, SessionLocal

from .mapeadores import MapeadorEvento
from .dto import Evento as EventoDTO

from uuid import UUID

class RepositorioEventosSQLAlchemy(RepositorioEventos):

    def __init__(self):
        self._fabrica_eventos: FabricaEventos = FabricaEventos()
        
    @property
    def db(self):
        from traking.seedwork.infraestructura.uow import UnidadTrabajoPuerto
        return UnidadTrabajoPuerto.get_uow().db

    @property
    def fabrica_eventos(self):
        return self._fabrica_eventos

    def obtener_por_id(self, id: UUID) -> Evento:
        with SessionLocal() as db:
            evento_dto = db.query(EventoDTO).filter_by(id=str(id)).one()
            return self.fabrica_eventos.crear_objeto(evento_dto, MapeadorEvento())

    def obtener_todos(self) -> list[Evento]:
        # TODO
        raise NotImplementedError

    def agregar(self, evento: Evento):
        evento_dto = self.fabrica_eventos.crear_objeto(evento, MapeadorEvento())
        self.db.add(evento_dto)

    def actualizar(self, evento: Evento):
        # TODO
        raise NotImplementedError

    def eliminar(self, evento_id: UUID):
        evento_dto = self.db.query(EventoDTO).filter(EventoDTO.id == evento_id).first()
        if evento_dto:
            self.db.delete(evento_dto)