provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "mlops_rg" {
  name     = "MLOps-Predictive-Maintenance"
  location = "West Europe" 
}

resource "azurerm_virtual_network" "mlops_vnet" {
  name                = "mlops-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.mlops_rg.location
  resource_group_name = azurerm_resource_group.mlops_rg.name
}

resource "azurerm_subnet" "mlops_subnet" {
  name                 = "mlops-subnet"
  resource_group_name  = azurerm_resource_group.mlops_rg.name
  virtual_network_name = azurerm_virtual_network.mlops_vnet.name
  address_prefixes     = ["10.0.2.0/24"]
}

resource "azurerm_public_ip" "mlops_ip" {
  name                = "mlops-public-ip"
  location            = azurerm_resource_group.mlops_rg.location
  resource_group_name = azurerm_resource_group.mlops_rg.name
  allocation_method   = "Dynamic"
}

resource "azurerm_network_security_group" "mlops_nsg" {
  name                = "mlops-nsg"
  location            = azurerm_resource_group.mlops_rg.location
  resource_group_name = azurerm_resource_group.mlops_rg.name

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

resource "azurerm_network_interface_security_group_association" "mlops_nic_nsg" {
  network_interface_id      = azurerm_network_interface.mlops_nic.id
  network_security_group_id = azurerm_network_security_group.mlops_nsg.id
}

resource "azurerm_linux_virtual_machine" "mlops_vm" {
  name                = "mlops-vm"
  resource_group_name = azurerm_resource_group.mlops_rg.name
  location            = azurerm_resource_group.mlops_rg.location
  size                = "Standard_B1s"
  admin_username      = "adminuser"
  
  network_interface_ids = [
    azurerm_network_interface.mlops_nic.id,
  ]

  # Seguridad por SSH, sin contraseñas en texto plano
  disable_password_authentication = true
  admin_ssh_key {
    username   = "adminuser"
    public_key = file("~/.ssh/id_rsa.pub")
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }

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

data "azurerm_public_ip" "mlops_ip_data" {
  name                = azurerm_public_ip.mlops_ip.name
  resource_group_name = azurerm_linux_virtual_machine.mlops_vm.resource_group_name
}

output "ip_publica_del_servidor" {
  value = data.azurerm_public_ip.mlops_ip_data.ip_address
}
