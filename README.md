# Personal Car Manager

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2-092E20?logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-Ready-000000?logo=vercel&logoColor=white)

Simple Django app to manage cars, maintenance history, and vehicle-related expenses in one place.

## Live Demo + Repository Links
- Live Demo (Vercel): https://personal-car-manager.vercel.app
- Production URL: https://personal-car-manager-39n0p06uu-gugavalencas-projects.vercel.app
- Repository: https://github.com/gugavalenca/personal-car-manager

## Overview
Personal Car Manager is a realistic fullstack portfolio project focused on common daily workflows:
- Registering vehicles
- Monitoring maintenance records
- Tracking expenses by car
- Viewing simple dashboard totals

The project uses Django templates and server-rendered pages for a clean and interview-friendly architecture.

## Features
- User-based car ownership (each user sees only their own cars)
- Car list and detail views
- Maintenance listing with cost and mileage
- Expense listing by type and amount
- Dashboard with totals for cars, maintenances, and expenses

## Screenshots
- Add screenshots in `docs/screenshots/` and reference them here:
- `Home page`
- `Dashboard`
- `Car detail`

## Tech Stack
- Backend: Python, Django 4.2
- Frontend: Django Templates, Bootstrap 5
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

## Usage
```bash
python manage.py runserver
```

Then open:
- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/admin/` (to add sample records quickly)

## Project Structure
```text
personal-car-manager/
|-- car_manager/          # Django project settings and root URLs
|-- cars/                 # Domain app: models, views, URLs, tests
|-- templates/cars/       # Server-rendered HTML templates
|-- static/               # Static assets
|-- manage.py
|-- requirements.txt
`-- vercel.json           # Vercel deployment config
```

## Technical Highlights / What I Learned
- Building owner-scoped queries with `request.user`
- Creating practical route tests for permissions and regressions
- Structuring Django templates for list/detail pages
- Preparing Django settings for local and cloud environments using environment variables

## Future Improvements
- Add create/edit forms outside Django Admin
- Add filters (date range, expense type, car make/model)
- Add pagination for maintenance and expense lists
- Add screenshot assets and UI polish

## Contributing
Contributions are welcome. Open an issue to discuss improvements before submitting a pull request.

## License
This project is currently unlicensed. Add a `LICENSE` file if you want to define usage terms.

## Contact
- GitHub: https://github.com/gugavalenca
