# Use an official Python 3.10 base image with required CUDA compatibility
FROM python:3.10

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
LABEL maintainer="jean@rakam.ai" \
      version="0.0"

# Set the working directory inside the container
WORKDIR /django_application

# Install system packages and Python dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        memcached \
        libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Link python and pip commands
RUN ln -s /usr/bin/python3.10 /usr/bin/python || true && \
    ln -s /usr/bin/pip3 /usr/bin/pip || true

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Install the rakam_systems package
RUN pip install -r ./application/rakam_systems/requirements.txt

# Install the application package in editable mode
RUN pip install -e ./application/rakam_systems

# Copy and set permissions for scripts
RUN chmod +x start_prod_server.sh

# Expose port 8000
EXPOSE 8000

# Set the Django settings module
ENV DJANGO_SETTINGS_MODULE=server.settings

# Command to start the production server
CMD ["./start_prod_server.sh"]
