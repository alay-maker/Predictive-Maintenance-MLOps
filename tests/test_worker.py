import pytest
from unittest.mock import patch, MagicMock
import src.worker

@patch("src.worker.redis.Redis")
def test_worker_alerta_critica(mock_redis_class):
    mock_redis = MagicMock()
    mock_redis_class.return_value = mock_redis
    
    mock_redis.xreadgroup.side_effect = [
        [["input_stream", [("12345-0", {"temperatura": "90"})]]],
        KeyboardInterrupt() # Simula que pulsamos Ctrl+C para salir del bucle
    ]
    
    def mock_hgetall(nodo):
        if nodo == "nodo:0":
            return {"tipo": "decision", "variable": "temperatura", "umbral": "50", "hijo_menor_igual": "nodo:1", "hijo_mayor": "nodo:2"}
        elif nodo == "nodo:2":
            return {"tipo": "hoja", "resultado": "Failure"}
    mock_redis.hgetall.side_effect = mock_hgetall

    # Ejecutamos la función de forma segura
    src.worker.main()

    # Comprobaciones
    mock_redis.lpush.assert_called_once()
    mock_redis.xack.assert_called_once()

@patch("src.worker.redis.Redis")
def test_worker_dato_normal(mock_redis_class):
    mock_redis = MagicMock()
    mock_redis_class.return_value = mock_redis
    
    mock_redis.xreadgroup.side_effect = [
        [["input_stream", [("12345-1", {"temperatura": "30"})]]],
        KeyboardInterrupt()
    ]
    
    def mock_hgetall(nodo):
        if nodo == "nodo:0":
            return {"tipo": "decision", "variable": "temperatura", "umbral": "50", "hijo_menor_igual": "nodo:1", "hijo_mayor": "nodo:2"}
        elif nodo == "nodo:1":
            return {"tipo": "hoja", "resultado": "Normal"}
    mock_redis.hgetall.side_effect = mock_hgetall

    src.worker.main()

    mock_redis.lpush.assert_not_called()
    mock_redis.xack.assert_called_once()
