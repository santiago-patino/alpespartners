import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback

from alpespartners.modulos.campañas.infraestructura.schema.v1.eventos import EventoCampañaCreada
from alpespartners.modulos.campañas.infraestructura.schema.v1.comandos import ComandoCrearCampaña
from alpespartners.seedwork.infraestructura import utils

def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-campaña', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='alpespartners-sub-eventos', schema=AvroSchema(EventoCampañaCreada))

        while True:
            mensaje = consumidor.receive()
            print(f'Evento recibido: {mensaje.value().data}')

            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_comandos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comandos-reserva', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='alpespartners-sub-comandos', schema=AvroSchema(ComandoCrearCampaña))

        while True:
            mensaje = consumidor.receive()
            print(f'Comando recibido: {mensaje.value().data}')

            consumidor.acknowledge(mensaje)     
            
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()