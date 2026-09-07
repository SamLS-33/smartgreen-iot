# Fichas Técnicas de Variables - SmartGreen IoT

## 1. Humedad del Suelo (soil_moisture)
* **Descripción:** Porcentaje de humedad volumétrica presente en la tierra del cultivo.
* **Tipo:** `number`
* **Unidad:** `%`
* **Rango válido:** `0.0` a `100.0`
* **Regla de alerta:** Menor a `20.0` (Alerta por sequía crítica).

## 2. Temperatura Ambiental (temperature)
* **Descripción:** Temperatura ambiental registrada en el interior del invernadero.
* **Tipo:** `number`
* **Unidad:** `°C`
* **Rango válido:** `-10.0` a `60.0`
* **Regla de alerta:** Mayor a `30.0` (Alerta por estrés térmico).

## 3. Nivel de Agua (water_level)
* **Descripción:** Altura de la columna de agua disponible en el tanque de reserva.
* **Tipo:** `number`
* **Unidad:** `cm`
* **Rango válido:** `0.0` a `50.0`
* **Regla de alerta:** Menor a `5.0` (Alerta por nivel de agua insuficiente).
