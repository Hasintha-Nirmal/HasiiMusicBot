# Use a lightweight Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install required system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    unzip \
    nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -U pip setuptools && \
    pip install --no-cache-dir -U -r requirements.txt

# Copy the rest of the application files
COPY . .

# Start the bot
CMD ["python3", "-m", "HasiiMusic"]
