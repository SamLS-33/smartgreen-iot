# SmartGreen IoT

## Sistema Inteligente de Monitoreo y Riego Automatizado para Invernaderos Caseros

SmartGreen IoT es un proyecto orientado al monitoreo de variables ambientales en un invernadero casero mediante un dispositivo IoT simulado por software.

El sistema representa el funcionamiento de un entorno de monitoreo y riego automatizado. Para ello, genera datos de humedad del suelo, temperatura y nivel de agua, los estructura en mensajes JSON y los transmite mediante HTTP a un backend encargado de recibir, validar y almacenar la telemetría.

Actualmente, el proyecto cuenta con un simulador IoT, un backend desarrollado con FastAPI y un sistema de persistencia local mediante SQLite.

---

## Objetivo

Desarrollar un sistema capaz de simular un dispositivo IoT encargado de monitorear las condiciones de un invernadero y representar decisiones básicas de riego a partir de las variables generadas.

El sistema permite:

- Generar lecturas ambientales de manera consecutiva.
- Mantener un estado interno para las variables simuladas.
- Representar la activación y desactivación del riego.
- Generar mensajes con una estructura JSON definida.
- Ejecutar escenarios normales y de alerta.
- Enviar telemetría mediante solicitudes HTTP POST.
- Recibir y validar mensajes mediante un backend.
- Almacenar las lecturas recibidas en una base de datos SQLite.
- Verificar el funcionamiento mediante pruebas automatizadas.

---

## Variables simuladas

El dispositivo simulado trabaja principalmente con las siguientes variables:

| Variable | Descripción |
|---|---|
| `soil_moisture` | Porcentaje de humedad del suelo. |
| `temperature` | Temperatura del invernadero en grados Celsius. |
| `water_level` | Nivel disponible de agua. |
| `irrigation_active` | Indica si el sistema de riego se encuentra activo. |

Además, cada mensaje contiene información de identificación y seguimiento:

| Campo | Descripción |
|---|---|
| `message_id` | Identificador único del mensaje. |
| `device_id` | Identificador del dispositivo IoT. |
| `timestamp` | Fecha y hora de generación del mensaje. |
| `sequence` | Número consecutivo de la lectura. |
| `measurements` | Conjunto de variables medidas. |

---

## Lógica del simulador

El simulador mantiene el estado de las variables entre lecturas.

En el escenario normal, el sistema evalúa principalmente la humedad del suelo y el nivel de agua disponible.

Cuando la humedad del suelo se encuentra por debajo del umbral configurado y existe suficiente agua, el riego se activa. Al activarse:

- La humedad del suelo aumenta.
- El nivel de agua disminuye.
- `irrigation_active` toma el valor `true`.

Cuando no se cumplen las condiciones para activar el riego, la humedad del suelo puede disminuir progresivamente.

Esta lógica permite comprobar la coherencia entre las variables generadas y el comportamiento esperado del sistema.

---

## Escenarios

### Escenario normal

Representa el comportamiento habitual del invernadero.

```json
"scenario": "normal"
```

En este escenario las variables evolucionan de acuerdo con las reglas configuradas para el simulador.

### Escenario de alerta

Permite provocar intencionalmente una condición crítica de humedad del suelo para comprobar el comportamiento del simulador ante una situación de alerta.

```json
"scenario": "alert"
```

Este escenario permite generar valores de humedad inferiores al umbral establecido.

---

## Arquitectura general

El sistema utiliza el siguiente flujo de comunicación:

1. El simulador genera una lectura de las variables ambientales.
2. Los datos se estructuran en un mensaje JSON.
3. El simulador envía el mensaje mediante una solicitud HTTP POST.
4. FastAPI recibe la solicitud.
5. Pydantic valida la estructura y los tipos de los datos.
6. El backend almacena la telemetría en SQLite.
7. El backend devuelve una respuesta HTTP que informa el resultado de la operación.

**Tecnologías principales de la arquitectura:**

- Python para la lógica del sistema.
- FastAPI para el desarrollo del backend.
- Pydantic para la validación de datos.
- SQLite para la persistencia de telemetría.
- HTTP y JSON para la comunicación entre componentes.

---

## Estructura del proyecto

```text
smartgreen-iot/
├── README.md
├── .gitignore
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   ├── database.py
│   └── requirements.txt
├── contracts/
│   └── examples/
│       ├── invalid-messages.json
│       └── valid-message.json
├── database/
│   └── iot.db
├── docs/
│   ├── arquitectura/
│   ├── decisiones/
│   │   └── persistencia.md
│   ├── evidencias/
│   │   └── guia-3/
│   └── variables/
│       └── ficha-variables.md
├── frontend/
│   └── .gitkeep
├── simulator/
│   ├── .gitignore
│   ├── config.json
│   ├── device-config.json
│   ├── receiver_test.py
│   ├── simulator.py
│   └── tests/
│       └── test_simulator.py
└── tests/
    └── test_backend.py
```

