FROM ubuntu:22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    openscad \
    python3-pip \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy application code
COPY src/ /app/src/
COPY config/ /app/config/
WORKDIR /app

# Set entrypoint
ENTRYPOINT ["python3", "src/main.py"]