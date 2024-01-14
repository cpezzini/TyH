
from flask import Flask, request, jsonify
import time
import logging
import requests
import json

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

url_microservicio_user = "http://localhost:5001/obtener_suscripcion"
url_microservicio_predict = "http://localhost:5002/predict"
url_microservicio_bitacora = "http://localhost:5003/bitacora"

# Función para obtener el tipo de suscripción del usuario
def obtener_tipo_suscripcion(user, password):
    response_user = requests.get(f"{url_microservicio_user}/{user}/{password}")
    if response_user.status_code == 200:
        tipo_suscripcion = response_user.json().get("tipo_suscripcion")
        return tipo_suscripcion
    else:
        raise Exception(f'Error al obtener el tipo de suscripción: {response_user.status_code}, {response_user.text}')

# Endpoint principal
@app.route('/index', methods=['GET', 'POST'])
def index():
    start_time = time.time()

    user = request.args.get('user') if request.method == 'GET' else request.json.get('user')
    password = request.args.get('password') if request.method == 'GET' else request.json.get('password')
    nivel_colesterol = float(request.args.get('nivel_colesterol', 0.0))
    presion_arterial = float(request.args.get('presion_arterial', 0.0))
    glucosa = float(request.args.get('glucosa', 0.0))
    edad = int(request.args.get('edad', 0))
    sobrepeso = int(request.args.get('sobrepeso', 0))
    tabaquismo = int(request.args.get('tabaquismo', 0))

    try:
        if not (1.0 <= nivel_colesterol <= 3.0):
            return jsonify({"error": "El nivel de colesterol está fuera del rango permitido (1.0, 3.0)"})

        if not (0.6 <= presion_arterial <= 1.8):
            return jsonify({"error": "La presión arterial está fuera del rango permitido (0.6, 1.8)"})

        if not (0.5 <= glucosa <= 2.0):
            return jsonify({"error": "El nivel de glucosa está fuera del rango permitido (0.5, 2.0)"})

        if not (0 <= edad <= 99):
            return jsonify({"error": "La edad está fuera del rango permitido (0, 99)"})

        if sobrepeso not in [0, 1]:
            return jsonify({"error": "El valor de sobrepeso debe ser 0 o 1"})

        if tabaquismo not in [0, 1]:
            return jsonify({"error": "El valor de tabaquismo debe ser 0 o 1"})

        tipo_suscripcion = obtener_tipo_suscripcion(user, password)

        datos_riesgo_cardiaco = {
            "colesterol": nivel_colesterol,
            "presion": presion_arterial,
            "glucosa": glucosa,
            "edad": edad,
            "sobrepeso": sobrepeso,
            "tabaquismo": tabaquismo
        }

        headers = {'Content-Type': 'application/json'}
        respuesta_riesgo_cardiaco = requests.post(url_microservicio_predict, json=datos_riesgo_cardiaco, headers=headers)
        print("Respuesta del microservicio de riesgo cardiaco:")
        respuesta_riesgo_cardiaco.raise_for_status()

        end_time = time.time()
        processing_time = end_time - start_time

        # Almacenar la respuesta del riesgo cardiaco en una variable
        datos_respuesta_riesgo_cardiaco = respuesta_riesgo_cardiaco.json() if respuesta_riesgo_cardiaco.status_code == 200 else None

        datos_bitacora = {
            "datos_user": {
                "user": user,
                "password": password
            },
            "datos_riesgo_cardiaco": datos_riesgo_cardiaco,
            "respuesta_riesgo_cardiaco": datos_respuesta_riesgo_cardiaco,  # Incluye la respuesta del riesgo cardiaco en la bitácora
            "processing_time": processing_time
        }

        respuesta_bitacora = requests.post(url_microservicio_bitacora, json=datos_bitacora, headers=headers)
        print(f"Respuesta del microservicio de bitácora: {respuesta_bitacora}")
        respuesta_bitacora.raise_for_status()

    except requests.RequestException as e:
        logging.error(f"Error en la solicitud: {str(e)}")
        return jsonify({"error": f"Error en la solicitud: {str(e)}"}), 429

    except ValueError as e:
        logging.error(f"Error en los datos: {str(e)}")
        return jsonify({"error": f"Error en los datos: {str(e)}"}), 400

    except Exception as e:
        logging.error(f"Error inesperado: {str(e)}")
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500

    return jsonify({
        "message": "success",
        "user": user,
        "password": password,
        "tipo_suscripcion": tipo_suscripcion,
        "datos_riesgo_cardiaco": datos_riesgo_cardiaco,
        "respuesta_riesgo_cardiaco": datos_respuesta_riesgo_cardiaco,  # Incluye la respuesta del riesgo cardiaco en la respuesta JSON
        "processing_time": processing_time
    }), 200

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
