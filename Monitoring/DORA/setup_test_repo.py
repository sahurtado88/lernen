#!/usr/bin/env python3
"""
Puebla un repo de GitHub con datos de prueba para validar dora.py end-to-end.

Qué hace:
  1. Crea el repo si no existe (público o privado)
  2. Inicializa con workflows que matchean los nombres de producción
  3. Crea el label 'incident'
  4. Crea y cierra issues de incidentes de prueba
  5. Actualiza config.json apuntando al repo

Uso:
  python setup_test_repo.py --token ghp_xxx --owner mi-usuario
  python setup_test_repo.py --token ghp_xxx --owner mi-usuario --repo testdora
  python setup_test_repo.py --token ghp_xxx --owner mi-usuario --repo testdora --cleanup
"""

import sys
import json
import time
import base64
import argparse
import os

try:
    import requests
except ImportError:
    print("Instala requests: pip install requests")
    sys.exit(1)

DEFAULT_REPO = "dora-test-repo"
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

WORKFLOW_NAMES = [
    ("deploy prod",            "deploy-prod.yml"),
    ("despliegue prod",        "despliegue-prod.yml"),
    ("despliegue automatizado","despliegue-automatizado.yml"),
]

WORKFLOW_TEMPLATE = """\
name: {name}
on:
  push:
    branches: [main]
  workflow_dispatch:
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Simular deploy
        run: |
          echo "Deploying to production..."
          sleep 2
          echo "Deploy completed successfully"
"""

INCIDENTS = [
    ("Incidente #1 — Error 503 en API gateway",         True),
    ("Incidente #2 — Degradación en servicio de pagos", True),
    ("Incidente #3 — Timeout en base de datos",         False),
]


def api(method, path, token, **kwargs):
    r = getattr(requests, method)(
        f"https://api.github.com{path}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        **kwargs,
    )
    return r


def create_repo(token, owner, repo_name, private):
    print(f"[1/5] Verificando repo '{repo_name}'...")
    r = api("get", f"/repos/{owner}/{repo_name}", token)
    if r.status_code == 200:
        print(f"       El repo ya existe, continuando...")
        return
    print(f"       Creando repo...")
    r = api("post", "/user/repos", token, json={
        "name": repo_name,
        "description": "Repo de prueba para DORA metrics dashboard",
        "private": private,
        "auto_init": True,
    })
    r.raise_for_status()
    print(f"       ✓ {r.json()['html_url']}")
    time.sleep(2)


def create_workflows(token, owner, repo_name):
    print(f"[2/5] Creando workflows de producción...")
    for name, filename in WORKFLOW_NAMES:
        content = WORKFLOW_TEMPLATE.format(name=name)
        encoded = base64.b64encode(content.encode()).decode()
        path    = f"/repos/{owner}/{repo_name}/contents/.github/workflows/{filename}"

        existing = api("get", path, token)
        payload  = {
            "message": f"ci: add {name} workflow",
            "content": encoded,
        }
        if existing.status_code == 200:
            payload["sha"] = existing.json()["sha"]
        r = api("put", path, token, json=payload)
        r.raise_for_status()
        print(f"       ✓ {filename}")
        time.sleep(1)


def create_incident_label(token, owner, repo_name):
    print(f"[3/5] Creando label 'incident'...")
    r = api("post", f"/repos/{owner}/{repo_name}/labels", token, json={
        "name": "incident",
        "color": "d93f0b",
        "description": "Production incident",
    })
    if r.status_code == 422:
        print("       El label ya existe, ok.")
    else:
        r.raise_for_status()
        print("       ✓ label 'incident' creado")


def get_default_branch(token, owner, repo_name):
    r = api("get", f"/repos/{owner}/{repo_name}", token)
    r.raise_for_status()
    return r.json().get("default_branch", "main")


