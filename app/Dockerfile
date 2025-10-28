FROM python:3.10-slim as builder

WORKDIR /install

# Install build deps for packages that might need compilation
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
# Install into the system site-packages path under /usr/local so the final image
# picks up packages without extra PYTHONPATH fiddling
RUN pip install --no-cache-dir -r requirements.txt --prefix /install

FROM python:3.10-slim

WORKDIR /app

# Copy installed site-packages from builder to the same system location
# Copy installed files (including console scripts) from builder prefix into /usr/local
COPY --from=builder /install /usr/local

# Copy application sources
COPY . .

# Remove apt lists if any leftover
RUN rm -rf /var/lib/apt/lists/* || true

EXPOSE 5000

# Run gunicorn with external config (app/gunicorn_config.py)
CMD ["gunicorn", "-c", "gunicorn_config.py", "app:app"]
