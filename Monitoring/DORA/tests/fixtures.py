"""Datos de prueba que simulan respuestas de la GitHub API."""

from datetime import datetime, timezone, timedelta

def days_ago(n, hour=12):
    return (datetime.now(timezone.utc) - timedelta(days=n)).replace(
        hour=hour, minute=0, second=0, microsecond=0
    ).strftime("%Y-%m-%dT%H:%M:%SZ")


# 15 workflow runs exitosos distribuidos en los últimos 90 días
WORKFLOW_RUNS = [
    {"id": i, "name": "deploy prod", "updated_at": days_ago(d), "conclusion": "success"}
    for i, d in enumerate([2, 5, 8, 12, 15, 19, 23, 28, 33, 40, 47, 55, 63, 72, 85])
]

# 5 PRs mergeados
MERGED_PRS = [
    {
        "number": 101, "title": "feat: nuevo endpoint de usuarios",
        "merged_at": days_ago(3), "created_at": days_ago(5),
    },
    {
        "number": 98, "title": "fix: corregir timeout en conexión DB",
        "merged_at": days_ago(10), "created_at": days_ago(11),
    },
    {
        "number": 95, "title": "chore: actualizar dependencias de seguridad",
        "merged_at": days_ago(20), "created_at": days_ago(22),
    },
    {
        "number": 90, "title": "feat: integración con servicio de pagos",
        "merged_at": days_ago(35), "created_at": days_ago(40),
    },
    {
        "number": 85, "title": "refactor: modularizar capa de autenticación",
        "merged_at": days_ago(60), "created_at": days_ago(65),
    },
]

# Commits del primer PR (más antiguo = inicio del lead time)
PR_COMMITS = {
    101: days_ago(5, hour=9),   # primer commit 5 días atrás
    98:  days_ago(11, hour=8),
    95:  days_ago(22, hour=10),
    90:  days_ago(40, hour=14),
    85:  days_ago(65, hour=11),
}

# 2 incidentes: uno resuelto en 3h, otro en 26h
INCIDENTS = [
    {
        "number": 201,
        "title": "Producción caída — error 503 en API gateway",
        "created_at": days_ago(6, hour=2),
        "closed_at":  days_ago(6, hour=5),   # 3 horas después
        "state": "closed",
        "labels": [{"name": "incident"}],
    },
    {
        "number": 188,
        "title": "Degradación de rendimiento en servicio de pagos",
        "created_at": days_ago(30, hour=18),
        "closed_at":  days_ago(29, hour=20),  # ~26 horas después
        "state": "closed",
        "labels": [{"name": "incident"}],
    },
]

# Métricas esperadas con estos fixtures
EXPECTED = {
    "df_total": 15,
    "df_avg_per_week_approx": 1.17,   # 15 / (90/7)
    "df_level": "High",
    "cfr_rate_approx": 13.3,           # 2/15 * 100
    "cfr_level": "Medium",
    "mttr_avg_hours_approx": 14.5,     # (3 + 26) / 2
    "mttr_level": "High",
}
