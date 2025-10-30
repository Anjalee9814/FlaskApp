
# Flask Student Management System with PostgreSQL

<!-- CI badge -->
[![CI](https://github.com/Anjalee9814/FlaskApp/actions/workflows/ci.yml/badge.svg)](https://github.com/Anjalee9814/FlaskApp/actions/workflows/ci.yml)

**Release v0.1.0** — Flask + PostgreSQL Docker Compose example with student management form (Gunicorn, DB init, Adminer, tests, CI).

## Overview

This project demonstrates a Flask web application with PostgreSQL database, fully containerized with Docker and orchestrated using Docker Compose. The app includes a student management system where you can add and view student records.

### Features
- ✅ Student management web form (add students with name, age, email, course)
- ✅ View all students (web UI and JSON API)
- ✅ PostgreSQL database with auto-initialization
- ✅ Adminer database UI for direct database access
- ✅ Health check endpoint
- ✅ Production-ready with Gunicorn WSGI server
- ✅ Automated tests and CI/CD with GitHub Actions

## Prerequisites

Before you begin, ensure you have the following installed on your system:

1. **Docker Desktop** (required)
   - Download from: https://www.docker.com/products/docker-desktop
   - **Windows**: Docker Desktop for Windows
   - **macOS**: Docker Desktop for Mac
   - **Linux**: Docker Engine + Docker Compose

2. **Git** (to clone the repository)
   - Download from: https://git-scm.com/downloads

## Getting Started

### Step 1: Clone the Repository

Open your terminal (PowerShell on Windows, Terminal on macOS/Linux) and run:

```bash
git clone https://github.com/Anjalee9814/FlaskApp.git
cd FlaskApp
```

### Step 2: Start Docker Desktop

- **Windows/macOS**: Launch Docker Desktop from your Applications menu
- **Linux**: Ensure Docker daemon is running: `sudo systemctl start docker`
- Wait until Docker Desktop shows "Engine running" status (usually 10-30 seconds)

### Step 3: Build and Run the Application

#### For Windows (PowerShell):

```powershell
# Navigate to the project directory
cd FlaskApp

# Build and start all services
docker compose up --build -d

# Wait a few seconds for services to initialize
Start-Sleep -Seconds 10

# Check if services are running
docker compose ps
```

#### For macOS/Linux (Terminal):

```bash
# Navigate to the project directory
cd FlaskApp

# Build and start all services
docker compose up --build -d

# Wait a few seconds for services to initialize
sleep 10

# Check if services are running
docker compose ps
```

### Step 4: Access the Application

Once the services are running, open your web browser and visit:

- **Student Management Form**: http://localhost:5000/
  - Add new students with name, age, email, and course
  - View recently added students
  
- **All Students (JSON API)**: http://localhost:5000/students
  - Get all students in JSON format

- **Health Check**: http://localhost:5000/health
  - Check if the application is running

- **Adminer (Database UI)**: http://localhost:8080/
  - Direct database access and management
  - Login credentials:
    - **System**: PostgreSQL
    - **Server**: db
    - **Username**: student
    - **Password**: student123
    - **Database**: studentdb

### Step 5: Stop the Application

When you're done, stop all services:

```powershell
# Windows PowerShell
docker compose down
```

```bash
# macOS/Linux
docker compose down
```

```bash
# macOS/Linux
docker compose down
```

## Troubleshooting

### Docker Desktop Not Running
**Error**: `error during connect: ... The system cannot find the file specified`

**Solution**: 
1. Start Docker Desktop application
2. Wait for "Engine running" status
3. Try the `docker compose up` command again

### Port Already in Use
**Error**: `Bind for 0.0.0.0:5000 failed: port is already allocated`

**Solution**:
```powershell
# Find what's using the port (Windows PowerShell)
Get-NetTCPConnection -LocalPort 5000

# Or stop any existing containers
docker compose down
```

### Services Not Starting
**Solution**:
```powershell
# View logs to see what's wrong
docker compose logs

# View logs for a specific service
docker compose logs web
docker compose logs db
```

### Database Connection Errors
**Solution**: The database might still be initializing. Wait 10-15 seconds and refresh the page.

## Project Structure

```
FlaskApp/
├── app/
│   ├── app.py                 # Main Flask application
│   ├── init_db.py            # Database initialization script
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile            # Multi-stage Docker build
│   ├── gunicorn_config.py    # Gunicorn WSGI server config
│   ├── healthcheck.py        # Health check script
│   └── tests/                # Unit and integration tests
├── docker-compose.yml         # Docker Compose orchestration
├── .gitignore                # Git ignore rules
├── README.md                 # This file
└── scripts/
    └── tasks.ps1             # PowerShell helper scripts
```

## Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Student management form (add and view students) |
| `/add-student` | POST | Add a new student (form submission) |
| `/students` | GET | Get all students as JSON |
| `/health` | GET | Health check endpoint |
| `/data` | GET | Get greeting message from database |

## Database Schema

### Students Table
```sql
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INTEGER NOT NULL,
    email VARCHAR(100) NOT NULL,
    course VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Development

### Running Tests Locally

First, create a Python virtual environment and install dependencies:

**Windows PowerShell:**
```powershell
python -m venv app\.venv
.\app\.venv\Scripts\Activate.ps1
pip install -r app\requirements.txt

# Run unit tests
pytest app/tests/test_app.py

# Run integration tests (requires running containers)
pytest app/tests/test_integration.py
```

**macOS/Linux:**
```bash
python3 -m venv app/.venv
source app/.venv/bin/activate
pip install -r app/requirements.txt

# Run unit tests
pytest app/tests/test_app.py

# Run integration tests (requires running containers)
pytest app/tests/test_integration.py
```

### Viewing Logs

```bash
# View all logs
docker compose logs

# Follow logs in real-time
docker compose logs -f

# View logs for specific service
docker compose logs web
docker compose logs db
```

### Rebuild After Code Changes

If you modify the code, rebuild and restart:

```bash
docker compose up --build -d
```

## Advanced Usage

### Using PowerShell Helper Script (Windows)

The project includes a helper script for common tasks:

```powershell
# Build images
.\scripts\tasks.ps1 -Task build

# Start services
.\scripts\tasks.ps1 -Task up

# Run all (start, test, logs, stop)
.\scripts\tasks.ps1 -Task run-all

# Stop services
.\scripts\tasks.ps1 -Task down
```

### Using Makefile (macOS/Linux)

```bash
make build          # Build images
make up             # Start services
make down           # Stop services
make test-unit      # Run unit tests
make test-integration  # Run integration tests
```

### Environment Variables

You can customize the application by modifying `docker-compose.yml`:

- `DATABASE_URL`: PostgreSQL connection string
- `GUNICORN_WORKERS`: Number of Gunicorn worker processes (default: 2)

## Technologies Used

- **Flask 2.2.5** - Web framework
- **PostgreSQL 14** - Database
- **Gunicorn 20.1.0** - WSGI HTTP server
- **Docker & Docker Compose** - Containerization
- **Adminer** - Database management UI
- **pytest** - Testing framework
- **GitHub Actions** - CI/CD

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available for educational purposes.

## Contact

- **Author**: Anjalee9814
- **Repository**: https://github.com/Anjalee9814/FlaskApp
- **Issues**: https://github.com/Anjalee9814/FlaskApp/issues

## Acknowledgments

- Flask documentation: https://flask.palletsprojects.com/
- Docker documentation: https://docs.docker.com/
- PostgreSQL documentation: https://www.postgresql.org/docs/

