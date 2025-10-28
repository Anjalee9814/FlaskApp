
# Flask with PostgreSQL (Docker + Docker Compose)

<!-- CI badge: replace OWNER/REPO in the URL below with your GitHub repository to enable the badge -->
[![CI](https://github.com/Anjalee9814/FlaskApp/actions/workflows/ci.yml/badge.svg)](https://github.com/Anjalee9814/FlaskApp/actions/workflows/ci.yml)

This small project demonstrates a Flask app containerized with Docker and using PostgreSQL via Docker Compose.

Location: The project folder is `flask-docker`.

Quick start (Windows PowerShell):

1. Open PowerShell and change to the project directory:

```powershell
cd "c:\Users\Anjalee Himalki\Desktop\cloud assignment PaaS\flask-docker"
```

2. Build and start the services:

```powershell
docker-compose up --build
```

3. Visit the app:

- Home: http://localhost:5000
- Data from DB: http://localhost:5000/data

4. Stop the stack:

```powershell
docker-compose down
```

- Notes:
- The database initialization is run by a one-shot Compose service named `initdb` (it runs `python init_db.py`). The `web` service depends on `initdb` so the DB will be seeded before the app starts.
- Database connection is provided via the `DATABASE_URL` env var defined in `docker-compose.yml`.
- Adminer is included on port `8080` for a lightweight DB GUI. Use the following to log in:

	- System / Server: postgres or leave blank (Adminer will use the host below)
	- Server: `db`
	- Username: `student`
	- Password: `student123`
	- Database: `studentdb`

	Open Adminer at: http://localhost:8080
- If you change code, rebuild with `docker-compose up --build`.

Troubleshooting:
- If the web service fails with DB connection errors, wait a few seconds and restart; `depends_on` ensures ordering but not readiness. The `init_db.py` script retries until the DB accepts connections.

Quick helper (PowerShell)
-------------------------
I added a small helper script `scripts/tasks.ps1` to speed up common tasks. Example usages (from project root):

```powershell
# Build images
.\scripts\tasks.ps1 -Task build

# Start the stack in detached mode
.\scripts\tasks.ps1 -Task up

# Run unit tests
.\scripts\tasks.ps1 -Task test-unit

# Run integration test (brings stack up, runs test, tears down)
.\scripts\tasks.ps1 -Task test-integration

# Full run (up -> wait for health -> integration test -> logs -> down)
.\scripts\tasks.ps1 -Task run-all

# Tear down
.\scripts\tasks.ps1 -Task down
```

This script assumes you have the project venv at `app/.venv` (see earlier steps to create and install requirements).

Makefile & gunicorn notes
-------------------------
- There's a `Makefile` at the project root with convenience targets: `make build`, `make up`, `make down`, `make test-unit`, `make test-integration`. This is intended for macOS / Linux users; Windows users should use `scripts/tasks.ps1` or WSL.

- The app container now runs Gunicorn (configured via `app/gunicorn_config.py`). You can change the number of workers by setting the `GUNICORN_WORKERS` environment variable in `docker-compose.yml` or your host environment.
 - The app container now runs Gunicorn (configured via `app/gunicorn_config.py`). You can change the number of workers by setting the `GUNICORN_WORKERS` environment variable in `docker-compose.yml` or your host environment.

