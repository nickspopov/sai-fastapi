#!/bin/sh

# Debug information
echo "Current directory: $(pwd)"
echo "Contents of current directory:"
ls -la
echo "Script location: $0"
echo "Script permissions:"
ls -l $0

# Check if we need to wait for postgres
if [ "$CHECK_DB_CONNECTION" = "true" ]; then
    # Wait for postgres to be ready
    echo "Waiting for PostgreSQL to be ready..."
    while ! pg_isready -h postgres -U postgres; do
        sleep 1
    done
fi

# Run migrations
echo "Running database migrations..."
python migrate.py upgrade

# Start the application
echo "Starting FastAPI application..."
exec uvicorn main:app --host 0.0.0.0 --port 3000 