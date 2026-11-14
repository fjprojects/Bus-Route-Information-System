# Bus Route Information System

**Wayfinder** is a route-discovery product concept built with React and Django. It focuses on a clear journey-planning workflow: choose an origin and destination, compare route options, inspect stop sequences and understand sample service frequency.

> **Data status:** The network in this repository is fictional sample data. It is not connected to a transport operator, official timetable, GPS, GTFS feed or live vehicle service. Do not use the estimates to plan a real journey.

## Live deployment

- **Frontend:** https://wayfinder-route-explorer.vercel.app
- **Django API:** https://wayfinder-api-wkuw.onrender.com
- **Health endpoint:** https://wayfinder-api-wkuw.onrender.com/api/health/

The frontend is hosted on Vercel. The Django API is hosted as a Docker web service on Render.

## Product capabilities

- Search route names, origins, destinations and intermediate stops.
- Filter by origin and destination with case-insensitive matching.
- Sort by sample journey duration, sample service frequency or route name, in ascending or descending order.
- Retrieve distinct stop/location suggestions and individual route details.
- Paginated, validated JSON responses with structured errors.
- Database-aware health reporting and read-only route access.
- Responsive route-planning interface with loading, empty and error states.
- Original concept page preserved at `frontend/public/prototype.html`.

## Technology

| Layer | Stack |
|---|---|
| Frontend | React 19.3.1, Vite 8.3.8, JavaScript |
| Backend | Django 6.1.3, Python 3.13 |
| Data | Django ORM, SQLite for the sample deployment |
| API | Read-only JSON endpoints |
| Hosting | Vercel frontend, Render Docker API |
| CI | GitHub Actions |

## Runtime requirements

- Node.js 22.12 or newer
- Python 3.12 or newer (Python 3.13 is used in CI and deployment)

## Run locally

### 1. Start the Django API

```bash
cd backend
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo_data
python manage.py runserver 8000
```

### 2. Start the React frontend

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL printed in the terminal (normally `http://localhost:5173`). The Vite development server proxies `/api` requests to Django on port 8000.

## API reference

All endpoints are read-only and accept GET requests.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health/` | Framework and database connectivity |
| GET | `/api/routes/` | List demonstration routes |
| GET | `/api/routes/?origin=Central%20Station` | Filter by origin |
| GET | `/api/routes/?destination=University` | Filter by destination |
| GET | `/api/routes/?q=museum` | Search route names, endpoints and intermediate stops |
| GET | `/api/routes/?sort=frequency&order=desc` | Sort by duration, frequency or name |
| GET | `/api/routes/locations/` | Return distinct origins, destinations and intermediate stops |
| GET | `/api/routes/blue-line/` | Retrieve one route by its identifier |

### Pagination and validation

- `page` is a positive integer (default `1`).
- `page_size` is an integer from `1` to `100` (default `25`).
- `count` reports the total number of matched routes; `items` contains only the requested page.
- Invalid query values return HTTP 400 with a structured `error` object; missing route identifiers return HTTP 404.
- `sort` accepts `duration`, `frequency` or `name`; `order` accepts `asc` or `desc`.

Responses include the fictional-data source and disclaimer. Write methods are not enabled.

## Quality checks

Backend:

```bash
cd backend
python -m pip install -r requirements.txt
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

Frontend:

```bash
cd frontend
npm install
npm test
npm run build
```

GitHub Actions runs the frontend tests/build and Django checks/tests on pushes to `main` and pull requests.

## Deployment configuration

- **Vercel frontend root:** `frontend/`
- **Vercel build:** `npm run build`
- **Vercel output:** `dist/`
- **Frontend API variable:** `VITE_API_BASE_URL=https://wayfinder-api-wkuw.onrender.com`
- **Render runtime:** Docker, using `backend/Dockerfile`
- **Render startup:** applies migrations, loads the fictional route catalogue and starts Gunicorn.
- Configure `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=false`, `DJANGO_ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS` in the backend environment. The production CORS allowlist should contain only the deployed frontend origin.

The current API is a read-only demonstration service. The bundled SQLite database is seeded on startup and is not a persistent transit-data store.

## Roadmap

1. Integrate licensed and verified timetable data for a defined region.
2. Add multi-leg journey planning and interchange rules.
3. Add service alerts only when an authoritative operator feed is available.
4. Include feed timestamps, provenance, freshness and stale-data handling.
5. Validate accessibility and usability with public-transport users.

No actual journey should be planned using the fictional values in this prototype.
