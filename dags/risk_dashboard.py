from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

from airflow import DAG
from airflow.operators.python import PythonOperator


BASE_URL = "http://10.160.143.250:8081".rstrip("/") #os.environ.get("RISK_DASHBOARD_BASE_URL", "http://risk_dashboard:8080").rstrip("/")
TOKEN = None


def post_refresh(endpoint: str) -> None:
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"

    req = urllib.request.Request(url, data=b"{}", headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            print(f"POST {url} -> {resp.status}")
            if body:
                print(body)
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"POST {url} failed: {e.code} {e.reason}\n{detail}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"POST {url} failed: {e}") from e


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="refresh_risk_dashboard",
    default_args=default_args,
    description="Refresh risk_dashboard datasets",
    start_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
    schedule="0 9 * * *",
    catchup=False,
    tags=["risk-dashboard", "refresh"],
) as dag:
    refresh_market_risk = PythonOperator(
        task_id="refresh_market_risk",
        python_callable=post_refresh,
        op_kwargs={"endpoint": "/api/market-risk/refresh"},
    )

    refresh_verdtrygging = PythonOperator(
        task_id="refresh_verdtrygging",
        python_callable=post_refresh,
        op_kwargs={"endpoint": "/api/verdtrygging/refresh"},
    )

    refresh_aml = PythonOperator(
        task_id="refresh_aml",
        python_callable=post_refresh,
        op_kwargs={"endpoint": "/api/aml/refresh"},
    )

    refresh_risk_countries = PythonOperator(
        task_id="refresh_risk_countries",
        python_callable=post_refresh,
        op_kwargs={"endpoint": "/api/aml/risk-countries/refresh"},
    )

    refresh_market_risk >> refresh_verdtrygging >> refresh_aml >> refresh_risk_countries