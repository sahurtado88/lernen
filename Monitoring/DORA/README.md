# DORA Metrics Dashboard

Dashboard local que calcula las 4 métricas DORA desde la GitHub API y las visualiza en el browser.

## ¿Qué mide el dashboard?

Las métricas DORA (DevOps Research and Assessment) son los 4 indicadores clave para medir el rendimiento de un equipo de ingeniería. El dashboard las calcula automáticamente desde la actividad real del repo en GitHub.

### Deployment Frequency
**¿Con qué frecuencia llegas a producción?**
Cuenta los workflow runs exitosos de tus workflows de producción en el periodo configurado y calcula el promedio semanal. A mayor frecuencia, mayor capacidad de entregar valor de forma continua.

### Lead Time for Changes
**¿Cuánto tarda un cambio desde que se escribe hasta que llega a producción?**
Mide el tiempo desde el primer commit de un Pull Request hasta que el workflow de deploy completa su ejecución tras el merge. Incluye tiempo de revisión, aprobación y despliegue. Tiempos bajos indican un proceso de entrega ágil y sin fricción.

### Mean Time to Recovery (MTTR)
**¿Cuánto tardas en recuperarte cuando algo falla en producción?**
Calcula el tiempo entre la apertura y el cierre de un Issue con el label `incident`. Refleja la capacidad del equipo para detectar, diagnosticar y resolver problemas en producción.

### Change Failure Rate
**¿Qué porcentaje de tus deploys causan un incidente?**
Divide el número de incidentes entre el número de deploys en el periodo. Un valor alto indica que los cambios llegan a producción con poca estabilidad o sin suficientes pruebas.

---

### Fuentes de datos

| Métrica | Origen en GitHub |
|---|---|
| Deployment Frequency | Workflow runs con estado `success` de los workflows configurados |
| Lead Time | Fecha del primer commit del PR → fecha de completado del deploy posterior al merge |
| MTTR | `created_at` → `closed_at` de Issues con el label `incident` |
| Change Failure Rate | `total de incidentes / total de deploys × 100` |

### Niveles de rendimiento

| Nivel | Deployment Frequency | Lead Time | MTTR | Change Failure Rate |
|---|---|---|---|---|
| **Elite** | > 1/día | < 1 hora | < 1 hora | < 5% |
| **High** | 1/día – 1/semana | < 1 día | < 1 día | 5–10% |
| **Medium** | 1/semana – 1/mes | < 1 semana | < 1 semana | 10–15% |
| **Low** | < 1/mes | > 1 semana | > 1 semana | > 15% |

## Requisitos

- Python 3.8+
- Librería `requests`

```bash
pip install requests
```

## Configuración

### 1. GitHub Token

1. Ve a **GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens**
2. Crea un token con permiso **Contents: Read-only** y **Actions: Read-only** sobre tu repo
3. Copia el token

### 2. Edita `config.json`

```json
{
  "github_token": "ghp_tu_token_aqui",
  "owner": "tu-usuario-o-org",
  "repo": "nombre-del-repo",
  "production_workflows": [
    "deploy prod",
    "despliegue prod",
    "despliegue automatizado"
  ],
  "incident_label": "incident",
  "days": 90
}
```

| Campo | Descripción |
|---|---|
| `github_token` | Token de acceso personal de GitHub |
| `owner` | Usuario u organización dueña del repo |
| `repo` | Nombre del repositorio (sin el owner) |
| `production_workflows` | Nombres exactos de los workflows de deploy a producción |
| `incident_label` | Label de GitHub Issues usado para marcar incidentes |
| `days` | Periodo de análisis en días (por defecto 90) |

### 3. Label de incidentes (para MTTR y Change Failure Rate)

Crea el label `incident` en tu repo:

**GitHub → tu repo → Issues → Labels → New label → nombre: `incident`**

A partir de ahí, cuando ocurra un incidente en producción:
- **Abre** un Issue con el label `incident` → marca el inicio del incidente
- **Cierra** el Issue cuando se resuelva → el script calcula el MTTR automáticamente

## Ejecución

```bash
python3 dora.py
```

El script:
1. Consulta la GitHub API (puede tardar ~30s dependiendo del volumen de PRs)
2. Genera un archivo HTML temporal
3. Lo abre automáticamente en el browser

## Niveles de rendimiento DORA

| Nivel | Color | Deployment Frequency | Lead Time | MTTR | Change Failure Rate |
|---|---|---|---|---|---|
| **Elite** | Verde | > 1/día | < 1 hora | < 1 hora | < 5% |
| **High** | Azul | 1/día – 1/semana | < 1 día | < 1 día | 5–10% |
| **Medium** | Amarillo | 1/semana – 1/mes | < 1 semana | < 1 semana | 10–15% |
| **Low** | Rojo | < 1/mes | > 1 semana | > 1 semana | > 15% |

## Testing

Hay dos formas de validar que el script funciona correctamente.

### Opción 1 — Tests unitarios (sin internet, sin token)

Ejecutan las métricas contra datos mock y verifican cálculos y niveles DORA.

```bash
# Sin pytest
python3 tests/test_metrics.py

# Con pytest
pip install pytest
pytest tests/ -v
```

Cubren 29 casos: todos los niveles DORA por métrica, cálculo de DF/MTTR/CFR, casos borde (0 deploys, 0 incidentes) y generación de HTML válido.

### Opción 2 — Repo de prueba real en GitHub (end-to-end)

Crea un repo `dora-test-repo` con workflows reales, incidentes de prueba y actualiza `config.json` automáticamente.

```bash
python3 setup_test_repo.py --token ghp_xxx --owner tu-usuario

# Para repo privado
python3 setup_test_repo.py --token ghp_xxx --owner tu-usuario --private
```

El script:
1. Crea el repo con los 3 workflows de producción configurados
2. Los dispara con un push → generan runs reales en GitHub Actions
3. Crea el label `incident` y 3 issues de prueba (2 cerrados, 1 abierto)
4. Actualiza `config.json` apuntando al nuevo repo

Después espera ~1 minuto a que los workflows terminen y ejecuta el dashboard normalmente:

```bash
python3 dora.py
```

Para eliminar el repo de prueba cuando termines:

```bash
python3 setup_test_repo.py --token ghp_xxx --owner tu-usuario --cleanup
```

## Solución de problemas

**"No se encontraron workflows con esos nombres"**
El script imprime los nombres reales de los workflows en tu repo. Cópialos exactamente en `config.json`.

**"Token inválido o sin permisos"**
Verifica que el token tenga acceso al repo privado y los scopes `repo` y `actions`.

**Lead Time muestra N/A**
No se encontraron PRs mergeados con un deploy posterior en el periodo configurado. Aumenta `days` en `config.json`.

**MTTR muestra N/A**
No hay issues cerrados con el label `incident` en el periodo. Revisa que el label exista y esté escrito igual que en `config.json`.
