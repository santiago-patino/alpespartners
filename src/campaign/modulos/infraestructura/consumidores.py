import logging
import traceback
import pulsar, _pulsar
import aiopulsar
import asyncio
from pulsar.schema import *
from campaign.seedwork.infraestructura import utils
from campaign.modulos.aplicacion.comandos.registrar_campaign import ComandoRegistrarCampaign
from campaign.modulos.aplicacion.comandos.cancelar_campaign import ComandoCancelarCampaign
from partner.modulos.infraestructura.v1.comandos import ComandoRegistrarPartner, RegistrarPartner
from campaign.seedwork.aplicacion.comandos import ejecutar_commando
from campaign.modulos.sagas.aplicacion.coordinadores.saga_campaigns import oir_mensaje
from pydispatch import dispatcher
from campaign.modulos.infraestructura.despachadores import Despachador
import json

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
                    
                    if topico == "evento-campaigns":
                        print(f'Evento recibido: {datos}')
                    elif topico == "evento-partners":
                        print(f'Evento recibido partners: {datos}')
                        
                        if datos.type == "partner_registrado":
                            evento = datos.partner_registrado
                        elif datos.type == "partner_fallido":
                            evento = datos.partner_fallido
                        else:
                            raise ValueError(f"Tipo de evento no soportado: {datos.type}")
                        
                        dispatcher.send(evento=evento, signal=f'{evento.__class__.__name__}Integracion')
                        
                    elif topico == "comando-registrar-campaign":
                        print(f'Comando registrar: {datos}')
                        comando = ComandoRegistrarCampaign(datos.data.nombre, datos.data.presupuesto, datos.data.divisa, datos.data.marca_id, datos.data.participantes)
                        ejecutar_commando(comando)
                        # comando_registrar_partners(datos.data)
                    elif topico == "comando-cancelar-campaign":
                        print(f'Comando cancelar: {datos}')
                        comando = ComandoCancelarCampaign(datos.data.id)
                        ejecutar_commando(comando)
                        
                    await consumidor.acknowledge(mensaje)    

    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        
def comando_registrar_partners(data):
    print(data)
    print(data.participantes)
    participantes = json.loads(data.participantes)
    
    despachador = Despachador()
    
    # for p in participantes:
    #     payload = RegistrarPartner(
    #         id_campaign=""
    #         nombre=p["nombre"],
    #         tipo=TipoPartner[p["tipo"].lower()] if isinstance(TipoPartner, dict) else TipoPartner.influencer,  
    #         informacion_perfil=p["informacion_perfil"],
    #         fecha_creacion=utils.time_millis()
    #     )
    
    #     comando = ComandoRegistrarPartner(
    #         time=utils.time_millis(),
    #         ingestion=utils.time_millis(),
    #         datacontenttype=RegistrarPartner.__name__,
    #         data=payload
    #     )
        
    #     despachador.publicar_mensaje(comando, "comando-registrar-partner")
    
    # payload = RegistrarPartner(
    #     id_campaign = "camp12345",
    #     nombre = "Juan",
    #     tipo = TipoPartner.influencer,
    #     informacion_perfil = "Influencer de moda con 200k seguidores",
    #     fecha_creacion = utils.time_millis()
    # )

    # comando = ComandoRegistrarPartner(
    #     time=utils.time_millis(),
    #     ingestion=utils.time_millis(),
    #     datacontenttype=RegistrarPartner.__name__,
    #     data = payload
    # )
    
    # despachador.publicar_mensaje(comando, "comando-registrar-partner")