import pytest
from unittest.mock import patch, mock_open, MagicMock
from src.setup_redis import preparar_base_datos

# Usamos 'patch' para interceptar las llamadas a Redis y a la lectura de archivos (open)
@patch("src.setup_redis.redis.Redis")
@patch("builtins.open", new_callable=mock_open, read_data='{"nodo:1": {"feature": "temperatura", "threshold": 50}}')
def test_preparar_base_datos_exito(mock_archivo, mock_redis_class):
    """Prueba que el modelo se inyecta correctamente si Redis y el JSON funcionan."""
    
    # 1. PREPARACIÓN: Creamos nuestro "Redis de mentira"
    mock_redis_instancia = MagicMock()
    mock_redis_class.return_value = mock_redis_instancia
    mock_redis_instancia.ping.return_value = True # Simulamos que el ping responde bien
    
    # Configuramos el pipeline de Redis
    mock_pipeline = MagicMock()
    mock_redis_instancia.pipeline.return_value = mock_pipeline
    mock_redis_instancia.scan_iter.return_value = [] # Simulamos que no hay nodos antiguos

    # 2. ACCIÓN: Ejecutamos tu función real
    resultado = preparar_base_datos()

    # 3. COMPROBACIÓN: Afirmamos (assert) que todo ha ido como esperábamos
    assert resultado is True
    mock_redis_instancia.ping.assert_called_once() # Comprobamos que hizo ping a Redis
    mock_pipeline.execute.assert_called_once()     # Comprobamos que ejecutó el guardado

@patch("src.setup_redis.redis.Redis")
def test_preparar_base_datos_fallo_conexion(mock_redis_class):
    """Prueba que la función maneja bien un error si Redis está apagado."""
    
    # Hacemos que el "Redis de mentira" lance un error al intentar conectarse
    mock_redis_class.side_effect = Exception("Error de conexión simulado")

    # Ejecutamos tu función
    resultado = preparar_base_datos()

    # Afirmamos que la función devolvió False (como tienes programado en tu bloque except)
    assert resultado is False
