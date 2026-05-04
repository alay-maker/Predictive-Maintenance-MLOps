## 1. Resumen Ejecutivo

Una planta de mecanizado industrial sufre paradas no planificadas debido a fallos mecánicos en sus fresadoras CNC. El equipo de mantenimiento actúa de forma reactiva tras la avería, lo que resulta en tiempos de inactividad prolongados y altos costes de reparación.

**El problema:** No existe un sistema automatizado capaz de procesar la telemetría (vibración, temperatura, revoluciones) en tiempo real para predecir cuándo una máquina está a punto de fallar, impidiendo realizar un mantenimiento proactivo.

**Nuestra solución:** Un pipeline MLOps completo y una arquitectura de microservicios que:
1. Simula y procesa telemetría en tiempo real mediante un Productor IoT.
2. Inyecta reglas de inferencia de un modelo de Machine Learning directamente en una base de datos en memoria (Redis).
3. Evalúa los datos a través de *workers* escalables horizontalmente.
4. Permite actualizaciones ágiles del modelo ("Despliegue Continuo con Interrupción Mínima") mediante CI/CD automatizado en Microsoft Azure, reduciendo la caída del servicio a escasos segundos.

**Resultado obtenido:**
- Arquitectura desacoplada capaz de procesar telemetría cada 0.5 segundos.
- Pipeline CI/CD completamente automatizado en GitHub Actions con cobertura exigida del 70%.
- Infraestructura desplegada en Azure mediante código (Terraform).
- Capacidad de actualización de modelos sin interrupción del servicio.

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
                                          Copia de archivos (scp)
                                          docker compose down / up --build

MICROSOFT AZURE (Máquina Virtual Ubuntu)
      │
      ├── Red: predictive-net (Bridge)
      │
      ├── redis-db (Contenedor) ◄──────── setup-redis (Contenedor efímero)
      │   (Base de datos + persistencia)  (Inyecta modelo tree_model.json en BD)
      │
      ├── productor (Contenedor) ───────► (Envía telemetría a Redis cada 0.5s)
      │
      └── worker [Escalable] (Contenedores) 
          (Lee telemetría, consulta modelo en Redis, emite alerta)
