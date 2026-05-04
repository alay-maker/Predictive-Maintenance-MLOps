# Predictive Maintenance MLOps

> **Real-time Industrial Equipment Telemetry Classification and Predictive Maintenance System**

A production-grade MLOps platform for ingesting, processing, and classifying real-time telemetry data from industrial machinery using Redis streams, machine learning models, and containerized microservices.

---

## 📋 Quick Navigation

- **[🚀 Quick Start](#quick-start)** - Get running in 5 minutes
- **[☁️ Azure Deployment](#azure-deployment)** - Production cloud setup
- **[📐 Architecture Diagrams](ARCHITECTURE.md)** - Visual system design

---

## 🎯 Overview

This project implements a **real-time predictive maintenance system** for industrial manufacturing equipment (CNC machines, mills, etc.). The system:

- **Ingests** high-frequency telemetry data from industrial sensors
- **Processes** streaming data using Redis as a distributed event broker
- **Classifies** equipment status using pre-trained machine learning models
- **Generates** real-time alerts when anomalies are detected
- **Scales** horizontally through containerized worker nodes

### Key Features

- ✅ Real-time data streaming with Redis streams
- ✅ Horizontally scalable worker architecture
- ✅ ML-powered anomaly detection
- ✅ Containerized with Docker & Docker Compose
- ✅ Infrastructure as Code (Terraform)
- ✅ Automated Azure deployment with GitHub Actions

---

## 📦 Prerequisites

### Local Development
- Python 3.11+ | Redis 7.0+ | Docker 1.29+

### Cloud Deployment
- Azure CLI | Terraform 1.0+ | SSH Key Pair | Active Azure Subscription

### System Requirements
- **Minimum**: 2 CPU cores, 4 GB RAM, 10 GB storage
- **Recommended**: 4+ CPU cores, 8+ GB RAM, 20 GB storage

---

## 🚀 Quick Start

### Option 1: Docker Compose (Development)

```bash
# Clone and setup
git clone https://github.com/alay-maker/Predictive-Maintenance-MLOps.git
cd Predictive-Maintenance-MLOps
git checkout main  # Use current branch

# Run the system
docker compose up -d --build

# Monitor logs
docker compose logs -f

# Scale workers
docker compose up -d --scale worker=3

# Cleanup
docker compose down -v
```

### Option 2: Local Python

```bash
# Install dependencies
pip install -r requirements.txt

# Start Redis (macOS: brew install redis && brew services start redis)
python src/setup_redis.py

# Terminal 1: Producer
python src/productor.py

# Terminal 2+: Workers
python src/worker.py worker_1
python src/worker.py worker_2

# Clean test data
python src/borrar_datos.py
```

---

## 📁 Project Structure

```
Predictive-Maintenance-MLOps/
├── src/                          # Application source code
│   ├── setup_redis.py           # Redis initialization & model loading
│   ├── productor.py             # Telemetry data generator
│   ├── worker.py                # Stream consumer & ML classifier
│   └── borrar_datos.py          # Cleanup utility
├── models/                      # Pre-trained ML models
├── terraform/                   # Azure infrastructure as code
├── tests/                       # Unit tests (pytest)
├── .github/workflows/           # GitHub Actions CI/CD
├── Dockerfile                   # Container definition
├── docker-compose.yml           # Multi-container orchestration
├── requirements.txt             # Python dependencies
├── ARCHITECTURE.md              # Detailed system design 📐
└── README.md                    # This file
```

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────┐
│          Predictive Maintenance System              │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────┐    ┌─────────────┐    ┌──────────┐  │
│  │Producer  │───▶│Redis Streams│◀───│ Workers  │  │
│  └──────────┘    └─────────────┘    └──────────┘  │
│       │                 │                   │      │
│  Telemetry        Message Queue      ML & Alerts  │
│   Data            Persistence                     │
│                                                     │
│      Configuration & Setup (setup_redis.py)        │
│   • Redis streams initialization                   │
│   • ML model loading                               │
│   • Alert threshold configuration                  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**[📐 See ARCHITECTURE.md for complete system design, data flows, and scaling strategies](#)**

---

## ☁️ Azure Deployment

### Two Deployment Options

#### Option A: Manual Deployment

Complete step-by-step guide:

1. **Infrastructure**: `terraform apply` creates VM & networking
2. **SSH Connection**: Connect securely to Azure VM
3. **Docker Setup**: Install Docker on the VM
4. **Code Deploy**: Clone repository
5. **System Launch**: Start microservices with Docker Compose
6. **Scaling**: Demonstrate worker scaling
7. **Monitoring**: View real-time logs & metrics
8. **Cleanup**: Destroy resources

See [Detailed Manual Deployment Guide](#manual-deployment-steps) below.

#### Option B: Automated Deployment (Recommended)

**Automatic deployment with GitHub Actions:**

```bash
# 1. Prepare Terraform and save outputs
cd terraform
terraform init
terraform plan -out=tfplan
terraform apply tfplan

# Terraform outputs:
# - AZURE_VM_IP (public IP)
# - SSH_KEY (private key path)
```

```bash
# 2. Add GitHub Secrets (one-time setup)
# Go to: Settings → Secrets and variables → Actions → New repository secret

# Add these secrets:
# AZURE_VM_IP = "20.XX.XXX.XX"  (from terraform output)
# SSH_PRIVATE_KEY = (content of ~/.ssh/id_rsa)
# AZURE_SUBSCRIPTION_ID = (your Azure subscription ID)
```

```bash
# 3. Trigger automatic deployment
git add .
git commit -m "deploy: trigger automated Azure deployment"
git push origin main

# GitHub Actions automatically:
# ✅ Connects to Azure VM via SSH
# ✅ Installs Docker
# ✅ Clones this repository
# ✅ Starts Docker Compose
# ✅ Scales workers
# ✅ Validates system is running
```

**Check deployment status:** Actions tab in GitHub

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

### Data Streams

**telemetria stream** (telemetry - 1 week TTL):
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
  "message": "Equipment vibration above threshold"
}
```

---

## 📈 Monitoring & Troubleshooting

### View Logs

```bash
docker compose logs -f              # All services
docker compose logs -f productor    # Specific service
docker stats                        # Resource usage
```

### Redis Monitoring

```bash
docker exec -it redis-server redis-cli

# Inside redis-cli:
XLEN telemetria                  # Telemetry count
XLEN alertas                     # Alert count
XINFO STREAM telemetria          # Stream info
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Redis connection refused | `docker compose restart redis-db` |
| Consumer group missing | `docker compose restart setup-redis` |
| Worker crashes | `docker compose up -d --build` |
| No data flowing | `docker compose logs productor` |

---

## 🛠️ Development

### Setup

```bash
python -m venv venv
source venv/bin/activate           # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy
```

### Testing

```bash
pytest                             # Run all tests
pytest --cov=src tests/            # With coverage
pytest -v tests/test_worker.py     # Specific file
```

### Code Quality

```bash
black src/ tests/                  # Format code
flake8 src/ tests/                 # Style check
mypy src/                          # Type checking
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/name`
3. Make changes and test locally
4. Commit: `git commit -m "feat: description"`
5. Push: `git push origin feature/name`
6. Create Pull Request

---

---

# Manual Deployment Steps

Complete guide for step-by-step Azure deployment.

## 1️⃣ Provision Infrastructure with Terraform

```bash
cd terraform
terraform init
terraform plan -out=tfplan
terraform apply tfplan

# Save outputs:
AZURE_VM_IP=$(terraform output -raw vm_public_ip)
echo "VM IP: $AZURE_VM_IP"
```

## 2️⃣ Connect to Azure VM

```bash
ssh -i ~/.ssh/id_rsa adminuser@$AZURE_VM_IP
```

## 3️⃣ Install Docker

```bash
sudo apt-get update && sudo apt-get upgrade -y
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $(whoami)
newgrp docker
docker --version
```

## 4️⃣ Deploy Application

```bash
git clone https://github.com/alay-maker/Predictive-Maintenance-MLOps.git
cd Predictive-Maintenance-MLOps
git checkout main
docker compose up -d --build
```

## 5️⃣ Scale Workers

```bash
docker compose up -d --scale worker=3
```

## 6️⃣ Monitor System

```bash
docker compose logs -f
```

## 7️⃣ Cleanup

```bash
docker compose down -v
cd terraform
terraform destroy
```

---

## 📚 Additional Resources

- [Full Architecture Design](ARCHITECTURE.md)
- [Redis Streams Documentation](https://redis.io/docs/data-types/streams/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Terraform Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 👥 Authors

- **alay-maker** - [GitHub Profile](https://github.com/alay-maker)
- **Colaborador** - [GitHub Profile](https://github.com/colaborador)

**Last Updated**: May 4, 2026 | **Status**: Active Development
