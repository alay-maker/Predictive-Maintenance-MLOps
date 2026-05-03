import redis
import json
import os

# Conexión usando variables de entorno para Docker
host = os.getenv('REDIS_HOST', 'localhost')
r = redis.Redis(host=host, port=6379, db=0)

def cargar_modelo():
    with open('models/tree_model.json', 'r') as f:
        modelo = json.load(f)
    r.set('modelo_mantenimiento', json.dumps(modelo))
    print("✅ Modelo cargado en Redis correctamente.")

if __name__ == "__main__":
    cargar_modelo()