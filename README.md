# Predictive Maintenance MLOps

> **Real-time Industrial Equipment Telemetry Classification and Predictive Maintenance System**

A production-grade MLOps platform for ingesting, processing, and classifying real-time telemetry data from industrial machinery using Redis streams, machine learning models, and containerized microservices.

---

## 📋 Quick Navigation

- **[📐 Architecture Diagrams](ARCHITECTURE.md)** ⭐ _Visual system design with detailed data flows_
- **[🚀 Quick Start](#quick-start)** - Get running in 5 minutes
- **[☁️ Azure Deployment](#azure-end-to-end-deployment)** - Production cloud setup
- **[📚 Full Documentation](#full-documentation)** - Complete reference

---

## 🎯 Overview

This project implements a **real-time predictive maintenance system** for industrial manufacturing equipment (CNC machines, mills, etc.). The system:

- **Ingests** high-frequency telemetry data from industrial sensors
- **Processes** streaming data using Redis as a distributed event broker
- **Classifies** equipment status using pre-trained machine learning models
- **Generates** real-time alerts when anomalies are detected
- **Scales** horizontally through containerized worker nodes

### Use Cases

- **Condition-Based Maintenance**: Predict equipment failure before it occurs
- **Downtime Reduction**: Identify maintenance needs during planned windows
- **Cost Optimization**: Prevent costly unplanned equipment breakdowns
- **Performance Analytics**: Track equipment health metrics over time

---

## ✨ Features

- ✅ **Real-time Data Streaming** - High-throughput telemetry ingestion using Redis streams
- ✅ **Distributed Processing** - Horizontally scalable worker architecture
- ✅ **Machine Learning Integration** - Pre-trained models for equipment classification
- ✅ **Anomaly Detection** - Automatic identification of abnormal equipment behavior
- ✅ **Docker Containerization** - Consistent environments across dev/test/prod
- ✅ **Alert System** - Real-time notifications for critical events
- ✅ **Infrastructure as Code** - Terraform templates for Azure deployment
- ✅ **Horizontal Scaling** - Add workers dynamically without restart
- ✅ **Data Persistence** - Redis-backed storage with configurable TTL

---

## 📦 Prerequisites

### Local Development

- **Python 3.11+** | **Redis 7.0+** | **Docker & Compose 1.29+**

### Cloud Deployment

- **Azure CLI** | **Terraform 1.0+** | **SSH Key Pair** | **Active Azure Subscription**

### System Requirements

- **Minimum**: 2 CPU cores, 4 GB RAM, 10 GB storage
- **Recommended**: 4+ CPU cores, 8+ GB RAM, 20 GB storage

---

## 🚀 Quick Start

### Option 1: Docker Compose (Development)

```bash
# 1. Clone and setup
git clone https://github.com/alay-maker/Predictive-Maintenance-MLOps.git
cd Predictive-Maintenance-MLOps
git checkout test-deploy

# 2. Run the system
docker-compose up --build

# 3. Monitor (in another terminal)
docker-compose logs -f

# 4. Access Redis
docker exec -it redis-server redis-cli
XLEN telemetria    # View telemetry stream
XLEN alertas       # View alerts stream

# 5. Scale workers
docker-compose up -d --scale worker=3

# 6. Cleanup
docker-compose down -v
```

### Option 2: Local Python

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start Redis (macOS: brew install redis && brew services start redis)
# 3. Initialize system
python src/setup_redis.py

# 4. Start producer (Terminal 1)
python src/productor.py

# 5. Start workers (Terminal 2+)
python src/worker.py worker_local_1
python src/worker.py worker_local_2

# 6. Clean test data
python src/borrar_datos.py
```

---

## 📁 Project Structure

```
Predictive-Maintenance-MLOps/
├── src/                              # Application source code
│   ├── setup_redis.py               # Redis initialization & model loading
│   ├── productor.py                 # Telemetry data generator
│   ├── worker.py                    # Stream consumer & ML classifier
│   └── borrar_datos.py              # Cleanup utility
│
├── models/                          # Pre-trained ML models
├── terraform/                       # Azure infrastructure as code
├── tests/                           # Unit tests (pytest)
├── notebooks/                       # Jupyter notebooks (EDA, training)
│
├── Dockerfile                       # Container definition
├── docker-compose.yml               # Multi-container orchestration
├── requirements.txt                 # Python dependencies
├── ARCHITECTURE.md                  # Detailed system architecture 📐
└── README.md                        # This file
```

---

## 🏗️ System Architecture

### Simplified View

```
Sensors → Producer → Redis Streams ← Workers (×N) → Alerts
           (Data Gen)  (Broker)      (Classifiers)  (Output)
```

### Complete Architecture

**[📐 See ARCHITECTURE.md for:**
- Core system design diagrams
- Data flow lifecycle
- Horizontal scaling architecture
- Technology stack layers
- Azure cloud deployment
- Redis streams configuration
- Consumer group coordination
- Performance characteristics

---

## 🔧 System Components

| Component | Purpose | Key Responsibility |
|-----------|---------|-------------------|
| **productor.py** | Data Source | Generate realistic telemetry data from CNC machines |
| **Redis Streams** | Message Broker | Distribute data to workers, persist events |
| **worker.py** | Processor | Apply ML models, detect anomalies, generate alerts |
| **setup_redis.py** | Initialization | Create streams, load models, configure thresholds |

---

## 📊 Configuration

### Environment Variables

```bash
# Redis
REDIS_HOST=redis-db              # Redis server hostname
REDIS_PORT=6379                  # Redis port
REDIS_DB=0                       # Database number

# Application
PYTHONUNBUFFERED=1               # Real-time logging
PYTHONPATH=/app                  # Module path

# Worker
WORKER_ID=worker_docker          # Worker identifier
BATCH_SIZE=50                    # Messages per iteration
POLL_INTERVAL=1000               # Poll frequency (ms)
```

### Redis Streams

**telemetria stream** (telemetry data - 1 week TTL):
```json
{
  "timestamp": "2026-05-04T10:30:45.123Z",
  "equipment_id": "fresadora-1",
  "temperatura": 75.5,
  "vibracion": 2.3,
  "presion": 120.5,
  "rpm": 1200
}
```

**alertas stream** (alerts - 30 day TTL):
```json
{
  "timestamp": "2026-05-04T10:30:46.001Z",
  "equipment_id": "fresadora-1",
  "alert_type": "ANOMALY",
  "severity": 0.85,
  "message": "Equipment vibration above threshold",
  "recommended_action": "Schedule maintenance"
}
```

---

## ☁️ Azure End-to-End Deployment

### Quick Summary

Complete step-by-step guide includes:
1. **Infrastructure Provisioning** - Terraform creates VM & networking
2. **SSH Connection** - Secure remote access
3. **Docker Installation** - Clean setup on Azure VM
4. **Code Deployment** - Clone & configure app
5. **System Launch** - Start microservices
6. **Scalability Testing** - Demonstrate load balancing
7. **Real-time Monitoring** - View logs & metrics
8. **Cleanup** - Graceful shutdown & resource cleanup

### Complete Deployment Steps

**[📖 See README.md Section "Azure End-to-End Deployment" for full 8-step guide]**

Or jump to specific steps:
- [1️⃣ Provision Infrastructure with Terraform](#1️⃣-provision-infrastructure-with-terraform)
- [2️⃣ Connect to Azure VM via SSH](#2️⃣-connect-to-azure-vm-via-ssh)
- [3️⃣ Install Docker](#3️⃣-install-docker-clean-installation)
- [4️⃣ Download Project Code](#4️⃣-download-project-code)
- [5️⃣ Deploy Architecture](#5️⃣-deploy-the-architecture)
- [6️⃣ Demonstrate Scalability](#6️⃣-demonstrate-scalability)
- [7️⃣ Real-Time Monitoring](#7️⃣-real-time-monitoring)
- [8️⃣ Cleanup](#8️⃣-cleanup-and-shutdown)

---

## 📈 Monitoring & Troubleshooting

### View Logs

```bash
docker-compose logs -f              # All services
docker-compose logs -f productor    # Specific service
docker-compose logs --tail=100      # Last 100 lines
```

### Redis Monitoring

```bash
docker exec -it redis-server redis-cli

# Inside redis-cli:
XLEN telemetria                     # Pending entries count
XINFO STREAM telemetria             # Stream statistics
XINFO GROUPS telemetria             # Consumer groups info
```

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Redis connection refused | Redis not running | `docker-compose restart redis-db` |
| Consumer group missing | setup_redis.py failed | `docker-compose restart setup-redis` |
| Worker crashes | Model not found | `docker-compose up -d --build` |
| No data flowing | Producer stopped | `docker-compose logs productor` |

### Resource Monitoring

```bash
docker stats                        # CPU, memory, network usage
docker-compose logs --timestamps    # With timestamps
```

---

## 🛠️ Development

### Setup

```bash
python -m venv venv
source venv/bin/activate            # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy
```

### Testing

```bash
pytest                              # Run all tests
pytest --cov=src tests/             # With coverage
pytest -v tests/test_worker.py      # Specific file
```

### Code Quality

```bash
black src/ tests/                   # Format code
flake8 src/ tests/                  # Check style
mypy src/                           # Type checking
```

### Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/name`
3. Commit changes: `git commit -m "feat: description"`
4. Push to fork: `git push origin feature/name`
5. Create Pull Request

---

## 🤝 Support

For issues, questions, or suggestions:

1. **Check** [GitHub Issues](https://github.com/alay-maker/Predictive-Maintenance-MLOps/issues)
2. **Review** [ARCHITECTURE.md](ARCHITECTURE.md) for system design
3. **Create** new issue with:
   - Clear problem description
   - Steps to reproduce
   - Expected vs. actual behavior
   - Environment details (OS, Python, Docker versions)

---

## 📚 Additional Resources

- [Architecture Diagrams](ARCHITECTURE.md) - Complete system design
- [Redis Streams Documentation](https://redis.io/docs/data-types/streams/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [scikit-learn Documentation](https://scikit-learn.org/)
- [Terraform Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Azure CLI Documentation](https://learn.microsoft.com/en-us/cli/azure/)

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 👥 Author

**alay-maker** - [GitHub Profile](https://github.com/alay-maker)

**Last Updated**: May 4, 2026 | **Status**: Active Development

---

---

# 🚀 Azure End-to-End Deployment

Complete step-by-step guide to deploy the entire system from scratch on Microsoft Azure.

## 📌 Overview

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

## 1️⃣ Provision Infrastructure with Terraform

**Objective**: Create Azure Virtual Machine and networking resources

### Step 1: Navigate to Terraform directory

```bash
cd terraform
```

### Step 2: Initialize Terraform

```bash
terraform init
```

Downloads Azure provider plugin and initializes state management.

### Step 3: Review infrastructure plan

```bash
terraform plan -out=tfplan
```

Previews Resource Groups, VMs, network interfaces, and security groups.

### Step 4: Apply Terraform configuration

```bash
terraform apply tfplan
```

**Wait for completion** (~5-10 minutes). Output displays:

```
Apply complete! Resources: X added, 0 changed, 0 destroyed.

Outputs:
vm_public_ip = "20.XX.XXX.XX"
redis_connection_string = "redis://20.XX.XXX.XX:6379"
admin_username = "adminuser"
```

### Step 5: Save the public IP

```bash
AZURE_VM_IP=$(terraform output -raw vm_public_ip)
echo "VM Public IP: $AZURE_VM_IP"
```

---

## 2️⃣ Connect to Azure VM via SSH

**Objective**: Establish secure remote connection

### Step 1: Verify SSH key

```bash
ls -la ~/.ssh/id_rsa

# If missing, generate:
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
```

### Step 2: Connect to VM

```bash
ssh -i ~/.ssh/id_rsa adminuser@$AZURE_VM_IP
```

Success indicator - Ubuntu prompt appears:
```
adminuser@pred-maint-vm:~$
```

### Step 3: Verify connectivity

```bash
uname -a
hostname
```

---

## 3️⃣ Install Docker (Clean Installation)

**Objective**: Install Docker without dependency conflicts

### Step 1: Update system

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### Step 2: Download Docker script

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
```

### Step 3: Execute installation

```bash
sudo sh get-docker.sh
```

Installs Docker Engine, CLI, and container runtime with all dependencies.

### Step 4: Add user to Docker group

```bash
sudo usermod -aG docker $(whoami)
newgrp docker
```

Allows running Docker without `sudo`.

### Step 5: Verify installation

```bash
docker --version
docker ps
```

Expected output:
```
Docker version 24.X.X, build XXXXX
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

---

## 4️⃣ Download Project Code

**Objective**: Clone and prepare the application

```bash
git clone https://github.com/alay-maker/Predictive-Maintenance-MLOps.git
cd Predictive-Maintenance-MLOps
git checkout test-deploy

# Verify structure
ls -la
```

Expected files: `Dockerfile`, `docker-compose.yml`, `models/`, `src/`, `terraform/`

---

## 5️⃣ Deploy the Architecture

**Objective**: Launch all microservices (Redis, Producer, Workers)

### Step 1: Build and start containers

```bash
docker compose up -d --build
```

- `-d`: Run in detached mode (background)
- `--build`: Rebuild images from Dockerfile

### Step 2: Wait for initialization (~30 seconds)

System initializes:
- Application image build
- Redis image pull
- Container startup
- Redis streams creation
- ML model loading

### Step 3: Verify all services running

```bash
docker ps
```

Expected: 3+ containers (Redis, Productor, Workers)

### Step 4: Check initialization logs

```bash
docker compose logs setup-redis
```

Look for: `✅ El modelo de árbol de decisión ha sido cargado en Redis`

---

## 6️⃣ Demonstrate Scalability

**Objective**: Scale worker services to process data in parallel

### Step 1: Scale to 3 workers

```bash
docker compose up -d --scale worker=3
```

- Adds additional worker containers
- Keeps existing services running
- Workers automatically join consumer group
- Load distributed across all workers

### Step 2: Verify scaling

```bash
docker ps
```

Now shows 3 worker containers plus Redis and Productor.

### Step 3: Verify load distribution

```bash
docker compose logs worker
```

Output from multiple workers processing different messages.

---

## 7️⃣ Real-Time Monitoring

**Objective**: View live telemetry data, alerts, and metrics

### Step 1: Monitor producer

```bash
docker compose logs -f productor
```

Expected output:
```
[PRODUCTOR]: Conectado a servidor Redis. PONG
[PRODUCTOR]: Enviando datos de sensores... ID: 1234567890-0
```

Press `Ctrl+C` to exit.

### Step 2: Monitor worker alerts

```bash
docker compose logs -f worker
```

Look for critical alerts:
```
[worker_1] ¡ALERTA CRÍTICA! Fallo detectado.
[worker_2] ¡ALERTA CRÍTICA! Fallo detectado.
```

### Step 3: Combined monitoring

```bash
docker compose logs -f --timestamps
```

### Step 4: Advanced Redis monitoring

```bash
docker exec -it redis-server redis-cli

# Inside redis-cli:
XLEN input_stream              # Telemetry count
XLEN registro_alertas          # Alert count
XREAD COUNT 5 STREAMS input_stream 0
```

### Step 5: Resource monitoring

```bash
docker stats --no-stream
```

Shows CPU, memory, network usage for each container.

---

## 8️⃣ Cleanup and Shutdown

**Objective**: Gracefully stop services and destroy resources

### Step 1: Stop containers

```bash
docker compose stop
```

### Step 2: Remove containers

```bash
docker compose down
```

### Step 3: Clean volumes (optional)

```bash
docker compose down -v
```

⚠️ **Warning**: This deletes all persisted data including Redis streams.

### Step 4: Destroy Azure infrastructure

```bash
cd terraform
terraform destroy
```

Confirmation prompt: Type `yes` and press Enter.

**Wait for completion** (~5-10 minutes):
```
Destroy complete! Resources: X destroyed.
```

### Step 5: Verify destruction

```bash
terraform state list        # Should be empty
```

Also verify in Azure Portal - Resource Group should be deleted.

---

## 🔍 Complete Workflow Summary

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

## ⚠️ Troubleshooting

### Terraform Authentication Failed

```bash
az login
az account show
```

Ensure subscription is active and you have permissions.

### SSH Connection Refused

```bash
# Verify security group allows SSH (port 22)
# Check VM status in Azure Portal
echo $AZURE_VM_IP
```

### Docker Daemon Not Responding

```bash
sudo systemctl restart docker
sudo usermod -aG docker $(whoami)
newgrp docker
```

### Containers Won't Start

```bash
docker compose logs              # Check error messages
docker compose up -d --build     # Rebuild images
df -h                            # Check disk space
```

---

## 📚 Additional Help

- **Architecture Details**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Local Testing**: [Quick Start](#quick-start) section
- **Issues**: [GitHub Issues](https://github.com/alay-maker/Predictive-Maintenance-MLOps/issues)
