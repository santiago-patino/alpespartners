from pulsar.schema import *
from alpespartners.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class CampañaCreadaPayload(Record):
    id_campaña = String()
    id_marca = String()
    estado = String()
    fecha_inicio = Long()

class EventoCampañaCreada(EventoIntegracion):
    data = CampañaCreadaPayload()