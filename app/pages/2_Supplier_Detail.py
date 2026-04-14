"""
Suppliers — Detail / Edit / New
Compact layout: all data for one supplier on a single screen.
"""
import sys
from pathlib import Path

_root = str(Path(__file__).resolve().parent.parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

import streamlit as st
from app.components.ui import sidebar_css, page_title, HOTELS, SEX_OPTIONS
from src.services.supplier_queries import (
    fetch_supplier,
    fetch_categories,
    create_supplier,
    update_supplier,
    delete_supplier,
    create_category,
)

# -- Session state defaults --
if "supplier_id" not in st.session_state:
    st.session_state["supplier_id"] = None
if "detail_mode" not in st.session_state:
    st.session_state["detail_mode"] = "new"

sidebar_css()

supplier_id = st.session_state.get("supplier_id")
mode = st.session_state.get("detail_mode", "new")

# Load existing supplier data if viewing/editing
supplier = {}
if supplier_id and mode in ("view", "edit"):
    supplier = fetch_supplier(supplier_id) or {}
    if not supplier:
        st.error("Supplier not found.")
        st.stop()

is_new = mode == "new"
is_edit = mode == "edit"
is_view = mode == "view"

# -- Title & action bar --
if is_new:
    page_title(":material/person_add: New Supplier", "Create a new supplier")
else:
    page_title(
        f":material/contact_page: {supplier.get('company', '')}",
        "View or edit supplier details",
    )

# -- Mode indicator --
if not is_new:
    if is_view:
        st.caption("You are in view mode")
    else:
        st.caption("You are in Edit mode")

# -- Buttons row (all on same line, no captions) --
col_back, col_mode, col_delete = st.columns([1, 1, 1])

with col_back:
    if st.button(":material/arrow_back: Back to list"):
        st.switch_page("pages/1_Suppliers.py")

if not is_new:
    with col_mode:
        if is_view:
            if st.button(":material/edit: Go to Edit mode", type="primary"):
                st.session_state["detail_mode"] = "edit"
                st.rerun()
        else:
            if st.button(":material/visibility: Go to View mode"):
                st.session_state["detail_mode"] = "view"
                st.rerun()

    with col_delete:
        if st.button(":material/delete: Delete", type="secondary"):
            st.session_state["confirm_delete"] = True

        if st.session_state.get("confirm_delete"):
            st.warning("Are you sure you want to delete this supplier?")
            c1, c2 = st.columns(2)
            if c1.button("Yes, delete", type="primary"):
                delete_supplier(supplier_id)
                st.session_state["confirm_delete"] = False
                st.session_state["supplier_id"] = None
                st.switch_page("pages/1_Suppliers.py")
            if c2.button("Cancel"):
                st.session_state["confirm_delete"] = False
                st.rerun()

st.divider()

disabled = is_view

# -- Categories --
categories = fetch_categories()
CAT_OTHER = "+ New category..."
cat_options = categories + [CAT_OTHER]
def _s(key: str) -> str:
    return supplier.get(key) or ""

current_cat = _s("category")
cat_index = cat_options.index(current_cat) if current_cat in cat_options else 0

# -- Compact form --
with st.form("supplier_form"):

    # === Line 1: Company, Category, Hotels, Tags ===
    c1, c2, c3, c4, c5, c6 = st.columns([2.5, 1.8, 0.8, 0.7, 0.8, 1.5])
    company = c1.text_input("Company *", value=_s("company"), disabled=disabled, max_chars=60)
    selected_category = c2.selectbox("Category", options=cat_options, index=cat_index if current_cat in cat_options else 0, disabled=disabled)
    current_hotels = supplier.get("hotels") or []
    selected_hotels = []
    c3.markdown("<div style='margin-bottom:0.45rem'>&nbsp;</div>", unsafe_allow_html=True)
    c4.markdown("<div style='margin-bottom:0.45rem'>&nbsp;</div>", unsafe_allow_html=True)
    c5.markdown("<div style='margin-bottom:0.45rem'>&nbsp;</div>", unsafe_allow_html=True)
    if c3.checkbox("MIAOU", value="MIAOU" in current_hotels, disabled=disabled):
        selected_hotels.append("MIAOU")
    if c4.checkbox("COIN", value="COIN" in current_hotels, disabled=disabled):
        selected_hotels.append("COIN")
    if c5.checkbox("WOUAF", value="WOUAF" in current_hotels, disabled=disabled):
        selected_hotels.append("WOUAF")
    tags_str = ", ".join(supplier.get("tags") or [])
    tags_input = c6.text_input("Tags", value=tags_str, disabled=disabled, help="Comma-separated keywords")

    new_category_name = ""
    if selected_category == CAT_OTHER and not disabled:
        new_category_name = st.text_input("New category name", max_chars=40)

    # === Line 2: Title, Last name, First name, Phone1, Phone2 ===
    c1, c2, c3, c4, c5 = st.columns([0.6, 1.8, 1.8, 1.2, 1.2])
    sex_value = _s("sex")
    sex = c1.selectbox("Title", options=SEX_OPTIONS, index=SEX_OPTIONS.index(sex_value) if sex_value in SEX_OPTIONS else 0, disabled=disabled)
    last_name = c2.text_input("Last name", value=_s("last_name"), disabled=disabled, max_chars=40)
    first_name = c3.text_input("First name", value=_s("first_name"), disabled=disabled, max_chars=40)
    phone1 = c4.text_input("Phone 1", value=_s("phone1"), disabled=disabled, max_chars=20)
    phone2 = c5.text_input("Phone 2", value=_s("phone2"), disabled=disabled, max_chars=20)

    # === Line 3: Email, Website, Facebook, Instagram ===
    c1, c2, c3, c4 = st.columns(4)
    email = c1.text_input("Email", value=_s("email"), disabled=disabled, max_chars=60)
    website = c2.text_input("Website", value=_s("website"), disabled=disabled, max_chars=80)
    facebook = c3.text_input("Facebook", value=_s("facebook"), disabled=disabled, max_chars=80)
    instagram = c4.text_input("Instagram", value=_s("instagram"), disabled=disabled, max_chars=80)

    # === Line 4: Address, City, Country ===
    c1, c2, c3 = st.columns([4, 2, 1.5])
    address = c1.text_input("Address", value=_s("address"), disabled=disabled, max_chars=100)
    city = c2.text_input("City", value=_s("city"), disabled=disabled, max_chars=40)
    country = c3.text_input("Country", value=_s("country") or "Spain", disabled=disabled, max_chars=30)

    # === Line 5: VAT, Payment terms, IBAN, Rating ===
    c1, c2, c3, c4 = st.columns([1.2, 1.2, 2, 1])
    vat_number = c1.text_input("VAT number", value=_s("vat_number"), disabled=disabled, max_chars=20)
    payment_terms = c2.text_input("Payment terms", value=_s("payment_terms"), disabled=disabled, max_chars=20)
    iban = c3.text_input("IBAN", value=_s("iban"), disabled=disabled, max_chars=34)
    rating = c4.slider("Rating", min_value=0, max_value=5, value=supplier.get("rating") or 0, disabled=disabled, help="0 = not rated")

    # === Line 6: Notes (full width) ===
    notes = st.text_area("Notes", value=_s("notes"), height=80, disabled=disabled)

    # === Submit ===
    if is_view:
        # Streamlit requires a submit button in every form — hide it in view mode
        st.markdown("<style>[data-testid='stFormSubmitButton'] { display: none; }</style>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Save", disabled=True)
    else:
        submitted = st.form_submit_button(
            "Save" if not is_new else "Create Supplier",
            type="primary",
        )

    if submitted:
        if not company.strip():
            st.error("Company name is required.")
            st.stop()

        final_category = selected_category
        if selected_category == CAT_OTHER:
            if new_category_name.strip():
                final_category = new_category_name.strip()
                create_category(final_category)
            else:
                final_category = None

        tags = [t.strip() for t in tags_input.split(",") if t.strip()] if tags_input else None

        data = {
            "company": company.strip(),
            "category": final_category if final_category else None,
            "sex": sex if sex else None,
            "last_name": last_name.strip() if last_name.strip() else None,
            "first_name": first_name.strip() if first_name.strip() else None,
            "phone1": phone1.strip() if phone1.strip() else None,
            "phone2": phone2.strip() if phone2.strip() else None,
            "email": email.strip() if email.strip() else None,
            "website": website.strip() if website.strip() else None,
            "facebook": facebook.strip() if facebook.strip() else None,
            "instagram": instagram.strip() if instagram.strip() else None,
            "address": address.strip() if address.strip() else None,
            "city": city.strip() if city.strip() else None,
            "country": country.strip() if country.strip() else None,
            "vat_number": vat_number.strip() if vat_number.strip() else None,
            "payment_terms": payment_terms.strip() if payment_terms.strip() else None,
            "iban": iban.strip() if iban.strip() else None,
            "hotels": selected_hotels if selected_hotels else None,
            "rating": rating if rating > 0 else None,
            "notes": notes.strip() if notes.strip() else None,
            "tags": tags,
        }

        if is_new:
            result = create_supplier(data)
            st.success(f"Supplier **{company}** created!")
            st.session_state["supplier_id"] = result["id"]
            st.session_state["detail_mode"] = "view"
            st.rerun()
        else:
            update_supplier(supplier_id, data)
            st.success("Supplier updated!")
            st.session_state["detail_mode"] = "view"
            st.rerun()
