# Personal Car Manager

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2-092E20?logo=django&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=000)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?logo=postgresql&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-Deployed-000000?logo=vercel&logoColor=white)

A Django + React app for keeping track of vehicle costs — maintenance, fuel, insurance, and trips — built with taxi/ride-share and small delivery fleets in mind as much as a regular personal car.

## Try it live
**https://personal-car-manager.vercel.app**

Log in with `demo` / `demo12345`. It comes preloaded with three cars (a personal daily driver, a ride-share car, and a delivery truck) so the dashboard actually has something to look at instead of a blank slate. Feel free to poke around, add a trip or a fuel record — nothing will break, and I reset the seed data occasionally.

## What it actually does
Register a car, log its maintenance history, track what you spend on it (insurance, registration, parking, whatever), and if you drive for a living, log trips with income so you can see net balance per car — not just costs. The dashboard rolls all of that up: total spend, fuel cost, trip income, distance, and the bottom line.

Everything is scoped to the logged-in user. I added a test early on specifically to prove that user A can't pull up user B's car by guessing an ID (`cars/tests.py`, `test_user_cannot_access_another_users_car_detail`) — it's a small thing but it's the kind of bug that's easy to introduce by accident in a Django app with plain `pk` lookups, so I wanted it locked down and tested rather than just "probably fine."

## About the architecture, honestly
This isn't a React SPA talking to a Django API, even though the tech stack badges above might suggest that. Once you're logged in, the whole app — dashboard, car list, every form — is server-rendered Django with Bootstrap. React only handles the landing page and the sign-in card (`frontend/src/pages/Index.tsx` and `frontend/src/components/LoginCard.tsx`); it's built once with Vite and the compiled output gets served by Django directly.

I went back and forth on whether to keep it this way or "finish the job" and turn it into a real SPA. I decided against it — the CRUD flows here don't need client-side routing or optimistic updates, and building a second UI layer just to say "it's a SPA" would have been complexity for its own sake. There used to be a `/api/dashboard/` JSON endpoint sitting here unused, a leftover from when I was considering that direction — I ended up removing it rather than leaving dead code around just in case.

## Stack
- **Backend:** Python, Django 4.2
- **Frontend (the actual app):** Django templates, Bootstrap 5
- **Frontend (login/signup only):** React, TypeScript, Vite, Tailwind
- **Database:** PostgreSQL in production, SQLite for local dev (see below for why)
- **Auth hardening:** `django-axes` for login lockout, CSRF enforced on the SPA login endpoint, secure cookies + HSTS in production
- **Deploy:** Vercel
- **CI:** GitHub Actions runs the Django test suite and the frontend lint/typecheck/test/build on every push

## Running it locally
```bash
git clone https://github.com/gugavalenca/personal-car-manager.git
cd personal-car-manager
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py seed_demo_data     # optional, but the dashboard is a lot more interesting with data in it
python manage.py runserver
```

Then just open `http://127.0.0.1:8000/` and log in with the demo account (same credentials as the live site), or run `python manage.py createsuperuser` and start from a clean account.

A couple of things worth knowing before you dig in:

- **The database.** SQLite works fine locally, but Vercel's serverless functions have a filesystem that doesn't persist between deploys — data written there just disappears. That's why production uses a real Postgres instance via `DATABASE_URL`, and SQLite stays as the zero-config local default. Both are wired up through the same `dj_database_url.config()` call in `car_manager/settings.py`.
- **Environment variables.** `.env.example` documents everything the app reads. The only two that actually matter for a real deployment are `DJANGO_SECRET_KEY` and `DATABASE_URL` — everything else has a sane default.
- **The frontend build.** You don't need Node installed just to run the Django app — the compiled React output is already committed under `static/app/`. You'd only need `cd frontend && npm install && npm run build` if you're changing the login/signup screens themselves, and then copying the new build output + `manifest.json` into `static/app/` (there's a small template tag that reads the manifest so the Django templates never hardcode a filename).

## Project layout
```text
personal-car-manager/
├── .github/workflows/     CI: backend tests + frontend lint/test/build
├── car_manager/           Django project settings, root urls
├── cars/                  the actual app - models, views, forms, admin, tests
│   ├── management/        seed_demo_data command
│   └── templatetags/      resolves the built SPA's hashed filenames
├── frontend/               React, but only for login/signup/admin-login
├── templates/              server-rendered pages (everything past login)
├── static/                 css, favicon, and the compiled SPA bundle
├── requirements.txt
├── .env.example
└── vercel.json
```

## Things I'd still like to add
- A real permissions layer (owner / driver / fleet manager, instead of just "owner")
- Recurring expenses and a monthly budget view
- CSV export for anyone who wants to hand this data to an accountant

## License
MIT — see [LICENSE](LICENSE).

## Contact
GitHub: [github.com/gugavalenca](https://github.com/gugavalenca)
