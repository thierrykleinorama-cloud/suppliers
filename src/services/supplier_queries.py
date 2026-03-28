"""
Suppliers — CRUD & Smart Search
"""
import streamlit as st

from src.database import get_supabase, TABLE_SUPPLIERS, TABLE_SUPPLIER_CATEGORIES


# ---------------------------------------------------------------------------
# Categories
# ---------------------------------------------------------------------------

@st.cache_data(ttl=300)
def fetch_categories() -> list[str]:
    """Fetch all supplier categories, ordered by sort_order."""
    client = get_supabase()
    result = (
        client.table(TABLE_SUPPLIER_CATEGORIES)
        .select("name")
        .order("sort_order")
        .execute()
    )
    return [r["name"] for r in result.data]


def create_category(name: str) -> None:
    """Add a new category."""
    client = get_supabase()
    max_order = 98  # 'Other' is 99
    client.table(TABLE_SUPPLIER_CATEGORIES).insert(
        {"name": name, "sort_order": max_order}
    ).execute()
    st.cache_data.clear()


# ---------------------------------------------------------------------------
# Suppliers CRUD
# ---------------------------------------------------------------------------

@st.cache_data(ttl=60)
def fetch_all_suppliers() -> list[dict]:
    """Fetch all suppliers ordered by company name."""
    client = get_supabase()
    result = (
        client.table(TABLE_SUPPLIERS)
        .select("*")
        .order("company")
        .execute()
    )
    return result.data


def fetch_supplier(supplier_id: str) -> dict | None:
    """Fetch a single supplier by ID."""
    client = get_supabase()
    result = (
        client.table(TABLE_SUPPLIERS)
        .select("*")
        .eq("id", supplier_id)
        .execute()
    )
    return result.data[0] if result.data else None


def create_supplier(data: dict) -> dict:
    """Insert a new supplier. Returns the created row."""
    client = get_supabase()
    # Remove None values and id
    clean = {k: v for k, v in data.items() if v is not None and k != "id"}
    result = client.table(TABLE_SUPPLIERS).insert(clean).execute()
    st.cache_data.clear()
    return result.data[0]


def update_supplier(supplier_id: str, data: dict) -> dict:
    """Update an existing supplier. Returns the updated row."""
    client = get_supabase()
    # Remove id and timestamps from update payload
    skip = {"id", "created_at", "updated_at"}
    clean = {k: v for k, v in data.items() if k not in skip}
    result = (
        client.table(TABLE_SUPPLIERS)
        .update(clean)
        .eq("id", supplier_id)
        .execute()
    )
    st.cache_data.clear()
    return result.data[0]


def delete_supplier(supplier_id: str) -> None:
    """Delete a supplier by ID."""
    client = get_supabase()
    client.table(TABLE_SUPPLIERS).delete().eq("id", supplier_id).execute()
    st.cache_data.clear()


# ---------------------------------------------------------------------------
# Smart Search
# ---------------------------------------------------------------------------

def smart_search(query: str, suppliers: list[dict]) -> list[dict]:
    """
    Client-side smart search across all text fields.
    Searches: company, category, last_name, first_name, phone1, phone2,
    email, city, country, notes, tags.
    """
    if not query or not query.strip():
        return suppliers

    terms = query.lower().split()
    results = []

    for s in suppliers:
        # Build a searchable text blob from all relevant fields
        parts = [
            s.get("company") or "",
            s.get("category") or "",
            s.get("last_name") or "",
            s.get("first_name") or "",
            s.get("phone1") or "",
            s.get("phone2") or "",
            s.get("email") or "",
            s.get("website") or "",
            s.get("city") or "",
            s.get("country") or "",
            s.get("notes") or "",
            s.get("vat_number") or "",
            s.get("payment_terms") or "",
        ]
        # Add array fields
        for tag in (s.get("tags") or []):
            parts.append(tag)
        for hotel in (s.get("hotels") or []):
            parts.append(hotel)

        blob = " ".join(parts).lower()

        # All terms must match (AND logic)
        if all(term in blob for term in terms):
            results.append(s)

    return results
