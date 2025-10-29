# Y2K Shopping - Backend API

FastAPI backend for the Y2K Shopping Website.

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Installation

1. **Create and activate virtual environment**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # venv\Scripts\activate   # On Windows
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run the development server**:
   ```bash
   uvicorn app.main:app --reload
   ```
   
   Or alternatively:
   ```bash
   python -m app.main
   ```

5. **Access the API**:
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/api/v1/docs
   - Alternative docs: http://localhost:8000/api/v1/redoc

## 📁 Project Structure

```
backend/
├── app/
│   ├── core/              # Configuration and settings
│   │   ├── config.py      # Application settings
│   │   └── __init__.py
│   ├── models/            # SQLAlchemy database models
│   │   └── __init__.py
│   ├── routes/            # API route handlers
│   │   └── __init__.py
│   ├── schemas/           # Pydantic schemas for validation
│   │   └── __init__.py
│   ├── database.py        # Database connection setup
│   ├── main.py           # FastAPI application entry point
│   └── __init__.py
├── alembic/              # Database migrations (to be configured)
├── requirements.txt      # Python dependencies
├── .env.example         # Example environment variables
└── README.md            # This file
```

## 🔧 Configuration

The application uses environment variables for configuration. Copy `.env.example` to `.env` and adjust:

- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Secret key for JWT tokens (change in production!)
- `BACKEND_CORS_ORIGINS`: Allowed frontend origins

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc

## 🗄️ Database

### Using SQLite (Default - Easy Start)
- No additional setup required
- Database file: `y2k_shopping.db` (created automatically)
- Perfect for development

### Switching to PostgreSQL (Production)
1. Install PostgreSQL
2. Create database: `createdb y2k_shopping`
3. Update `DATABASE_URL` in `.env`:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/y2k_shopping
   ```

## 🔐 Authentication

JWT-based authentication will be implemented using:
- `python-jose` for token generation
- `passlib` for password hashing
- Token expiration configured in settings

## 🧪 Testing

Run tests with:
```bash
pytest
```

## 📝 Next Steps

1. ✅ Basic project structure created
2. ⏳ Create database models (User, Product, Order, etc.)
3. ⏳ Implement authentication routes
4. ⏳ Create product CRUD operations
5. ⏳ Implement shopping cart logic
6. ⏳ Add payment integration (Stripe)
7. ⏳ Set up database migrations with Alembic

## 🐛 Development Tips

- Use `--reload` flag with uvicorn for auto-reload on code changes
- Check API docs at `/api/v1/docs` for testing endpoints
- Keep virtual environment activated while developing
- Use `.env` for local configuration (never commit this file!)

## 📦 Adding New Dependencies

```bash
pip install package-name
pip freeze > requirements.txt
```
