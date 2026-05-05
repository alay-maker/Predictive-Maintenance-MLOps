# Sprint Retrospective — Global del Proyecto

**Fecha:** 05/05/2026  
**Equipo:** ExcellentApproximation, alay-maker  
**Formato:** Start / Stop / Continue

---

## ¿Qué fue bien? (Continue)

- **Uso de Redis como Motor de Inferencia:** La decisión de inyectar el modelo en la base de datos (US-02) fue un acierto total. Nos permitió desacoplar la lógica del modelo de los Workers, facilitando el procesamiento en tiempo real de la telemetría.
- **Pipeline CI/CD Automatizado:** La configuración de GitHub Actions (US-07) para desplegar en Azure tras pasar los tests (`pytest` > 70%) funcionó perfectamente y agilizó los últimos días del proyecto.
- **División en Microservicios:** Contenerizar el Productor, Redis, Setup y Workers (US-04) nos permitió escalar fácilmente y trabajar en paralelo.

---

## ¿Qué no funcionó? (Stop)

- **Nombres estáticos en contenedores:** Al principio, fijamos `container_name: python-worker` en Docker Compose. Esto nos bloqueó temporalmente cuando quisimos escalar los workers horizontalmente, ya que Docker daba error por colisión de nombres.
- **El falso "Zero-Downtime":** En el Sprint 3, intentamos que la actualización del modelo fuera invisible. Sin embargo, al tener `depends_on: setup-redis` en los workers, Docker los destruía en cadena al actualizar. Tuvimos que parar, refactorizar la arquitectura para que dependieran solo de `redis-db` y aceptar un enfoque de "Interrupción Mínima".

---

## ¿Qué mejoraríamos? (Start)

- **Terraform desde el Sprint 1:** Dejamos la Infraestructura como Código (US-06) para el final. Esto nos obligó a hacer pruebas manuales en la nube durante los primeros sprints. En el futuro, aprovisionaremos la VM de Azure primero.
- **Añadir un endpoint de métricas (Health Check):** Para que Azure o GitHub Actions sepan si los contenedores se han levantado correctamente antes de dar el despliegue por exitoso.

---

## Reflexión sobre la metodología ágil

**¿Sirvió SCRUM para este proyecto?**

Completamente. Tener el tablero Kanban en GitHub Projects nos dio visibilidad. La US-02 (Motor de Inferencia) era la más compleja (8 puntos) y dividirla en el Sprint 1 nos permitió enfocar nuestros esfuerzos donde más riesgo técnico había.

---

## Velocidad por sprint

| Sprint | Puntos planificados | Puntos completados | % completado |
|--------|---------------------|-------------------|--------------|
| Sprint 1 | 18 | 18 | 100% |
| Sprint 2 | 10 | 10 | 100% |
| Sprint 3 | 13 | 13 | 100% |
| **Total** | **41** | **41** | **100%** |
