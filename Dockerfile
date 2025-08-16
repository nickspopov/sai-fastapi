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

# Copy migration-related files first
COPY alembic.ini migrate.py ./
COPY alembic ./alembic

# Copy the rest of the application
COPY . .

# Debug: List contents to verify files
RUN ls -la /app && \
    echo "Contents of /app/alembic:" && \
    ls -la /app/alembic

# Expose the port the app runs on
EXPOSE 3000

# ENTRYPOINT ["sh", "-c", "\
#     if [ \"$CHECK_DB_CONNECTION\" = \"true\" ]; then \
#         echo 'Waiting for PostgreSQL to be ready...' && \
#         while ! pg_isready -h postgres -U postgres; do \
#             sleep 1; \
#         done; \
#     fi && \
#     echo 'Running database migrations...' && \
#     python migrate.py upgrade && \
#     echo 'Starting FastAPI application...' && \
#     exec uvicorn main:app --host 0.0.0.0 --port 3000 \
# "] 
# Set the entrypoint script
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"] 