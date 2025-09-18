import pulsar
from pulsar.schema import *

from campaign.modulos.infraestructura.mapeadores import MapadeadorEventosCampaign
from campaign.seedwork.infraestructura import utils

class Despachador:
    def __init__(self):
        self.mapper = MapadeadorEventosCampaign()

    def publicar_mensaje(self, mensaje, topico, schema = None):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        if schema is None:
            schema = AvroSchema(mensaje.__class__)
        # publicador = cliente.create_producer(topico, schema=AvroSchema(mensaje.__class__))
        publicador = cliente.create_producer(topico, schema=schema)
        publicador.send(mensaje)
        cliente.close()
        
    def publicar_evento(self, evento, topico):
       evento = self.mapper.entidad_a_dto(evento)
       self.publicar_mensaje(evento, topico, AvroSchema(evento.__class__))
