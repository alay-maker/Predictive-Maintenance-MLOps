import pytest
from unittest.mock import patch, MagicMock

@patch("src.worker.redis.Redis")
def test_worker_alerta_critica(mock_redis_class):
    """Prueba que el worker lee un mensaje, sigue el árbol y genera una alerta."""
    
    # 1. PREPARAMOS EL REDIS FALSO
    mock_redis = MagicMock()
    mock_redis_class.return_value = mock_redis
    
    # Simulamos que xreadgroup devuelve un dato de sensor
    mock_redis.xreadgroup.side_effect = [
        # Primera vuelta: devuelve datos
        [["input_stream", [("12345-0", {"temperatura": "90"})]]],
        # Segunda vuelta: lanzamos una excepción para romper el bucle infinito del while True
        KeyboardInterrupt()
    ]
    
    # Simulamos los nodos del árbol de decisión
    def mock_hgetall(nodo):
        if nodo == "nodo:0":
            return {"tipo": "decision", "variable": "temperatura", "umbral": "50", "hijo_menor_igual": "nodo:1", "hijo_mayor": "nodo:2"}
        elif nodo == "nodo:2":
            return {"tipo": "hoja", "resultado": "Failure"}
    mock_redis.hgetall.side_effect = mock_hgetall

    # 2. EJECUTAMOS EL WORKER (Atrapamos el KeyboardInterrupt que simula el fin)
    with pytest.raises(KeyboardInterrupt):
        import src.worker

    # 3. COMPROBACIONES
    mock_redis.lpush.assert_called_once() # Confirmamos que se guardó la alerta
    mock_redis.xack.assert_called_once()  # Confirmamos que se avisó a Redis de la lectura

@patch("src.worker.redis.Redis")
def test_worker_dato_normal(mock_redis_class):
    """Prueba que el worker lee un mensaje normal y no genera alerta."""
    
    mock_redis = MagicMock()
    mock_redis_class.return_value = mock_redis
    
    # Simulamos un dato que no debe dar alerta
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

    # Ejecutamos
    with pytest.raises(KeyboardInterrupt):
        import importlib
        import src.worker
        # Recargamos el módulo porque ya se importó en el test anterior
        importlib.reload(src.worker)

    # Comprobaciones: NO debe haber alerta, pero SÍ confirmación de lectura
    mock_redis.lpush.assert_not_called()
    mock_redis.xack.assert_called_once()
