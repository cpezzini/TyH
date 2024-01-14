Instructivo para Ejecutar el Proceso de Entrenamiento del Modelo de Machine Learning

Requisitos.
Python instalado
Instalación de librerías requeridas: pandas, numpy, scikit-learn, tensorflow, seaborn, matplotlib, Flask

Pasos a seguir.
Descargar los archivos:

riesgocardiaco.csv (archivo de datos)
Los códigos Python proporcionados:
riesgo_cardiaco.py (Código de entrenamiento del modelo)
app_riesgocardiaco.py (Código para el servidor de predicción)

Configuración del entorno:
Abrir una terminal o consola y navegar hasta el directorio que contiene los archivos descargados.

Ejecución del servidor de caché (Memcached o Memurai(para windows)):
Antes de ejecutar el proceso de entrenamiento, se debe tener instalado y ejecutado el servidor de Memcached. Necesario para la funcionalidad de caché en el proceso de predicción.


Entrenamiento del modelo de Machine Learning.
Ejecutar el comnando entrenamiento del modelo: 

python riesgo_cardiaco.py
Inicia el proceso de entrenamiento del modelo basado en los datos de riesgocardiaco.csv. El código también evalua el modelo y guarda los resultados y el modelo entrenado en la carpeta especificada.

Verificación del modelo entrenado:
Confirmar que el modelo se ha guardado correctamente en la ruta mencionada en el código (c:/topicos2/riesgo_cardiaco.keras).

Ejecución del servidor para la predicción.
Ejecuta el servidor Flask para la predicción utilizando el siguiente comando:

python app_riesgocardiaco.py
Este código activará el servidor Flask en la máquina. Se pueden realizar solicitudes POST a la ruta /predict con datos en formato JSON para obtener predicciones utilizando el modelo previamente entrenado.


Ejemplo de rango de datos para la predicción: 
colesterol =  (1.0, 3.0)
presion = (0.6, 1.8)
azucar= (0.5, 2.0)
edad = (0,99)
sobrepeso 0 o 1, donde 1 representa presencia de sobrepeso.
tabaquismo 0 o 1, donde 1 representa presencia de tabaquismo.
