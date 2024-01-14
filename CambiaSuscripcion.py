from flask import Flask, request, jsonify
import pymongo
import memcache

app = Flask(__name__)

mongo_client = pymongo.MongoClient("mongodb+srv://<username>:<password>@<cluster-address>/<database>?retryWrites=true&w=majority")
db = mongo_client['nombre_db']
api_keys_collection = db['collection_datos_usuario']  

class CachedRequestHandler:
    def __init__(self):
        self.cache = memcache.Client(['127.0.0.1:6379'])  # Conexión al servidor Memcached

    def fetch(self, key, expire_after=None):
        cached_data = self.cache.get(key)
        return cached_data

    def add_to_cache(self, key, data, expire_after=None):
        self.cache.set(key, data, expire_after)

    def get_from_cache(self, key):
        cached_data = self.cache.get(key)
        return cached_data

handler = CachedRequestHandler()

@app.route('/change_subscription', methods=['POST'])
def change_subscription():
    if 'Authorization' not in request.headers:
        return jsonify({'message': 'API Key missing'}), 401
    
    api_key = request.headers['Authorization']
    current_subscription_type = request.json.get('current_subscription_type')

    new_subscription_type = 'FREEMIUM' if current_subscription_type == 'PREMIUM' else 'PREMIUM'

    result = api_keys_collection.update_one({'api_key': api_key}, {'$set': {'subscription_type': new_subscription_type}})
    
    if result.modified_count > 0:
        handler.add_to_cache(f"subscription_{api_key}", new_subscription_type)
        return jsonify({'message': f'Subscription updated to {new_subscription_type}'}), 200
    else:
        return jsonify({'message': 'API Key not found'}), 404

if __name__ == '__main__':
   app.run(host='localhost', port=5008, debug=True) 
