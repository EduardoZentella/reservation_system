# Dockerfile
# Use the official Python image from Docker Hub
FROM python:3.13-slim
# Set the working directory for the application
WORKDIR /app
# Copy the requirements file into the container
COPY requirements.txt .
# Install the dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt
# Copy the rest of the application code into the container
COPY . .
# Pending code to run the application