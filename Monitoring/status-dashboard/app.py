import datetime as dt
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Tuple

import feedparser
import pandas as pd
import requests
import streamlit as st
from streamlit_autorefresh import st_autorefresh

REFRESH_SECONDS = 60
HTTP_TIMEOUT = 10

STATUSPAGE_ENDPOINTS = {
    "Claude": "https://status.claude.com/api/v2/summary.json",
    "GitHub": "https://www.githubstatus.com/api/v2/summary.json",
}
AWS_RSS_URL = "https://status.aws.amazon.com/rss/all.rss"
AWS_DASHBOARD_URL = "https://health.aws.amazon.com/health/status"

STATUS_LABELS = {
    "none": ("Operational", "🟢"),
    "minor": ("Minor incident", "🟡"),
    "major": ("Major incident", "🟠"),
    "critical": ("Critical incident", "🔴"),
    "maintenance": ("Maintenance", "🔵"),
}

st.set_page_config(page_title="Cloud Status Dashboard", page_icon="🟢", layout="wide")


@st.cache_data(ttl=REFRESH_SECONDS)
def statuspage_summary(name: str, url: str) -> Dict[str, Any]:
    response = requests.get(url, timeout=HTTP_TIMEOUT)
    response.raise_for_status()
    data = response.json()
    indicator = data.get("status", {}).get("indicator", "unknown")
    description = data.get("status", {}).get("description", "Unknown")
    incidents = data.get("incidents", []) or []
    maintenances = data.get("scheduled_maintenances", []) or []
    components = data.get("components", []) or []
    return {
        "name": name,
        "indicator": indicator,
        "description": description,
        "incidents": incidents,
        "maintenances": maintenances,
        "components": components,
        "url": url.replace("/api/v2/summary.json", ""),
    }


@st.cache_data(ttl=REFRESH_SECONDS)
def aws_summary() -> Dict[str, Any]:
    feed = feedparser.parse(AWS_RSS_URL)
    if getattr(feed, "bozo", False) and not feed.entries:
        raise RuntimeError("No se pudo leer el RSS público de AWS.")

    entries = []
    now_utc = dt.datetime.now(dt.timezone.utc)
    for entry in feed.entries[:30]:
        published = None
        if getattr(entry, "published_parsed", None):
            published = dt.datetime(*entry.published_parsed[:6], tzinfo=dt.timezone.utc)
        is_recent = published and (now_utc - published) <= dt.timedelta(days=7)
        entries.append({
            "title": entry.get("title", "AWS event"),
            "published": published.isoformat() if published else "",
            "summary": entry.get("summary", ""),
            "link": entry.get("link", AWS_DASHBOARD_URL),
            "recent": bool(is_recent),
        })

    recent_entries = [e for e in entries if e["recent"]]
    indicator = "none" if not recent_entries else "minor"
    description = "No recent public AWS RSS events" if not recent_entries else f"{len(recent_entries)} recent public AWS event(s)"
    return {
        "name": "AWS",
        "indicator": indicator,
        "description": description,
        "incidents": recent_entries,
        "components": [],
        "maintenances": [],
        "url": AWS_DASHBOARD_URL,
        "rss_entries": entries,
    }


def safe_fetch(fetcher, *args) -> Tuple[Dict[str, Any] | None, str | None]:
    try:
        return fetcher(*args), None
    except Exception as exc:
        return None, str(exc)


def fetch_all_services():
    with ThreadPoolExecutor(max_workers=3) as executor:
        f_aws = executor.submit(safe_fetch, aws_summary)
        f_claude = executor.submit(safe_fetch, statuspage_summary, "Claude", STATUSPAGE_ENDPOINTS["Claude"])
        f_github = executor.submit(safe_fetch, statuspage_summary, "GitHub", STATUSPAGE_ENDPOINTS["GitHub"])
    return f_aws.result(), f_claude.result(), f_github.result()


def render_card(service: Dict[str, Any], error: str | None = None):
    name = service.get("name", "Unknown") if service else "Unknown"
    indicator = service.get("indicator", "unknown") if service else "unknown"
    label, icon = STATUS_LABELS.get(indicator, (indicator.title(), "⚪"))
    if error:
        label, icon = "Check failed", "⚫"

    st.markdown(f"### {icon} {name}")
    st.metric("Status", label)
    if error:
        st.error(error)
    else:
        st.caption(service.get("description", ""))
        st.link_button("Open status page", service.get("url", "#"))


def flatten_statuspage_incidents(service: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows = []
    for item in service.get("incidents", []):
        rows.append({
            "service": service["name"],
            "name": item.get("name", ""),
            "status": item.get("status", ""),
            "impact": item.get("impact", ""),
            "created_at": item.get("created_at", ""),
            "updated_at": item.get("updated_at", ""),
            "url": item.get("shortlink") or item.get("url") or service.get("url"),
        })
    for item in service.get("maintenances", []):
        rows.append({
            "service": service["name"],
            "name": item.get("name", "Scheduled maintenance"),
            "status": item.get("status", ""),
            "impact": "maintenance",
            "created_at": item.get("scheduled_for", ""),
            "updated_at": item.get("updated_at", ""),
            "url": item.get("shortlink") or item.get("url") or service.get("url"),
        })
    return rows


st.title("Cloud Status Dashboard")
st.caption("AWS public health RSS + Claude Status + GitHub Status. Auto-refresh cada 60 segundos.")
st_autorefresh(interval=REFRESH_SECONDS * 1000, key="refresh")

with st.sidebar:
    st.header("Opciones")
    show_components = st.checkbox("Mostrar componentes", value=True)
    show_aws_history = st.checkbox("Mostrar últimos eventos RSS de AWS", value=True)
    st.caption(f"Última actualización: {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

(aws, aws_error), (claude, claude_error), (github, github_error) = fetch_all_services()

services = [(aws, aws_error), (claude, claude_error), (github, github_error)]
cols = st.columns(3)
for col, (service, error) in zip(cols, services):
    with col:
        render_card(service or {"name": "Unknown", "indicator": "unknown"}, error)

st.divider()

incident_rows = []
for service, error in services:
    if service and not error:
        if service["name"] == "AWS":
            for item in service.get("incidents", []):
                incident_rows.append({
                    "service": "AWS",
                    "name": item["title"],
                    "status": "public RSS event",
                    "impact": "unknown",
                    "created_at": item["published"],
                    "updated_at": "",
                    "url": item["link"],
                })
        else:
            incident_rows.extend(flatten_statuspage_incidents(service))

st.subheader("Incidentes y mantenimientos activos / recientes")
if incident_rows:
    st.dataframe(pd.DataFrame(incident_rows), use_container_width=True, hide_index=True)
else:
    st.success("No hay incidentes activos reportados por las fuentes consultadas.")

if show_components:
    st.subheader("Componentes Claude / GitHub")
    component_rows = []
    for service, error in [(claude, claude_error), (github, github_error)]:
        if service and not error:
            for c in service.get("components", []):
                component_rows.append({
                    "service": service["name"],
                    "component": c.get("name", ""),
                    "status": c.get("status", ""),
                    "updated_at": c.get("updated_at", ""),
                })
    if component_rows:
        st.dataframe(pd.DataFrame(component_rows), use_container_width=True, hide_index=True)
    else:
        st.info("No se encontraron componentes para mostrar.")

if show_aws_history and aws and not aws_error:
    st.subheader("Últimos eventos públicos de AWS RSS")
    rows = aws.get("rss_entries", [])[:15]
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.info("El RSS de AWS no devolvió eventos.")
