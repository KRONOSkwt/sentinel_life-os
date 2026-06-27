# Sentinel Life OS

A modular Life OS with 6 independent modules for personal tracking and self-management.

## Modules

| Module | Purpose |
|--------|---------|
| **Gimnasio** | Gym training logs, workout tracking, PRs |
| **Deportes** | Sports activity tracking |
| **Lesiones** | Injury management, recovery timelines |
| **Pastoral** | Spiritual/pastoral activity journaling |
| **Filosofia** | Philosophy study notes and reflections |
| **Ciberseguridad** | Cybersecurity learning, tools, notes |

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Monorepo** | Nx 19.4 |
| **Web** | Angular 18 (standalone components, SCSS) |
| **Backend** | FastAPI (Python 3.12), SQLite, SQLAlchemy, JWT auth |
| **Android** | Kotlin, Jetpack Compose, Material3, Hilt |
| **Design Tokens** | Single `tokens.json` → CSS + Compose theme |
| **Infrastructure** | Docker Compose, Cloudflare Tunnel, Vercel |
| **CI** | GitHub Actions (lint, test, build, token validation) |

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    CLOUD (Vercel)                       │
│  Angular SPA ──/api/*──▶ Cloudflare Tunnel ──▶ Docker  │
└─────────────────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│               LOCAL (Docker Compose)                    │
│  ┌──────────────┐  ┌──────────────────┐                │
│  │   FastAPI    │  │   cloudflared    │                │
│  │   :8000      │  │   (tunnel)       │                │
│  └──────┬───────┘  └──────────────────┘                │
│         │                                               │
│  ┌──────▼───────┐                                      │
│  │   SQLite     │                                      │
│  └──────────────┘                                      │
└─────────────────────────────────────────────────────────┘
```

**Key design decisions:**
- **Offline-first**: Angular caches data in localStorage, syncs when online
- **Single tokens.json**: CSS and Compose theme generated from one source
- **JWT auth**: Email + password, access + refresh tokens
- **Per-module SQLite**: Future module independence

## Prerequisites

- **Node.js** >= 20.0.0
- **Python** >= 3.12
- **Java** >= 17 (for Android)
- **Android SDK** (via Android Studio)
- **Docker** + Docker Compose (for backend in production)

## Setup

### Clone & Install

```bash
git clone https://github.com/KRONOSkwt/sentinel_life-os.git
cd sentinel-life-os

# Root dependencies (Nx)
npm install

# Backend dependencies
cd apps/backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
cd ../..

# Web dependencies (if not hoisted)
cd apps/web && npm install && cd ../..

# Android — open in Android Studio and sync Gradle
```

### Environment Variables

```bash
cp .env.example .env
# Edit .env with your values (JWT_SECRET, CORS_ORIGINS, etc.)
```

### Run Locally

```bash
# Backend (from apps/backend/)
uvicorn src.main:app --reload --port 8000

# Web (from apps/web/)
npx ng serve

# Android — run via Android Studio or:
cd apps/android && ./gradlew installDebug
```

### Docker

```bash
cd docker
docker compose up --build
```

The backend will be available at `http://localhost:8000` with auto-generated API docs at `/docs`.

## Design Tokens

Tokens live in `libs/shared/tokens/tokens.json`. Generate platform outputs:

```bash
# CSS
python tools/token-pipeline/generate.py --format css

# Compose theme
python tools/token-pipeline/generate.py --format compose

# Validate tokens
python tools/token-pipeline/validate.py libs/shared/tokens/tokens.json
```

## Project Structure

```
sentinel-life-os/
├── apps/
│   ├── backend/          # FastAPI (Python)
│   │   ├── src/
│   │   │   ├── core/     # Database, security, deps
│   │   │   ├── middleware/# CORS, rate limiting
│   │   │   ├── models/   # SQLAlchemy + Pydantic schemas
│   │   │   ├── routers/  # Auth, modules, activities
│   │   │   ├── main.py   # App entry point
│   │   │   └── config.py # Pydantic Settings
│   │   └── pyproject.toml
│   ├── web/              # Angular (TypeScript)
│   │   └── src/app/
│   │       ├── core/     # Auth guard, interceptor
│   │       ├── layouts/  # Bento grid layout
│   │       └── modules/  # 6 module shells + home
│   └── android/          # Kotlin + Compose
│       └── app/src/main/
│           └── java/com/sentinel/lifeos/
├── libs/shared/          # Cross-platform models + tokens
│   ├── models/           # Python, TypeScript, Kotlin
│   └── tokens/           # tokens.json + generators
├── tools/token-pipeline/ # generate.py, validate.py
├── docker/               # Compose configs + tunnel
└── .github/workflows/    # CI pipeline
```

## Development Workflow

1. **Branch from master** for each feature
2. **Commit with conventional format**: `feat:`, `fix:`, `chore:`, `ci:`, `docs:`
3. **CI runs automatically** on push/PR to master:
   - Token validation
   - Python lint (ruff) + test (pytest)
   - Angular build
   - Android debug build
4. **PRs require passing CI** before merge

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/health` | No | Health check |
| POST | `/auth/register` | No | Register new user |
| POST | `/auth/login` | No | Login (returns JWT) |
| POST | `/auth/refresh` | No | Refresh access token |
| GET | `/auth/me` | Yes | Current user profile |

## License

Personal project — not licensed for distribution.
