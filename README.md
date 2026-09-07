# SmartGreen IoT
## Sistema Inteligente de Monitoreo y Riego Automatizado para Invernaderos Caseros

Proyecto Integrador IoT - Ingeniería de Sistemas  
**Universidad de San Buenaventura, Bogotá D.C.**  

* **Integrantes:** Brandon González, Samuel Botache  
* **Asignatura:** Desarrollo de Aplicaciones AV  

---

## 📌 Descripción del Proyecto
**SmartGreen IoT** es una solución tecnológica diseñada para optimizar el control microclimático e hídrico en invernaderos caseros y urbanos. El sistema monitorea en tiempo real variables críticas para el cultivo mediante dispositivos IoT simulados, permitiendo una supervisión constante y la generación de alertas tempranas ante situaciones de estrés hídrico o térmico.

## 🌿 Variables Monitoreadas
1. **Humedad del Suelo (`soil_moisture`):** Porcentaje de humedad volumétrica (`%`). Genera alerta crítica si desciende del umbral de sequía.
2. **Temperatura Ambiental (`temperature`):** Registro térmico interior en grados Celsius (`°C`). Controla los límites de estrés térmico para los cultivos.
3. **Nivel de Agua (`water_level`):** Altura de la columna de agua disponible en el tanque de reserva (`cm`). Emite alertas de nivel insuficiente para el sistema de riego.

## 📂 Estructura del Repositorio
El proyecto se encuentra organizado bajo la siguiente estructura modular:
* `simulator/config/`: Contiene los archivos de configuración JSON del comportamiento del dispositivo simulado.
* `contracts/examples/`: Ejemplos formales de los contratos de telemetría (mensajes válidos y casos de prueba para validación de errores).
* `docs/variables/`: Documentación detallada y fichas técnicas de las variables del sistema.
