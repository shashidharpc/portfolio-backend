# Shashidhar P C — Portfolio Backend API

High-performance Python backend built with **FastAPI**, **SQLAlchemy**, and **Pydantic**, powering data persistence, authentication, telemetry, and automated attendance verification for Shashidhar P C's engineering portfolio platform.

---

## Architecture Overview

- **Framework**: FastAPI (Asynchronous REST API)
- **Database Engine**: SQLAlchemy 2.0 ORM (PostgreSQL in production, SQLite for local dev)
- **Validation**: Pydantic v2 schemas
- **Authentication**: JWT token issuance with `httpOnly` cookie support
- **Geofencing & Automation**: Haversine distance calculations for QR code attendance verification

---

## Project Structure

```
backend/
├── app/
│   ├── main.py                # FastAPI entry point, CORS, lifespan seeding
│   ├── core/
│   │   ├── config.py          # Pydantic BaseSettings from env
│   │   ├── security.py        # Password hashing & JWT issuance
│   │   └── deps.py            # get_db, get_current_user, require_admin
│   ├── db/
│   │   ├── base.py            # DeclarativeBase
│   │   ├── session.py         # SQLAlchemy engine & SessionLocal
│   │   └── seed.py            # Database auto-seed script
│   ├── models/                # SQLAlchemy ORM models
│   ├── schemas/               # Pydantic request/response schemas
│   ├── services/              # Geofence & attendance business logic
│   └── api/
│       └── v1/                # Versioned REST API endpoints
├── tests/                     # Pytest suite
├── Dockerfile                 # Production container setup
├── requirements.txt           # Python dependencies
└── .env.example               # Environment variables template
```

---

## API Endpoints

### Public Endpoints
- `GET /health`: Health check and system status
- `GET /api/v1/content/profile`: Retrieve verified engineer bio and social links
- `GET /api/v1/content/skills`: Retrieve skill categories and tech proficiencies
- `GET /api/v1/content/experiences`: Retrieve experience and education timeline
- `GET /api/v1/projects`: List portfolio case studies (`?category=Full Stack`)
- `GET /api/v1/projects/{slug}`: Project detail
- `POST /api/v1/projects/{slug}/view`: Increment view counter
- `POST /api/v1/messages`: Submit contact form
- `POST /api/v1/attendance/qr/scan`: Submit GPS coordinate and QR token

### Authenticated Endpoints (Admin)
- `POST /api/v1/auth/login`: Issue session token / set cookie
- `GET /api/v1/auth/me`: Get current admin details
- `POST /api/v1/auth/logout`: Invalidate session
- `GET /api/v1/dashboard/layout`: Retrieve custom dnd-kit widget positions
- `PUT /api/v1/dashboard/layout`: Persist custom widget canvas state
- `GET /api/v1/dashboard/stats`: Telemetry and traffic overview
- `GET /api/v1/messages`: Review contact inbox
- `POST /api/v1/projects`: Create new project
- `PATCH /api/v1/projects/{id}`: Edit project
- `DELETE /api/v1/projects/{id}`: Delete project

---

## Local Development

```bash
# 1. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate # Linux/macOS

# 2. Install dependencies
pip install -r requirements.txt

# 3. Seed database
python -m app.db.seed

# 4. Start local development server
uvicorn app.main:app --reload --port 8000
```

Interactive Swagger documentation will be available at: `http://localhost:8000/docs`

---

## Deployment (Render / Railway / Fly.io / Docker)

Build and run using Docker:
```bash
docker build -t portfolio-backend .
docker run -p 8000:8000 -e DATABASE_URL="postgresql://user:pass@host:5432/db" portfolio-backend
```
