from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler  

app = Flask(__name__)

# Cargar el modelo previamente entrenado
modelo = load_model('c:/topicos2/riesgo_cardiaco.keras')
import warnings
warnings.filterwarnings("ignore", message="X does not have valid feature names", category=UserWarning)

# Inicializar el scaler
scaler = MinMaxScaler()

# Cargar los datos desde el archivo CSV
data = pd.read_csv('riesgocardiaco.csv')

# Excluir la columna 'riesgo_cardiaco' al ajustar el scaler
columns_to_normalize = ['colesterol', 'presion', 'glucosa', 'edad', 'sobrepeso', 'tabaquismo']
scaler.fit(data[columns_to_normalize])  # Ajusta el scaler con los datos seleccionados

# Ruta para la predicción
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()  # Obtener datos en formato JSON desde la solicitud
        
        # Obtener los datos necesarios para la predicción desde el JSON
        colesterol = float(data.get('nivel_colesterol', 0))
        presion = float(data.get('presion_arterial', 0))
        glucosa = float(data.get('glucosa', 0))
        edad = float(data.get('edad', 0))
        sobrepeso = float(data.get('sobrepeso', 0))
        tabaquismo = float(data.get('tabaquismo', 0))

        # Preprocesamiento de los datos para la predicción
        datos = np.array([[colesterol, presion, glucosa, edad, sobrepeso, tabaquismo]])

        # Realizar la predicción con el modelo cargado
        prediccion = modelo.predict(scaler.transform(datos))
        resultado = "Paciente en riesgo cardíaco" if prediccion[0][0] > 0.5 else "Paciente sin riesgo cardíaco"

        # Retorna la predicción como respuesta en formato JSON
        return jsonify({"prediction": resultado})

    except Exception as e:
        return jsonify({"error": f"Error en la predicción: {str(e)}"}), 500

if __name__ == '__main__':
 
  app.run(host='localhost', port=5002, debug=True)
    