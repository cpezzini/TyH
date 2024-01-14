ADR #2: Escenario de Respuesta a Fallos - Acceso a la Bitácora en ausencia de datos en caché y falla del Microservicio Predictor

Estado: Aceptada, no implementado.
Contexto
En situaciones donde el microservicio predictor se encuentra inactivo, es necesario establecer un proceso alternativo para asegurar el correcto manejo de las solicitudes de diagnóstico de riesgo cardíaco.

Decisión
Se prevee un proceso de respuesta a fallos cuando el microservicio predictor esté inactivo.:

Proceso de Respuesta a Fallos
Acceso a la Bitácora en MongoDB Atlas: Se implementará un mecanismo para acceder a la bitácora almacenada en una base de datos MongoDB. Esta bitácora contiene información detallada de todas las solicitudes procesadas, incluyendo datos relevantes para el diagnóstico de riesgo cardíaco, tiempos de procesamiento y las API key.

Búsqueda en la Bitácora: Se ejecutará un proceso para recuperar la solicitud de diagnóstico pendiente. El enfoque se centrará en los datos clínicos del paciente, incluyendo niveles de colesterol, presión arterial, azúcar en sangre, edad, sobrepeso y tabaquismo.

Generación de Respuesta de Contingencia: Con base en la información obtenida de la bitácora en MongoDB, se generará una respuesta provisional para la solicitud actual de diagnóstico de riesgo cardíaco. Esta respuesta puede incluir datos previamente registrados en la bitácora, si están disponibles, o bien, se emite un mensaje indicando que no se encuentran datos disponibles, debido a la inactividad del predictor.

Consideraciones Adicionales
Gestión Segura de la Bitácora en MongoDB: Se asegurará que la gestión de la bitácora en la base de datos MongoDB en la nube, cumpla con estándares de seguridad y privacidad, garantizando el acceso seguro y la protección de datos sensibles.

Tiempo de Respuesta en Escenarios de Fallos: La recuperación y análisis de la bitácora puede tomar más tiempo, en comparación con las respuestas directas del microservicio. Se considerará este aspecto al evaluar los tiempos de respuesta en escenarios de fallos.