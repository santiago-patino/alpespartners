# Alpes Partners - Entrega 5

Repositorio del proyecto Alpes Partner, correspondiente a la entrega 5. Para esta entrega se implementaron las sagas generan una coreografia entre servicios. Ejecutandose a partir de el resultado de cada uno de los eventos de integracion.

## Estructura del proyecto

Este repositorio sigue en general la misma estructura del repositorio de origen. Sin embargo, hay un par de adiciones importante mencionar:

- El proyecto alpespartners contiene los siguientes son los cambios relevantes en cada módulo:
    - **api**: En este módulo contiene el API de `campaña.py` el cual cuenta con los endpoints: `/campaña-commando` y `/campaña-query`, los cuales por detrás de escenas usan un patrón CQRS como la base de su comunicación.
    - **modulos/aplicacion**: Este módulo contiene los sub-módulos: `queries` y `comandos`. En dichos directorios se desacoplaron las operaciones lectura y escritura. El módulo `campaña` contiene los archivos `crear_campaña.py` para lograr el desacoplamiento.
    - **modulos/aplicacion/handlers.py**: En el modulo de campañas encontramos handlers para eventos de integración los cuales pueden ser disparados desde la capa de infraestructura, la cual está consumiendo eventos y comandos del broker de eventos.
    - **modulos/dominio/eventos.py**: Este archivo contiene todos los eventos de dominio que son disparados cuando una actividad de dominio es ejecutada de forma correcta.
    - **modulos/infraestructura/consumidores.py**: Este archivo cuenta con toda la lógica en términos de infrastructura para consumir los eventos y comandos que provienen del broker de eventos. Desarrollado de una forma funcional.
    - **modulos/infraestructura/despachadores.py**: Este archivo cuenta con toda la lógica en terminos de infrastructura para publicar los eventos y comandos de integración en el broker de eventos. Desarrollado de manera OOP.
    - **modulos/infraestructura/schema**: En este directorio encontramos la definición de los eventos y comandos de integración. Puede ver que se usa un formato popular en la comunidad de desarrollo de software open source, en donde los directorios/módulos nos dan un indicio de las versiones `/schema/v1/...`. De esta manera podemos estar tranquilos con versiones incrementales y menores, pero listos cuando tengamos que hacer un cambio grande.

## Alpes Partners

Ejecucion Paso a Paso

### Ejecutar Pulsar

Si requiere ejecutar todo lo relacionado con pulsar y broker de eventos ejecute

```bash
docker-compose --profile pulsar up
```

### Ejecutar Base de Datos

Si requiere ejecutar todo la base de datos

```bash
docker-compose --profile db up
```

### Correr docker-compose usando profiles
```bash
docker-compose --profile <pulsar|db> up
```

### Ejecutar Servicios

Primero debe instalar el requirements.txt. Recuerde navegar a la ruta /src

**Instalar dependencias:**
```bash
pip install -r requirements.txt
```

**Ejecutar servicio bff:**
```bash
uvicorn bff.main:app --host localhost --port 8000 --reload
```

**Ejecutar servicio campaign:**
```bash
uvicorn campaign.main:app --host localhost --port 8001 --reload
```

**Ejecutar servicio partner:**
```bash
uvicorn partner.main:app --host localhost --port 8002 --reload
```

**Ejecutar servicio traking:**
```bash
uvicorn traking.main:app --host localhost --port 8003 --reload
```

## Documentacion Sagas

#### Escenarios

```bash
#  Exitoso
Paso 1: RegistrarCampaña ✅
Paso 2: RegistrarPartner ✅
Paso 3: RegistrarEvento ✅
Paso 4: AprobarReserva ✅
```

```bash
#  Registro Evento Fallido
Paso 1: RegistrarCampaña ✅
Paso 2: RegistrarPartner ✅
Paso 3: RegistrarEvento ❌ FALLA
    ↓
Compensaciones:
1️⃣ CancelarPartner (Paso 2)
2️⃣ CancelarCampaña (Paso 1)
```

```bash
#  Registro Partner Fallido
Paso 1: RegistrarCampaña ✅
Paso 2: RegistrarPartner ❌ FALLA
Paso 3: RegistrarEvento
    ↓
Compensaciones:
1️⃣ CancelarCampaña (Paso 1)
```

### Pasos Sagas

Para esta entrega el servicio campaign, se encarga de realizar la coreografia entre los otros servicios, ejecutando los comandos y reaccionando a los eventos de integracion asociados

Archivo:  
`src/campaign/modulos/sagas/aplicacion/coordinadores/saga_campaigns.py`

```bash
Inicio (index=0)

Transaccion (
  index=1,
  comando=ComandoRegistrarCampaign,
  evento=CampaignRegistrada,
  error=RegistroCampaignFallido,
  compensacion=ComandoCancelarCampaign
)

Transaccion (
  index=2,
  comando=ComandoRegistrarPartner,
  evento=PartnerRegistrado,
  error=RegistroPartnerFallido,
  compensacion=ComandoCancelarPartner
)

Transaccion (
  index=3,
  comando=ComandoRegistrarEvento,
  evento=EventoRegistrado,
  error=RegistroEventoFallido,
  compensacion=ComandoCancelarEvento
)

Fin (index=4)
```

## Documentacion Postman

Esta documentacion corresponde a las solicitudes realizadas directamente al BFF. El cual genera los eventos correspondientes o realiza las peticiones HTTP en el caso de los querys.

Puede descargar el archivo json e importarlo en su postman

### Ejecucion Local
[📥 Descargar colección Postman](./AlpesPartners.postman_collection.json)

