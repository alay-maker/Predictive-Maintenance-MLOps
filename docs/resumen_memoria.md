## 1. Resumen Ejecutivo

Una planta de mecanizado industrial sufre paradas no planificadas debido a fallos mecánicos en sus fresadoras CNC. El equipo de mantenimiento actúa de forma reactiva tras la avería, lo que resulta en tiempos de inactividad prolongados y altos costes de reparación.

**El problema:** No existe un sistema automatizado capaz de procesar la telemetría (vibración, temperatura, revoluciones) en tiempo real para predecir cuándo una máquina está a punto de fallar, impidiendo realizar un mantenimiento proactivo.

**Nuestra solución:** Un pipeline MLOps completo y una arquitectura de microservicios que:
1. Simula y procesa telemetría en tiempo real mediante un Productor IoT.
2. Inyecta reglas de inferencia de un modelo de Machine Learning directamente en una base de datos en memoria (Redis).
3. Evalúa los datos a través de *workers* escalables horizontalmente.
4. Permite actualizaciones del modelo en **Zero-Downtime real** mediante CI/CD automatizado en Microsoft Azure: los *workers* continúan procesando telemetría sin interrupción durante el despliegue.

**Resultado obtenido:**
- Arquitectura desacoplada capaz de procesar telemetría cada 0.5 segundos.
- Pipeline CI/CD completamente automatizado en GitHub Actions con cobertura exigida del 70%.
- Infraestructura desplegada en Azure mediante código (Terraform).
- Actualización de modelos con **Zero-Downtime verificado**: workers activos no se interrumpen durante el despliegue.

---

## 2. Descripción del Problema y Caso de Negocio

### 2.1 Contexto

El sistema monitoriza una fresadora industrial. Los sensores recogen métricas críticas continuamente. Un modelo de Machine Learning (Árbol de Decisión) ha sido previamente entrenado para identificar patrones anómalos que preceden a un fallo catastrófico de la herramienta o del motor.

### 2.2 Valor de negocio

En el sector del mecanizado de precisión, una parada no planificada de una máquina CNC cuesta aproximadamente 5.000€ por hora (sumando lucro cesante, horas extra y piezas defectuosas).
- **Coste de fallo reactivo:** Una rotura de husillo suele implicar 8 horas de parada = ~40.000€.
- **Mantenimiento predictivo:** Detectar la anomalía permite programar el cambio de pieza en un turno inactivo, reduciendo el tiempo de intervención a 1 hora = ~5.000€.
- **Ahorro potencial:** ~35.000€ por incidente evitado.

### 2.3 Métricas de éxito

En este contexto industrial, se prioriza el **Recall (Sensibilidad)** sobre la Precision. Es preferible que el sistema lance una falsa alarma (y un técnico revise la máquina en 5 minutos) a que el sistema omita una advertencia y la máquina sufra una avería de 40.000€. A nivel de infraestructura, la métrica de éxito es la **Latencia y Continuidad**: el sistema no debe perder paquetes de telemetría durante las actualizaciones del modelo.

---

## 3. Arquitectura de la Solución

### 3.1 Diagrama de arquitectura

```text
DESARROLLADOR
      │  git push
      ▼
GITHUB REPOSITORY
      │
      ├── CI Pipeline ──────────────────► Tests (pytest)
      │                                   Cobertura ≥ 70%
      │
      └── CD Pipeline (Si CI = OK)──────► SSH a Máquina Virtual en Azure
                                          Copia atómica de archivos (rsync)
                                          docker compose build (sin detener workers)
                                          docker compose up --no-recreate
                                          docker compose restart setup-redis

MICROSOFT AZURE (Máquina Virtual Ubuntu)
      │
      ├── Red: predictive-net (Bridge)
      │
      ├── redis-db (Contenedor) ◄──────── setup-redis (Contenedor efímero)
      │   (Base de datos + persistencia)  (Inyecta modelo tree_model.json en BD)
      │
      ├── productor (Contenedor) ───────► (Envía telemetría a Redis cada 0.5s)
      │
      └── worker [Escalable] (Contenedores) ← Sin interrupción durante despliegue
          (Lee telemetría, consulta modelo en Redis, emite alerta)
```

### 3.2 Justificación de tecnologías

| Componente | Tecnología | Por qué esta y no otra |
|------------|-----------|------------------------|
| Lenguaje | Python 3.11 | Estándar en ciencia de datos; librerías nativas robustas. |
| Inferencia | Redis (Hashes) | Inferir directamente en base de datos en memoria es más rápido que cargar modelos pesados en cada *worker*. Permite actualizar el modelo sin recompilar imágenes. |
| Contenedores | Docker Compose V2 | Orquestación suficiente y ligera para este caso de uso, sin la sobrecarga operativa de Kubernetes. |
| CI/CD | GitHub Actions | Integración nativa con el código y aprovisionamiento automático de runners Ubuntu. |
| Cloud | Microsoft Azure | Requisito del proyecto; máquinas virtuales altamente disponibles y seguras. |
| IaC | Terraform | Permite versionar la creación de la máquina virtual; evita configuraciones manuales propensas a error. |

