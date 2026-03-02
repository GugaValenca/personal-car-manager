# Personal Car Manager

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2-092E20?logo=django&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=000)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-Ready-000000?logo=vercel&logoColor=white)

Fullstack car management platform with Django backend plus Lovable React frontend for personal cars, taxi operation, and fleet cost control.

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

The project now includes:
- Django web interface for secure operations and admin workflows
- JSON API endpoints for frontend integration
- Lovable-generated React frontend in `frontend/` connected to backend data

## Features
- User-based car ownership (each user sees only their own cars)
- Car list and detail views
- Maintenance listing with cost and mileage
- Expense listing by type and amount
- Fuel records with liters, unit price, odometer and station
- Trip records with type, distance, passengers and income
- Dashboard with operational KPIs:
- total fuel cost
- trip distance
- trip income
- net balance (income - maintenance - expenses - fuel)
- API endpoint for frontend consumption: `/api/dashboard/`

## Screenshots
- Add screenshots in `docs/screenshots/` and reference them here:
- `Home page`
- `Dashboard`
- `Car detail`

## Tech Stack
- Backend: Python, Django 4.2
- Frontend (server-rendered): Django Templates, Bootstrap 5
- Frontend (SPA): React, TypeScript, Vite, Tailwind (Lovable export)
- Database: SQLite (default development database)
- Deployment: Vercel (`vercel.json` configured)

## Installation
```bash
git clone https://github.com/gugavalenca/personal-car-manager.git
cd personal-car-manager
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

Optional frontend setup:
```bash
cd frontend
npm install
```

## Usage
```bash
python manage.py runserver
```

Then open:
- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/admin/` (to add sample records quickly)

Frontend development (Lovable app):
```bash
cd frontend
npm run dev
```

By default, the frontend consumes backend metrics from:
- `http://127.0.0.1:8000/api/dashboard/`

## Project Structure
```text
personal-car-manager/
|-- car_manager/          # Django project settings and root URLs
|-- cars/                 # Domain app: models, views, URLs, tests
|-- frontend/             # Lovable React frontend integrated into this repo
|-- templates/cars/       # Server-rendered HTML templates
|-- static/               # Static assets
|-- manage.py
|-- requirements.txt
`-- vercel.json           # Vercel deployment config
```

## Technical Highlights / What I Learned
- Building owner-scoped queries with `request.user`
- Creating practical route tests for permissions and regressions
- Designing a hybrid architecture (Django + React frontend)
- Structuring APIs for dashboard metrics and operational summaries
- Modeling data for personal and fleet scenarios (fuel + trips + income)
- Preparing Django settings for local and cloud environments using environment variables

## Future Improvements
- Add role-based access (owner, driver, fleet manager)
- Add recurring costs and monthly budget alerts
- Add CSV export and PDF reports for accounting
- Add frontend auth flow with token/session refresh

## Contributing
Contributions are welcome. Open an issue to discuss improvements before submitting a pull request.

## License
This project is currently unlicensed. Add a `LICENSE` file if you want to define usage terms.

## Contact
- GitHub: https://github.com/gugavalenca
