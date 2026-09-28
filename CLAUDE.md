# SupplyGuard

Proyecto personal (portfolio) inspirado en la gestión de calidad incoming de una fábrica. Web para registrar, analizar, resolver y medir incidencias de piezas defectuosas de proveedores. El objetivo es practicar el stack típico de proyectos de digitalización industrial (API REST, BD relacional, roles, BigQuery, dashboards, alertas).

## Sobre mí
- Estudiante de Ingeniería Informática (UPV), rama software.
- Vengo de C#/ASP.NET Core, Spring Boot, PostgreSQL, Blazor, React Native, Next.js. Python y FastAPI son nuevos para mí: explica brevemente las decisiones y convenciones propias de Python.
- Quiero aprender: no me des todo hecho sin explicar. Prefiero pasos pequeños que pueda entender y probar.
- Idioma: español para explicaciones; código, commits y README en inglés (salvo que diga otra cosa).

## Stack
- Backend: FastAPI + Pydantic, SQLAlchemy 2.0, Alembic, PostgreSQL
- Auth: JWT (OAuth2 password flow) con roles
- Front: Next.js + Recharts (fase 2)
- PDF: WeasyPrint (fase 3)
- Avisos: webhook Teams/Discord con httpx (fase 3)
- Cloud: export a BigQuery + Looker Studio (fase 4)
- Calidad: pytest, ruff, GitHub Actions
- Despliegue local: Docker Compose

## Estructura prevista
```
supplyguard/
├── backend/
│   ├── app/
│   │   ├── api/        # routers por módulo
│   │   ├── models/     # SQLAlchemy
│   │   ├── schemas/    # Pydantic
│   │   ├── services/   # lógica de negocio, PDF, BigQuery, webhooks
│   │   └── core/       # config, seguridad
│   ├── alembic/
│   └── tests/
├── frontend/
├── docker-compose.yml
└── README.md
```

## Dominio
Flujo de una incidencia: `abierta → en análisis → acción correctiva → cerrada`.

Ejemplo: un operario detecta que un lote de soportes del proveedor "Metalex" llega con agujeros descentrados y crea la incidencia (pieza, lote, proveedor, severidad, descripción, foto). Un ingeniero la analiza y crea un plan de acción con tareas (responsable y fecha límite). Al completarse las tareas se cierra. Todo queda en el historial y se puede descargar una ficha en PDF. Un panel muestra KPIs.

Roles:
| Rol | Permisos |
|---|---|
| operario | crear y consultar incidencias |
| ingeniero | analizar, crear planes de acción, cambiar estados |
| admin | gestionar usuarios, proveedores y piezas |

Entidades: users, suppliers, parts (referencia, lote, proveedor), incidents, action_plans, tasks, incident_history (quién hizo qué y cuándo).

KPIs: incidencias abiertas, tiempo medio de cierre, ranking de proveedores por incidencias.

Módulos independientes: incidencias, proveedores/piezas, planes de acción, KPIs, usuarios/roles, notificaciones.

## Plan por fases
| Fase | Contenido | Horas |
|---|---|---|
| 0 | Repo, Docker Compose, PostgreSQL, esqueleto FastAPI, Alembic | 4-6 |
| 1 | Modelo de datos, API de incidencias/proveedores/planes, auth JWT con roles | 15-22 |
| 2 | Front Next.js: login, listado, detalle, formulario, KPIs | 12-18 |
| 3 | PDF de la ficha, webhook, tests, GitHub Actions | 8-12 |
| 4 | Export nocturno a BigQuery y dashboard en Looker Studio | 8-12 |
| 5 | README, diagrama de arquitectura, capturas | 4-6 |

## Prioridad actual
Deadline personal: **16/10/2026** (solicitud de prácticas Ford). Para esa fecha basta con **Fases 0 y 1** funcionando, documentadas en Swagger y subidas a GitHub con README básico. Las fases 2-5 vienen después.

## Cómo quiero trabajar
- Empezar por la Fase 0 y avanzar de una fase a otra solo cuando la anterior funcione y tenga tests básicos.
- Commits pequeños y descriptivos (Conventional Commits).
- Antes de escribir mucho código, propón el plan del paso y espera mi visto bueno.
- Variables sensibles en `.env` (nunca en el repo); incluir `.env.example`.
- Cuando algo sea específico de Python/FastAPI (dependencias, async, tipado), explícalo en una o dos frases comparándolo con C#/Java.
- El README debe indicar que es un proyecto personal inspirado en la gestión de calidad incoming.

## Comandos (actualizar al crearlos)
- Levantar todo: `docker compose up --build`
- Tests: `pytest`
- Lint: `ruff check .`
- Migraciones: `alembic revision --autogenerate -m "msg"` y `alembic upgrade head`
