FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN groupadd --system app && useradd --system --gid app --create-home app

COPY --chown=app:app calcpython/calculadora.py /app/calculadora.py

USER app

CMD ["python", "/app/calculadora.py"]
