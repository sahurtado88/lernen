# TODO — DORA Dashboard

## Despliegue en producción

- [ ] Adaptar `dora.py` para guardar el HTML en `dashboard/index.html` en vez de un archivo temporal
- [ ] Crear `.github/workflows/dora-dashboard.yml` con schedule diario (lunes-viernes 8am UTC) y trigger manual
- [ ] Añadir el PAT como secret `DORA_TOKEN` en el repo (Settings → Secrets → Actions)
- [ ] Definir dónde se publica el dashboard:
  - GitHub Pages si hay plan Pro/Team → habilitar en Settings → Pages → Source: GitHub Actions
  - Netlify si plan gratuito → conectar repo y añadir `NETLIFY_AUTH_TOKEN` como secret

---

## Escalabilidad — Opción A: Dashboard central (recomendada)

Un solo repo `dora-dashboard` que monitorea múltiples repos y genera una vista unificada.

- [ ] Crear repo dedicado `dora-dashboard` en la org
- [ ] Crear `repos.json` con la lista de repos a monitorear:
  ```json
  [
    { "owner": "mi-org", "repo": "api-service", "name": "API Service" },
    { "owner": "mi-org", "repo": "frontend",    "name": "Frontend" }
  ]
  ```
- [ ] Modificar `dora.py` para iterar sobre `repos.json` y generar:
  - `dashboard/index.html` — vista general con todos los repos comparados
  - `dashboard/<repo>/index.html` — dashboard individual por repo
- [ ] Crear un único PAT con acceso de lectura a todos los repos de la org
- [ ] Workflow cron que genera todos los dashboards y publica en GitHub Pages

**Ventaja:** para añadir un repo nuevo solo se edita `repos.json`, sin tocar los repos monitoreados.

---

## Escalabilidad — Opción B: Reusable workflow

Cada repo llama al workflow centralizado y gestiona su propio dashboard.

- [ ] Crear `.github/workflows/reusable.yml` en `dora-dashboard` con `on: workflow_call`
- [ ] En cada repo a monitorear, añadir:
  ```yaml
  jobs:
    dora:
      uses: mi-org/dora-dashboard/.github/workflows/reusable.yml@main
      with:
        repo: ${{ github.repository }}
      secrets:
        dora_token: ${{ secrets.DORA_TOKEN }}
  ```
- [ ] Cada repo necesita su propio secret `DORA_TOKEN`

**Ventaja:** cada equipo tiene autonomía sobre su propio dashboard.

---

## Comparativa de opciones de escalabilidad

| | Opción A (Central) | Opción B (Reusable) |
|---|---|---|
| Añadir repo | Editar `repos.json` | Añadir workflow al repo |
| Vista unificada | ✓ | ✗ |
| Autonomía de equipos | ✗ | ✓ |
| Un token para todo | ✓ | ✗ |
| Complejidad | Baja | Media |

**Recomendación:** Opción A si los repos son de la misma org. Opción B si son equipos independientes.
