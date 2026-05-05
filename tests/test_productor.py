import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import src.productor

@patch("src.productor.redis.Redis")
@patch("src.productor.pd.read_csv")
@patch("src.productor.time.sleep")
def test_productor_flujo_completo(mock_sleep, mock_read_csv, mock_redis_class):
    mock_redis = MagicMock()
    mock_redis_class.return_value = mock_redis
    mock_redis.ping.return_value = True  # Conexión exitosa al primer intento

    datos_falsos = pd.DataFrame({
        "temperatura_sensor": [45.5],
        "vibracion_motor": [1.2],
        "Machine failure": [0]
    })
    mock_read_csv.return_value = datos_falsos
    mock_sleep.side_effect = [None, KeyboardInterrupt()]  # ← primer sleep del xadd OK, segundo interrumpe

    src.productor.main()

    mock_read_csv.assert_called_once_with('data/processed/datos_sensores_test.csv')
    mock_redis.xadd.assert_called_once()