**¿Por qué inferencia en Redis y no en el Worker?**
Si el *worker* tuviera el modelo embebido en su código, actualizar el modelo implicaría reconstruir la imagen del *worker* y reiniciar todos los nodos, deteniendo la planta. Al guardar el modelo como reglas en Redis, logramos una arquitectura desacoplada donde el modelo se actualiza inyectando datos nuevos, sin tocar el código ejecutable de los *workers*.

---

## 4. Implementación del Pipeline

### 4.1 Pipeline de Datos e Inferencia

El flujo de trabajo se divide en dos ciclos de vida independientes:
1. **El modelo de Machine Learning:** Se exporta a un formato ligero (`tree_model.json`). El contenedor efímero `setup-redis` lee este archivo e inyecta los umbrales y nodos como *Hashes* en Redis usando un pipeline atómico.
2. **El flujo de telemetría:** El `productor` simula sensores. El `worker` lee estos datos, cruza los valores con los nodos almacenados en Redis y determina si se dispara una alerta. Si un nodo no se encuentra durante la actualización, el mensaje no se marca como procesado (`xack`) y permanece disponible para reintento — garantizando que no se pierde ningún dato.

### 4.2 Gate de Calidad (Quality Gate)

El pipeline de GitHub Actions incluye un *Job* de testeo estricto con 8 tests unitarios. Si los tests no superan el 70% de cobertura, el *Job* finaliza con error y bloquea inmediatamente el paso de despliegue en Azure (`needs: test`). Esto garantiza que nunca se despliega código no validado en el entorno de producción.

---

## 5. CI/CD y Automatización

### 5.1 Pipeline Integrado (`azure-deploy.yml`)

| Fase | Acción | Qué valida |
|---------|---------|-------------|
| CI (Tests) | `pytest tests/ --cov=src --cov-fail-under=70` | Verifica la lógica del productor, workers y configuración. Exige ≥ 70% de cobertura. |
| Transferencia | `appleboy/scp-action` → directorio temporal | Copia los archivos esenciales a un directorio temporal para evitar lecturas en caliente. |
| Swap atómico | `rsync -a tmp/ → producción/` | Reemplaza los archivos de forma atómica una vez la copia está completa. |
| CD (Deploy) | `appleboy/ssh-action` | Construye la nueva imagen, levanta servicios faltantes sin recrear los activos, recarga solo `setup-redis`. |
| Verificación | `docker compose wait setup-redis` | Confirma que el nuevo modelo se cargó correctamente antes de dar el despliegue por exitoso. |

### 5.2 Estrategia Zero-Downtime

El despliegue utiliza tres mecanismos combinados para garantizar que los *workers* activos nunca se interrumpen:

1. **`--no-recreate`:** Docker Compose no toca los contenedores que ya están corriendo, aunque la imagen haya cambiado.
2. **Separación de build y deploy:** `docker compose build` construye la nueva imagen sin afectar los contenedores en marcha. Solo los servicios nuevos o los reiniciados explícitamente usarán la imagen actualizada.
3. **Reinicio selectivo:** Solo `setup-redis` se reinicia para recargar el modelo. El productor y los workers continúan sin interrupción.

> **Nota sobre escalado:** El número de workers activos en producción se gestiona manualmente en la VM (`docker compose up -d --scale worker=N`). El pipeline de CI/CD no especifica un `--scale` fijo para no destruir workers adicionales que puedan estar corriendo.

---

## 6. Infraestructura como Código

### 6.1 Recursos desplegados con Terraform

La infraestructura base en la nube ha sido definida utilizando Terraform. El archivo `main.tf` se encarga de aprovisionar:
- Grupo de Recursos en Azure.
- Red Virtual y Subred.
- Máquina Virtual Linux (Ubuntu) con IP Pública.
- Reglas de Seguridad (NSG) habilitando los puertos SSH (22) y servicios necesarios.

### 6.2 Coste estimado (Entorno Base)

| Recurso (Azure) | Uso estimado | Coste mensual aprox. |
|---------|-------------|--------------|
| B1s / B2s Virtual Machine | 730h/mes (24/7) | ~10.00€ - 20.00€ |
| Dirección IP Pública | Estática | ~3.00€ |
| Disco OS (SSD Premium 30GB) | Almacenamiento base | ~4.50€ |
| **Total** | | **~17.50€ - 27.50€/mes** |

---

## 7. Escalabilidad y Tolerancia a Fallos

### 7.1 Escalabilidad Horizontal
La arquitectura fue refactorizada eliminando el parámetro estático `container_name` de los *workers* en el `docker-compose.yml`. Esto permite adaptar la capacidad de cómputo en tiempo real según el volumen de telemetría:
```bash
sudo docker compose up -d --scale worker=5
```

