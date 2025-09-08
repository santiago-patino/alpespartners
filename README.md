# Alpes Partners - CQRS y manejo de eventos

Repositorio del proyecto Alpes Partenes, a partir de implementar el codigo utilizando DDD y la arquitectura Hexagonal. Se implementan el registro y comunicacion por eventos usando el patron CQRS y eventos de dominio e integracion sobre los contextos acotados y sistemas externos a futuro.

## Estructura del proyecto

Este repositorio sigue en general la misma estructura del repositorio de origen. Sin embargo, hay un par de adiciones importante mencionar:

- El proyecto alpespartners contiene los siguientes son los cambios relevantes en cada módulo:
    - **api**: En este módulo contiene el API de `campaña.py` el cual cuenta con los endpoints: `/campaña-commando` y `/campaña-query`, los cuales por detrás de escenas usan un patrón CQRS como la base de su comunicación.
    - **modulos/../aplicacion**: Este módulo contiene los sub-módulos: `queries` y `comandos`. En dichos directorios se desacoplaron las operaciones lectura y escritura. El módulo `campaña` contiene los archivos `crear_campaña.py` para lograr el desacoplamiento.
    - **modulos/../aplicacion/handlers.py**: En el modulo de campañas encontramos handlers para eventos de integración los cuales pueden ser disparados desde la capa de infraestructura, la cual está consumiendo eventos y comandos del broker de eventos.
    - **modulos/../dominio/eventos.py**: Este archivo contiene todos los eventos de dominio que son disparados cuando una actividad de dominio es ejecutada de forma correcta.
    - **modulos/../infraestructura/consumidores.py**: Este archivo cuenta con toda la lógica en términos de infrastructura para consumir los eventos y comandos que provienen del broker de eventos. Desarrollado de una forma funcional.
    - **modulos/../infraestructura/despachadores.py**: Este archivo cuenta con toda la lógica en terminos de infrastructura para publicar los eventos y comandos de integración en el broker de eventos. Desarrollado de manera OOP.
    - **modulos/../infraestructura/schema**: En este directorio encontramos la definición de los eventos y comandos de integración. Puede ver que se usa un formato popular en la comunidad de desarrollo de software open source, en donde los directorios/módulos nos dan un indicio de las versiones `/schema/v1/...`. De esta manera podemos estar tranquilos con versiones incrementales y menores, pero listos cuando tengamos que hacer un cambio grande.
    - **seedwork/aplicacion/comandos.py**: Definición general de los comandos, handlers e interface del despachador.
    - **seedwork/infraestructura/queries.py**: Definición general de los queries, handlers e interface del despachador.
    - **seedwork/infraestructura/uow.py**: La Unidad de Trabajo (UoW) mantiene una lista de objetos afectados por una transacción de negocio y coordina los cambios de escritura. Este objeto nos va ser de gran importancia, pues cuando comenzamos a usar eventos de dominio e interactuar con otros módulos, debemos ser capaces de garantizar consistencia entre los diferentes objetos y partes de nuestro sistema.

## Alpes Partners

Ya que se implemento docker para ejecutar este proyecto

### Ejecutar Pulsar

Si requiere ejecutar todo lo relacionado con pulsar y broker de eventos ejecute

```bash
docker-compose --profile pulsar up
```

### Ejecutar Aplicación

Desde el directorio principal ejecute el siguiente comando.
Primero se debe crear la imagen de la aplicaion

**Crear la imagen:**
```bash
docker build . -f alpespartners.Dockerfile -t alpespartners/flask
```

**Ejecute la aplicacion a partir de la imagen:**
Se utiliza el puerto 5001, debido a que en ocasiones este puerto se encontraba ocupado
```bash
docker run -p 5001:5000 alpespartners/flask
```

## Ejecutar Request

Los siguientes JSON pueden ser usados para probar el API:

### Crear Campaña Comando

- **Endpoint**: `/campaña-comando`
- **Método**: `POST`
- **Headers**: `Content-Type='aplication/json'`

```json
{
  "id": "c-12345",
  "nombre": "Campaña Moda Primavera 2025",
  "tipo": "Influencer",  
  "estado": "draft",
  "fecha_inicio": "2025-09-10T00:00:00Z",
  "fecha_fin": "2025-12-10T23:59:59Z",
  "presupuesto": {
    "monto": 15000.00,
    "divisa": "USD"
  },
  "marca_id": "b-12345",  
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


### Correr docker-compose usando profiles
```bash
docker-compose --profile <pulsar|alpespartners|ui|notificacion> up
```
