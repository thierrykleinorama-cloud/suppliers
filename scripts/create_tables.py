"""
Create Supabase tables for the Suppliers project.
Uses the Supabase Management API (since PostgREST can't run DDL).

Usage:
    python scripts/create_tables.py

Requires SUPABASE_ACCESS_TOKEN in .env (personal access token from supabase.com/dashboard/account/tokens).
The project ID is extracted from SUPABASE_URL.
"""
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_root))
load_dotenv(_root / ".env")


def get_project_id() -> str:
    """Extract project ID from SUPABASE_URL."""
    url = os.getenv("SUPABASE_URL", "")
    # https://PROJECTID.supabase.co
    return url.replace("https://", "").split(".")[0]


def run_sql(sql: str) -> dict:
    """Run SQL via Supabase Management API."""
    project_id = get_project_id()
    token = os.getenv("SUPABASE_ACCESS_TOKEN")
    if not token:
        raise ValueError(
            "SUPABASE_ACCESS_TOKEN not set. "
            "Get one at https://supabase.com/dashboard/account/tokens"
        )

    resp = requests.post(
        f"https://api.supabase.com/v1/projects/{project_id}/database/query",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={"query": sql},
    )

    if resp.status_code not in (200, 201):
        print(f"ERROR {resp.status_code}: {resp.text}")
        sys.exit(1)

    return resp.json()


def main():
    # Read the schema SQL
    schema_path = _root / "supabase" / "schema_suppliers.sql"
    sql = schema_path.read_text(encoding="utf-8")

    print("Creating suppliers tables...")
    result = run_sql(sql)
    print(f"Done! Result: {result}")

    # Verify
    print("\nVerifying tables exist...")
    check = run_sql("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name IN ('suppliers', 'supplier_categories');")
    print(f"Tables: {check}")


if __name__ == "__main__":
    main()
