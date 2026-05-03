# 1. Definimos que nuestro proveedor de nube será Azure
provider "azurerm" {
  features {}
}

# 2. El Grupo de Recursos: Azure obliga a meter todo dentro de una "caja" organizativa
resource "azurerm_resource_group" "mlops_rg" {
  name     = "MLOps-Predictive-Maintenance"
  location = "West Europe" # Puedes usar esta región u otra cercana
}

# 3. La Red Virtual: Creamos una red privada para nuestro servidor
resource "azurerm_virtual_network" "mlops_vnet" {
  name                = "mlops-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.mlops_rg.location
  resource_group_name = azurerm_resource_group.mlops_rg.name
}

# 4. La Subred: Una porción de la red virtual donde vivirá el servidor
resource "azurerm_subnet" "mlops_subnet" {
  name                 = "mlops-subnet"
  resource_group_name  = azurerm_resource_group.mlops_rg.name
  virtual_network_name = azurerm_virtual_network.mlops_vnet.name
  address_prefixes     = ["10.0.2.0/24"]
}

# 5. IP Pública: Necesitamos una dirección IP para poder conectarnos desde casa
resource "azurerm_public_ip" "mlops_ip" {
  name                = "mlops-public-ip"
  location            = azurerm_resource_group.mlops_rg.location
  resource_group_name = azurerm_resource_group.mlops_rg.name
  allocation_method   = "Dynamic"
}

# 6. Cortafuegos (Network Security Group): Abrimos la puerta para acceder
resource "azurerm_network_security_group" "mlops_nsg" {
  name                = "mlops-nsg"
  location            = azurerm_resource_group.mlops_rg.location
  resource_group_name = azurerm_resource_group.mlops_rg.name

  # Regla para permitir conexiones por terminal (SSH)
  security_rule {
    name                       = "SSH"
    priority                   = 1001
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

# 7. Tarjeta de Red: Une la IP pública, la red privada y el cortafuegos
resource "azurerm_network_interface" "mlops_nic" {
  name                = "mlops-nic"
  location            = azurerm_resource_group.mlops_rg.location
  resource_group_name = azurerm_resource_group.mlops_rg.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.mlops_subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.mlops_ip.id
  }
}

# Vinculamos el cortafuegos a la tarjeta de red
resource "azurerm_network_interface_security_group_association" "mlops_nic_nsg" {
  network_interface_id      = azurerm_network_interface.mlops_nic.id
  network_security_group_id = azurerm_network_security_group.mlops_nsg.id
}

# 8. LA MÁQUINA VIRTUAL: Nuestro servidor de producción
resource "azurerm_linux_virtual_machine" "mlops_vm" {
  name                = "mlops-vm"
  resource_group_name = azurerm_resource_group.mlops_rg.name
  location            = azurerm_resource_group.mlops_rg.location
  size                = "Standard_B1s" # Tamaño económico/gratuito
  admin_username      = "adminuser"
  
  network_interface_ids = [
    azurerm_network_interface.mlops_nic.id,
  ]

  # Autenticación mediante contraseña (cámbiala por una segura tuya)
  admin_password                  = "PasswordSeguraMLOps123!"
  disable_password_authentication = false

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  # Imagen del sistema operativo: Ubuntu 22.04 LTS
  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }

  # Script que se ejecuta automáticamente al encenderse por primera vez
  custom_data = base64encode(<<-EOF
              #!/bin/bash
              apt-get update
              apt-get install -y docker.io docker-compose git
              systemctl start docker
              systemctl enable docker
              usermod -aG docker adminuser
              EOF
  )
}

# 9. Output: Terraform nos chivará la IP al terminar
data "azurerm_public_ip" "mlops_ip_data" {
  name                = azurerm_public_ip.mlops_ip.name
  resource_group_name = azurerm_linux_virtual_machine.mlops_vm.resource_group_name
}

output "ip_publica_del_servidor" {
  value = data.azurerm_public_ip.mlops_ip_data.ip_address
}
