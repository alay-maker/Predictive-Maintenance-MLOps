# 🔧 Predictive Maintenance MLOps

> **Real-time Industrial Equipment Telemetry Classification and Predictive Maintenance System**

A production-grade MLOps platform for ingesting, processing, and classifying real-time telemetry data from industrial machinery using Redis streams, machine learning models, and containerized microservices.

![CI/CD](https://github.com/alay-maker/Predictive-Maintenance-MLOps/actions/workflows/azure-deploy.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 📋 Quick Navigation

- [🚀 Quick Start](#-quick-start) - Get running locally in 5 minutes
- [☁️ Cloud Deployment Pipeline](#️-cloud-deployment-pipeline-azure-cicd) - Automated Azure CI/CD Workflow
- [📐 Architecture](#️-system-architecture) - Visual system design

---

## 🎯 Overview

This project implements a real-time predictive maintenance system for industrial manufacturing equipment (CNC machines, mills, etc.). The system:

- Ingests high-frequency telemetry data from industrial sensors
- Processes streaming data using Redis as a distributed event broker
- Classifies equipment status using pre-trained machine learning models
- Generates real-time alerts when anomalies are detected
- Scales horizontally through containerized worker nodes

### Key Features

- ✅ Real-time data streaming with Redis streams
- ✅ Horizontally scalable worker architecture with true zero-downtime updates
- ✅ ML-powered anomaly detection (decision tree via Redis)
- ✅ Containerized with Docker & Docker Compose
- ✅ Infrastructure as Code (Terraform)
- ✅ Automated Azure deployment with GitHub Actions CI/CD

---

## 📦 Prerequisites

### Local Development

| Tool | Version |
|------|---------|
| Python | 3.11+ |
| Redis | 7.0+ |
| Docker Compose | v2+ |

### Cloud Deployment

- Development environment (Codespace or local) with **Azure CLI** and **Terraform** installed
- SSH Key Pair generated
- **GitHub Secrets** configured: SSH keys and Azure credentials must be added to your repository's Secrets

---

## ☁️ Cloud Deployment Pipeline (Azure CI/CD)

The system is designed for a **100% automated MLOps deployment**. Below are the steps to provision the infrastructure, deploy the code, and test the CI/CD pipeline in a production Azure environment.

### 1. Infrastructure Provisioning (Terraform)

First, generate the network and the Ubuntu virtual machine in Azure.

```bash
cd terraform
terraform init
terraform plan
terraform apply -auto-approve
```

> **Note:** Upon completion, Terraform will output the VM's public IP. This IP must be saved in your GitHub Secrets so the CI/CD pipeline can connect.

### 2. Initial Deployment (GitHub Actions)

Once the machine is created, force the pipeline execution to install Docker and spin up the microservices:

```bash
git add .
git commit -m "deploy: aprovisionamiento inicial"
git push origin main
```

The GitHub workflow will execute coverage tests (`pytest`) and perform the automated deployment via SSH.

### 3. Worker Monitoring

To verify that the data flow is correct, access the Azure machine via SSH to read the logs in real-time:

```bash
ssh adminuser@<IP_DE_AZURE>
cd predictive-maintenance
sudo docker compose ps
sudo docker compose logs -f worker
```

### 4. Model Update (Zero-Downtime)

The system supports updating the ML model without interrupting active workers. The pipeline uses an atomic file swap + `--no-recreate` strategy so running workers are never stopped.

1. Modify a threshold in the `models/tree_model.json` file
2. Push the changes to the repository:

```bash
git add models/tree_model.json
git commit -m "mlops: actualizacion de umbrales del modelo"
git push origin main
```

> Workers kept open from Step 3 will continue processing messages uninterrupted and automatically pick up the new model once `setup-redis` finishes reloading.

> **Note on scaling:** The pipeline deploys with a fixed `--scale` value. If you manually scaled workers on the VM (e.g. to 5), set the `--scale` in the workflow to match or remove it to avoid workers being terminated to meet the target count.

### 5. Environment Cleanup

To clean up the cloud environment (delete containers and destroy Azure resources to avoid costs):

```bash
# On the SSH server:
sudo docker compose down -v
exit

# On your local terminal (terraform folder):
terraform destroy -auto-approve
```

---

## 🚀 Quick Start (Local Development)

### Option 1: Docker Compose

```bash
# Clone and setup
git clone https://github.com/alay-maker/Predictive-Maintenance-MLOps.git
cd Predictive-Maintenance-MLOps

# Run the system
docker compose up -d --build

# Monitor logs
docker compose logs -f

# Scale workers
docker compose up -d --scale worker=3

# Cleanup
docker compose down -v
```

### Option 2: Local Python Environment

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
```

---

## 📁 Project Structure

Predictive-Maintenance-MLOps/
├── src/ # Application source code
│ ├── setup_redis.py # Redis initialization & model loading
│ ├── productor.py # Telemetry data generator
│ └── worker.py # Stream consumer & ML classifier
├── models/ # Pre-trained ML models (tree_model.json)
├── data/ # Dataset files
├── notebooks/ # Jupyter notebooks (EDA & model training)
├── docs/ # Additional documentation
├── terraform/ # Azure infrastructure as code
├── tests/ # Unit tests (pytest)
├── .github/workflows/ # GitHub Actions CI/CD
├── Dockerfile # Container definition
├── docker-compose.yml # Multi-container orchestration
├── setup_env.sh # Environment setup helper
├── apagar_azure.sh # Azure teardown helper script
├── presentacion.html # Project presentation slides
├── ARCHITECTURE.md # Detailed system design 📐
└── README.md # This file

text

---

## 🏗️ System Architecture

┌─────────────────────────────────────────────────────┐
│ Predictive Maintenance System                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│ ┌──────────┐     ┌─────────────┐    ┌──────────┐    │
│ │Producer  │───▶│Redis Streams│◀───│ Workers  │    │
│ └──────────┘     └─────────────┘    └──────────┘    │
│       │                 │                 │         │
│ Telemetry Message Queue ML & Alerts                 │
│ Data Persistence                                    │
│                                                     │
│ Configuration & Setup (setup_redis.py)              │
│ - Redis streams initialization                      │
│ - ML model loading (atomic pipeline)                │
│ - Alert threshold configuration                     │
│                                                     │
└─────────────────────────────────────────────────────┘

text

📐 [See ARCHITECTURE.md for complete system design, data flows, and scaling strategies](ARCHITECTURE.md)

---

## 📊 Configuration

### Environment Variables

```env
# Redis
REDIS_HOST=redis-db              # Redis server hostname
REDIS_PORT=6379                  # Redis port
REDIS_DB=0                       # Database number

# Application
PYTHONUNBUFFERED=1               # Real-time logging
PYTHONPATH=/app                  # Module path

# Worker (optional overrides)
STREAM_NAME=input_stream         # Input stream name
GROUP_NAME=equipo_triaje         # Consumer group name
ALERT_STREAM=registro_alertas    # Alerts output stream
```

### Data Streams

**`input_stream`** — telemetry input from sensors:

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

**`registro_alertas`** — anomaly alerts (Redis list):

```json
{
  "timestamp": "2026-05-04 10:30:46",
  "id_mensaje_origen": "1714819846001-0",
  "datos_sensor": { "temperatura": "75.5", "vibracion": "2.3" }
}
```

---

## 📈 Monitoring & Troubleshooting

### View Logs

```bash
docker compose logs -f              # All services
docker compose logs -f worker       # Workers only
docker stats                        # Resource usage
```

### Redis Monitoring

```bash
docker exec -it redis-server redis-cli

# Inside redis-cli:
XLEN input_stream                # Pending telemetry messages
LLEN registro_alertas            # Total alerts generated
XINFO STREAM input_stream        # Stream metadata
XINFO GROUPS input_stream        # Consumer group status
```

---

## 🛠️ Development

### Testing

```bash
pytest                             # Run all tests
pytest --cov=src tests/            # With coverage report
pytest --cov=src --cov-fail-under=70 tests/   # Enforce 70% minimum
```

### Code Quality

```bash
black src/ tests/                  # Format code
flake8 src/ tests/                 # Style check
mypy src/                          # Type checking
```

---

## 📚 Additional Resources

- [Full Architecture Design](ARCHITECTURE.md)
- [Redis Streams Documentation](https://redis.io/docs/data-types/streams/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Terraform Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)

---

## 📄 License

MIT License — See [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **alay-maker** — [GitHub Profile](https://github.com/alay-maker)
- **ExcellentApproximation** — [GitHub Profile](https://github.com/ExcellentApproximation)

![Status](https://img.shields.io/badge/status-active%20development-brightgreen)
