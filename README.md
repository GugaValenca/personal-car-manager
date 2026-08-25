# Personal Car Manager

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2-092E20?logo=django&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=000)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-Ready-000000?logo=vercel&logoColor=white)

Fullstack car management platform with Django backend plus React frontend for personal cars, taxi operation, and fleet cost control.

## Live Demo + Repository Links
- Live Demo (Vercel): https://personal-car-manager.vercel.app
- Production URL: https://personal-car-manager-39n0p06uu-gugavalencas-projects.vercel.app
- Repository: https://github.com/gugavalenca/personal-car-manager

## Overview
Personal Car Manager is a realistic fullstack portfolio project focused on common daily workflows:
- Registering vehicles
- Monitoring maintenance records
- Tracking expenses by car
- Logging fuel records and trip operation data
- Measuring income vs. cost for taxi and fleet scenarios

**Architecture note:** this is a Django server-rendered app (Bootstrap templates)
for everything past login — dashboard, cars, maintenance, expenses, fuel,
trips. The React app in `frontend/` renders only the landing page, the sign-in
card, and the signup/admin-login screens; it is not a full SPA consuming the
data endpoints below. `frontend/src/pages/Index.tsx` and
`frontend/src/components/LoginCard.tsx` are the actual entry points.

The project includes:
- Django web interface for all authenticated CRUD operations
- A JSON endpoint (`/api/dashboard/`) exposing dashboard metrics, currently
  unused by any client — a starting point for a real API, not a finished one
- A React (Vite) auth shell for login/signup, pre-built and served by Django

## Features
- User-based car ownership (each user sees only their own cars)
- Car list and detail views
- Maintenance listing with cost and mileage
- Expense listing by type and amount
- Fuel records with liters, unit price, odometer and station
- Trip records with type, distance, passengers and income
- Native UI forms (no admin required) for:
- add car
- add maintenance record
- add expense
- add fuel record
- add trip
- Dashboard with operational KPIs:
- total fuel cost
- trip distance
- trip income
- net balance (income - maintenance - expenses - fuel)
- JSON endpoint for dashboard metrics: `/api/dashboard/` (not yet consumed by a client)

## Screenshots
- Add screenshots in `docs/screenshots/` and reference them here:
- `Home page`
- `Dashboard`
- `Car detail`

## Tech Stack
- Backend: Python, Django 4.2
- Frontend (server-rendered, all authenticated pages): Django Templates, Bootstrap 5
- Frontend (auth screens only): React, TypeScript, Vite, Tailwind
- Database: SQLite locally by default; Postgres in production via `DATABASE_URL`
  (see [Environment variables](#environment-variables) — SQLite does **not**
  persist reliably on Vercel's serverless filesystem)
- Deployment: Vercel (`vercel.json` configured)
- CI: GitHub Actions (`.github/workflows/ci.yml`) runs the Django test suite
  and the frontend lint/typecheck/test/build on every push and PR

## Environment variables
Copy `.env.example` to `.env` for local development (or export the variables
directly). See that file for the full list and defaults; the two you actually
need to set for a real deployment are `DJANGO_SECRET_KEY` and `DATABASE_URL`.

## Installation
```bash
git clone https://github.com/gugavalenca/personal-car-manager.git
cd personal-car-manager
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # then edit as needed; DJANGO_DEBUG=True is enough locally
python manage.py migrate
python manage.py createsuperuser
```

Frontend setup (only needed if you're changing the login/signup screens —
the compiled output is already committed under `static/app/`):
```bash
cd frontend
npm install
npm run build   # writes frontend/dist/, copy assets + manifest.json into static/app/
```

## Usage
```bash
python manage.py runserver
```

Then open:
- `http://127.0.0.1:8000/` (React login screen)
- `http://127.0.0.1:8000/dashboard/`
- `http://127.0.0.1:8000/admin/` (to add sample records quickly)
- `http://127.0.0.1:8000/cars/new/`
- `http://127.0.0.1:8000/maintenances/new/`
- `http://127.0.0.1:8000/expenses/new/`
- `http://127.0.0.1:8000/fuel-records/new/`
- `http://127.0.0.1:8000/trips/new/`

Frontend development (only the login/signup screens live here — `npm run dev`
starts Vite's own dev server on port 8080, separate from Django):
```bash
cd frontend
npm run dev
```

## Project Structure
```text
personal-car-manager/
|-- .github/workflows/    # CI: Django tests + frontend lint/test/build
|-- car_manager/          # Django project settings and root URLs
|-- cars/                 # Domain app: models, views, URLs, tests
|   `-- templatetags/     # Resolves the built SPA's hashed filenames
|-- frontend/             # React auth shell (login/signup/admin-login only)
|-- templates/            # Server-rendered HTML templates (Bootstrap)
|-- static/                # Static assets, including the compiled SPA bundle
|-- manage.py
|-- requirements.txt
|-- .env.example          # Documents every environment variable the app reads
`-- vercel.json           # Vercel deployment config
```

## Technical Highlights / What I Learned
- Building owner-scoped queries with `request.user`, with a regression test
  proving one user cannot read another user's car (`cars/tests.py`)
- Creating practical route tests for permissions, pagination, CSRF, and the
  compiled-asset resolution described below
- Designing a hybrid architecture (Django server-rendered app + a React auth
  shell) and being explicit in this README about where that split actually is
- Fixing a login CSRF gap (the SPA login endpoint was `@csrf_exempt`) by
  wiring `ensure_csrf_cookie` + a `X-CSRFToken` header instead
- Avoiding hardcoded build hashes: a small template tag
  (`cars/templatetags/vite_assets.py`) reads Vite's `manifest.json` so the
  Django templates always point at whatever was last built
- Preparing Django settings for local and cloud environments using
  environment variables, including a fail-closed `SECRET_KEY`/`DEBUG` default
  and a `DATABASE_URL`-driven switch between SQLite and Postgres

## Future Improvements
- Add role-based access (owner, driver, fleet manager)
- Add recurring costs and monthly budget alerts
- Add CSV export and PDF reports for accounting
- Turn `/api/dashboard/` into a real API (DRF, pagination, OpenAPI docs) and
  actually consume it from a client
- Add demo/seed data so the live deployment isn't empty on first visit

## Contributing
Contributions are welcome. Open an issue to discuss improvements before submitting a pull request.

## License
MIT — see [LICENSE](LICENSE).

## Contact
- GitHub: https://github.com/gugavalenca
