# Bus Route Information System

**Wayfinder** is a route-discovery product concept built with React and Django. It explores a clear journey-planning workflow with origin/destination filters, route comparisons, stop sequences and a responsive interface.

> **Data status:** The included network is fictional sample data. This project is not connected to a transport operator, official timetable, GPS, GTFS feed or live vehicle service.

## Product capabilities
- Search sample routes by line, origin, destination or stop name.
- Filter by origin and destination, then sort by journey duration or sample frequency.
- Inspect stop-by-stop route details.
- Responsive route-planning workspace with API loading, empty and error states.
- Django-backed route records, seed command and query-filtered JSON endpoints.
- Original concept demo preserved at frontend/public/prototype.html.

## Runtime requirements\n- Node.js 22.12 or newer\n- Python 3.12 or newer (Python 3.13 is used in CI)\n\n## Technology
| Layer | Stack |
|---|---|
| Frontend | React 19.3.1, Vite 8.3.8, JavaScript |
| Backend | Django 6.1.3, Python |
| Data | Django ORM, SQLite locally, PostgreSQL via DATABASE_URL |
| API | JSON endpoints |
| Deployment | Vercel frontend, Python web host for API |

## Run locally

### 1. Django API
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

### 2. React frontend
```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal (normally http://localhost:5173). Vite proxies /api requests to Django on port 8000.

## API reference
| Method | Endpoint | Purpose |
|---|---|---|
| GET | /api/health/ | Health and framework version |
| GET | /api/routes/ | List demonstration routes |
| GET | /api/routes/?origin=Central%20Station | Filter by origin |
| GET | /api/routes/?destination=University | Filter by destination |
| GET | /api/routes/?q=museum | Search route, origin and destination |

The routes endpoint returns a JSON object containing count, items, source and disclaimer.

## Quality checks
```bash
cd backend
python manage.py check
python manage.py test
```
```bash
cd frontend
npm run build
```

GitHub Actions runs these checks on pushes to main and pull requests.

## Deployment notes
- Set the Vercel project root to frontend, build with npm run build and use dist as output.
- Set VITE_API_BASE_URL to the deployed Django API origin when building the frontend.
- Deploy backend as a Python web service with gunicorn config.wsgi:application.
- Configure DJANGO_SECRET_KEY, DJANGO_DEBUG=false, DJANGO_ALLOWED_HOSTS, CORS_ALLOWED_ORIGINS and a persistent PostgreSQL DATABASE_URL.
- Run python manage.py migrate and python manage.py seed_demo_data after deployment.

## Roadmap
1. Integrate licensed and verified timetable data for a defined region.
2. Add multi-leg journey planning and interchange rules.
3. Add service alerts only when an authoritative operator feed is available.
4. Add source timestamps, feed-health monitoring and stale-data states.
5. Validate accessibility and usability with public-transport users.

No actual journey should be planned using the fictional values in this prototype.