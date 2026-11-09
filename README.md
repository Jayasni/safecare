# Healora – Healthcare Appointment Booking Platform

**Healthcare, made simpler.**

Healora is a modern healthcare appointment booking platform designed to simplify the process of discovering hospitals, exploring medical services, finding doctors, and managing appointments.

The platform provides role-based access for administrators, doctors, and patients, with a React frontend and a FastAPI backend.

## Features

### Authentication & Authorization
- User registration and login.
- JWT-based authentication.
- Role-based access control.
- Access management for Admin, Doctor, and Patient roles.
- Token-based protected API endpoints.

### Hospital Management
- Create, view, update, and deactivate hospitals.
- Manage hospital information and contact details.
- Support multiple hospitals.

### Medical Services Management
- Manage healthcare services offered by hospitals.
- Associate doctors with hospitals and medical services.

### Doctor Management
- Manage doctor profiles.
- Assign doctors to hospitals.
- Associate doctors with specific medical services.

### Doctor Availability
- Manage doctor availability by hospital.
- Configure available days and schedules.

### Appointment Management
- Book appointments with doctors.
- Associate appointments with hospitals and medical services.
- Manage appointment information and status.

### Dashboards
- Admin dashboard for management activities.
- Patient dashboard for appointment-related activities.
- Doctor dashboard for doctor-related activities.

## Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | React, Vite, JavaScript (JSX) |
| Styling | Tailwind CSS |
| Routing | React Router |
| HTTP Client | Axios |
| Icons | Lucide React |
| Backend | Python, FastAPI |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Authentication | JWT, Argon2 |
| API Documentation | Swagger UI |
| Database Migrations | Alembic |
| Testing | Pytest, Vitest |
| Version Control | Git, GitHub |

## Project Architecture

Healora follows a layered backend architecture.

```text
Frontend (React + Vite)
        |
        | HTTP Requests (Axios)
        v
Backend (FastAPI)
        |
        v
API Routers
        |
        v
Service Layer
        |
        v
Repository Layer
        |
        v
SQLAlchemy ORM
        |
        v
PostgreSQL Database
```

### Backend Architecture

- **Routers:** Handle HTTP requests and API endpoints.
- **Schemas:** Validate request and response data using Pydantic.
- **Services:** Implement business logic.
- **Repositories:** Handle database operations.
- **Models:** Define database tables and relationships.
- **Core:** Contains application configuration and security functionality.

## Project Structure

```text
Healora/
│
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── routers/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── tests/
│   │   ├── utils/
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   └── main.py
│   │
│   ├── alembic/
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── assets/
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── .env.example
│
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

Install the following before running the project:

- Python 3.10+
- Node.js and npm
- PostgreSQL
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Jayasni/safecare.git
cd safecare
```

### 2. Backend Setup

Open a terminal:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file inside the backend directory.

Configure your PostgreSQL connection string and authentication settings according to the project's backend configuration.

Example database connection format:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/healora_db
```

Use your own secure credentials and secret keys. Never commit `.env` files to GitHub.

### 4. Database Setup

Make sure PostgreSQL is running and the `healora_db` database exists.

Run database migrations using Alembic:

```bash
alembic upgrade head
```

### 5. Start the Backend

```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

Backend URL:

http://127.0.0.1:8001

Swagger API Documentation:

http://127.0.0.1:8001/docs

### 6. Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Frontend URL:

http://localhost:5173

## API Modules

The backend provides API modules for:

| Module | Purpose |
|---|---|
| Authentication | Registration, login, and token management |
| Users | User management |
| Doctors | Doctor profile management |
| Hospitals | Hospital management |
| Medical Services | Healthcare service management |
| Doctor Assignments | Doctor-hospital relationships |
| Availability | Doctor scheduling |
| Appointments | Appointment booking and management |
| Admin | Administrative operations |

API documentation is available through Swagger UI at `/docs`.

## User Roles

**Admin**
- Manage hospitals and healthcare services.
- Manage doctors and assignments.
- Access administrative features.

**Doctor**
- Access doctor-related functionality.
- Manage availability and appointments.

**Patient**
- Register and log in.
- Explore healthcare services.
- Book and manage appointments.

## Design Theme

Healora uses a warm, professional healthcare-inspired design.

| Color | Hex Code |
|---|---|
| Warm Ivory | `#F5F3EB` |
| Sage Green | `#78917B` |
| Primary Text | `#29352D` |
| Secondary Text | `#69766B` |
| White | `#FFFFFF` |
| Light Sage | `#E5ECE4` |

## Security

- JWT-based authentication.
- Password hashing using Argon2.
- Role-based authorization.
- Environment variables for sensitive configuration.
- Protected administrative endpoints.

## Future Enhancements

- Online payment integration.
- Email and appointment notifications.
- Advanced appointment search and filtering.
- Doctor reviews and ratings.
- Appointment reminders.
- Advanced analytics and reports.
- Production deployment and monitoring.

## Author

**Jayasni Thota**

GitHub: https://github.com/Jayasni

## Project Repository

https://github.com/Jayasni/safecare

---

*Healora – Healthcare, made simpler.*
