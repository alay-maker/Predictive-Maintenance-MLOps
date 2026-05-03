#!/bin/bash

# Iniciar Redis en background
redis-server --daemonize yes --logfile /var/log/redis/redis.log

# Esperar a que Redis esté listo
sleep 2

# Verificar que Redis está corriendo
if ! redis-cli ping > /dev/null 2>&1; then
    echo "Error: Redis no se pudo iniciar"
    exit 1
fi

echo "Redis iniciado exitosamente"

# Ejecutar el orquestador principal
echo "Iniciando aplicación..."
python src/orquestador.py

# Mantener el contenedor activo
tail -f /var/log/redis/redis.log
