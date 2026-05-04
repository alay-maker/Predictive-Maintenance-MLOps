# Predictive Maintenance MLOps

> **Real-time Industrial Equipment Telemetry Classification and Predictive Maintenance System**

A production-grade MLOps platform for ingesting, processing, and classifying real-time telemetry data from industrial machinery using Redis streams, machine learning models, and containerized microservices.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [System Components](#system-components)
- [Configuration](#configuration)
- [Usage](#usage)
- [Development](#development)
- [Deployment](#deployment)
- [Azure End-to-End Deployment](#azure-end-to-end-deployment)
- [Monitoring & Troubleshooting](#monitoring--troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

This project implements a **real-time predictive maintenance system** for industrial manufacturing equipment (e.g., CNC machines, mills). The system:

- **Ingests** high-frequency telemetry data from industrial sensors
- **Processes** streaming data using Redis as a distributed event broker
- **Classifies** equipment status using pre-trained machine learning models
- **Generates** real-time alerts when anomalies or maintenance triggers are detected
- **Scales** horizontally through containerized worker nodes

### Use Cases

- **Condition-Based Maintenance**: Predict equipment failure before it occurs
- **Downtime Reduction**: Identify maintenance needs during planned windows
- **Cost Optimization**: Prevent costly unplanned equipment breakdowns
- **Performance Analytics**: Track equipment health metrics over time

---

## 🏗️ Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     Predictive Maintenance System                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                       │
│     ┌──────────────┐     ┌─────────────────┐     ┌──────────────┐     │
│     │  Productor   │────▶│  Redis Streams  │◀────│   Workers   │     │
│     │  (Producer)  │     │   (Broker/DB)   │     │ (Classifiers)│     │
│     └──────────────┘     └─────────────────┘     └──────────────┘     │
│            │                      │                      │            │
│   • Generates            • Message Queue        • ML Classification   │
│     telemetry data       • Persistent Store     • Anomaly Detection   │
│   • Stream ingestion     • Data Distribution    • Alert Generation    │
│                                                                       │
│     ┌───────────────────────────────────────────────────────────┐     │
│     │          Configuration & Setup (setup_redis.py)           │     │
│     │                                                           │     │
│     │  • Initialize Redis streams                               │     │
│     │  • Load ML models                                         │     │
│     │  • Configure alert thresholds                             │     │
│     └───────────────────────────────────────────────────────���───┘     │
│                                                                       │
└─────────────────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Message Broker** | Redis 7.0+ | Event streaming & distributed queue |
| **Language** | Python 3.11+ | Data processing & ML integration |
| **ML Framework** | scikit-learn | Equipment status classification |
| **Data Processing** | Pandas | Time-series analysis |
| **Containerization** | Docker & Docker Compose | Environment isolation & deployment |
| **Infrastructure** | Terraform (Azure) | Cloud deployment & IaC |
| **Testing** | pytest | Quality assurance |

---

## ✨ Features

- ✅ **Real-time Data Streaming**: High-throughput telemetry ingestion using Redis streams
- ✅ **Distributed Processing**: Horizontally scalable worker architecture
- ✅ **Machine Learning Integration**: Pre-trained models for equipment classification
- ✅ **Anomaly Detection**: Automatic identification of abnormal equipment behavior
- ✅ **Docker Containerization**: Consistent environments across dev/test/prod
- ✅ **Data Persistence**: Redis-backed storage with volume management
- ✅ **Alert System**: Real-time notifications for critical events
- ✅ **Service Orchestration**: docker-compose for local development
- ✅ **Infrastructure as Code**: Terraform templates for cloud deployment
- ✅ **Logging & Monitoring**: Comprehensive logging for troubleshooting

---

## 📦 Prerequisites

### Local Development

- **Python 3.11+**
- **Redis 7.0+** (local or container)
- **Docker & Docker Compose 1.29+**
- **pip** (Python package manager)

### Cloud Deployment

- **Azure CLI** (az command)
- **Terraform 1.0+**
- **SSH Key Pair** (~/.ssh/id_rsa)
- **Active Azure Subscription**

### System Requirements

- **Minimum**: 2 CPU cores, 4 GB RAM, 10 GB storage
- **Recommended**: 4+ CPU cores, 8+ GB RAM, 20 GB storage
- **Network**: Inbound TCP ports 6379 (Redis)

---

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended for Development)

**1. Clone the repository:**
```bash
git clone https://github.com/alay-maker/Predictive-Maintenance-MLOps.git
cd Predictive-Maintenance-MLOps
git checkout test-deploy
```

**2. Build and start the system:**
```bash
docker-compose up --build
```

This command will:
- Build the Docker image with all dependencies
- Start Redis server with persistent storage
- Initialize the system via `setup_redis.py`
- Launch the producer (data generator)
- Launch worker(s) for classification

**3. Monitor the system:**
```bash
# View logs from all services
docker-compose logs -f

# View specific service logs
docker-compose logs -f productor
docker-compose logs -f worker
```

**4. Access Redis CLI:**
```bash
# Connect to Redis container
docker exec -it redis-server redis-cli

# View streams
XLEN telemetria
XLEN alertas

# Monitor in real-time
XREAD COUNT 10 STREAMS telemetria 0
```

**5. Clean up:**
```bash
# Stop and remove containers
docker-compose down

# Also remove volumes (careful: this deletes data)
docker-compose down -v
```

---

### Option 2: Local Python Installation

**1. Install dependencies:**
```bash
pip install -r requirements.txt
```

**2. Start Redis locally:**

**macOS (Homebrew):**
```bash
brew install redis
brew services start redis
```

**Linux:**
```bash
sudo apt-get install redis-server
sudo systemctl start redis-server
```

**Windows (WSL2):**
```bash
wsl sudo apt-get install redis-server
wsl sudo systemctl start redis-server
```

**3. Initialize the system:**
```bash
python src/setup_redis.py
```

**4. Start the producer (in Terminal 1):**
```bash
python src/productor.py
```

**5. Start workers (in separate terminals):**
```bash
# Terminal 2
python src/worker.py worker_local_1

# Terminal 3
python src/worker.py worker_local_2
```

**6. Clean test data (when needed):**
```bash
python src/borrar_datos.py
```

---

## 📁 Project Structure

```
Predictive-Maintenance-MLOps/
├── src/                              # Main application source code
│   ├── setup_redis.py               # Redis initialization & model loading
│   ├── productor.py                 # Telemetry data producer/simulator
│   ├── worker.py                    # Stream consumer & classifier worker
│   ├── borrar_datos.py              # Utility to clean Redis data
│   └── [ML models and utilities]    # Additional modules
│
├── data/                            # Data directory
│   ├── raw/                        # Raw sensor data
│   ├── processed/                  # Processed datasets
│   └── models/                     # Trained ML models (if applicable)
│
├── models/                         # Serialized ML models
│   └── [classifier_model.pkl]     # Pre-trained classification model
│
├── tests/                          # Test suite
│   ├── test_*.py                  # Unit tests
│   └── conftest.py                # pytest configuration
│
├── terraform/                      # Infrastructure as Code
│   ├── main.tf                    # Azure infrastructure
│   ├── variables.tf               # Terraform variables
│   └── outputs.tf                 # Deployment outputs
│
├── notebooks/                      # Jupyter notebooks
│   ├── eda.ipynb                  # Exploratory data analysis
│   └── model_training.ipynb       # ML model training
│
├── Dockerfile                      # Container image definition
├── docker-compose.yml              # Multi-container orchestration
├── entrypoint.sh                   # Container startup script
├── setup_env.sh                    # Development environment setup
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
├── .dockerignore                   # Docker build ignore rules
└── README.md                       # This file
```

---

## 🔧 System Components

### 1. **setup_redis.py** - Initialization Service

**Purpose**: Initializes the Redis environment before processing starts

**Responsibilities**:
- Creates Redis streams for telemetry data
- Creates streams for alerts and classifications
- Loads trained ML models from disk
- Initializes configuration and thresholds
- Validates system connectivity

**Triggers**: Runs once during system startup via docker-compose

---

### 2. **productor.py** - Data Producer

**Purpose**: Simulates industrial equipment telemetry data

**Data Streams**:
- **Input**: N/A (generates synthetic data)
- **Output**: `telemetria` stream (telemetry data)

**Characteristics**:
- Generates realistic sensor readings (temperature, vibration, pressure, RPM)
- Simulates normal and anomalous equipment states
- Continuous stream with configurable frequency
- Includes timestamp and equipment ID metadata

**Configuration**:
```python
# Adjustable parameters in productor.py
INTERVAL = 1  # seconds between readings
MACHINES = ['fresadora-1', 'fresadora-2']  # equipment IDs
BATCH_SIZE = 10  # readings per batch
```

---

### 3. **worker.py** - Classification Worker

**Purpose**: Consumes telemetry data and performs ML classification

**Data Flow**:
- **Input**: Consumes from `telemetria` Redis stream
- **Processing**: Applies ML model to classify equipment status
- **Output**: Writes to `alertas` stream (if anomaly detected)

**Key Features**:
- Consumer group for distributed processing
- Automatic acknowledgment of processed messages
- Threshold-based alert generation
- Error handling and retry logic

**Worker Group**: Multiple workers can consume from the same stream concurrently

**Configuration**:
```python
# Adjustable parameters in worker.py
ANOMALY_THRESHOLD = 0.7  # confidence threshold for alerts
WINDOW_SIZE = 100  # feature window for analysis
```

---

### 4. **borrar_datos.py** - Data Cleanup Utility

**Purpose**: Removes all streams and alerts for testing

**Operations**:
- Deletes `telemetria` stream
- Deletes `alertas` stream
- Resets consumer groups
- Clears cached predictions

**Use Cases**:
- Test environment cleanup
- Data reset between test runs
- Production debugging (use with caution)

---

## ⚙️ Configuration

### Environment Variables

Configure via `docker-compose.yml` or shell environment:

```bash
# Redis Configuration
REDIS_HOST=redis-db              # Redis server hostname
REDIS_PORT=6379                  # Redis server port (default)
REDIS_DB=0                       # Redis database number

# Application Configuration
PYTHONUNBUFFERED=1               # Real-time logging
PYTHONDONTWRITEBYTECODE=1        # Prevent .pyc generation
PYTHONPATH=/app                  # Python module path

# Worker Configuration
WORKER_ID=worker_docker          # Unique worker identifier
BATCH_SIZE=50                    # Messages processed per iteration
POLL_INTERVAL=1000               # Poll frequency (milliseconds)
```

### Redis Streams Configuration

**Stream**: `telemetria`
```
Structure: {
  "timestamp": "2026-05-04T10:30:45.123Z",
  "equipment_id": "fresadora-1",
  "temperatura": 75.5,
  "vibracion": 2.3,
  "presion": 120.5,
  "rpm": 1200
}
TTL: 1 week (default)
```

**Stream**: `alertas`
```
Structure: {
  "timestamp": "2026-05-04T10:30:45.123Z",
  "equipment_id": "fresadora-1",
  "alert_type": "ANOMALY" | "MAINTENANCE_REQUIRED" | "CRITICAL",
  "severity": 0.85,
  "message": "Equipment vibration above threshold",
  "recommended_action": "Schedule maintenance within 24 hours"
}
TTL: 30 days
```

---

## 📊 Usage

### Common Operations

#### Monitor Real-Time Data

```bash
# Using redis-cli (inside container)
docker exec -it redis-server redis-cli

# Monitor telemetry stream
XREAD COUNT 5 STREAMS telemetria 0-0

# Monitor alerts
XREAD COUNT 5 STREAMS alertas 0-0

# Get stream statistics
XINFO STREAM telemetria
XINFO STREAM alertas
```

#### Scale Workers

```bash
# Start additional worker instances
docker-compose up -d --scale worker=3

# View running containers
docker ps

# Check worker logs
docker-compose logs worker
```

#### Custom Data Filtering

```python
# In worker.py or custom script
import redis

r = redis.Redis(host='redis-db', port=6379, decode_responses=True)

# Get all alerts for a specific equipment
alerts = r.xrange('alertas', match={'equipment_id': 'fresadora-1'})

# Get high-severity alerts
high_severity = [a for a in alerts if float(a[1]['severity']) > 0.8]
```

---

## 🛠️ Development

### Setting Up Development Environment

**1. Initialize development environment:**
```bash
bash setup_env.sh
```

This script installs:
- Azure CLI
- Terraform
- SSH key generation (if needed)

**2. Create Python virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**3. Install development dependencies:**
```bash
pip install pytest pytest-cov black flake8 mypy
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_worker.py -v

# Run with detailed output
pytest -vv --tb=short
```

### Code Quality

```bash
# Format code with Black
black src/ tests/

# Check code style
flake8 src/ tests/

# Type checking
mypy src/
```

### Adding New Features

1. **Create feature branch**:
```bash
git checkout -b feature/equipment-monitoring
```

2. **Develop and test locally**:
```bash
docker-compose up
# Test your changes
```

3. **Run full test suite**:
```bash
pytest
```

4. **Commit and push**:
```bash
git add .
git commit -m "feat: Add equipment health monitoring"
git push origin feature/equipment-monitoring
```

5. **Create Pull Request** on GitHub

---

## ☁️ Deployment

### Azure Cloud Deployment (via Terraform)

**1. Prepare Azure credentials:**
```bash
bash setup_env.sh  # Logs into Azure and generates SSH keys
```

**2. Configure Terraform variables:**

Create `terraform/terraform.tfvars`:
```hcl
azure_subscription_id = "your-subscription-id"
resource_group_name   = "predictive-maintenance-rg"
location              = "eastus"
vm_name               = "pred-maint-vm"
vm_size               = "Standard_D2s_v3"
docker_image_uri      = "your-registry/predictive-maintenance:latest"
```

**3. Initialize Terraform:**
```bash
cd terraform
terraform init
```

**4. Plan and apply:**
```bash
terraform plan -out=tfplan
terraform apply tfplan
```

**5. Retrieve outputs:**
```bash
terraform output vm_public_ip
terraform output redis_connection_string
```

### Docker Hub / Container Registry

**1. Build image:**
```bash
docker build -t your-registry/predictive-maintenance:latest .
```

**2. Push to registry:**
```bash
docker login
docker push your-registry/predictive-maintenance:latest
```

**3. Deploy with updated image:**
```bash
docker-compose pull
docker-compose up -d
```

---

## 🚀 Azure End-to-End Deployment

This section provides a **complete step-by-step guide** to deploy the entire Predictive Maintenance system from scratch on Microsoft Azure, including infrastructure provisioning, Docker setup, and live demonstrations of the system.

### 📌 Overview

The deployment process consists of:
1. **Infrastructure Provisioning** - Create Azure VMs and resources using Terraform
2. **SSH Connection** - Connect to the VM securely
3. **Docker Installation** - Install Docker cleanly without dependency conflicts
4. **Code Deployment** - Clone and configure the application
5. **System Launch** - Start all microservices
6. **Scalability Testing** - Demonstrate horizontal scaling
7. **Real-time Monitoring** - View live logs and metrics
8. **Cleanup** - Graceful shutdown and resource cleanup

---

### 1️⃣ Provision Infrastructure with Terraform

**Objective**: Create Azure Virtual Machine and networking resources

#### Step 1: Navigate to Terraform directory

```bash
cd terraform
```

#### Step 2: Initialize Terraform

Terraform needs to download provider plugins and prepare your working directory:

```bash
terraform init
```

**What this does**:
- Downloads Azure provider plugin
- Initializes state management
- Creates `.terraform/` directory with dependencies

#### Step 3: Review infrastructure plan

Before applying changes, preview what will be created:

```bash
terraform plan -out=tfplan
```

**Output includes**:
- Resource Group creation
- Virtual Machine configuration
- Network interfaces and security groups
- Storage accounts (if applicable)

#### Step 4: Apply Terraform configuration

Create the infrastructure in Azure:

```bash
terraform apply tfplan
```

**Wait for completion** (~5-10 minutes). The output will display:

```
Apply complete! Resources: X added, 0 changed, 0 destroyed.

Outputs:

vm_public_ip = "20.XX.XXX.XX"
redis_connection_string = "redis://20.XX.XXX.XX:6379"
admin_username = "adminuser"
```

#### Step 5: Save the public IP address

Store the output IP for the next steps:

```bash
AZURE_VM_IP=$(terraform output -raw vm_public_ip)
echo "VM Public IP: $AZURE_VM_IP"
```

---

### 2️⃣ Connect to Azure VM via SSH

**Objective**: Establish secure remote connection to your Virtual Machine

#### Step 1: Verify SSH key exists

```bash
ls -la ~/.ssh/id_rsa
```

If the file doesn't exist, generate it:

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
```

#### Step 2: Connect to the VM

Use SSH to connect with your private key:

```bash
ssh -i ~/.ssh/id_rsa adminuser@$AZURE_VM_IP
```

**Success indicator**: You'll see the Ubuntu command prompt:

```
adminuser@pred-maint-vm:~$
```

#### Step 3: Verify connectivity

Confirm you're on the correct machine:

```bash
uname -a
hostname
```

---

### 3️⃣ Install Docker (Clean Installation)

**Objective**: Install Docker without dependency conflicts using official scripts

#### Step 1: Update system packages

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

#### Step 2: Download official Docker installation script

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
```

This downloads the official Docker installation script maintained by Docker Inc.

#### Step 3: Execute Docker installation

```bash
sudo sh get-docker.sh
```

**Installation includes**:
- Docker Engine
- Docker CLI
- Container runtime
- All required dependencies (automatically resolved)

#### Step 4: Add current user to Docker group

Allow running Docker commands without `sudo`:

```bash
sudo usermod -aG docker $(whoami)
```

#### Step 5: Activate group membership

Apply the new group assignment:

```bash
newgrp docker
```

#### Step 6: Verify Docker installation

Test that Docker is working correctly:

```bash
docker --version
docker ps
```

**Expected output**:
```
Docker version 24.X.X, build XXXXX
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

---

### 4️⃣ Download Project Code

**Objective**: Clone the repository and prepare the application

#### Step 1: Clone the repository

```bash
git clone https://github.com/alay-maker/Predictive-Maintenance-MLOps.git
```

#### Step 2: Navigate to project directory

```bash
cd Predictive-Maintenance-MLOps
```

#### Step 3: Checkout deployment branch

```bash
git checkout test-deploy
```

#### Step 4: Verify project structure

```bash
ls -la
```

You should see:
```
Dockerfile
docker-compose.yml
models/
src/
data/
terraform/
README.md
```

---

### 5️⃣ Deploy the Architecture

**Objective**: Launch all microservices (Redis, Producer, Workers)

#### Step 1: Build and start containers

```bash
docker compose up -d --build
```

**Flags explained**:
- `-d`: Run in detached mode (background)
- `--build`: Rebuild images from Dockerfile

#### Step 2: Wait for services to initialize

The system needs ~30 seconds to:
- Build the application image
- Pull Redis image
- Start containers
- Initialize Redis streams
- Load ML models

#### Step 3: Verify all services are running

```bash
docker ps
```

**Expected output** (minimum 3 containers):
```
CONTAINER ID   IMAGE                    STATUS          PORTS
abcd1234       redis:latest             Up 10 seconds   0.0.0.0:6379->6379/tcp
efgh5678       predictive-maint:latest  Up 5 seconds    
ijkl9012       predictive-maint:latest  Up 3 seconds    
```

#### Step 4: Check initialization logs

Verify that setup_redis.py ran successfully:

```bash
docker compose logs setup-redis
```

**Look for**:
```
✅ El modelo de árbol de decisión ha sido cargado en Redis
```

---

### 6️⃣ Demonstrate Scalability

**Objective**: Scale the worker services to process data in parallel

#### Step 1: Scale to 3 worker instances

```bash
docker compose up -d --scale worker=3
```

This command:
- Adds additional worker containers
- Keeps existing services running
- Workers automatically join the consumer group
- Load is distributed across all workers

#### Step 2: Verify scaling worked

```bash
docker ps
```

Now you should see **3 worker containers** (plus Redis and Productor):
```
CONTAINER ID   IMAGE                    STATUS
worker_1       predictive-maint:latest  Up 5 seconds
worker_2       predictive-maint:latest  Up 4 seconds
worker_3       predictive-maint:latest  Up 2 seconds
redis          redis:latest             Up 2 minutes
productor      predictive-maint:latest  Up 2 minutes
```

#### Step 3: Verify load distribution

Check that each worker is consuming messages:

```bash
docker compose logs worker
```

You should see output from multiple workers processing different messages:
```
[worker_1]: Esperando datos de la fresadora...
[worker_2]: Esperando datos de la fresadora...
[worker_3]: Esperando datos de la fresadora...
```

---

### 7️⃣ Real-Time Monitoring

**Objective**: View live telemetry data, alerts, and system metrics

#### Step 1: Monitor producer telemetry stream

Watch data being generated in real-time:

```bash
docker compose logs -f productor
```

**Expected output**:
```
[PRODUCTOR]: Conectado a servidor Redis. PONG
[PRODUCTOR]: Enviando datos de sensores... ID: 1234567890-0
```

Press `Ctrl+C` to exit

#### Step 2: Monitor worker alerts

In a new terminal, view alerts generated by workers:

```bash
docker compose logs -f worker
```

**Look for critical alerts**:
```
[worker_1] ¡ALERTA CRÍTICA! Fallo detectado. (ID: 1234567890-0)
[worker_2] ¡ALERTA CRÍTICA! Fallo detectado. (ID: 1234567891-0)
[worker_3] ¡ALERTA CRÍTICA! Fallo detectado. (ID: 1234567892-0)
```

#### Step 3: Monitor all services continuously

View combined logs with timestamps:

```bash
docker compose logs -f --timestamps
```

#### Step 4: Connect to Redis for advanced monitoring

Open interactive Redis CLI:

```bash
docker exec -it redis-server redis-cli
```

**View stream statistics**:
```bash
# Check telemetry stream length
XLEN input_stream

# View alert stream length
XLEN registro_alertas

# Monitor streams in real-time
XREAD COUNT 5 STREAMS input_stream 0

# Exit Redis CLI
exit
```

#### Step 5: Monitor container resource usage

View CPU, memory, and network metrics:

```bash
docker stats --no-stream
```

**Shows for each container**:
- CPU percentage
- Memory usage
- Network I/O
- Block I/O

---

### 8️⃣ Cleanup and Shutdown

**Objective**: Gracefully stop services and destroy Azure resources

#### Step 1: Stop all Docker services

Stop containers but preserve data:

```bash
docker compose stop
```

#### Step 2: Remove containers

Delete all containers (not images):

```bash
docker compose down
```

#### Step 3: Clean up volumes (optional)

⚠️ **Warning**: This deletes all persisted data including Redis streams

```bash
docker compose down -v
```

#### Step 4: Destroy Azure infrastructure

Remove all Terraform-managed resources to avoid charges:

```bash
cd terraform
terraform destroy
```

**Confirmation prompt**:
```
Do you really want to destroy all resources?
Type 'yes' to confirm.
```

Type `yes` and press Enter.

**Wait for completion** (~5-10 minutes). The output will show:
```
Destroy complete! Resources: X destroyed.
```

#### Step 5: Verify destruction

Confirm resources are gone:

```bash
terraform state list
# Should be empty
```

Also verify in Azure Portal - Resource Group should be deleted.

---

### 🔍 Complete Workflow Summary

```bash
# 1. Provision Infrastructure
cd terraform
terraform init
terraform plan -out=tfplan
terraform apply tfplan
AZURE_VM_IP=$(terraform output -raw vm_public_ip)

# 2. Connect to VM
ssh -i ~/.ssh/id_rsa adminuser@$AZURE_VM_IP

# 3. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $(whoami)
newgrp docker

# 4. Deploy Application
git clone https://github.com/alay-maker/Predictive-Maintenance-MLOps.git
cd Predictive-Maintenance-MLOps
git checkout test-deploy

# 5. Launch System
docker compose up -d --build

# 6. Scale Workers
docker compose up -d --scale worker=3

# 7. Monitor (in separate terminals)
docker compose logs -f productor
docker compose logs -f worker
docker stats

# 8. Cleanup
docker compose down
docker compose down -v
cd terraform
terraform destroy
```

---

### ⚠️ Troubleshooting Azure Deployment

#### Issue: Terraform fails to authenticate

**Solution**:
```bash
az login
az account show
```

Ensure your subscription is active and you have permissions.

#### Issue: SSH connection refused

**Solution**:
```bash
# Verify security group allows SSH (port 22)
# Check VM is in "Running" state in Azure Portal
# Verify correct IP address
echo $AZURE_VM_IP
```

#### Issue: Docker daemon not responding

**Solution**:
```bash
# Restart Docker
sudo systemctl restart docker

# Or reconnect group membership
sudo usermod -aG docker $(whoami)
newgrp docker
```

#### Issue: Containers won't start

**Solution**:
```bash
# Check Docker logs
docker compose logs

# Rebuild images
docker compose up -d --build

# Check disk space
df -h
```

---

## 📈 Monitoring & Troubleshooting

### Logs and Diagnostics

**View service logs:**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f productor

# Last 100 lines
docker-compose logs --tail=100 worker

# Timestamps included
docker-compose logs --timestamps
```

### Common Issues

#### ❌ "Redis connection refused"

**Cause**: Redis not running or not accessible

**Solution**:
```bash
# Check Redis is running
docker ps | grep redis

# Or restart
docker-compose restart redis-db
```

#### ❌ "Consumer group does not exist"

**Cause**: `setup_redis.py` didn't run successfully

**Solution**:
```bash
# Re-run initialization
docker-compose restart setup-redis

# Or manually in redis-cli
XGROUP CREATE telemetria workers $ MKSTREAM
```

#### ❌ "No module named 'src'"

**Cause**: PYTHONPATH not set correctly

**Solution**:
```bash
# Set PYTHONPATH locally
export PYTHONPATH=/path/to/repo

# Or use correct working directory
cd /path/to/repo
python -m src.worker
```

#### ❌ Worker crashes on startup

**Cause**: Model file not found or corrupted

**Solution**:
```bash
# Check model exists
docker exec redis-server ls -la /app/models/

# Re-initialize
docker-compose down
docker-compose up --build
```

### Performance Monitoring

**Stream metrics:**
```bash
# Inside redis-cli
XINFO STREAM telemetria  # Info about telemetry stream
XLEN telemetria          # Number of pending messages
XINFO GROUPS telemetria  # Consumer group status
```

**Redis memory usage:**
```bash
docker exec redis-server redis-cli INFO memory
```

**Container resource usage:**
```bash
docker stats
```

---

## 🤝 Contributing

### Contribution Guidelines

1. **Fork** the repository
2. **Create** a feature branch (`feature/amazing-feature`)
3. **Commit** changes with descriptive messages
4. **Push** to your fork
5. **Submit** a Pull Request

### Standards

- Python code must follow PEP 8 (use Black for formatting)
- All new features require tests
- Update documentation for breaking changes
- Use meaningful commit messages

---

## 📄 License

This project is licensed under the **MIT License** - see the LICENSE file for details.

---

## 👥 Author

**alay-maker** - [GitHub Profile](https://github.com/alay-maker)

---

## 📚 Additional Resources

- [Redis Streams Documentation](https://redis.io/docs/data-types/streams/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [scikit-learn Documentation](https://scikit-learn.org/)
- [Terraform Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Azure CLI Documentation](https://learn.microsoft.com/en-us/cli/azure/)

---

## 🆘 Support

For issues, questions, or suggestions:

1. **Check** existing [GitHub Issues](https://github.com/alay-maker/Predictive-Maintenance-MLOps/issues)
2. **Review** the [Troubleshooting](#monitoring--troubleshooting) section above
3. **Create** a new issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs. actual behavior
   - Environment details (OS, Python version, Docker version)

---

**Last Updated**: May 4, 2026  
**Status**: Active Development
