# Decisión técnica: persistencia de telemetría

## Uso de SQLite

Se seleccionó SQLite como motor de persistencia porque el proyecto SmartGreen IoT se encuentra en una etapa de prototipo y requiere una solución sencilla, ligera y local. No necesita un servidor de base de datos independiente y permite almacenar las lecturas de telemetría de manera persistente.

## Límites de escalabilidad

SQLite es suficiente para el volumen de datos y las pruebas actuales. Sin embargo, si el sistema crece y recibe información simultánea de numerosos dispositivos, podría presentar limitaciones de concurrencia y rendimiento. En ese escenario se podría migrar a una solución como PostgreSQL.

## Almacenamiento de measurements en JSON

Las mediciones se almacenan como JSON dentro de una columna de tipo TEXT. Esta decisión permite conservar diferentes variables de los dispositivos sin modificar la estructura de la tabla cada vez que se incorpora una nueva medición. Además, facilita mantener la flexibilidad del contrato de telemetría.