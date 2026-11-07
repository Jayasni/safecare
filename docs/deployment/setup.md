# Deployment Guide

## Local Development
1. Install Node.js, Python 3.13, and PostgreSQL.
2. Create the `Sagecare_db` database in pgAdmin 4.
3. Copy `backend/.env.example` to `backend/.env` and configure secrets.
4. Install frontend dependencies:
   ```powershell
   cd frontend
   npm install
   ```
5. Install backend dependencies:
   ```powershell
   cd backend
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
6. Run migrations:
   ```powershell
   alembic upgrade head
   ```
7. Start backend:
   ```powershell
   uvicorn app.main:app --reload
   ```
8. Start frontend:
   ```powershell
   npm run dev
   ```

## Docker
```powershell
docker compose up --build
```

Frontend is available on port 80 and backend on port 8000. The frontend Nginx configuration proxies `/api/` to the backend service.

## Environment Separation
- Development: `backend/.env`
- Testing: `backend/tests/conftest.py` uses `sagecare_db_test`
- Production: provide secured environment variables externally, especially `DATABASE_URL` and `SECRET_KEY`.

## Production Checklist
- Run `alembic upgrade head`
- Set a strong random `SECRET_KEY`
- Use production database credentials
- Configure HTTPS and secure cookies
- Verify frontend production build
- Run backend tests
- Run frontend tests
- Review CORS configuration