"""
Suppliers — List View
Smart search + category filter + compact table.
"""
import sys
from pathlib import Path

_root = str(Path(__file__).resolve().parent.parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

import streamlit as st
from app.components.ui import sidebar_css, page_title, hotel_badges
from src.services.supplier_queries import (
    fetch_all_suppliers,
    fetch_categories,
    smart_search,
)

# -- Session state defaults --
if "search_query" not in st.session_state:
    st.session_state["search_query"] = ""

sidebar_css()
page_title(":material/contacts: Suppliers", "Search, browse and manage your suppliers")

# -- Top bar: search + new button --
col_search, col_new = st.columns([4, 1])
with col_search:
    query = st.text_input(
        "Smart search",
        value=st.session_state["search_query"],
        placeholder="Search across all fields...",
        label_visibility="collapsed",
        key="search_input",
    )
    st.session_state["search_query"] = query

with col_new:
    if st.button(":material/add: New Supplier", use_container_width=True, type="primary"):
        st.session_state["supplier_id"] = None
        st.session_state["detail_mode"] = "new"
        st.switch_page("pages/2_Supplier_Detail.py")

# -- Sidebar filters --
with st.sidebar:
    st.subheader("Filters")

    categories = fetch_categories()
    selected_cats = st.multiselect("Category", categories)

    hotels_all = ["MIAOU", "COIN", "WOUAF"]
    selected_hotels = st.multiselect("Hotel", hotels_all)

    rating_min = st.slider("Min rating", 0, 5, 0)

# -- Fetch & filter --
all_suppliers = fetch_all_suppliers()

filtered = smart_search(query, all_suppliers)

if selected_cats:
    filtered = [s for s in filtered if s.get("category") in selected_cats]

if selected_hotels:
    filtered = [
        s for s in filtered
        if any(h in (s.get("hotels") or []) for h in selected_hotels)
    ]

if rating_min > 0:
    filtered = [s for s in filtered if (s.get("rating") or 0) >= rating_min]

# -- Results count --
st.caption(f"{len(filtered)} supplier{'s' if len(filtered) != 1 else ''} found")

# -- Table display --
if not filtered:
    st.info("No suppliers found. Try adjusting your search or filters.")
else:
    # Header row — compact columns
    cols = st.columns([2.2, 1.4, 1.8, 1.3, 1.5, 1.5, 1.5, 0.8])
    cols[0].markdown("**Company**")
    cols[1].markdown("**Category**")
    cols[2].markdown("**Contact**")
    cols[3].markdown("**Phone**")
    cols[4].markdown("**Email**")
    cols[5].markdown("**Website**")
    cols[6].markdown("**Hotels**")
    cols[7].markdown("**Rating**")

    st.divider()

    for s in filtered:
        cols = st.columns([2.2, 1.4, 1.8, 1.3, 1.5, 1.5, 1.5, 0.8])

        if cols[0].button(
            s.get("company", "—"),
            key=f"view_{s['id']}",
            use_container_width=True,
        ):
            st.session_state["supplier_id"] = s["id"]
            st.session_state["detail_mode"] = "view"
            st.switch_page("pages/2_Supplier_Detail.py")

        cols[1].write(s.get("category") or "—")

        contact_parts = []
        if s.get("sex"):
            contact_parts.append(s["sex"])
        if s.get("first_name"):
            contact_parts.append(s["first_name"])
        if s.get("last_name"):
            contact_parts.append(s["last_name"])
        cols[2].write(" ".join(contact_parts) if contact_parts else "—")

        cols[3].write(s.get("phone1") or "—")
        cols[4].write(s.get("email") or "—")

        # Show website domain only (compact)
        web = s.get("website") or ""
        if web:
            web = web.replace("https://", "").replace("http://", "").replace("www.", "").rstrip("/")
        cols[5].write(web or "—")

        cols[6].write(hotel_badges(s.get("hotels")))
        cols[7].write(":star:" * (s.get("rating") or 0) if s.get("rating") else "—")
