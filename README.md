# Alpes Partners - Entrega 4

Repositorio del proyecto Alpes Partner, se implementan los microservicios correspondientes a la entrega. Se implementan el registro y comunicacion por eventos usando el patron CQRS y eventos de dominio.

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

## Ejecutar Request

Los siguientes JSON pueden ser usados para probar el API:

### Crear Campaign BFF

Genera el comando hacia el topico "comando-registrar-campaign". El cual es procesado si el servicio campaign esta activo

- **Endpoint**: `/crear-campaign`
- **Método**: `POST`
- **Headers**: `Content-Type='aplication/json'`

```json
{
    "nombre": "Test",
    "presupuesto": 10000,
    "divisa": "USD",
    "marca_id": "12dqweqwqdsxq",
    "participantes": [
        {
          "id": "p-98765",
          "tipo": "Influencer",
          "nombre": "Alice Doe",
          "informacion_perfil": "Influencer de moda con 200k seguidores"
        },
        {
          "id": "p-54321",
          "tipo": "Affiliate",
          "nombre": "Blog Moda Trends",
          "informacion_perfil": "Sitio web con 50k visitas mensuales"
        }
  ]
}
```

### Crear Partner BFF

Genera el comando hacia el topico "comando-registrar-partner". El cual es procesado si el servicio partner esta activo

- **Endpoint**: `/crear-partner`
- **Método**: `POST`
- **Headers**: `Content-Type='aplication/json'`

```json
{
    "nombre": "Alice Doe",
    "tipo": "influencer",
    "informacion_perfil": "Influencer de moda con 200k seguidores"
}
```


### Correr docker-compose usando profiles
```bash
docker-compose --profile <pulsar|db> up
```
