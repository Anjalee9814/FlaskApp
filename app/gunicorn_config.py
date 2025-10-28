import os

workers = int(os.environ.get("GUNICORN_WORKERS", "2"))
threads = int(os.environ.get("GUNICORN_THREADS", "2"))
bind = os.environ.get("GUNICORN_BIND", "0.0.0.0:5000")
accesslog = os.environ.get("GUNICORN_ACCESS_LOG", "-")
errorlog = os.environ.get("GUNICORN_ERROR_LOG", "-")

# graceful settings
timeout = int(os.environ.get("GUNICORN_TIMEOUT", "30"))
worker_class = os.environ.get("GUNICORN_WORKER_CLASS", "sync")

# recommended defaults
keepalive = int(os.environ.get("GUNICORN_KEEPALIVE", "2"))

# Example: set GUNICORN_WORKERS=4 in docker-compose.yml environment to override
