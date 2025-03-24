FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update --allow-insecure-repositories && \
    apt-get install -y --no-install-recommends \
        gnupg \
        wget \
        && \
    wget --no-check-certificate -O - https://download.docker.com/linux/debian/gpg | apt-key add - && \
    wget --no-check-certificate -O - https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    apt-get update --allow-insecure-repositories && \
    apt-get install -y --no-install-recommends \
        build-essential \
        && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 