# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Y2K Shopping Website - A full-stack e-commerce application with Y2K aesthetic, built with Vue.js 3 (frontend) and FastAPI (backend). Features pure CSS animations without external libraries for an authentic late 90s/early 2000s design.

## Development Commands

### Starting the Application

**Backend (FastAPI)**
```bash
# Using startup script (recommended)
./start-backend.sh

# Manual start
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

**Frontend (Vue.js + Vite)**
```bash
# Using startup script (recommended)
./start-frontend.sh

# Manual start
cd frontend
npm run dev
```

**Access Points**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs (Swagger): http://localhost:8000/api/v1/docs
- API Docs (ReDoc): http://localhost:8000/api/v1/redoc

### Testing

```bash
# Backend tests
cd backend
source venv/bin/activate
pytest

# Frontend tests (when implemented)
cd frontend
npm run test
```

### Building

```bash
# Frontend production build
cd frontend
npm run build
```

### Database Operations

```bash
# Create database tables (from backend directory with venv activated)
python -c "from app.database import engine, Base; Base.metadata.create_all(bind=engine)"

# With Alembic migrations (when configured)
alembic upgrade head
alembic revision --autogenerate -m "description"
```

### Package Management

```bash
# Backend - add new Python package
cd backend
source venv/bin/activate
pip install package-name
pip freeze > requirements.txt

# Frontend - add new npm package
cd frontend
npm install package-name
```

## Architecture

### Tech Stack

**Frontend:**
- Vue.js 3 with Composition API
- Vite (build tool with HMR)
- Vue Router for routing
- Axios for API calls
- Pure CSS for animations (no external animation libraries)

**Backend:**
- FastAPI (Python async web framework)
- SQLAlchemy ORM with SQLite (can switch to PostgreSQL)
- Pydantic for validation
- JWT authentication (python-jose)
- Automatic API documentation via OpenAPI/Swagger

### Project Structure

```
backend/
├── app/
│   ├── core/           # Configuration (settings from .env)
│   ├── models/         # SQLAlchemy database models
│   ├── routes/         # API endpoint routers
│   ├── schemas/        # Pydantic models for request/response
│   ├── database.py     # DB connection and session management
│   └── main.py         # FastAPI app initialization, CORS, router registration
├── alembic/            # Database migrations
├── venv/               # Python virtual environment
└── requirements.txt    # Python dependencies

frontend/
├── src/
│   ├── api/            # Axios API client with interceptors
│   ├── assets/         # Images, fonts, static files
│   ├── components/     # Reusable Vue components
│   ├── router/         # Vue Router configuration
│   ├── styles/         # Pure CSS (reset, variables, animations, global)
│   ├── views/          # Page-level components (Home, Products, Cart, Login)
│   ├── App.vue         # Root component
│   └── main.js         # App entry point, style imports
├── public/             # Static assets
└── vite.config.js      # Vite config with API proxy
```

### Key Design Patterns

**Backend (FastAPI):**
- Dependency injection for database sessions (`get_db()`)
- Layered architecture: routes → schemas (validation) → models (database)
- Router organization by feature (products, auth, cart, orders)
- Environment-based configuration via Pydantic Settings
- CORS configured for frontend origins (localhost:5173)

**Frontend (Vue.js):**
- Single File Components (.vue files)
- Lazy-loaded routes for code splitting
- Centralized API client with auth token interceptors
- CSS custom properties (variables) for theming
- Y2K design system: cyber pink, cyber blue, neon green, etc.

**API Communication:**
- Vite proxy forwards `/api` requests to backend (avoid CORS in dev)
- Axios client configured with base URL and auth headers
- JWT token stored in localStorage, auto-added to requests

### Y2K Design System

**CSS Structure:**
- `reset.css` - Browser normalization
- `variables.css` - Color palette, spacing, typography
- `animations.css` - 20+ custom keyframe animations
- `global.css` - Utility classes, components (buttons, cards, badges)

**Color Palette:**
- Cyber Pink: #ff00ff
- Cyber Blue: #00ffff
- Neon Green: #39ff14
- Electric Yellow: #ffff00
- Cyber Purple: #9945ff

**Key Animations:**
- `gradient-shift` - Animated gradient backgrounds
- `glitch` / `glitch-slow` - Glitch effects
- `neon-pulse` - Pulsing glow
- `holographic` - Holographic text
- `float`, `spin`, `pulse-scale`, `bounce`, `shake`
- Entrance animations: `fade-in-up`, `slide-in-right`, `scale-in`
- `shimmer` - Loading states

**Component Classes:**
- Buttons: `.btn-primary`, `.btn-secondary`, `.btn-ghost`
- Cards: `.card`, `.card-glow`
- Effects: `.glass`, `.neon-text`, `.holographic`, `.hover-glow`, `.hover-scale`

### Database Schema (Planned)

The application will use these models:
- **User**: Authentication and profile
- **Product**: Catalog items with name, description, price, image_url, category
- **Cart/CartItem**: Shopping cart state
- **Order/OrderItem**: Purchase records
- **Category**: Product organization

Database models inherit from `Base` (SQLAlchemy declarative base) defined in `database.py`.

## Development Workflow

### Adding a New Feature

1. **Backend:** Create model in `models/` → Create schema in `schemas/` → Create router in `routes/` → Register router in `main.py`
2. **Frontend:** Create component/view → Add route if needed → Connect to API via axios
3. Test API endpoints via Swagger UI before integrating frontend
4. Use Vue Router for navigation, not `window.location`

### Adding a New Database Model

```python
# 1. Create model (backend/app/models/example.py)
from sqlalchemy import Column, Integer, String
from app.database import Base

