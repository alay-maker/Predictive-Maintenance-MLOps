# Usar imagen base de Python 3.11
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar Redis desde el repositorio de sistemas
RUN apt-get update && apt-get install -y \
    redis-server \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código del proyecto
COPY . .

# Crear directorio para logs de Redis si es necesario
RUN mkdir -p /var/log/redis

# Exponer puerto de Redis (por defecto)
EXPOSE 6379

# Script de entrada para ejecutar Redis y la aplicación
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Ejecutar el script de entrada
ENTRYPOINT ["/app/entrypoint.sh"]
