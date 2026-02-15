# Design Decisions

| Area | Decision | Rationale |
|------|----------|-----------|
| **Stack** | Angular (frontend), FastAPI (backend), PostgreSQL (DB in Docker for POC) | Angular for enterprise SPA; FastAPI for async Python and CSV/Pandas; Postgres for relational data. |
| **CSV parsing** | Pandas on the backend | Robust parsing, type coercion, validation; chunked reads for large files. |
| **API style** | REST with JSON | Simple to consume from Angular; easy filters and pagination. |
| **Search** | Server-side filtering and pagination (limit/offset) | Scale; bounded response size. |
| **DB schema & migrations** | SQLAlchemy models; Alembic for all schema setup and migrations | Single source of truth; versioned, repeatable schema changes. |
| **Request/response validation** | Pydantic schemas aligned with SQLAlchemy models | FastAPI validates inputs; responses serialized and validated. |
| **Database (POC)** | PostgreSQL in Docker | Consistent local dev; no local Postgres install. |
| **Docker workflow** | One compose: db + backend + frontend; migrations on backend startup | `docker compose up` brings up all three; migrations run automatically. |