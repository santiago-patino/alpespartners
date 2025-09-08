import pulsar
from pulsar.schema import *

from alpespartners.modulos.campañas.infraestructura.schema.v1.eventos import EventoCampañaCreada, CampañaCreadaPayload
from alpespartners.modulos.campañas.infraestructura.schema.v1.comandos import ComandoCrearCampaña, ComandoCrearCampañaPayload
from alpespartners.seedwork.infraestructura import utils

import datetime

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(EventoCampañaCreada))
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del evento
        payload = CampañaCreadaPayload(
            id_campaña=str(evento.id_campaña), 
            id_marca=str(evento.id_marca), 
            estado=str(evento.estado), 
            fecha_inicio=int(unix_time_millis(evento.fecha_inicio))
        )
        
        evento_integracion = EventoCampañaCreada(data=payload)
        self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoCampañaCreada))

    def publicar_comando(self, comando, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del comando
        payload = ComandoCrearCampañaPayload(
            id_usuario=str(comando.id_usuario)
            # agregar itinerarios
        )
        comando_integracion = ComandoCrearCampaña(data=payload)
        self._publicar_mensaje(comando_integracion, topico, AvroSchema(ComandoCrearCampaña))
