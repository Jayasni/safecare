# sagecare-booking

Service Booking Application (Phase 01 - environment setup in progress).

## Tech Stack
- Frontend: React + Vite + JavaScript + Tailwind CSS
- Backend: FastAPI (Python)
- Database: PostgreSQL (local, managed with pgAdmin 4)

## Local Development

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Environment
- Copy `backend/.env.example` to `backend/.env` and set your PostgreSQL password (database name: `sagecare_db`).
- Copy `frontend/.env.example` to `frontend/.env` if needed.

### API Docs
- Swagger UI: http://localhost:8000/docs
- Health: http://localhost:8000/api/v1/health