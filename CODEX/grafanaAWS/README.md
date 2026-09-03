# Grafana + AWS MVP

MVP para levantar Grafana en Docker y conectarlo a AWS CloudWatch con provisión automática de:

- Data source: `AWS CloudWatch`
- Dashboard inicial: `AWS RED + USE Overview`
  - RED (ALB): Rate, Errors, Duration
  - USE (EC2): Utilization, Saturation, Errors

## Requisitos

- Docker + Docker Compose plugin
- Una cuenta AWS con permisos para leer CloudWatch (`cloudwatch:GetMetricData`, `cloudwatch:ListMetrics`, `ec2:DescribeInstances`)

## Arranque rápido

1. Crear variables de entorno:

```bash
cp .env.example .env
```

2. Iniciar Grafana:

```bash
docker compose up -d
```

3. Abrir Grafana:

- URL: http://localhost:3000
- Usuario/clave: definidos en `.env`

## Autenticación AWS

El contenedor usa el default credential chain de AWS SDK.

Opciones:

1. Perfil local AWS (recomendado)
- Se monta `~/.aws` en modo solo lectura.
- Define `AWS_PROFILE` y `AWS_REGION` en `.env`.

2. Access keys en `.env`
- Define `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` y opcional `AWS_SESSION_TOKEN`.

## Estructura

- `docker-compose.yml`: servicio de Grafana
- `grafana/provisioning/datasources/cloudwatch.yml`: datasource CloudWatch
- `grafana/provisioning/dashboards/dashboards.yml`: proveedor de dashboards
- `grafana/dashboards/aws-ec2-overview.json`: dashboard inicial

## Verificación

```bash
docker compose ps
docker compose logs grafana --tail=100
```

Si no ves métricas, revisa:

- Región correcta (`AWS_REGION`)
- Permisos IAM de CloudWatch/EC2
- Que existan instancias EC2 con datos recientes
