# 🏃‍♂️ SCRUM & Sprints Planning

Este documento detalla la metodología ágil seguida para la evolución del sistema desde su prueba de concepto local (MVP) hasta su despliegue automatizado en producción.

## 📋 Product Backlog (Historias de Usuario)

* **US-01:** Como ingeniero de datos, quiero un sistema basado en Redis Streams que simule e ingeste telemetría de una fresadora industrial en tiempo real.
* **US-02:** Como científico de datos, quiero inyectar un modelo de Árbol de Decisión en nodos de Redis (Hashes) para lograr latencia ultra-baja.
* **US-03:** Como operador, quiero que múltiples *workers* analicen datos en paralelo y generen alertas en una cola independiente.
* **US-04:** Como ingeniero DevOps, quiero contenerizar todos los microservicios usando Docker Compose.
* **US-05:** Como Tech Lead, quiero implementar tests con `pytest` que alcancen ≥ 70% de cobertura.
* **US-06:** Como arquitecto Cloud, quiero aprovisionar infraestructura en Azure utilizando Terraform.
* **US-07:** Como desarrollador, quiero un pipeline CI/CD en GitHub Actions para testear y desplegar automáticamente en Azure.

---

## 🚀 Iteraciones (Sprints)

### Sprint 1: Desarrollo del MVP (Motor de Inferencia Local)
* **Objetivo:** Construir la lógica de Machine Learning y la comunicación básica con Redis.
* **Historias de Usuario:** US-01, US-02, US-03
* **Tareas completadas:**
  * Entrenar el modelo de clasificación de maquinaria con `scikit-learn`.
  * Desarrollar `setup_redis.py` para mapear el árbol a Redis.
  * Desarrollar el simulador `productor.py` y el agente `worker.py`.

### Sprint 2: Estandarización, Testing y Refactorización
* **Objetivo:** Aislar la aplicación y asegurar la robustez del código mediante automatización de pruebas.
* **Historias de Usuario:** US-04, US-05
* **Tareas completadas:**
  * Crear `Dockerfile` y `docker-compose.yml`.
  * Encapsular código de ejecución suelto en bloques `def main():`.
  * Eliminar "código muerto" (`orquestador.py`, `borrar_datos.py`).
  * Implementar *Mocks* en Pytest para simular conexiones a Redis.

### Sprint 3: Despliegue Cloud y CI/CD
* **Objetivo:** Llevar la aplicación contenerizada a un entorno de producción en Microsoft Azure.
* **Historias de Usuario:** US-06, US-07
* **Tareas completadas:**
  * Declarar red virtual y máquina virtual en `main.tf`.
  * Configurar llaves SSH y seguridad de red.
  * Diseñar flujo de GitHub Actions (`azure-deploy.yml`) para validación de cobertura y despliegue continuo vía SCP/SSH.

---

## 🔄 Sprint Retrospective (Post-Sprint 2)

**¿Qué salió bien?**
* La transición a Docker Compose fue muy fluida y unificó los entornos.
* Purgar el código muerto facilitó drásticamente el mantenimiento del proyecto.

**¿Qué no salió tan bien?**
* Los tests de `pytest` en entornos CI fallaban al principio por rutas relativas mal configuradas (falta de `PYTHONPATH`).
* El código original basado en bucles infinitos (`while True`) bloqueaba la ejecución de los tests automatizados.

**Action Items implementados:**
* Estandarización obligatoria: todo script ejecutable debe estar protegido bajo `if __name__ == "__main__":`.
* Uso de inyección de dependencias y Mocks de `unittest` para simular fallos de red sin colgar el pipeline.
