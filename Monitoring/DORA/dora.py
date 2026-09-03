#!/usr/bin/env python3
"""DORA Metrics Dashboard — genera un HTML local con métricas desde GitHub API."""

import json
import os
import sys
import webbrowser
import tempfile
from datetime import datetime, timedelta, timezone
from collections import defaultdict

try:
    import requests
except ImportError:
    print("Falta la librería 'requests'. Instálala con:\n  pip install requests")
    sys.exit(1)

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")


# ─── GitHub API ──────────────────────────────────────────────────────────────

def gh_headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "DORA-Dashboard",
    }


def gh_get(url, token, params=None):
    """GET paginado contra la GitHub API. Devuelve lista o dict."""
    results = []
    page = 1
    while True:
        p = {"per_page": 100, "page": page, **(params or {})}
        r = requests.get(url, headers=gh_headers(token), params=p, timeout=15)
        if r.status_code == 401:
            print("ERROR: Token inválido o sin permisos. Revisa config.json.")
            sys.exit(1)
        if r.status_code == 404:
            print(f"ERROR 404: Repo no encontrado. Revisa owner/repo en config.json.")
            sys.exit(1)
        r.raise_for_status()
        data = r.json()
        if isinstance(data, dict):
            return data
        if not data:
            break
        results.extend(data)
        if len(data) < 100:
            break
        page += 1
    return results


# ─── Fetchers ─────────────────────────────────────────────────────────────────

def fetch_workflow_runs(cfg, since):
    owner, repo, token = cfg["owner"], cfg["repo"], cfg["github_token"]
    target_names = {n.lower() for n in cfg["production_workflows"]}

    # Obtener todos los workflows del repo
    all_wf = gh_get(f"https://api.github.com/repos/{owner}/{repo}/actions/workflows", token)
    matched_ids = [
        wf["id"] for wf in all_wf.get("workflows", [])
        if wf["name"].lower() in target_names
    ]

    if not matched_ids:
        print(f"AVISO: No se encontraron workflows con esos nombres. Nombres actuales en el repo:")
        for wf in all_wf.get("workflows", []):
            print(f"  - {wf['name']}")
        return []

    runs = []
    for wf_id in matched_ids:
        data = gh_get(
            f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{wf_id}/runs",
            token,
            {"status": "success"},
        )
        wf_runs = data.get("workflow_runs", []) if isinstance(data, dict) else data
        for run in wf_runs:
            dt = datetime.fromisoformat(run["updated_at"].replace("Z", "+00:00"))
            if dt >= since:
                runs.append(run)

    return runs


def fetch_merged_prs(cfg, since):
    owner, repo, token = cfg["owner"], cfg["repo"], cfg["github_token"]
    prs = gh_get(
        f"https://api.github.com/repos/{owner}/{repo}/pulls",
        token,
        {"state": "closed", "sort": "updated", "direction": "desc"},
    )
    merged = []
    for pr in prs:
        if pr.get("merged_at"):
            dt = datetime.fromisoformat(pr["merged_at"].replace("Z", "+00:00"))
            if dt >= since:
                merged.append(pr)
    return merged


def fetch_pr_first_commit(cfg, pr_number):
    owner, repo, token = cfg["owner"], cfg["repo"], cfg["github_token"]
    commits = gh_get(
        f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/commits",
        token,
    )
    dates = []
    for c in commits:
        d = (c.get("commit", {}).get("author", {}).get("date")
             or c.get("commit", {}).get("committer", {}).get("date"))
        if d:
            dates.append(datetime.fromisoformat(d.replace("Z", "+00:00")))
    return min(dates) if dates else None


def fetch_incidents(cfg, since):
    owner, repo, token = cfg["owner"], cfg["repo"], cfg["github_token"]
    label = cfg.get("incident_label", "incident")
    issues = gh_get(
        f"https://api.github.com/repos/{owner}/{repo}/issues",
        token,
        {"labels": label, "state": "all", "sort": "created", "direction": "desc"},
    )
    result = []
    for issue in issues:
        if "pull_request" in issue:
            continue
        dt = datetime.fromisoformat(issue["created_at"].replace("Z", "+00:00"))
        if dt >= since:
            result.append(issue)
    return result


# ─── Cálculo de métricas ──────────────────────────────────────────────────────

def dora_level(metric, value):
    levels = {
        "df":   [(7, "Elite"), (1, "High"), (0.25, "Medium")],
        "lt":   [(1, "Elite"), (24, "High"), (168, "Medium")],
        "mttr": [(1, "Elite"), (24, "High"), (168, "Medium")],
        "cfr":  [(5, "Elite"), (10, "High"), (15, "Medium")],
    }
    colors = {"Elite": "#22c55e", "High": "#3b82f6", "Medium": "#f59e0b", "Low": "#ef4444"}
    thresholds = levels[metric]
    for threshold, label in thresholds:
        if metric in ("df",) and value >= threshold:
            return label, colors[label]
        if metric not in ("df",) and value <= threshold:
            return label, colors[label]
    return "Low", colors["Low"]


