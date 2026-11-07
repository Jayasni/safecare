# sagecare-booking

Service Booking Application for clinic appointment scheduling.

## Overview
Customers can register, log in, browse services, view availability, book appointments, reschedule, cancel, and view booking history. Administrators can manage services, providers, availability, and bookings.

## Tech Stack
- Frontend: React, JavaScript, Vite, Tailwind CSS
- Backend: FastAPI, Python, SQLAlchemy, Alembic
- Database: PostgreSQL (pgAdmin 4)
- Authentication: JWT with refresh-token rotation
- Testing: Pytest, HTTPX, Vitest, React Testing Library

## Folder Structure
```text
sagecare-booking/
├── frontend/
├── backend/
├── database/
├── docs/
├── files/
├── docker-compose.yml
├── .env.example
└── README.md
```

## Prerequisites
- Node.js 20+
- Python 3.13
- PostgreSQL installed locally
- pgAdmin 4

## PostgreSQL Setup
1. Open pgAdmin 4.
2. Connect to the local PostgreSQL server.
3. Create a database named `Sagecare_db`.
4. Use owner `postgres`.

## Environment Variables
Backend:
```powershell
cd backend
Copy-Item .env.example .env
```
Update `backend/.env` with your PostgreSQL password and JWT secret.

Frontend:
```powershell
cd frontend
Copy-Item .env.example .env
```

## Backend Setup
```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Backend API:
- API base URL: `http://localhost:8000/api/v1`
- Swagger UI: `http://localhost:8000/docs`
- Health: `http://localhost:8000/api/v1/health`
- Database health: `http://localhost:8000/api/v1/health/db`

## Frontend Setup
```powershell
cd frontend
npm install
npm run dev
```

Frontend URL: `http://localhost:5173`

## Admin Account Setup
Public registration always creates customer accounts. To create an administrator, run a controlled Python command after configuring `backend/.env`:

```powershell
cd backend
venv\Scripts\activate
python -c "from app.core.security import hash_password; from app.db.session import SessionLocal; from app.models.enums import UserRole; from app.models.user import User; db=SessionLocal(); db.add(User(full_name='Admin User', email='admin@example.com', password_hash=hash_password('ChangeThisPassword'), role=UserRole.admin, is_active=True)); db.commit(); db.close()"
```

Change the email and password to secure values before running this in a real environment.

## Testing
Backend:
```powershell
cd backend
pytest
```

Frontend:
```powershell
cd frontend
npm run test
```

Production frontend build:
```powershell
cd frontend
npm run build
```

## Docker
```powershell
docker compose up --build
```

Frontend: `http://localhost`
Backend API: `http://localhost:8000`
The Nginx configuration proxies `/api/` requests to the backend service.

When running Docker Desktop on Windows, update `backend/.env` so PostgreSQL points to the host:
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@host.docker.internal:5432/Sagecare_db
```

## Database Backup
See `docs/database/backup.md`.

## Additional Documentation
- `docs/deployment/setup.md`
- `files/architecture.md`
- `files/PRD.md`
- `files/phases.md`
- `.opencoderules`

## Security Notes
- Do not commit real `.env` files.
- Set a strong `SECRET_KEY` in production.
- Use HTTPS in production.
- Admin accounts must be created through an approved administrative process.