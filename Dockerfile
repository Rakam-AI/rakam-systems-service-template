# Use an official NVIDIA CUDA base image
FROM python:3.10

ENV DEBIAN_FRONTEND=noninteractive

# Metadata as described above
LABEL maintainer="jean@rakam.ai" \
      version="0.0"

# Set the working directory inside the container
WORKDIR /application

# Install system packages and Python.
RUN apt-get update

RUN apt-get install -y --no-install-recommends \
    gcc \
    memcached \
    libpq-dev

RUN apt-get clean

RUN rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3.8 /usr/bin/python || true && \
    ln -s /usr/bin/pip3 /usr/bin/pip || true

# Copy your requirements file into the container
COPY requirements.txt .

# Upgrade pip and install required python packages
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the application code into the container.
COPY . .

# Expose port 8000 (the port Gunicorn will run on) for the container.
EXPOSE 8000
# EXPOSE 8000

#This is required for gunicorn to find and use the settings module
ENV DJANGO_SETTINGS_MODULE=server.settings

# Command to run Gunicorn server.
RUN chmod +x start_prod_server.sh
CMD ["./start_prod_server.sh"]




