"""
Suppliers — Directory for Hotel Noucentista
Streamlit entry point.
"""
import sys
from pathlib import Path

# Ensure project root is on sys.path
_root = str(Path(__file__).resolve().parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

import streamlit as st

st.set_page_config(
    page_title="Suppliers Directory",
    page_icon=":material/contacts:",
    layout="wide",
    initial_sidebar_state="expanded",
)

pg = st.navigation(
    {
        "": [
            st.Page("pages/1_Suppliers.py", title="Suppliers list", icon=":material/list:", default=True),
            st.Page("pages/2_Supplier_Detail.py", title="Supplier Detail", icon=":material/contact_page:"),
        ],
    }
)

pg.run()
