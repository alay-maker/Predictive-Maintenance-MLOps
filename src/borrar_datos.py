import redis
import sys

try:
    # Conecta a la base de datos
    cliente_redis = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    cliente_redis.ping()
    
    pipe = cliente_redis.pipeline()

    # Destruye las claves
    claves_a_borrar = [
        "input_stream",   # El Stream de telemetría
        "registro_alertas"  # La Lista de historial de fallos
    ]
    
    pipe.delete(*claves_a_borrar)

    nodos_antiguos = list(cliente_redis.scan_iter(match="nodo:*"))
    
    if nodos_antiguos:
        pipe.delete(*nodos_antiguos)

    pipe.execute()
    
    print("\nEntorno de pruebas reiniciado con éxito")
    
    # cliente_redis.flushdb()
    # print("FLUSHDB EJECUTADO: Base de datos completamente vacía.")

except redis.ConnectionError:
    print("ERROR: No se pudo conectar a Redis. ¿Está encendido el servidor en WSL?")
    sys.exit(1)