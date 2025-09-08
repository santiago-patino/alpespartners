# Alpes Partners - Arquitectura Hexagonal DDD 

Repositorio con código base para el desarrollo de una arquitectura hexagonal siguiendo los principios y patrones de DDD.

## Estructura del proyecto

El repositorio en su raíz está estructurado de la siguiente forma:

- **src**: En este directorio encuentra el código fuente para alpespartners. En la siguiente sección se explica un poco mejor la estructura del mismo
- **.gitignore**: Archivo con la definición de archivos que se deben ignorar en el repositorio GIT
- **README.md**: El archivo que está leyendo :)
- **requirements.txt**: Archivo con los requerimientos para el correcto funcionamiento del proyecto (librerias Python)

## Crear - Activar entorno virtual

**En Mac/Linux:**
```bash
python3 -m venv venv
```

**En Windows**
```bash
python -m venv venv
```

**En Mac/Linux:**
```bash
source venv/bin/activate
```

**En Windows**
```bash
venv\Scripts\activate
```

## Instalar Dependencias

```bash
pip install -r requirements.txt
```

## Ejecutar Aplicación

Desde el directorio principal ejecute el siguiente comando.

```bash
flask --app src/alpespartners/api run
```

Siempre puede ejecutarlo en modo DEBUG:

```bash
flask --app src/alpespartners/api --debug run
```


## Request de ejemplo

Los siguientes JSON pueden ser usados para probar el API:

### Crear Campaña

- **Endpoint**: `/campaña`
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

### Ver Campaña

- **Endpoint**: `/campaña/{id}`
- **Método**: `GET`
- **Headers**: `Content-Type='aplication/json'`
