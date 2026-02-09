FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# OTel distro + exporter + instrumentaciones (zero-code)
RUN pip install --no-cache-dir \
    opentelemetry-distro \
    opentelemetry-exporter-otlp \
    opentelemetry-instrumentation \
    opentelemetry-instrumentation-flask \
    opentelemetry-instrumentation-redis \
    opentelemetry-instrumentation-psycopg2 \
 && opentelemetry-bootstrap -a install

COPY app.py .

# Importante: NO cambiamos el código, solo el comando de arranque
CMD ["opentelemetry-instrument", \
     "gunicorn", "-b", "0.0.0.0:8000", "app:app", "--workers=2", "--threads=4"]