def calculate(cfg):
    days = cfg.get("days", 90)
    since = datetime.now(timezone.utc) - timedelta(days=days)

    print(f"\nObteniendo datos de los últimos {days} días...\n")

    print("  [1/4] Workflow runs de producción...")
    runs = fetch_workflow_runs(cfg, since)
    print(f"        → {len(runs)} deploys encontrados")

    print("  [2/4] Pull Requests mergeados...")
    prs = fetch_merged_prs(cfg, since)
    print(f"        → {len(prs)} PRs mergeados")

    print("  [3/4] Incidentes (issues con label incident)...")
    incidents = fetch_incidents(cfg, since)
    print(f"        → {len(incidents)} incidentes")

    # ── Deployment Frequency ──
    by_week = defaultdict(int)
    for run in runs:
        dt = datetime.fromisoformat(run["updated_at"].replace("Z", "+00:00"))
        by_week[dt.strftime("%Y-W%V")] += 1
    avg_df = len(runs) / (days / 7)

    # ── Lead Time ──
    print("  [4/4] Calculando Lead Time (commits por PR)...")
    lead_times = []
    prs_sample = prs[:15]
    if not prs_sample:
        print("        ⚠ No se encontraron PRs mergeados en el periodo")
    for pr in prs_sample:
        merged_at = datetime.fromisoformat(pr["merged_at"].replace("Z", "+00:00"))
        first_commit = fetch_pr_first_commit(cfg, pr["number"])
        deploy_after = next(
            (datetime.fromisoformat(r["updated_at"].replace("Z", "+00:00"))
             for r in sorted(runs, key=lambda x: x["updated_at"])
             if datetime.fromisoformat(r["updated_at"].replace("Z", "+00:00")) >= merged_at),
            None
        )
        if first_commit and deploy_after:
            hours = (deploy_after - first_commit).total_seconds() / 3600
            lead_times.append({
                "pr": pr["number"],
                "title": pr["title"][:45] + ("…" if len(pr["title"]) > 45 else ""),
                "hours": hours,
                "date": merged_at.strftime("%Y-%m-%d"),
            })
            sys.stdout.write(f"\r        → PR #{pr['number']} ✓ ({fmt_hours(hours)})")
        else:
            motivo = []
            if not first_commit:
                motivo.append("sin commits")
            if not deploy_after:
                motivo.append(f"sin deploy después del merge ({merged_at.strftime('%Y-%m-%d %H:%M')} UTC)")
            print(f"\n        ⚠ PR #{pr['number']} omitido: {', '.join(motivo)}")
        sys.stdout.flush()
    print()

    avg_lt = sum(l["hours"] for l in lead_times) / len(lead_times) if lead_times else None

    # ── MTTR ──
    mttr_list = []
    for issue in incidents:
        if issue.get("closed_at"):
            created = datetime.fromisoformat(issue["created_at"].replace("Z", "+00:00"))
            closed  = datetime.fromisoformat(issue["closed_at"].replace("Z", "+00:00"))
            raw_hours = (closed - created).total_seconds() / 3600
            mttr_list.append({
                "title": issue["title"][:45],
                "hours": raw_hours,
                "date": created.strftime("%Y-%m-%d"),
            })
    avg_mttr = sum(m["hours"] for m in mttr_list) / len(mttr_list) if mttr_list else 0

    # ── Change Failure Rate ──
    cfr = (len(incidents) / len(runs) * 100) if runs else 0

    weeks = sorted(by_week.keys())
    return {
        "period_days": days,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "repo": f"{cfg['owner']}/{cfg['repo']}",
        "df": {
            "total": len(runs),
            "avg_per_week": round(avg_df, 2),
            "weeks": weeks,
            "counts": [by_week[w] for w in weeks],
        },
        "lt": {
            "avg_hours": avg_lt,
            "items": lead_times,
        },
        "mttr": {
            "avg_hours": avg_mttr,
            "total": len(incidents),
            "resolved": len(mttr_list),
            "items": mttr_list,
        },
        "cfr": {
            "rate": round(cfr, 1),
            "incidents": len(incidents),
            "deployments": len(runs),
        },
    }


# ─── HTML ─────────────────────────────────────────────────────────────────────

def fmt_hours(h):
    if not h:
        return "N/A"
    if h < 1/60:
        return f"{int(h*3600)}s"
    if h < 1:
        return f"{int(h*60)}m"
    if h < 24:
        return f"{h:.1f}h"
    return f"{h/24:.1f}d"


