from flask import Flask, jsonify
import os
import time
import redis
import psycopg2

app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
PG_HOST = os.getenv("PG_HOST", "postgres")
PG_DB = os.getenv("PG_DB", "appdb")
PG_USER = os.getenv("PG_USER", "appuser")
PG_PASS = os.getenv("PG_PASS", "apppass")

r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

def pg_conn():
    return psycopg2.connect(
        host=PG_HOST, dbname=PG_DB, user=PG_USER, password=PG_PASS, port=5432
    )

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/work")
def work():
    # Redis
    r.incr("hits")
    hits = int(r.get("hits") or 0)

    # Postgres
    with pg_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT now()")
            now = cur.fetchone()[0]

    # Simula algo de trabajo
    time.sleep(0.05)

    return jsonify({"hits": hits, "db_now": str(now)})
