# Dockerfile

# Start with a lightweight, official Python base image.
FROM python:3.11-slim

# Set environment variables to ensure Python runs smoothly inside the container.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container to /app.
WORKDIR /app

# Copy the requirements file into the container's working directory.
COPY requirements.txt .

# Run the pip install command inside the container to install our Python libraries.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of our project files (app.py, templates/, etc.) into the container.
COPY . .

# This is the final, corrected command to start your production web server.
CMD gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 app:app
