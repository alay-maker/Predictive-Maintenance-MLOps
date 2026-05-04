#!/bin/bash
# 'set -e' hace que el script se detenga si algún comando falla
set -e

echo "🚀 Iniciando configuración del entorno MLOps..."

# 1. Comprueba e instala Azure CLI si no existe
if ! command -v az &> /dev/null; then
    echo "📦 Instalando Azure CLI..."
    curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
else
    echo "✅ Azure CLI ya está instalado."
fi

# 2. Comprueba e instala Terraform si no existe
if ! command -v terraform &> /dev/null; then
    echo "📦 Instalando Terraform..."
    # Aseguramos dependencias para añadir repositorios
    sudo apt-get update && sudo apt-get install -y gnupg software-properties-common wget
    wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
    sudo apt update && sudo apt -y install terraform
else
    echo "✅ Terraform ya está instalado."
fi

# 3. COMPROBACIÓN CRÍTICA: Clave SSH para el main.tf
# Si la clave no existe, la creamos para que Terraform no falle.
if [ ! -f ~/.ssh/id_rsa.pub ]; then
    echo "🔑 No se encontró clave SSH pública (~/.ssh/id_rsa.pub)."
    echo "🔨 Generando un nuevo par de claves..."
    mkdir -p ~/.ssh
    ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
    echo "✅ Clave SSH generada exitosamente."
else
    echo "✅ Clave SSH detectada correctamente."
fi

# 4. Inicia sesión en Azure usando código de dispositivo
echo "🔑 Abriendo conexión con Azure..."
az login --use-device-code

echo "-------------------------------------------------------------------"
echo "🎉 ¡Entorno listo!"
echo "📍 Tu main.tf está en la carpeta /terraform."
echo "💡 Recuerda subir el contenido de '~/.ssh/id_rsa' a los Secrets de GitHub"
echo "   con el nombre AZURE_VM_SSH_KEY para que el despliegue funcione."
echo "-------------------------------------------------------------------"
