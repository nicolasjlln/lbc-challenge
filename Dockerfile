# Dockerfile

# Pull the official docker image
FROM python:3.7-bullseye

# Set work directory
WORKDIR /app

# Prevented from writing .pyc or .pyo files
ENV PYTHONDONTWRITEBYTECODE 1
# Ensure python output streams are sent straight to terminal
ENV PYTHONUNBUFFERED 1

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .