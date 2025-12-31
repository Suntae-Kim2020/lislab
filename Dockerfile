# Django Backend Dockerfile for Cloud Run
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add Cloud SQL Proxy support
RUN pip install --no-cache-dir cloud-sql-python-connector[pg8000]

# Copy project
COPY . .

# Create necessary directories
RUN mkdir -p /app/static /app/staticfiles /app/media

# Create entrypoint script
RUN echo '#!/bin/bash\n\
set -e\n\
echo "Running database migrations..."\n\
python manage.py migrate --noinput\n\
echo "Collecting static files..."\n\
python manage.py collectstatic --noinput\n\
echo "Starting server..."\n\
exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 0\n\
' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Create a non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Run entrypoint script
CMD ["/app/entrypoint.sh"]
