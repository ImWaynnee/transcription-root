#!/bin/bash
set -e

# Wait for any pre-run scripts to complete
echo "Running entrypoint script..."

# Clear the uploads directory
rm -rf /app/uploads/*

# Initialize the database only if it doesn't exist
if [ ! -f /app/data/transcriptions.db ]; then
    echo "Database not found, initializing..."
    python -c "from app.db.session import init_db; init_db()"
fi

# Start the FastAPI application using the PORT environment variable
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --reload 