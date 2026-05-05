# Production-ready container for the cricket dashboard.
# Build:  docker build -t cricket-dash .
# Run:    docker run -p 8501:8501 cricket-dash
FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies first — better Docker layer caching.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project.
COPY . .

EXPOSE 8501

# Streamlit needs to bind 0.0.0.0 inside a container to be reachable.
CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--browser.gatherUsageStats=false"]
