import redis
import json
import os

# --- AJUSTES PARA DOCKER ---
# Lee la variable de entorno que inyecta docker-compose
HOST_REDIS = os.getenv('REDIS_HOST', 'localhost')
# La ruta del modelo es relativa a la carpeta /app dentro del contenedor
RUTA_JSON = 'models/tree_model.json'

def preparar_base_datos():
    """Inyecta el modelo desde el JSON a Redis"""
    print("[Fase 1] Configurando Base de Datos Redis...")

    try:
        # decode_responses=True es vital para que trabaje con texto y no con bytes
        cliente = redis.Redis(host=HOST_REDIS, port=6379, decode_responses=True)
        cliente.ping()
        
        # Lee el archivo JSON estático
        with open(RUTA_JSON, 'r') as f:
            diccionario_nodos = json.load(f)
            
        # Limpieza e inyección atómica usando Pipeline (¡Excelente práctica!)
        nodos_antiguos = list(cliente.scan_iter(match="nodo:*"))
        pipe = cliente.pipeline()
        
        if nodos_antiguos:
            pipe.delete(*nodos_antiguos)
            
        for key, value in diccionario_nodos.items():
            pipe.hset(name=key, mapping=value)
            
        pipe.execute()
        print(f"✅ El modelo de árbol de decisión ha sido cargado en Redis ({len(diccionario_nodos)} nodos).")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR al conectar con Redis o leer JSON. Detalle: {e}")
        return False

# Esto hace que el script se ejecute automáticamente cuando Docker lo llama
if __name__ == "__main__":
    preparar_base_datos()