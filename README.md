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
┌───────────────────────────────────────────────────────────────────────┐
│                     Predictive Maintenance System                     │
├───────────────────────────────────────────────────────────────────────┤
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
│     └───────────────────────────────────────────────────────────┘     │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
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