def create_prs(token, owner, repo_name):
    print(f"[4/6] Creando Pull Requests de prueba (para Lead Time)...")
    base = get_default_branch(token, owner, repo_name)

    # Obtener SHA de la rama base
    r = api("get", f"/repos/{owner}/{repo_name}/git/ref/heads/{base}", token)
    r.raise_for_status()
    base_sha = r.json()["object"]["sha"]

    prs_data = [
        ("feat: agregar endpoint de usuarios",       "feature/usuarios"),
        ("fix: corregir timeout en conexión a DB",   "fix/timeout-db"),
        ("chore: actualizar dependencias",           "chore/deps"),
    ]

    for title, branch in prs_data:
        # Crear rama
        r = api("post", f"/repos/{owner}/{repo_name}/git/refs", token, json={
            "ref": f"refs/heads/{branch}",
            "sha": base_sha,
        })
        if r.status_code not in (201, 422):
            r.raise_for_status()

        # Commit un archivo en la nueva rama
        file_path = f"changes/{branch.replace('/', '-')}.md"
        content = base64.b64encode(f"# {title}\n\nCambio de prueba.\n".encode()).decode()
        existing = api("get", f"/repos/{owner}/{repo_name}/contents/{file_path}", token)
        payload  = {"message": title, "content": content, "branch": branch}
        if existing.status_code == 200:
            payload["sha"] = existing.json()["sha"]
        r = api("put", f"/repos/{owner}/{repo_name}/contents/{file_path}", token, json=payload)
        r.raise_for_status()

        # Crear PR
        r = api("post", f"/repos/{owner}/{repo_name}/pulls", token, json={
            "title": title,
            "body": "PR de prueba creado por setup_test_repo.py",
            "head": branch,
            "base": base,
        })
        if r.status_code == 422:
            print(f"       PR ya existe para '{branch}', saltando")
            continue
        r.raise_for_status()
        pr_number = r.json()["number"]

        time.sleep(2)

        # Mergear PR
        r = api("put", f"/repos/{owner}/{repo_name}/pulls/{pr_number}/merge", token, json={
            "commit_title": f"Merge: {title}",
            "merge_method": "merge",
        })
        r.raise_for_status()
        print(f"       ✓ PR #{pr_number} mergeado: {title}")
        time.sleep(1)

        # Actualizar base_sha para el siguiente PR
        r = api("get", f"/repos/{owner}/{repo_name}/git/ref/heads/{base}", token)
        r.raise_for_status()
        base_sha = r.json()["object"]["sha"]


def create_incidents(token, owner, repo_name):
    print(f"[5/6] Creando issues de incidentes (para MTTR)...")
    for title, close_it in INCIDENTS:
        r = api("post", f"/repos/{owner}/{repo_name}/issues", token, json={
            "title": title,
            "labels": ["incident"],
            "body": "Incidente de prueba creado por setup_test_repo.py",
        })
        r.raise_for_status()
        issue_number = r.json()["number"]
        print(f"       ✓ Issue #{issue_number}: {title}")

        if close_it:
            time.sleep(30)  # simula tiempo de resolución
            cr = api("patch", f"/repos/{owner}/{repo_name}/issues/{issue_number}", token, json={
                "state": "closed",
                "state_reason": "completed",
            })
            cr.raise_for_status()
            print(f"         → cerrado tras 30s (MTTR simulado)")
        time.sleep(0.5)


def update_config(owner, repo_name):
    print(f"[6/6] Actualizando config.json...")
    with open(CONFIG_FILE) as f:
        cfg = json.load(f)
    cfg["owner"] = owner
    cfg["repo"]  = repo_name
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)
    print(f"       ✓ config.json apunta ahora a {owner}/{repo_name}")


def cleanup(token, owner, repo_name):
    print(f"Eliminando repo {owner}/{repo_name}...")
    r = api("delete", f"/repos/{owner}/{repo_name}", token)
    if r.status_code == 204:
        print("✓ Repo eliminado.")
    elif r.status_code == 404:
        print("El repo no existía.")
    else:
        print(f"Error: {r.status_code} {r.text}")


def main():
    parser = argparse.ArgumentParser(description="Puebla un repo de prueba para DORA dashboard")
    parser.add_argument("--token",   required=True, help="GitHub Personal Access Token")
    parser.add_argument("--owner",   required=True, help="GitHub username o org")
    parser.add_argument("--repo",    default=DEFAULT_REPO, help="Nombre del repo (default: dora-test-repo)")
    parser.add_argument("--private", action="store_true", help="Crear repo privado si no existe")
    parser.add_argument("--cleanup", action="store_true", help="Eliminar el repo de prueba")
    args = parser.parse_args()

    if args.cleanup:
        cleanup(args.token, args.owner, args.repo)
        return

    create_repo(args.token, args.owner, args.repo, args.private)
    create_workflows(args.token, args.owner, args.repo)
    create_incident_label(args.token, args.owner, args.repo)
    create_prs(args.token, args.owner, args.repo)
    create_incidents(args.token, args.owner, args.repo)
    update_config(args.owner, args.repo)

    print(f"""
┌─────────────────────────────────────────────────────────────┐
│  Repo de prueba listo                                       │
│                                                             │
│  URL: https://github.com/{args.owner}/{args.repo:<28}│
│                                                             │
│  Próximos pasos:                                            │
│  1. Espera ~1 min a que los workflows terminen de correr    │
│  2. Ejecuta: python3 dora.py                                │
│                                                             │
│  Para limpiar:                                              │
│    python setup_test_repo.py --token TOKEN \\                │
│      --owner {args.owner} --repo {args.repo} --cleanup      │
└─────────────────────────────────────────────────────────────┘
""")


if __name__ == "__main__":
    main()
