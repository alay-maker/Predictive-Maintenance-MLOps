# 🏗️ Predictive Maintenance MLOps - Architecture Guide

## System Architecture Overview

### 1. Core System Design (Local/Docker Deployment)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     Predictive Maintenance System                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐   │
│   │   PRODUCTOR      │───▶│  REDIS STREAMS   │◀───│     WORKERS      │   │
│   │  (Data Source)   │    │  (Message Broker)│    │  (Classifiers)   │   │
│   └──────────────────┘    └──────────────────┘    └──────────────────┘   │
│        ▲                           ▲                        ▲              │
│        │                           │                        │              │
│   • CNC Machine           • Streams: telemetria      • ML Classification  │
│   • Temperature Sensor    • Streams: alertas         • Anomaly Detection  │
│   • Vibration Sensor      • Consumer Groups          • Alert Generation   │
│   • Pressure Gauge        • Data Persistence         • Horizontal Scale   │
│   • RPM Sensor            • Real-time Distribution   • Load Balancing     │
│                                                                            │
│   ┌──────────────────────────────────────────────────────────────────┐   │
│   │        INITIALIZATION LAYER (setup_redis.py)                    │   │
│   │                                                                  │   │
│   │  ✓ Redis streams creation     ✓ ML model loading               │   │
│   │  ✓ Consumer groups setup      ✓ Alert thresholds               │   │
│   │  ✓ Configuration loading      ✓ System validation               │   │
│   └──────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 2. Data Flow Lifecycle

```
SENSOR DATA INGESTION
        │
        ▼
    ┌────────────────────────────────┐
    │  PRODUCTOR                     │
    │  (Data Generator)              │
    │                                │
    │  • Reads from sensors/APIs     │
    │  • Generates synthetic data    │
    │  • Formats telemetry packets   │
    └────────┬───────────────────────┘
             │
             ▼ (XADD to stream)
    ┌────────────────────────────────┐
    │  REDIS TELEMETRIA STREAM       │
    │  (Persistent Message Queue)    │
    │                                │
    │  Entry: {                      │
    │    timestamp: "2026-05-04...", │
    │    equipment_id: "fresadora-1",│
    │    temperatura: 75.5,          │
    │    vibracion: 2.3,             │
    │    presion: 120.5,             │
    │    rpm: 1200                   │
    │  }                             │
    └────────┬───────────────────────┘
             │
             ▼ (XREAD from consumer group)
    ┌────────────────────────────────┐
    │  WORKER PROCESS                │
    │  (Classification & Anomaly     │
    │   Detection)                   │
    │                                │
    │  • Load telemetry data         │
    │  • Apply ML model              │
    │  • Calculate anomaly score     │
    │  • Threshold comparison        │
    └────────┬───────────────────────┘
             │
             ├──── Normal ────────────┐
             │                        │
             └──── Anomaly ──┐        │
                             ▼        │
                    ┌──────────────────────────────┐
                    │  REDIS ALERTAS STREAM        │
                    │  (Alert Queue)               │
                    │                              │
                    │  Entry: {                    │
                    │    timestamp: "...",         │
                    │    equipment_id: "...",      │
                    │    alert_type: "CRITICAL",   │
                    │    severity: 0.95,           │
                    │    message: "...",           │
                    │    action: "..."             │
                    │  }                           │
                    └──────────────────────────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  ALERT HANDLER   │
                    │  (Log/Notify)    │
                    └──────────────────┘
```

---

### 3. Horizontal Scaling Architecture

```
                    ┌─────────────────────────────────┐
                    │    REDIS BROKER                 │
                    │  (telemetria stream)            │
                    │  (alertas stream)               │
                    │  (Consumer Group: workers)      │
                    └──────────────┬──────────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
        ┌───────────▼────────────┐  ┌───────────▼────────────┐
        │  WORKER_1              │  │  WORKER_2              │
        │                        │  │                        │
        │  Process entries:      │  │  Process entries:      │
        │  • 1-0 to 50-0         │  │  • 51-0 to 100-0       │
        │                        │  │                        │
        │  [ACTIVE]              │  │  [ACTIVE]              │
        └────────────────────────┘  └────────────────────────┘
                    │
        ┌───────────▼────────────┐  ┌───────────────────────┐
        │  WORKER_3              │  │  WORKER_N             │
        │                        │  │                        │
        │  Process entries:      │  │  Process entries:      │
        │  • 101-0 to 150-0      │  │  • Pending queue      │
        │                        │  │                        │
        │  [ACTIVE]              │  │  [READY TO SCALE]      │
        └────────────────────────┘  └───────────────────────┘

CONSUMER GROUP COORDINATION:
✓ Each worker claims pending entries
✓ Automatic load distribution
✓ Acknowledgment (XACK) on completion
✓ Failed entries go to pending entry list (PEL)
```

