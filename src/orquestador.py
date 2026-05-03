import subprocess
import time
import sys
import redis
import json
import os

# Rutas a los archivos dentro de la carpeta de producción
RUTA_JSON = os.path.join("models", "tree_model.json")
RUTA_WORKER = os.path.join("src", "worker.py")
RUTA_PRODUCTOR = os.path.join("src", "productor.py")
RUTA_BORRADO = os.path.join("src", "borrar_datos.py")
HOST_REDIS = os.getenv('REDIS_HOST', 'localhost')

def preparar_base_datos():
    """Inyecta el modelo desde el JSON a Redis"""
    print("[Fase 1] Configurando Base de Datos Redis...")

    try:
        cliente = redis.Redis(host=HOST_REDIS, port=6379, decode_responses=True)
        cliente.ping()
        
        # Lee el archivo JSON estático
        with open(RUTA_JSON, 'r') as f:
            diccionario_nodos = json.load(f)
            
        # Limpieza e inyección atómica
        nodos_antiguos = list(cliente.scan_iter(match="nodo:*"))
        pipe = cliente.pipeline()
        if nodos_antiguos:
            pipe.delete(*nodos_antiguos)
            
        for key, value in diccionario_nodos.items():
            pipe.hset(name=key, mapping=value)
            
        pipe.execute()
        print(f"El modelo de árbol de decisión ha sido cargado en Redis ({len(diccionario_nodos)} nodos).")
        return True
        
    except Exception as e:
        print(f"ERROR al conectar con Redis o leer JSON. Detalle: {e}")
        return False

def iniciar_demo():
    print("\n INICIANDO ENTORNO DE PRODUCCIÓN IOT")
    print("="*50)
    
    if not preparar_base_datos():
        sys.exit(1)

    procesos = []
    try:
        print("\n[Fase 2] Arrancando microservicios...")

        while True:

            try:
                NUMERO_WORKERS = int(input("¿Cuantos workers desea tener en ejecución?: "))

                if 0 < NUMERO_WORKERS < 6:
                    break
                else:
                    print("\nERROR: El valor debe estar entre 1 y 5\n")

            except ValueError:
                print("\nERROR: El valor debe ser un número entero.\n")
        
        print(" -> Iniciando Workers (Esperando datos en Stream)...")

        for num_worker in range(1, NUMERO_WORKERS+1):

            nombre_worker = f"Worker_{num_worker}"

            # Subprocess simula la apertura de terminales nuevas
            procesos.append(subprocess.Popen([sys.executable, "-u", RUTA_WORKER, nombre_worker]))
            
            time.sleep(1) # Garantiza la carga del worker
        
        print(" -> Iniciando Productor (Simulador de Fresadora)...")
        procesos.append(subprocess.Popen([sys.executable, "-u", RUTA_PRODUCTOR]))

        print("\nFRESADORA EN LÍNEA. Mostrando logs en tiempo real (Pulsa Ctrl+C para apagar):\n")
        
        # Mantiene el script principal en marcha
        procesos[0].wait() 
        
    except KeyboardInterrupt:
        print("\n\nDeteniendo microservicios...")
        for p in procesos:
            p.terminate()
        print("Demo finalizada correctamente.")

def eliminar_datos_creados():

    print("\n-------- ELIMINAR DATOS REDIS --------\n")
    while True:
        respuesta = input("¿Quiere eliminar los datos generados y almacenados en Redis? (s/n): ")
        if respuesta in ["s", "S"]:
            subprocess.Popen([sys.executable, "-u", RUTA_BORRADO])
            time.sleep(1)
            break
        elif respuesta in ["n", "N"]:
            break
        else:
            print("\nRespuesta no válida\n")

if __name__ == "__main__":
    iniciar_demo()
    eliminar_datos_creados()
