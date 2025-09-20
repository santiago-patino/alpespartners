import logging
import traceback
import pulsar, _pulsar
import aiopulsar
import asyncio
from pulsar.schema import *
from traking.seedwork.infraestructura import utils
from traking.modulos.aplicacion.comandos.registrar_evento import ComandoRegistrarEvento
from traking.modulos.aplicacion.comandos.cancelar_evento import ComandoCancelarEvento
from traking.seedwork.aplicacion.comandos import ejecutar_commando

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
                    datos = mensaje.value()
                    
                    if topico == "evento-partners":
                        print(f'Evento recibido: {datos}')
                        #await manejar_evento_partner(datos)
                    elif topico == "comando-registrar-evento-conversion":
                        print(f'Comando registrar: {datos}')
                        comando = ComandoRegistrarEvento(datos.data.id_partner, datos.data.id_campana, datos.data.fecha)
                        ejecutar_commando(comando)
                    elif topico == "comando-cancelar-evento":
                        print(f'Comando cancelar: {datos}')
                        comando = ComandoCancelarEvento(datos.data.id)
                        ejecutar_commando(comando)
                        
                    await consumidor.acknowledge(mensaje)    

    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()