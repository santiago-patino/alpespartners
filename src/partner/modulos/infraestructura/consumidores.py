import logging
import traceback
import pulsar, _pulsar
import aiopulsar
import asyncio
from pulsar.schema import *
from partner.seedwork.infraestructura import utils
from partner.modulos.aplicacion.comandos.registrar_partner import ComandoRegistrarPartner
from partner.seedwork.aplicacion.comandos import ejecutar_commando

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
                    elif topico == "comando-registrar-partner":
                        print(f'Comando registrar: {datos}')
                        comando = ComandoRegistrarPartner(datos.data.nombre, datos.data.tipo, datos.data.informacion_perfil)
                        ejecutar_commando(comando)
                        
                    await consumidor.acknowledge(mensaje)    

    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()