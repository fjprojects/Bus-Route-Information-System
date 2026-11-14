# Bus Route Information System

A **React + Django** starter for a public-transport route assistant.

## Stack
- React 19.3 + Vite 8 frontend
- Django 6.1 JSON API
- Vite proxies local `/api` calls to Django on port 8000

## Structure
- `frontend/` — React application and preserved earlier prototype at `public/prototype.html`
- `backend/` — Django project and JSON endpoints

## Run locally

### Terminal 1 — Django API
```bash
cd backend
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py runserver 8000
```

### Terminal 2 — React frontend
```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL printed in the terminal (normally `http://localhost:5173`). The React page fetches `GET /api/health/` and `GET /api/routes/`.

## Production configuration
Set `VITE_API_BASE_URL` in `frontend/.env.local` to the deployed Django backend URL before building. On the backend configure `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=false`, `DJANGO_ALLOWED_HOSTS`, and `CORS_ALLOWED_ORIGINS`.

## Data limitations
All route names, stops, frequencies and journey times are fictional sample data. This API is not connected to a transport operator, official timetable, GPS or live vehicle feed. The earlier Wayfinder page is preserved separately; its UI has not yet been rewritten as React components.
