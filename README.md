# Flask React Application with PostgreSQL, Redis, and Celery

## Running with Docker Compose (Recommended)

### Prerequisites
- Docker
- Docker Compose

### Quick Start

1. Clone the repository
2. Create virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```
3. Install dependencies
```bash
pip install poetry
poetry install --no-root
```
4. Run the backend:
```bash
docker-compose up --build
```
5. Run the frontend:
```bash
cd frontend
npm install
npm run dev
```

Optionally you can seed data with a few users by running:
```bash
python scripts/seed_users.py
```

The application will be available at:
- Frontend: http://localhost:5000
- Backend API: http://localhost:8000

### Services
- Flask Web Application (http://localhost:8000)
- Celery Worker for background tasks
- PostgreSQL Database (port 5432)
- Redis Server (port 6379)

## Local Development Setup (Alternative)

### Prerequisites
- Python 3.11+
- PostgreSQL
- Redis
- Node.js 20+
- Poetry (Python package manager)


### Access the Application
- Frontend: http://localhost:5000
- Backend API: http://localhost:8000

## Test Coach Credentials
```
Email: jimharbaugh@gmail.com
Password: bad_pass
```

## Test Student Credentials
```
Email: jjmccarthy@gmail.com
Password: bad_pass
```

## Available Features
- User Authentication (Login/Register)
- Real-time Statistics Dashboard
- User Management
- Background Task Processing with Celery
- Redis Caching

## Development
- Frontend code is in the `frontend` directory
- Backend code is in the `backend` directory

## Docker Development Commands

### Build and Start Services
```bash
docker-compose up --build
```

### View Logs
```bash
docker-compose logs -f [service_name]
```

### Stop Services
```bash
docker-compose down
```

### Access PostgreSQL
```bash
docker-compose exec db psql -U postgres -d flask_app
```

### Access Redis CLI
```bash
docker-compose exec redis redis-cli
```
