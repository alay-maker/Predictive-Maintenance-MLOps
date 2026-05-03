import redis
import time
import pandas as pd

host_redis = os.getenv('REDIS_HOST', 'localhost')

# Conecta con el servidor Redis

cliente_redis = redis.Redis(host=host_redis, port=6379, db=0, decode_responses=True)
print(f"[PRODUCTOR]: Conectado a servidor Redis. {cliente_redis.ping()}")

# Carga datos reservados durante el proceso de entrenamiento

df = pd.read_csv('data/processed/datos_sensores_test.csv')
test_data = df.drop(columns=['Machine failure'])

# Simula la sensorización de una fresadora

try:

    for id, data in test_data.iterrows():

        # Genera un Redis stream en caso de no existir y añade las mediciones
        event_id = cliente_redis.xadd(name="input_stream", fields=data.to_dict(), maxlen=10000, approximate=True)

        time.sleep(1)

except KeyboardInterrupt:
    print("\nFresadora detenida manualmente por el usuario.")