### Descripción de los directorios

**`backend/`**

Contiene el backend desarrollado con FastAPI. Incluye los endpoints HTTP, los esquemas de validación Pydantic y las funciones encargadas de gestionar la base de datos SQLite.

**`contracts/`**

Contiene ejemplos de mensajes válidos e inválidos utilizados como referencia para el contrato de telemetría.

**`database/`**

Es el directorio destinado al almacenamiento local de la base de datos SQLite. El archivo `iot.db` se genera automáticamente al iniciar el backend y no se incluye en el repositorio.

**`docs/`**

Contiene la documentación técnica del proyecto, las decisiones de implementación, la documentación de variables y las evidencias de las pruebas realizadas.

**`frontend/`**

Directorio reservado para el desarrollo de la interfaz de usuario en etapas posteriores.

**`simulator/`**

Contiene el simulador IoT, sus archivos de configuración, el receptor HTTP de prueba y las pruebas automatizadas de su funcionamiento.

**`tests/`**

Contiene las pruebas automatizadas correspondientes al backend.

---

## Configuración del simulador

La configuración utilizada actualmente por `simulator.py` se encuentra en:

```text
simulator/config.json
```

Algunos de los parámetros principales son:

```json
{
  "device_id": "ZONA-INVERNADERO-01",
  "interval_seconds": 15,
  "scenario": "normal",
  "seed": 42,
  "http_url": "http://127.0.0.1:8000/api/telemetry"
}
```

También se configuran los valores iniciales de humedad, temperatura y nivel de agua, además de los parámetros relacionados con el comportamiento del riego.

El parámetro `scenario` permite seleccionar el escenario normal o el escenario de alerta.

---

## Backend y persistencia

El backend se desarrolló utilizando FastAPI y permite recibir las lecturas generadas por el simulador.

