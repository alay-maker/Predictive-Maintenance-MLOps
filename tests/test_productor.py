import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import src.productor

@patch("src.productor.redis.Redis")
@patch("src.productor.pd.read_csv")
@patch("src.productor.time.sleep")
def test_productor_flujo_completo(mock_sleep, mock_read_csv, mock_redis_class):
    """Prueba que el productor lee el CSV y envía al menos un dato a Redis."""
    
    # 1. Preparar el Redis Falso
    mock_redis = MagicMock()
    mock_redis_class.return_value = mock_redis
    mock_redis.ping.return_value = True

    # 2. Preparar el DataFrame Falso
    datos_falsos = pd.DataFrame({
        "temperatura_sensor": [45.5],
        "vibracion_motor": [1.2],
        "Machine failure": [0] 
    })
    mock_read_csv.return_value = datos_falsos
    
    # 3. Engañamos a time.sleep() para que no se quede pausado
    mock_sleep.side_effect = KeyboardInterrupt()

    # 4. Ejecutar la función principal de forma segura
    src.productor.main()

    # 5. Comprobaciones de que todo ha funcionado
    mock_read_csv.assert_called_once_with('data/processed/datos_sensores_test.csv')
    mock_redis.xadd.assert_called_once()
