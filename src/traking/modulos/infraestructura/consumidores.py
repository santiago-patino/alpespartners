import logging
import traceback
import pulsar, _pulsar
import aiopulsar
import asyncio
from pulsar.schema import *
from ...seedwork.infraestructura import utils
from ...modulos.aplicacion.comandos.registrar_evento import ComandoRegistrarEvento
from ...seedwork.aplicacion.comandos import ejecutar_commando

async def suscribirse_a_topico(topico: str, suscripcion: str, schema: Record, tipo_consumidor:_pulsar.ConsumerType=_pulsar.ConsumerType.Shared):
    try:
        async with aiopulsar.connect(f'pulsar://{utils.broker_host()}:6650') as cliente:
            async with cliente.subscribe(
                topico, 
                consumer_type=tipo_consumidor,
                subscription_name=suscripcion, 
                schema=AvroSchema(schema)
            ) as consumidor:
                while True:
                    mensaje = await consumidor.receive()
                    print(mensaje)
                    datos = mensaje.value()
                    print(f'Evento recibido: {datos}')
                    
                    if topico == "evento-partners":
                        print("Evento execute")
                        #await manejar_evento_partner(datos)
                    elif topico == "comando-registrar-evento-conversion":
                        comando = ComandoRegistrarEvento(datos.data.id_partner, datos.data.id_campana, datos.data.fecha)
                        ejecutar_commando(comando)
                        
                    await consumidor.acknowledge(mensaje)    

    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()