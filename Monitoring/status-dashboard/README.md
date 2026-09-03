# Cloud Status Dashboard

Dashboard en Streamlit para validar el estado público de:

- AWS Health Dashboard RSS
- Claude Status API
- GitHub Status API

## Ejecutar local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Abrir: http://localhost:8501

## Ejecutar con Docker

```bash
docker build -t cloud-status-dashboard .
docker run --rm -p 8501:8501 cloud-status-dashboard
```

## Ejecutar con Docker Compose

```bash
docker compose up --build
```

Para ejecutar en segundo plano:

```bash
docker compose up --build -d
docker compose logs -f   # ver logs
docker compose down      # parar y eliminar el contenedor
```

## Notas

- Claude y GitHub usan Statuspage `summary.json`.
- AWS usa el RSS público `https://status.aws.amazon.com/rss/all.rss`. Para eventos específicos de tu cuenta AWS, lo correcto es integrar AWS Health con EventBridge.
