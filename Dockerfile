# Dockerfile
# Use the official Python image from Docker Hub
FROM python:3.13-slim
# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
# Copy the current directory contents into the container at /app
COPY . /app
# Set the working directory to /app
WORKDIR /app
# Install any needed dependencies
RUN uv sync --frozen --no-dev
# Run the application using uv
CMD ["/app/.venv/bin/fastapi", "run", "app/main.py", "--port", "80", "--host", "0.0.0.0"]