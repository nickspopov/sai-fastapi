#!/bin/bash
set -e

# echo "Waiting for PostgreSQL to be ready..."
# until pg_isready -h postgres -U postgres; do
#   echo "PostgreSQL is unavailable - sleeping"
#   sleep 1
# done

# echo "PostgreSQL is ready!"

# echo "Running database migrations..."
# python migrate.py upgrade

# if [ $? -eq 0 ]; then
#   echo "Database migrations completed successfully!"
# else
#   echo "Database migrations failed!"
#   exit 1
# fi

echo "Starting FastAPI application..."
exec uvicorn main:app --host 0.0.0.0 --port 3000
