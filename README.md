# SmartGreen IoT

## Sistema Inteligente de Monitoreo y Riego Automatizado para Invernaderos Caseros

SmartGreen IoT es un proyecto orientado al monitoreo de variables ambientales en un invernadero casero mediante un dispositivo IoT simulado por software.

El proyecto busca representar el comportamiento de un sistema de monitoreo y riego automatizado, generando datos de humedad del suelo, temperatura y nivel de agua. La información generada se estructura en mensajes JSON y puede enviarse mediante HTTP a un receptor.

Actualmente, el proyecto se encuentra en la etapa de desarrollo y validación del simulador IoT.

---

## Objetivo

Desarrollar un sistema capaz de simular un dispositivo IoT encargado de monitorear las condiciones de un invernadero y representar decisiones básicas de riego a partir de las variables generadas.

El simulador permite:

* Generar lecturas ambientales de manera consecutiva.
* Mantener un estado interno para las variables simuladas.
* Representar la activación y desactivación del riego.
* Generar mensajes con una estructura JSON definida.
* Ejecutar escenarios normales y de alerta.
* Enviar la telemetría mediante solicitudes HTTP POST.
* Validar el comportamiento mediante pruebas automatizadas.

---

## Variables simuladas

El dispositivo simulado trabaja principalmente con las siguientes variables:

| Variable            | Descripción                                        |
| ------------------- | -------------------------------------------------- |
| `soil_moisture`     | Porcentaje de humedad del suelo.                   |
| `temperature`       | Temperatura del invernadero en grados Celsius.     |
| `water_level`       | Nivel disponible de agua.                          |
| `irrigation_active` | Indica si el sistema de riego se encuentra activo. |

Además, cada mensaje contiene información de identificación y seguimiento:

| Campo          | Descripción                             |
| -------------- | --------------------------------------- |
| `message_id`   | Identificador único del mensaje.        |
| `device_id`    | Identificador del dispositivo IoT.      |
| `timestamp`    | Fecha y hora de generación del mensaje. |
| `sequence`     | Número consecutivo de la lectura.       |
| `measurements` | Conjunto de variables medidas.          |

---

## Lógica del simulador

El simulador mantiene el estado de las variables entre lecturas.

En el escenario normal, el sistema evalúa principalmente la humedad del suelo y el nivel de agua disponible.

Cuando la humedad del suelo se encuentra por debajo del umbral configurado y existe suficiente agua, el riego se activa. Al activarse:

* La humedad del suelo aumenta.
* El nivel de agua disminuye.
* `irrigation_active` toma el valor `true`.

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

## Estructura del proyecto

```text
smartgreen-iot/
├── README.md
├── contracts/
│   └── examples/
│       ├── invalid-messages.json
│       └── valid-message.json
├── docs/
│   └── variables/
│       └── ficha-variables.md
└── simulator/
    ├── config.json
    ├── device-config.json
    ├── receiver_test.py
    ├── simulator.py
    └── tests/
        └── test_simulator.py
```

### Descripción de los directorios

`contracts/`
Contiene ejemplos de mensajes válidos e inválidos utilizados como referencia para el contrato de telemetría.

`docs/`
Contiene documentación relacionada con las variables utilizadas por el proyecto.

`simulator/`
Contiene el simulador IoT, su configuración, el receptor HTTP de prueba y las pruebas automatizadas.

`simulator/tests/`
Contiene las pruebas automatizadas del comportamiento del simulador.

---

## Configuración

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
  "http_url": "http://localhost:8000/api/telemetry"
}
```

También se configuran los valores iniciales de humedad, temperatura y nivel de agua, además de los parámetros relacionados con el comportamiento del riego.

---

## Ejecución

Para ejecutar el simulador desde la carpeta `simulator`:

```powershell
python simulator.py --console --count 5
```

El parámetro `--console` permite visualizar las lecturas sin realizar el envío HTTP.

El parámetro `--count` permite indicar la cantidad de mensajes que se desean generar.

También es posible ejecutar el simulador enviando las lecturas al receptor HTTP:

```powershell
python simulator.py --count 1
```

---

## Ejemplo de telemetría

Una lectura generada por el simulador tiene una estructura similar a:

```json
{
  "message_id": "ZONA-INVERNADERO-01-000001",
  "device_id": "ZONA-INVERNADERO-01",
  "timestamp": "2026-10-04T18:34:42Z",
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

El proyecto cuenta con pruebas automatizadas para verificar diferentes aspectos del simulador.

Para ejecutarlas:

```powershell
python -m unittest discover -s tests -v
```

Actualmente se validan:

* Rangos de las variables.
* Generación de identificadores diferentes.
* Coherencia del comportamiento del riego.
* Prevención del riego cuando no existe suficiente agua.
* Correspondencia entre el estado del riego y las variables generadas.

Resultado actual:

```text
Ran 5 tests in 1.507s

OK
```

---

## Comunicación HTTP

El simulador puede enviar las lecturas mediante una solicitud HTTP `POST`.

La dirección configurada actualmente es:

```text
http://localhost:8000/api/telemetry
```

Para realizar una prueba se puede iniciar primero el receptor:

```powershell
python receiver_test.py
```

En otra terminal se ejecuta:

```powershell
python simulator.py --count 1
```

Cuando el envío es recibido correctamente, el simulador muestra una respuesta HTTP `201`.

El receptor de prueba también muestra el mensaje JSON recibido.

---

## Tecnologías utilizadas

* Python
* JSON
* HTTP
* `unittest`
* Git
* GitHub

---

## Estado actual

El simulador IoT cuenta actualmente con:

* Generación de telemetría.
* Identificación mediante `device_id` y `message_id`.
* Secuencia de mensajes.
* Variables de humedad, temperatura y nivel de agua.
* Lógica básica de riego.
* Escenario normal.
* Escenario de alerta.
* Pruebas automatizadas.
* Envío de telemetría mediante HTTP.
* Receptor HTTP local para pruebas.

Las siguientes etapas del proyecto contemplan el desarrollo del backend, la persistencia de datos y las funcionalidades posteriores definidas para el sistema.

---

## Proyecto

**SmartGreen IoT**

Sistema Inteligente de Monitoreo y Riego Automatizado para Invernaderos Caseros.

Desarrollado como proyecto académico de Ingeniería de Sistemas.
