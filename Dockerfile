FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (no deprecated apt-key usage)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy and set up entrypoint script first
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Copy migration-related files
COPY alembic.ini migrate.py ./
COPY alembic ./alembic

# Copy the rest of the application
COPY . .

# Ensure entrypoint has correct permissions (in case COPY . overwrote it)
RUN chmod +x /app/entrypoint.sh

# Expose the port the app runs on
EXPOSE 3000

# Use entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"] 