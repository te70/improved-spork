# Base image — Trivy will scan this for OS-level vulnerabilities
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
# Trivy will scan these for known CVEs
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Create non-root user (security best practice)
RUN useradd --create-home --shell /bin/bash appuser
USER appuser

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "-m", "flask", "--app", "app/main", "run", "--host=0.0.0.0"]