---

### 4. Technology Stack Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                               │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Python 3.11+                                               │  │
│  │  • productor.py - Data generation                           │  │
│  │  • worker.py - ML inference                                 │  │
│  │  • setup_redis.py - System initialization                   │  │
│  └──────────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────────┤
│                    ML/DATA LAYER                                    │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  scikit-learn (Classification Models)                        │  │
│  │  Pandas (Data Processing)                                    │  │
│  │  NumPy (Numerical Computing)                                 │  │
│  └──────────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────────┤
│                 MESSAGE BROKER & STORAGE                            │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Redis 7.0+                                                  │  │
│  │  • Streams API (telemetria, alertas)                         │  │
│  │  • Consumer Groups (workers)                                 │  │
│  │  • Persistent Storage (AOF/RDB)                              │  │
│  └──────────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────────┤
│              CONTAINERIZATION & ORCHESTRATION                        │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Docker Engine                                               │  │
│  │  Docker Compose (Local) / Kubernetes (Enterprise)            │  │
│  └──────────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────────┤
│           INFRASTRUCTURE & CLOUD PROVISIONING                        │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Terraform + Azure Resource Manager                          │  │
│  │  • VM provisioning                                           │  │
│  │  • Network configuration                                     │  │
│  │  • Storage setup                                             │  │
│  │  • Security groups & access control                          │  │
│  └──────────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────────┤
│                    MONITORING & LOGGING                             │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Docker logs / Azure Monitor                                 │  │
│  │  Redis CLI (redis-cli) for debugging                         │  │
│  │  pytest for testing                                          │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

---

### 5. Azure Cloud Deployment Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                     AZURE SUBSCRIPTION                              │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  RESOURCE GROUP: predictive-maintenance-rg                    │ │
│  │                                                                │ │
│  │  ┌─────────────────────────────────────────────────────────┐  │ │
│  │  │  VIRTUAL MACHINE (Standard_D2s_v3)                      │  │ │
│  │  │                                                         │  │ │
│  │  │  ┌──────────────────────────────────────────────────┐   │  │ │
│  │  │  │  Ubuntu 20.04 LTS                               │   │  │ │
│  │  │  │                                                  │   │  │ │
│  │  │  │  ┌───────────────────────────────────────────┐  │   │  │ │
│  │  │  │  │  Docker Engine (ce)                       │  │   │  │ │
│  │  │  │  │                                            │  │   │  │ │
│  │  │  │  │  ┌──────────┐ ┌──────────┐ ┌──────────┐  │   │  │ │
│  │  │  │  │  │ Redis    │ │Productor │ │ Worker 1 │  │   │  │ │
│  │  │  │  │  │ :6379    │ │          │ │          │  │   │  │ │
│  │  │  │  │  └──────────┘ └──────────┘ └──────────┘  │   │  │ │
│  │  │  │  │                                            │   │  │ │
│  │  │  │  │  ┌──────────┐ ┌──────────┐               │   │  │ │
│  │  │  │  │  │ Worker 2 │ │ Worker N │               │   │  │ │
│  │  │  │  │  │          │ │          │ (Scalable)    │   │  │ │
│  │  │  │  │  └──────────┘ └──────────┘               │   │  │ │
│  │  │  │  └───────────────────────────────────────────┘   │   │  │ │
│  │  │  └──────────────────────────────────────────────────┘   │  │ │
│  │  │                                                         │  │ │
│  │  │  SSH Access: adminuser@<public-ip> (Port 22)           │  │ │
│  │  └─────────────────────────────────────────────────────────┘  │ │
│  │                                                                │ │
│  │  ┌─────────────────────────────────────────────────────────┐  │ │
│  │  │  NETWORK INTERFACE (vNIC)                              │  │ │
│  │  │  • Private IP: 10.0.1.4                                │  │ │
│  │  │  • Public IP: 20.XX.XXX.XX                             │  │ │
│  │  │  • NSG Rules: SSH(22), Redis(6379)                     │  │ │
│  │  └─────────────────────────────────────────────────────────┘  │ │
│  │                                                                │ │
│  │  ┌─────────────────────────────────────────────────────────┐  │ │
│  │  │  STORAGE (Managed Disk)                                │  │ │
│  │  │  • OS Disk: 30 GB (Standard SSD)                        │  │ │
│  │  │  • Data Disk: 50 GB (for Redis persistence)            │  │ │
│  │  └─────────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

### 6. Data Flow with Redis Streams