class Example(Base):
    __tablename__ = "examples"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

# 2. Create schemas (backend/app/schemas/example.py)
from pydantic import BaseModel

class ExampleBase(BaseModel):
    name: str

class Example(ExampleBase):
    id: int
    class Config:
        from_attributes = True

# 3. Create router (backend/app/routes/example.py)
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.get("/")
def get_examples(db: Session = Depends(get_db)):
    return []

# 4. Register in main.py
from app.routes import example
app.include_router(example.router, prefix=f"{settings.API_V1_STR}/examples", tags=["examples"])

# 5. Create tables
python -c "from app.database import engine, Base; from app.models.example import Example; Base.metadata.create_all(bind=engine)"
```

### Adding a New Vue Component

```vue
<!-- frontend/src/components/Example.vue -->
<template>
  <div class="card card-glow">
    <h3>{{ title }}</h3>
  </div>
</template>

<script>
export default {
  props: {
    title: String
  }
}
</script>

<style scoped>
/* Component-specific styles */
</style>
```

## Important Notes

### Authentication Flow
- JWT tokens managed via Axios interceptors (frontend/src/api/client.js)
- Token stored in localStorage
- 401 responses automatically redirect to login
- Backend expects `Authorization: Bearer <token>` header

### Environment Variables
- Backend: `.env` file for DATABASE_URL, SECRET_KEY, etc.
- Frontend: `.env` file for VITE_API_URL (defaults to http://localhost:8000/api/v1)
- Never commit `.env` files (use `.env.example` templates)

### CORS Configuration
- Backend allows origins from frontend dev server (localhost:5173)
- Update `BACKEND_CORS_ORIGINS` in `backend/app/core/config.py` if frontend port changes

### CSS Animation Guidelines
- All animations must be pure CSS (no JavaScript animation libraries)
- Use existing animations from `animations.css` before creating new ones
- Follow Y2K aesthetic: bold colors, gradients, glows, glitch effects
- Prefer CSS transitions for hover states, keyframes for continuous animations

### Code Style
- Backend: Follow FastAPI best practices, use type hints
- Frontend: Use Vue 3 Composition API for new components (not Options API)
- Use async/await for API calls
- Keep components small and focused

### Current Development Status
- Phase 1 (Complete): Project structure, design system, routing, API client
- Phase 2 (In Progress): Core e-commerce features (products, cart, auth, checkout)
- Phase 3 (Planned): Payment integration, order management, admin panel

### Git Branch Strategy
- Main branch: `dev`
- Create feature branches from `dev`
- Use conventional commit messages: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`