def build_html(m):
    df_level,   df_color   = dora_level("df",   m["df"]["avg_per_week"])
    lt_level,   lt_color   = dora_level("lt",   m["lt"]["avg_hours"] or 0)
    mttr_level, mttr_color = dora_level("mttr", m["mttr"]["avg_hours"])
    cfr_level,  cfr_color  = dora_level("cfr",  m["cfr"]["rate"])

    def best_unit(hours_list):
        if not hours_list:
            return 1, "horas"
        avg = sum(hours_list) / len(hours_list)
        if avg < 1/60:
            return 3600, "segundos"
        if avg < 1:
            return 60, "minutos"
        if avg < 24 * 7:
            return 1, "horas"
        return 1/24, "días"

    lt_hours   = [i["hours"] for i in m["lt"]["items"]]
    mttr_hours = [i["hours"] for i in m["mttr"]["items"]]
    lt_factor,   lt_unit   = best_unit(lt_hours)
    mttr_factor, mttr_unit = best_unit(mttr_hours)

    lt_labels   = json.dumps([f"#{i['pr']}" for i in m["lt"]["items"]])
    lt_data     = json.dumps([round(h * lt_factor, 2) for h in lt_hours])
    mttr_labels = json.dumps([i["date"] for i in m["mttr"]["items"]])
    mttr_data   = json.dumps([round(h * mttr_factor, 2) for h in mttr_hours])

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>DORA Metrics — {m["repo"]}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
         background: #0f172a; color: #e2e8f0; min-height: 100vh; padding: 2rem; }}
  h1 {{ font-size: 1.5rem; font-weight: 700; color: #f8fafc; }}
  .subtitle {{ color: #94a3b8; font-size: .875rem; margin-top: .25rem; }}
  .header {{ margin-bottom: 2rem; }}
  .grid-4 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin-bottom: 2rem; }}
  .grid-2 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(420px, 1fr)); gap: 1rem; }}
  .card {{ background: #1e293b; border-radius: 12px; padding: 1.5rem; border: 1px solid #334155; }}
  .card-title {{ font-size: .75rem; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: .05em; margin-bottom: .75rem; }}
  .metric-value {{ font-size: 2.5rem; font-weight: 800; line-height: 1; }}
  .metric-sub {{ font-size: .8rem; color: #64748b; margin-top: .4rem; }}
  .badge {{ display: inline-block; padding: .2rem .65rem; border-radius: 9999px; font-size: .7rem; font-weight: 700; margin-top: .75rem; }}
  canvas {{ width: 100% !important; }}
  .chart-card {{ background: #1e293b; border-radius: 12px; padding: 1.5rem; border: 1px solid #334155; }}
  .chart-title {{ font-size: .85rem; font-weight: 600; color: #cbd5e1; margin-bottom: 1rem; }}
  .footer {{ text-align: center; color: #475569; font-size: .75rem; margin-top: 2rem; }}
</style>
</head>
<body>
<div class="header">
  <h1>DORA Metrics</h1>
  <p class="subtitle">{m["repo"]} · últimos {m["period_days"]} días · generado {m["generated_at"]}</p>
</div>

<div class="grid-4">

  <div class="card">
    <div class="card-title">Deployment Frequency</div>
    <div class="metric-value" style="color:{df_color}">{m["df"]["avg_per_week"]}</div>
    <div class="metric-sub">deploys/semana · {m["df"]["total"]} total</div>
    <span class="badge" style="background:{df_color}22; color:{df_color}">{df_level}</span>
  </div>

  <div class="card">
    <div class="card-title">Lead Time for Changes</div>
    <div class="metric-value" style="color:{lt_color}">{fmt_hours(m["lt"]["avg_hours"])}</div>
    <div class="metric-sub">primer commit → deploy · {len(m["lt"]["items"])} PRs analizados</div>
    <span class="badge" style="background:{lt_color}22; color:{lt_color}">{lt_level}</span>
  </div>

  <div class="card">
    <div class="card-title">Mean Time to Recovery</div>
    <div class="metric-value" style="color:{mttr_color}">{fmt_hours(m["mttr"]["avg_hours"])}</div>
    <div class="metric-sub">{m["mttr"]["resolved"]} incidentes resueltos de {m["mttr"]["total"]}</div>
    <span class="badge" style="background:{mttr_color}22; color:{mttr_color}">{mttr_level}</span>
  </div>

  <div class="card">
    <div class="card-title">Change Failure Rate</div>
    <div class="metric-value" style="color:{cfr_color}">{m["cfr"]["rate"]}%</div>
    <div class="metric-sub">{m["cfr"]["incidents"]} incidentes / {m["cfr"]["deployments"]} deploys</div>
    <span class="badge" style="background:{cfr_color}22; color:{cfr_color}">{cfr_level}</span>
  </div>

</div>

<div class="grid-2">

  <div class="chart-card">
    <div class="chart-title">Deployment Frequency — deploys por semana</div>
    <canvas id="dfChart" height="200"></canvas>
  </div>

  <div class="chart-card">
    <div class="chart-title">Lead Time — {lt_unit} por PR</div>
    <canvas id="ltChart" height="200"></canvas>
  </div>

  <div class="chart-card">
    <div class="chart-title">MTTR — {mttr_unit} por incidente</div>
    <canvas id="mttrChart" height="200"></canvas>
  </div>

  <div class="chart-card">
    <div class="chart-title">Change Failure Rate — deploys vs incidentes</div>
    <canvas id="cfrChart" height="200"></canvas>
  </div>

</div>

<div class="footer">DORA Dashboard · GitHub API · <a href="https://dora.dev" style="color:#64748b">dora.dev</a></div>

<script>
const GRID = '#334155';
const TICK = '#64748b';
const defaults = {{
  plugins: {{ legend: {{ display: false }} }},
  scales: {{
    x: {{ grid: {{ color: GRID }}, ticks: {{ color: TICK }} }},
    y: {{ grid: {{ color: GRID }}, ticks: {{ color: TICK }}, beginAtZero: true }}
  }}
}};

// DF
new Chart(document.getElementById('dfChart'), {{
  type: 'bar',
  data: {{
    labels: {json.dumps(m["df"]["weeks"])},
    datasets: [{{ data: {json.dumps(m["df"]["counts"])}, backgroundColor: '{df_color}99', borderColor: '{df_color}', borderWidth: 1, borderRadius: 4 }}]
  }},
  options: defaults
}});

// LT
new Chart(document.getElementById('ltChart'), {{
  type: 'bar',
  data: {{
    labels: {lt_labels},
    datasets: [{{ data: {lt_data}, backgroundColor: '{lt_color}99', borderColor: '{lt_color}', borderWidth: 1, borderRadius: 4 }}]
  }},
  options: {{
    indexAxis: 'y',
    plugins: {{ legend: {{ display: false }} }},
    scales: {{
      x: {{ grid: {{ color: GRID }}, ticks: {{ color: TICK }}, beginAtZero: true }},
      y: {{ grid: {{ color: GRID }}, ticks: {{ color: TICK }} }}
    }}
  }}
}});

// MTTR
const mttrItems = {json.dumps(m["mttr"]["items"])};
new Chart(document.getElementById('mttrChart'), {{
  type: 'bar',
  data: {{
    labels: {mttr_labels},
    datasets: [{{ data: {mttr_data}, backgroundColor: '{mttr_color}99', borderColor: '{mttr_color}', borderWidth: 1, borderRadius: 4 }}]
  }},
  options: mttrItems.length === 0
    ? {{ plugins: {{ legend: {{ display: false }}, title: {{ display: true, text: 'Sin incidentes registrados', color: '#64748b' }} }} }}
    : defaults
}});

// CFR doughnut
new Chart(document.getElementById('cfrChart'), {{
  type: 'doughnut',
  data: {{
    labels: ['Deploys exitosos', 'Incidentes'],
    datasets: [{{
      data: [{m["cfr"]["deployments"] - m["cfr"]["incidents"]}, {m["cfr"]["incidents"]}],
      backgroundColor: ['#22c55e55', '#ef444455'],
      borderColor: ['#22c55e', '#ef4444'],
      borderWidth: 2
    }}]
  }},
  options: {{
    plugins: {{
      legend: {{ display: true, labels: {{ color: TICK }} }},
      title: {{ display: true, text: '{m["cfr"]["rate"]}% Change Failure Rate', color: '{cfr_color}', font: {{ size: 16, weight: 'bold' }} }}
    }},
    cutout: '65%'
  }}
}});
</script>
</body>
</html>"""


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    if not os.path.exists(CONFIG_FILE):
        print(f"No se encontró config.json en {CONFIG_FILE}")
        sys.exit(1)

    with open(CONFIG_FILE) as f:
        cfg = json.load(f)

    if "TU_TOKEN" in cfg.get("github_token", ""):
        print("Configura tu GitHub token en config.json antes de ejecutar.")
        print("  1. Ve a https://github.com/settings/tokens")
        print("  2. Crea un token con scope: repo")
        print("  3. Pégalo en config.json → github_token")
        sys.exit(1)

    metrics = calculate(cfg)

    html = build_html(metrics)
    tmp = tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8")
    tmp.write(html)
    tmp.close()

    print(f"\nDashboard generado: {tmp.name}")
    print("Abriendo en el browser...\n")
    webbrowser.open(f"file://{tmp.name}")


if __name__ == "__main__":
    main()