```
TELEMETRY STREAM EXAMPLE (telemetria)
───────────────────────────────────────

Time: 10:30:45.123
Entry ID: 1234567890-0
┌─────────────────────────────────────────────┐
│ timestamp: 2026-05-04T10:30:45.123Z         │
│ equipment_id: fresadora-1                   │
│ temperatura: 75.5 °C                        │
│ vibracion: 2.3 mm/s                         │
│ presion: 120.5 bar                          │
│ rpm: 1200                                   │
└─────────────────────────────────────────────┘
           │
           ▼ (Processed by Worker)
┌─────────────────────────────────────────────┐
│ ML Model Inference                          │
│ • Extract features                          │
│ • Normalize values                          │
│ • Apply decision tree                       │
│ • Calculate anomaly score: 0.85             │
│ • Compare with threshold (0.7)              │
└─────────────────────────────────────────────┘
           │
           ▼ (Score > Threshold)
ALERTS STREAM (alertas)
───────────────────────────────────────────────

Time: 10:30:46.001
Entry ID: 1234567891-0
┌─────────────────────────────────────────────┐
│ timestamp: 2026-05-04T10:30:46.001Z         │
│ equipment_id: fresadora-1                   │
│ alert_type: ANOMALY                         │
│ severity: 0.85                              │
│ message: "Vibration above threshold"        │
│ recommended_action: "Inspect bearings"      │
│ source_entry: 1234567890-0                  │
└─────────────────────────────────────────────┘
```

---

### 7. Consumer Group & Load Distribution

```
REDIS CONSUMER GROUP: "workers"
Stream: telemetria

Initial State (1 Worker):
┌──────────────────────────────┐
│  Worker Group: "workers"     │
│  ├─ Consumer: worker_1       │
│  │  └─ Pending Entries: 0    │
│  └─ Stream Length: 500       │
└──────────────────────────────┘
         all 500 entries
         processed by 1

After Scaling (3 Workers):
┌──────────────────────────────┐
│  Worker Group: "workers"     │
│  ├─ Consumer: worker_1       │
│  │  └─ Pending Entries: 170  │
│  ├─ Consumer: worker_2       │
│  │  └─ Pending Entries: 165  │
│  ├─ Consumer: worker_3       │
│  │  └─ Pending Entries: 165  │
│  └─ Stream Length: 500       │
└──────────────────────────────┘
      LOAD BALANCED
      ~167 each worker

Operations:
1. XGROUP CREATE telemetria workers $       (Create consumer group)
2. XREAD GROUP workers worker_1 COUNT 50   (Worker claims 50 entries)
3. XACK telemetria workers <id>            (Acknowledge after processing)
4. docker compose up -d --scale worker=3   (Add workers automatically)
```

---

## Key Architectural Features

### ✨ Real-Time Processing
- **Stream-based**: Redis streams provide ordered, persistent message queue
- **Low latency**: Sub-second processing with consumer groups
- **Fault tolerance**: Pending entry list (PEL) for failed messages

### 📈 Horizontal Scalability
- **Consumer groups**: Multiple workers share load automatically
- **No coordination**: Workers process independently
- **Dynamic scaling**: Add/remove workers without system restart

### 🔄 Data Persistence
- **Redis AOF/RDB**: Durable storage of telemetry and alerts
- **Stream TTL**: Configurable retention (1 week for telemetria, 30 days for alertas)
- **Volume mounting**: Docker volumes preserve data across restarts

### 🛡️ Reliability
- **Automatic retry**: Failed messages remain in PEL
- **Idempotent processing**: Workers handle duplicate messages safely
- **Consumer group tracking**: Knows which messages were processed

### 🚀 Production Ready
- **Containerized**: Consistent environments dev→test→prod
- **IaC**: Terraform for reproducible Azure deployments
- **Monitoring**: Comprehensive logging and Redis CLI debugging

---

## Performance Characteristics

| Metric | Value | Notes |
|--------|-------|-------|
| **Throughput** | ~1,000 msgs/sec | Per worker, adjustable |
| **Latency** | <100ms | End-to-end ingestion to alert |
| **Scalability** | Horizontal | Add workers linearly |
| **Storage** | 1-2 GB/day | Depends on sensor frequency |
| **Memory** | ~200 MB | Per worker container |

---

## For More Information

- **Quick Start**: See [README.md Quick Start section](#quick-start)
- **Deployment**: See [Azure End-to-End Deployment section](#azure-end-to-end-deployment)
- **Configuration**: See [Configuration section](#configuration)
- **Troubleshooting**: See [Monitoring & Troubleshooting section](#monitoring--troubleshooting)
