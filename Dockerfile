# Base image for Python 3.11
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a non-root user and sandbox space
RUN groupadd -r mcp && useradd -r -g mcp mcpuser
RUN mkdir -p /tmp/mcp_sandbox && chown -R mcpuser:mcp /tmp/mcp_sandbox

# Set working directory
WORKDIR /app

# Install dependencies first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY src/ src/
COPY .env* ./

# Switch to non-root user for security
USER mcpuser

# Default command (can be overridden by docker-compose to run specific servers)
# Using module 1 as default hello check
CMD ["python", "src/01_core_mechanics/hello_mcp.py"]
