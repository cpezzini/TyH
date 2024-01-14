ADR #6: Uso del Patrón Gateway para la orquestación del Sistema de Predicción de Riesgo Cardiovascular

Estado: Aceptada

Contexto
El sistema consta de tres microservicios que manejan la autenticación de usuarios, cambios de suscripción y la predicción de riesgo cardiovascular. Surge la necesidad de gestionar de manera eficiente las solicitudes entrantes, para dirigirlas a los microservicios correspondientes.

Decisión
Adoptaremos el patrón de diseño Gateway para centralizar y administrar las solicitudes entrantes a los microservicios existentes:

Autenticación y Validación de Usuarios
Las solicitudes de autenticación y validación de usuarios pasarán a través del Gateway. Este verificará y dirigirá las peticiones al microservicio de autenticación, gestionando los límites de peteciones por minuto antes de enviarlas al microservicio correspondiente.

Cambio de Suscripciones
El Gateway manejará las solicitudes de cambio de suscripciones (FREEMIUM y PREMIUM)(no desarrollado), gestionando los límites de peticiones por minuto antes de enviarlas al microservicio correspondiente.

Predicción de Riesgo Cardiovascular
Actuando como intermediario, el Gateway enrutará las solicitudes de predicción desde los clientes hacia el microservicio de predicción, asegurando un manejo adecuado de las solicitudes.

Consecuencias
Enrutamiento Centralizado: Optimiza el enrutamiento de las solicitudes a los microservicios correspondientes.
Seguridad Centralizada: Permite implementar medidas de seguridad, autenticación y verificación en un solo punto.
Control de Límites de Peticiones: Facilita la gestión de límites de solicitudes por minuto según el tipo de suscripción.

Implementación
Se desarrollará un componente Gateway utilizando tecnologías compatibles con la arquitectura existente. Este Gateway gestionará las solicitudes entrantes y las dirigirá a los microservicios correspondientes. 
(En nuestra aplicación index.py, puede considerarse como parte de un sistema tipo gateway).


