from flask import Flask, request, jsonify
from flask_caching import Cache
import pymongo

app = Flask(__name__)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Función para conectar a la base de datos en Atlas.
# Recupera el tipo de suscripción del usuario.

def conectar_atlas():
    # URI de conexión proporcionada por Atlas
    uri = "mongodb+srv://topicos2023:app1234@cluster0.dmuqbzs.mongodb.net/?retryWrites=true&w=majority"
    client = pymongo.MongoClient(uri)
    return client

# Función para obtener el tipo de suscripción del usuario
@cache.memoize(timeout=60)  
def obtener_tipo_suscripcion(user, password):
    # Intentar obtener la información desde la caché
    cached_result = cache.get((user, password))
    if cached_result is not None:
        return cached_result

    client = conectar_atlas()

    # Selecciona la base de datos 'app1' y la colección 'users'
    db = client.app1
    collection = db.users

    # Busca el usuario por nombre de usuario y contraseña
    resultado = collection.find_one({"user": user, "password": password})

    if resultado:
        tipo_suscripcion = resultado.get("subscription", "Sin suscripción")
        # Guardar en caché el resultado
        cache.set((user, password), tipo_suscripcion)
        return tipo_suscripcion
    else:
        return None  # Cambiado el mensaje

    # Cierra la conexión
    client.close()

# Diccionario para almacenar el contador de consultas por minuto para cada usuario
contadores_consultas = {}

# Endpoint para manejar las solicitudes con parámetros de usuario y contraseña en la URL
@app.route('/obtener_suscripcion/<user>/<password>', methods=['GET'])
def obtener_suscripcion(user, password):
    try:
        # Obtener el tipo de suscripción
        tipo_suscripcion = obtener_tipo_suscripcion(user, password)

        # Verificar si el usuario existe
        if tipo_suscripcion is not None:
            # Verificar el tipo de suscripción y aplicar límites de consulta
            limite_consultas = 0
            if tipo_suscripcion == "Premium":
                limite_consultas = 50
            elif tipo_suscripcion == "Freemium":
                limite_consultas = 5

            # Obtener el contador actual de consultas para el usuario
            contador_actual = contadores_consultas.get((user, password), 0)

            # Verificar si se ha alcanzado el límite de consultas
            if contador_actual < limite_consultas:
                # Incrementar el contador
                contadores_consultas[(user, password)] = contador_actual + 1

                return jsonify({"tipo_suscripcion": tipo_suscripcion}), 200
            else:
                return jsonify({"message": f"Se ha alcanzado el límite de consultas para {user}/{password}"}), 429
        else:
            return jsonify({"message": f"Usuario no encontrado"}), 404

    except Exception as e:
        print(f"Error en obtener_suscripcion: {str(e)}")
        return "Ocurrió un error al procesar la solicitud"

if __name__ == "__main__":
    app.run(debug=True, port=5001)
