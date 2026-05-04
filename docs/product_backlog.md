# Product Backlog — MLOps: Mantenimiento Predictivo Industrial

**Proyecto:** Pipeline MLOps — Mantenimiento Predictivo de Fresadora CNC  
**Product Owner:** ExcellentApproximation  
**Scrum Master:** alay-maker  

---

## Épicas

| # | Épica | Descripción |
|---|-------|-------------|
| E1 | Ingesta | Simulación y transmisión de telemetría IoT en tiempo real |
| E2 | Inferencia | Despliegue de reglas de ML en base de datos en memoria (Redis) |
| E3 | Workers | Procesamiento distribuido para evaluación de telemetría |
| E4 | Contenedores | Aislamiento y orquestación de la arquitectura (Docker) |
| E5 | CI/CD | Automatización de testing y despliegue continuo (GitHub Actions) |
| E6 | IaC | Provisión de infraestructura en nube (Terraform + Azure) |

---

## Backlog Priorizado (MoSCoW)

### Must Have (Obligatorio para MVP)

| ID  | Épica | Historia de Usuario | Criterios de Aceptación | Puntos | Sprint |
|-----|-------|---------------------|------------------------|--------|--------|
| US-01 | E1 | Como ingeniero de datos, quiero un servicio Productor que envíe telemetría de vibración, temperatura y revoluciones a Redis, para simular los sensores de la fresadora. | El script envía datos cada 0.5s; se conecta a Redis usando variables de entorno; maneja desconexiones sin crashear. | 5 | Sprint 1 |
| US-02 | E2 | Como Data Scientist, quiero que un servicio efímero (Setup) lea el modelo JSON y lo inyecte como Hashes en Redis, para separar las reglas de negocio del código ejecutable. | Lee `tree_model.json`; inyecta nodos en la base de datos; termina con `exit 0` cuando acaba la carga. | 8 | Sprint 1 |
| US-03 | E3 | Como desarrollador, quiero un Worker distribuido que lea la telemetría, consulte las reglas en Redis y evalúe si hay anomalías, para emitir alertas tempranas. | Lee mensajes de Redis; aplica la lógica de inferencia consultando los hashes; imprime logs de "Normal" o "Alerta". | 5 | Sprint 1 |
| US-04 | E4 | Como DevOps, quiero contenedorizar los tres servicios y la base de datos con Docker Compose, para garantizar que el sistema funcione igual en cualquier máquina. | `docker-compose up` levanta los 4 contenedores; la red bridge conecta los servicios correctamente; Redis usa volúmenes persistentes. | 5 | Sprint 2 |
| US-05 | E5 | Como QA, quiero que el código pase por un linter y tests automáticos (`pytest`), para evitar que subamos código roto al servidor. | Hay tests unitarios para las funciones principales; la cobertura supera el 70%; el workflow de GitHub falla si no se cumple. | 5 | Sprint 2 |
| US-06 | E6 | Como Arquitecto Cloud, quiero definir la infraestructura de Azure (Máquina Virtual, Red, Seguridad) en Terraform, para que el despliegue sea reproducible. | `terraform apply` levanta la VM en Azure; abre el puerto 22 (SSH); crea un admin con clave pública; se exporta la IP en `outputs.tf`. | 8 | Sprint 3 |
| US-07 | E5 | Como DevOps, quiero un pipeline CD que copie los archivos mediante SSH y reinicie Docker Compose en Azure tras un push, para lograr Despliegue Continuo. | Un push a `main` dispara el despliegue tras pasar los tests; el servidor recrea los contenedores necesarios sin intervención manual. | 5 | Sprint 3 |

### Should Have (Importante, no bloqueante)

| ID  | Épica | Historia de Usuario | Criterios de Aceptación | Puntos | Sprint |
|-----|-------|---------------------|------------------------|--------|--------|
| US-08 | E3 | Como Arquitecto, quiero poder escalar los Workers horizontalmente, para soportar picos de envío de telemetría sin cuellos de botella. | El comando `docker compose up --scale worker=3` levanta tres instancias sin error de colisión de nombres. | 3 | Sprint 2 |
| US-09 | E4 | Como SRE, quiero modificar las dependencias de Docker para que los workers no dependan de `setup-redis`, para lograr un Despliegue Continuo con Interrupción Mínima. | Actualizar el archivo `tree_model.json` e inyectarlo en Redis no destruye ni reinicia los workers en ejecución. | 5 | Sprint 3 |

---

## Velocidad del equipo

- **Sprint 1 (23 Mar - 06 Abr):** 18 puntos completados
- **Sprint 2 (06 Abr - 20 Abr):** 13 puntos completados (Incluyendo escalabilidad)
- **Sprint 3 (20 Abr - 04 May):** 18 puntos completados (Incluyendo refactorización para Interrupción Mínima)
- **Total: 49 puntos de historia**
