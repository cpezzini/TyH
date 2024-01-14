from pymongo import MongoClient

# URI de conexión proporcionada por Atlas
uri = "mongodb+srv://topicos2023:app1234@cluster0.dmuqbzs.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client.app1
bitacora_collection = db.bitacora

# Obtener todos los documentos de la colección bitacora
documentos_bitacora = bitacora_collection.find()

# Imprimir los documentos de la colección bitacora de forma más estructurada
for documento in documentos_bitacora:
    print("ID:", documento['_id'])
    print("Datos del usuario:", documento['datos_user'])
    print("Datos de riesgo cardiaco:", documento['datos_riesgo_cardiaco'])
    print("Respuesta de riesgo cardiaco:", documento['respuesta_riesgo_cardiaco'])
    print("Tiempo de procesamiento:", documento['processing_time'])
    print("Fecha de registro:", documento['timestamp'])
    print("\n")
