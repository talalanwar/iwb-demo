# Product Learning Studio

A browser-based demo SaaS application that helps product learners turn a rough product idea into a lightweight, reviewable product definition package.

## Overview

Product Learning Studio enables aspiring product teams to learn IBM Product Workbench by transforming product thinking into a small, structured, shareable specification package in one guided flow.

## Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: React + TypeScript + Vite
- **Database**: SQLite (default) with PostgreSQL portability
- **Authentication**: JWT with bcrypt password hashing

## Prerequisites

- **Python 3.11 or higher** - [Download from python.org](https://python.org)
- **Node.js 18 or higher** - [Download from nodejs.org](https://nodejs.org)
- **Git** - [Download from git-scm.com](https://git-scm.com/)
- **Git Bash** (Windows only) - Included with Git for Windows

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd iwb-demo
   ```

2. **Environment configuration (optional)**
   
   The application uses SQLite by default and includes a working dev configuration.
   For custom configuration, copy and edit `.env.example`:
   
   ```bash
   cp .env.example backend/.env
   ```
   
   Key environment variables:
   - `DATABASE_URL` - Database connection string (default: `sqlite:///./app.db`)
   - `JWT_SECRET_KEY` - Secret key for JWT token signing (change in production!)
   - `JWT_EXPIRE_MINUTES` - JWT token expiration time in minutes (default: 1440 = 24 hours)
   - `CORS_ORIGINS` - Allowed CORS origins (default: `http://localhost:5173`)

## Run

### Quick Start (Recommended)

Start the application using the startup script:

**macOS / Linux:**
```bash
./start.sh
```

**Windows:**
```batch
start.bat
```

The script will:
1. Check prerequisites (Python 3.11+, Node.js 18+)
2. Create Python virtual environment (if needed)
3. Install backend dependencies
4. Run database migrations
5. Seed demo data (idempotent)
6. Start backend on http://localhost:9000 (or next available port)
7. Start frontend on http://localhost:5173 (or next available port)

To stop the application:

**macOS / Linux:**
```bash
./stop.sh
```

**Windows:**
```batch
stop.bat
```

### Manual Setup (Alternative)

If you prefer to run services manually:

**Backend:**
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install .
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 9000
```

**Frontend (separate terminal):**
```bash
cd frontend
npm install
npm run dev
```

### Docker

Build and run with Docker Compose:

```bash
docker compose up --build
```

Access the application at http://localhost:80

## Default Credentials

For demo purposes, a default user is automatically seeded:

- **Email**: demo@example.com
- **Password**: demo1234

Use these credentials to sign in when you first access the application.

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | Database connection string | `sqlite:///./app.db` | No |
| `JWT_SECRET_KEY` | Secret key for JWT token signing | - | Yes (use default for dev) |
| `JWT_ALGORITHM` | Algorithm for JWT signing | `HS256` | No |
| `JWT_EXPIRE_MINUTES` | JWT token expiration time | `1440` (24 hours) | No |
| `BACKEND_PORT` | Backend server port (start.sh) | `9000` | No |
| `FRONTEND_PORT` | Frontend dev server port (start.sh) | `5173` | No |
| `CORS_ORIGINS` | Allowed CORS origins (comma-separated) | `http://localhost:5173` | No |

**Security Note:** Always change `JWT_SECRET_KEY` to a strong random value in production. Generate one with:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

## API Routes

The backend exposes the following API endpoints under `/api/v1`:

### Authentication
- `POST /api/v1/auth/login` - User authentication
- `POST /api/v1/auth/logout` - Sign out

### Workspace Management
- `GET /api/v1/workspace` - Get or create workspace aggregate
- `PUT /api/v1/workspace` - Update workspace metadata and vision
- `PUT /api/v1/workspace/stories` - Update stories and backlog
- `GET /api/v1/workspace/readiness` - Get readiness summary with gaps

### Review Mode
- `GET /api/v1/review/{shareToken}` - Get review snapshot (protected)
- `POST /api/v1/review/{shareToken}/notes` - Add review note

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:9000/api/docs
- **ReDoc**: http://localhost:9000/api/redoc

## Testing

### Backend Tests

Run backend unit tests with pytest:

```bash
cd backend
python -m pytest tests/ --tb=short
```

Generate JUnit XML report for CI/CD:

```bash
cd backend
python -m pytest tests/ --junitxml=test-results.xml --tb=short
```

### Frontend Tests

Run frontend component tests with vitest:

```bash
cd frontend
CI=true npm test
```

Generate JUnit XML report for CI/CD:

```bash
cd frontend
CI=true npm test -- --run --reporter=junit --outputFile=test-results.xml
```

### Build Verification

Verify the frontend builds successfully:

```bash
cd frontend
npm run build
```

## Deployment Notes

### PostgreSQL Production Setup

For production use with PostgreSQL:

1. **Install PostgreSQL dependencies:**
   ```bash
   cd backend
   pip install ".[postgres]"
   ```

2. **Set `DATABASE_URL` environment variable:**
   ```bash
   export DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/dbname
   ```

3. **Run migrations:**
   ```bash
   alembic upgrade head
   ```

### Docker Compose with PostgreSQL

For PostgreSQL in Docker, create `docker-compose.postgres.yml`:

```yaml
version: '3.8'
services:
  backend:
    build:
      args:
        PIP_TARGET: ".[postgres]"
    environment:
      DATABASE_URL: postgresql+psycopg://user:password@database:5432/iwb_demo
    depends_on:
      - database
  
  database:
    image: postgres:16
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: iwb_demo
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Then run:
```bash
docker compose -f docker-compose.yml -f docker-compose.postgres.yml up --build
```

### Security Checklist

- [ ] Change `JWT_SECRET_KEY` to a strong random value
- [ ] Use HTTPS/TLS 1.2+ for all non-local deployments
- [ ] Review and restrict `CORS_ORIGINS` to your actual frontend domain(s)
- [ ] Use PostgreSQL or another production database (not SQLite) for production
- [ ] Enable authentication on review endpoints if needed
- [ ] Set up proper database backups
- [ ] Configure rate limiting on authentication endpoints
- [ ] Review and harden CORS, CSP, and other security headers

## Project Structure

```
iwb-demo/
├── backend/              # FastAPI backend
│   ├── app/             # Application code
│   │   ├── api/         # API routes and dependencies
│   │   ├── core/        # Configuration, security, errors, logging
│   │   ├── models/      # SQLAlchemy ORM models
│   │   ├── schemas/     # Pydantic request/response schemas
│   │   ├── services/    # Business logic layer
│   │   ├── repositories/# Data access layer
│   │   ├── domain/      # Domain logic and rules
│   │   ├── main.py      # FastAPI application entry point
│   │   └── seed.py      # Database seed data
│   ├── alembic/         # Database migrations
│   │   └── versions/    # Migration files
│   ├── tests/           # Backend unit tests
│   ├── pyproject.toml   # Python dependencies
│   └── alembic.ini      # Alembic configuration
├── frontend/            # React + Vite frontend
│   ├── src/
│   │   ├── api/         # API client and service methods
│   │   ├── app/         # Router and providers
│   │   ├── components/  # React components
│   │   ├── hooks/       # Custom React hooks
│   │   ├── lib/         # Utility functions
│   │   ├── pages/       # Page components
│   │   ├── state/       # State management
│   │   └── types/       # TypeScript type definitions
│   ├── package.json     # Node.js dependencies
│   └── vite.config.ts   # Vite configuration
├── docker-compose.yml   # Docker Compose configuration
├── .env.example         # Environment variable template
├── start.sh             # Startup script (macOS/Linux)
├── stop.sh              # Stop script (macOS/Linux)
├── start.bat            # Startup script (Windows)
├── stop.bat             # Stop script (Windows)
└── README.md            # This file
```

## Troubleshooting

### Port Already in Use

The startup scripts automatically detect if the default ports (9000 for backend, 5173 for frontend) are in use and will try the next available port. Check the console output for the actual ports used.

### Python Version Issues

Ensure you have Python 3.11 or higher:
```bash
python3 --version
```

If you have multiple Python versions, you may need to specify the version explicitly in the startup script.

### Database Migration Issues

If you encounter migration errors, try resetting the database (warning: destroys all data):
```bash
cd backend
rm -f app.db  # or your custom database file
alembic upgrade head
```

### Frontend Build Issues

Clear the node_modules and reinstall:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## Contributing

[Add contribution guidelines here]

## License

[Add your license here]
