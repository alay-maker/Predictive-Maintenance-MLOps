# Práctica 1: Mantenimiento Predictivo con Redis

Este proyecto simula la ingesta y clasificación en tiempo real de telemetría de una fresadora industrial.

## Cómo probar el sistema:
1. Asegúrate de tener tu servidor Redis local en ejecución.
2. Instala las librerías necesarias: `pip install redis pandas`
3. Ejecuta el orquestador principal: `python simulacion.py`

*Nota: Para limpiar el entorno de pruebas (borrar streams y alertas generadas), puedes ejecutar `python borrar_datos.py`.*