### Endpoints disponibles

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/health` | Comprueba que el backend se encuentra disponible. |
| POST | `/api/telemetry` | Recibe, valida y almacena mensajes de telemetría. |

### Validación de solicitudes

Los mensajes recibidos deben cumplir con el esquema definido mediante Pydantic.

El backend contempla las siguientes respuestas:

| Código HTTP | Descripción |
|---|---|
| `200` | Solicitud de comprobación de estado procesada correctamente. |
| `201` | Mensaje de telemetría recibido y almacenado correctamente. |
| `400` | El campo `measurements` está vacío. |
| `404` | Endpoint o ruta no encontrada. |
| `409` | Se intenta registrar un mensaje con un `message_id` duplicado. |
| `422` | Los datos recibidos no cumplen con la estructura o los tipos esperados. |

### Base de datos SQLite

La persistencia se implementó mediante SQLite, utilizando el archivo local:

```text
database/iot.db
```

La tabla `telemetry` almacena los siguientes campos:

| Campo | Descripción |
|---|---|
| `id` | Identificador interno autoincremental. |
| `message_id` | Identificador único del mensaje. |
| `device_id` | Identificador del dispositivo que generó la lectura. |
| `timestamp` | Fecha y hora declaradas por el dispositivo. |
| `sequence` | Número consecutivo de la lectura. |
| `measurements_json` | Variables ambientales almacenadas en formato JSON. |
| `received_at` | Fecha y hora en que el backend recibió el mensaje. |

El campo `message_id` cuenta con una restricción `UNIQUE` para evitar registros duplicados.

Las mediciones se almacenan como JSON dentro de una columna de texto. Esto permite conservar flexibilidad cuando se incorporan nuevas variables al sistema.

La justificación de esta decisión se encuentra en `docs/decisiones/persistencia.md`.

---

## Instalación y ejecución

### Requisitos

- Python 3.12 o compatible.
- Git.
- Acceso a una terminal PowerShell.
- Dependencias especificadas en `backend/requirements.txt`.

### 1. Clonar el repositorio

```powershell
git clone https://github.com/SamLS-33/smartgreen-iot.git
cd smartgreen-iot
```

Si se desea trabajar con la rama de desarrollo del backend:

```powershell
git switch feature/backend-persistencia
```

### 2. Crear y activar el entorno virtual

Desde la carpeta raíz del proyecto:

```powershell
python -m venv .venv
```

Activar el entorno virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la ejecución del script, se puede habilitar temporalmente para la sesión actual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 3. Instalar dependencias

```powershell
python -m pip install -r backend/requirements.txt
```

### 4. Iniciar el backend

Desde la carpeta raíz del proyecto:

```powershell
python -m uvicorn backend.main:app --reload
```

El backend estará disponible en:

```text
http://127.0.0.1:8000
```

Para consultar la documentación interactiva de FastAPI:

```text
http://127.0.0.1:8000/docs
```

Para comprobar el estado del servicio:

```text
http://127.0.0.1:8000/health
```

La base de datos se inicializa automáticamente al iniciar el backend.

### 5. Ejecutar el simulador

Con el backend activo, abrir una segunda terminal.

Desde la raíz del proyecto, ingresar a la carpeta del simulador:

```powershell
cd simulator
```

Para generar y enviar diez mensajes de telemetría:

```powershell
python simulator.py --count 10
```

El simulador enviará las lecturas al endpoint configurado y mostrará las respuestas HTTP recibidas.

Cuando el backend almacena correctamente una lectura, responde con el código `201`.

Para visualizar lecturas sin realizar el envío HTTP:

```powershell
python simulator.py --console --count 5
```

El parámetro `--count` permite definir la cantidad de mensajes que se desean generar.

---

## Ejemplo de telemetría

Una lectura generada por el simulador tiene una estructura similar a:

```json
{
  "message_id": "ZONA-INVERNADERO-01-000001",
  "device_id": "ZONA-INVERNADERO-01",
  "timestamp": "2026-11-19T15:00:00Z",
  "sequence": 1,
  "measurements": {
    "soil_moisture": 33.0,
    "temperature": 32.2,
    "water_level": 18.5,
    "irrigation_active": true
  }
}
```

El `message_id` identifica cada mensaje y la secuencia permite diferenciar las lecturas generadas por el dispositivo.

---

## Pruebas automatizadas

El proyecto cuenta con pruebas automatizadas para verificar el comportamiento del simulador y del backend.

Se utiliza `pytest` para ejecutar las pruebas.

### Pruebas del simulador

Desde la carpeta `simulator`:

```powershell
python -m pytest -q tests
```

Se validan aspectos como:

- Rangos de las variables.
- Generación de identificadores diferentes.
- Coherencia del comportamiento del riego.
- Prevención del riego cuando no existe suficiente agua.
- Correspondencia entre el estado del riego y las variables generadas.

**Resultado de referencia:** 5 pruebas aprobadas.

### Pruebas del backend

Desde la carpeta raíz:

```powershell
python -m pytest -q tests/test_backend.py
```

Se comprueban:

- Disponibilidad del endpoint `/health`.
- Recepción y persistencia de telemetría.
- Rechazo de mensajes con identificadores duplicados.

**Resultado de referencia:** 3 pruebas aprobadas.

Las pruebas del backend utilizan una base de datos temporal para evitar modificar la base de datos real del proyecto.

---

## Comunicación HTTP y receptor de prueba

El simulador puede transmitir las lecturas mediante solicitudes HTTP `POST`.

La dirección configurada actualmente es:

```text
http://127.0.0.1:8000/api/telemetry
```

El receptor principal del proyecto es el backend desarrollado con FastAPI.

El archivo `receiver_test.py` se conserva dentro de `simulator/` como herramienta de prueba de etapas anteriores. No es necesario ejecutarlo cuando se utiliza el backend principal, ya que ambos servicios no deben intentar utilizar simultáneamente el mismo puerto.

---

## Tecnologías utilizadas

- **Python:** lenguaje de programación del proyecto.
- **FastAPI:** desarrollo de la API del backend.
- **Uvicorn:** servidor ASGI para ejecutar FastAPI.
- **Pydantic:** validación de los mensajes de telemetría.
- **SQLite:** almacenamiento local de las lecturas.
- **JSON:** estructura de intercambio de datos.
- **HTTP:** comunicación entre el simulador y el backend.
- **Pytest:** ejecución de pruebas automatizadas.
- **HTTPX:** soporte para pruebas del cliente HTTP.
- **Git:** control de versiones.
- **GitHub:** alojamiento y gestión del repositorio.

---

## Estado actual del proyecto

El proyecto SmartGreen IoT cuenta actualmente con:

- Generación de telemetría mediante un simulador.
- Identificación mediante `device_id` y `message_id`.
- Secuencia consecutiva de mensajes.
- Variables de humedad, temperatura y nivel de agua.
- Lógica básica de riego.
- Escenario normal y escenario de alerta.
- Envío de telemetría mediante HTTP.
- Backend desarrollado con FastAPI.
- Validación de datos mediante Pydantic.
- Endpoint de comprobación de estado.
- Recepción de mensajes mediante HTTP POST.
- Persistencia de lecturas mediante SQLite.
- Prevención de mensajes duplicados.
- Pruebas automatizadas para el simulador y el backend.
- Documentación de decisiones técnicas.

Las siguientes etapas contemplan el desarrollo de funcionalidades adicionales y la incorporación de una interfaz de usuario.

---

## Proyecto

**SmartGreen IoT**

Sistema Inteligente de Monitoreo y Riego Automatizado para Invernaderos Caseros.

Desarrollado como proyecto académico de Ingeniería de Sistemas.