#!/bin/bash
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
    wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
    sudo apt update && sudo apt -y install terraform
else
    echo "✅ Terraform ya está instalado."
fi

# 3. Inicia sesión en Azure usando código de dispositivo (seguro para Codespaces)
echo "🔑 Abriendo conexión con Azure..."
az login --use-device-code

echo "🎉 ¡Entorno listo! Ya puedes ir a tu carpeta terraform y ejecutar los comandos."