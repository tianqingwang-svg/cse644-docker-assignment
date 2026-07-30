# Simple Python Web Server Dockerfile for CSE644 Docker Assignment (Requirement 6)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy application source code
COPY app.py /app/app.py

# Expose port 8888 as required by assignment specification
EXPOSE 8888

# Run the Python web server
CMD ["python", "app.py"]
