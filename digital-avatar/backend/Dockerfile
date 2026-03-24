FROM python:3.12-slim

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY sql/ ./sql/
COPY business-challenges.md .
COPY index.md .

# Create knowledge base directory
RUN mkdir -p ./knowledge_base
COPY knowledge_base/ ./knowledge_base/

# Create frontend directory (static files are optional)
RUN mkdir -p ./frontend

# Environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/api/health')" || exit 1

# Run the application
CMD exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