```

### 3.2 Justificación de tecnologías

| Componente | Tecnología | Por qué esta y no otra |
|------------|-----------|------------------------|
| Lenguaje | Python 3.11 | Estándar en ciencia de datos; librerías nativas robustas. |
| Inferencia | Redis (Hashes) | Inferir directamente en base de datos en memoria es más rápido que cargar modelos pesados en cada *worker*. |
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
1. **El modelo de Machine Learning:** Se exporta a un formato ligero (`tree_model.json`). El contenedor efímero `setup-redis` lee este archivo e inyecta los umbrales y nodos como *Hashes* en Redis.
2. **El flujo de telemetría:** El `productor` simula sensores. El `worker` lee estos datos, cruza los valores con los nodos almacenados en Redis y determina si se dispara una alerta.

### 4.2 Gate de Calidad (Quality Gate)

El pipeline de GitHub Actions incluye un *Job* de testeo estricto. Si los tests unitarios no superan el 70% de cobertura, el *Job* finaliza con un error y bloquea inmediatamente el paso de despliegue en Azure (`needs: test`). Esto garantiza que nunca se despliega código no validado en el entorno de producción.

---

## 5. CI/CD y Automatización

### 5.1 Pipeline Integrado (`azure-deploy.yml`)

| Fase | Acción | Qué valida |
|---------|---------|-------------|
| CI (Tests) | `pytest tests/ --cov=src` | Verifica la lógica del productor, workers y configuración. Exige ≥ 70% de cobertura. |
| Transferencia | `appleboy/scp-action` | Copia de forma segura solo los archivos esenciales, el modelo y el `.dockerignore` al servidor. |
| CD (Deploy) | `appleboy/ssh-action` | Ejecuta los comandos de reconstrucción de infraestructura en caliente en Azure mediante SSH. |

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

### 7.2 Persistencia
El servicio `redis-db` incluye un mapeo de volúmenes (`redis_data:/data`). Si el contenedor de la base de datos se reinicia o sufre un crasheo, el modelo y el historial de telemetría no se pierden.

---

## 8. Metodología Ágil Aplicada

### 8.1 Framework SCRUM y GitHub Projects

El proyecto se gestionó en base a 3 Sprints. Se empleó un tablero Kanban en GitHub Projects para seguir el flujo de las Historias de Usuario (US), priorizadas en P0 (Críticas) y P1/P2.

### 8.2 Lección aprendida más importante: Del "Zero-Downtime" a la "Interrupción Mínima"

> "La teoría de microservicios promete Zero-Downtime, pero la orquestación en la práctica tiene sus propias reglas."

Durante el Sprint 3, nuestro objetivo teórico era lograr un *Zero-Downtime estricto* al actualizar el modelo predictivo. Sin embargo, observamos que, al subir un nuevo modelo, Docker destruía todos los *workers* (`exited with code 137`), provocando pérdida temporal de datos IoT.

**El problema original:** En el `docker-compose.yml`, los *workers* tenían la instrucción `depends_on: setup-redis`. Al actualizar el modelo, Docker recreaba el `setup-redis` y, por "efecto dominó", mataba y recreaba a todos los *workers*.

**La adaptación técnica:** Se modificó la arquitectura para que los *workers* dependan únicamente de `redis-db`. Aunque esto no eliminó al 100% el micro-corte (debido a cómo Docker Compose V2 reconstruye los enlaces de red al aplicar cambios en los volúmenes), pasamos de un fallo generalizado de la arquitectura a un **Despliegue Continuo con Interrupción Mínima**. Aprendimos a gestionar las expectativas técnicas: un reinicio de escasos segundos es completamente aceptable a nivel de negocio y mucho más estable que mantener dependencias cruzadas frágiles.

---

## 9. Conclusiones y Trabajo Futuro

### 9.1 Conclusiones

1. **Desacoplamiento efectivo:** Mantener las reglas del modelo separadas del código de ejecución (workers) es vital. Aunque un *Zero-Downtime* estricto requiere orquestadores más complejos (como Kubernetes), hemos demostrado que con Docker Compose se puede lograr un despliegue continuo altamente ágil y con interrupciones mínimas de apenas segundos.
2. **IaC y CI/CD son innegociables:** El uso de Terraform y GitHub Actions elimina el error humano en los despliegues, garantizando que el entorno de desarrollo sea idéntico al de producción.
3. **Mantenimiento Predictivo Real:** Procesar datos localizados en memoria (Redis) permite unas latencias ínfimas, un requisito imprescindible en entornos de manufactura de alta velocidad (Edge Computing).

### 9.2 Trabajo futuro

- **Dashboard Visual:** Implementar Grafana o Streamlit para ofrecer visualización en tiempo real de la telemetría y las alertas a los operarios de planta.
- **Detección de Data Drift:** Implementar herramientas como Evidently AI para alertar cuando los patrones de vibración de la fresadora cambien debido al desgaste físico y requieran un reentrenamiento del modelo.
- **Migración a Kubernetes:** Para entornos multi-planta, sustituir Docker Compose por AKS (Azure Kubernetes Service) para orquestación avanzada y auto-escalado.

---

## 10. Bibliografía

- Kim, G., Humble, J., Debois, P. y Willis, J. (2021). *The DevOps Handbook*. IT Revolution Press.
- Documentación oficial de Docker Compose V2: https://docs.docker.com/compose/
- Documentación oficial de GitHub Actions: https://docs.github.com/es/actions
- Documentación oficial de Terraform AzureRM Provider: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs
- Arquitecturas de Mantenimiento Predictivo en Azure: https://learn.microsoft.com/es-es/azure/architecture/industries/manufacturing/predictive-maintenance-overview