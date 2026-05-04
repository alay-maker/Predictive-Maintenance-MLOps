import redis
import time
import sys
import json
import os

def main():
    host_redis = os.getenv('REDIS_HOST', 'localhost')
    NOMBRE_STREAM = 'input_stream'
    GRUPO_TRABAJO = 'equipo_triaje'

    if len(sys.argv) > 1:
        NOMBRE_WORKER = sys.argv[1]
    else:
        NOMBRE_WORKER = 'worker_independiente'

    print(f"\n-------- Creando {NOMBRE_WORKER} --------\n")

    try:
        # Conecta con Redis
        cliente_redis = redis.Redis(host=host_redis, port=6379, db=0, decode_responses=True)
        print(f"[{NOMBRE_WORKER}]: Conectado a servidor Redis. {cliente_redis.ping()}")

        # Crea grupo de consumidores
        try:
            cliente_redis.xgroup_create(NOMBRE_STREAM, GRUPO_TRABAJO, id="$", mkstream=True)
        except redis.exceptions.ResponseError as e:
            if "BUSYGROUP" in str(e):
                print(f"[{NOMBRE_WORKER}]: Uniéndose al grupo existente '{GRUPO_TRABAJO}'.")
            else:
                raise e

        # 3. Bucle infinito de escucha y procesamiento de los datos
        print(f"[{NOMBRE_WORKER}]: Esperando datos de la fresadora...\n")
        while True:
            respuesta = cliente_redis.xreadgroup(
                groupname=GRUPO_TRABAJO,
                consumername=NOMBRE_WORKER,
                streams={NOMBRE_STREAM: '>'},
                count=1,
                block=2000
            )

            if not respuesta:
                continue
            
            for stream_name, mensajes in respuesta:
                for id_mensaje, datos in mensajes:
                    nodo_actual = "nodo:0" 
                    
                    while True:
                        info_nodo = cliente_redis.hgetall(nodo_actual)
                        if info_nodo['tipo'] == 'hoja':
                            resultado = info_nodo.get('resultado')
                            if resultado == 'Failure':
                                alerta = {
                                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                                    "id_mensaje_origen": id_mensaje,
                                    "datos_sensor": datos
                                }
                                cliente_redis.lpush("registro_alertas", json.dumps(alerta))
                                print(f"[{NOMBRE_WORKER}] ¡ALERTA CRÍTICA! Fallo detectado. (ID: {id_mensaje})")
                            break 
                            
                        elif info_nodo['tipo'] == 'decision':
                            variable = info_nodo['variable']
                            umbral = float(info_nodo['umbral'])
                            valor_sensor = float(datos.get(variable, 0))
                            
                            if valor_sensor <= umbral:
                                nodo_actual = info_nodo['hijo_menor_igual']
                            else:
                                nodo_actual = info_nodo['hijo_mayor']
                    
                    cliente_redis.xack(NOMBRE_STREAM, GRUPO_TRABAJO, id_mensaje)

    except redis.ConnectionError:
        print(f"[{NOMBRE_WORKER} ERROR]: No se pudo conectar a Redis.")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n{NOMBRE_WORKER} detenido manualmente.")

# Esta es la regla de oro en Python para que los tests no exploten:
if __name__ == "__main__":
    main()
