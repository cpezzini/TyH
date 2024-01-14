ADR #1: Arquitectura basada en Microservicios para "Autenticación", "Cambio de Suscripciones" y "Diagnóstico de Riesgo Cardíaco"

Estado: Aceptada

Contexto

El servicio web (API) destinado a clasificar el riesgo cardíaco basado en datos clínicos del paciente requiere funcionalidades específicas:
Autenticación del Usuario: Validación de la API Key y autorización para el acceso de usuarios registrados en la base de datos del sistema.
Gestión de Suscripciones: Cambio entre Freemium y Premium, limitando el número de solicitudes HTTP por minuto según el tipo de cuenta.
Predicción de Riesgo Cardíaco: Ejecución del modelo de red neuronal para diagnosticar el riesgo cardíaco basado en los datos clínicos del paciente.

Decisión
Se adopta una arquitectura basada en microservicios:

Microservicio de Autenticación.
Microservicio de Gestión de Suscripción.
Microservicio Predictor de Riesgo Cardíaco

Consecuencias
Escalabilidad Individualizada: Permite la escalabilidad independiente de cada funcionalidad, facilitando la gestión de los servicios en función de la demanda.
Modularidad y Mantenimiento: Simplifica actualizaciones y mantenimiento independiente de cada servicio, facilitando futuras expansiones o modificaciones.
Control de Acceso Granular: Implementa controles de acceso específicos para cada servicio, garantizando la seguridad y la autorización adecuada.