### 7.2 Resiliencia del Worker
Los *workers* incluyen protección ante fallos transitorios durante la actualización del modelo:
- Si `hgetall` devuelve un nodo vacío (Redis en proceso de actualización), el mensaje **no se marca como procesado** y queda disponible para otro worker — evitando pérdida de datos.
- Los errores de procesamiento por mensaje están aislados mediante `try/except` individual: un fallo en un mensaje no detiene el worker.
- Los nombres de streams y grupos de consumidores son configurables vía variables de entorno (`STREAM_NAME`, `GROUP_NAME`, `ALERT_STREAM`).

### 7.3 Persistencia
El servicio `redis-db` incluye un mapeo de volúmenes (`redis_data:/data`). Si el contenedor de la base de datos se reinicia o sufre un crasheo, el modelo y el historial de telemetría no se pierden.

---

## 8. Metodología Ágil Aplicada

### 8.1 Framework SCRUM y GitHub Projects

El proyecto se gestionó en base a 3 Sprints. Se empleó un tablero Kanban en GitHub Projects para seguir el flujo de las Historias de Usuario (US), priorizadas en P0 (Críticas) y P1/P2.

### 8.2 Evolución técnica: Del "Despliegue con Reinicio" al "Zero-Downtime Real"

> "La teoría de microservicios promete Zero-Downtime, pero la orquestación en la práctica tiene sus propias reglas."

Durante el Sprint 3, identificamos que al subir un nuevo modelo, Docker destruía todos los *workers* (`exited with code 137`), provocando pérdida temporal de datos IoT.

**El problema original:** Los *workers* tenían `depends_on: setup-redis`. Al actualizar el modelo, Docker recreaba `setup-redis` y, por efecto dominó, reiniciaba todos los *workers*. Además, el flag `--build` en el comando de deploy forzaba la recreación de todos los contenedores al detectar un cambio de imagen.

**La solución implementada** combinó varios cambios coordinados:
- Los *workers* se desvincularon de `setup-redis` y dependen únicamente de `redis-db`.
- Se separó `docker compose build` de `docker compose up --no-recreate`, impidiendo que Docker toque contenedores activos aunque la imagen cambie.
- Se implementó copia atómica de archivos vía directorio temporal + `rsync`, evitando que los *workers* lean archivos a mitad de escritura.
- Se añadió lógica de `procesado = False` en el worker para no hacer `xack` si el modelo estaba en transición, garantizando que ningún mensaje se pierde.

**Resultado verificado:** Workers en marcha procesando telemetría de forma continua durante un despliegue completo en Azure, sin ninguna línea de reinicio en los logs.

---

## 9. Conclusiones y Trabajo Futuro

### 9.1 Conclusiones

1. **Zero-Downtime real con Docker Compose:** Mediante la combinación de `--no-recreate`, separación del ciclo de build/deploy, swap atómico de archivos y lógica de resiliencia en el worker, se logró un despliegue continuo sin interrupción del servicio, sin necesidad de orquestadores complejos como Kubernetes.
2. **IaC y CI/CD son innegociables:** El uso de Terraform y GitHub Actions elimina el error humano en los despliegues, garantizando que el entorno de desarrollo sea idéntico al de producción.
3. **Mantenimiento Predictivo Real:** Procesar datos localizados en memoria (Redis) permite unas latencias ínfimas, un requisito imprescindible en entornos de manufactura de alta velocidad (Edge Computing).

### 9.2 Trabajo futuro

- **Dashboard Visual:** Implementar Grafana o Streamlit para ofrecer visualización en tiempo real de la telemetría y las alertas a los operarios de planta.
- **Detección de Data Drift:** Implementar herramientas como Evidently AI para alertar cuando los patrones de vibración de la fresadora cambien debido al desgaste físico y requieran un reentrenamiento del modelo.
- **Migración a Kubernetes:** Para entornos multi-planta, sustituir Docker Compose por AKS (Azure Kubernetes Service) para orquestación avanzada y auto-escalado nativo.

---

## 10. Bibliografía

- Kim, G., Humble, J., Debois, P. y Willis, J. (2021). *The DevOps Handbook*. IT Revolution Press.
- Documentación oficial de Docker Compose V2: [https://docs.docker.com/compose/](https://docs.docker.com/compose/)
- Documentación oficial de GitHub Actions: [https://docs.github.com/es/actions](https://docs.github.com/es/actions)
- Documentación oficial de Terraform AzureRM Provider: [https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- Arquitecturas de Mantenimiento Predictivo en Azure: [https://learn.microsoft.com/es-es/azure/architecture/industries/manufacturing/predictive-maintenance-overview](https://learn.microsoft.com/es-es/azure/architecture/industries/manufacturing/predictive-maintenance-overview)
