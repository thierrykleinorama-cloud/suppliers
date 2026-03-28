"""
Shared UI helpers — CSS, page title.
"""
import streamlit as st


HOTELS = ["MIAOU", "COIN", "WOUAF"]
SEX_OPTIONS = ["", "Mr", "Mrs"]


def sidebar_css():
    """Inject custom CSS for a cleaner look."""
    st.markdown(
        """
        <style>
        /* ===== Force white background everywhere ===== */
        :root, [data-testid="stAppViewContainer"] {
            --text-color: #111111 !important;
            --background-color: #ffffff !important;
        }

        html, body,
        [data-testid="stApp"],
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"],
        .main .block-container,
        .stApp {
            background-color: #ffffff !important;
        }

        /* Tighter sidebar */
        section[data-testid="stSidebar"] .block-container {
            padding-top: 1rem;
        }

        /* ===== ALL text: near-black ===== */
        p, span, label, div, li, h1, h2, h3, h4, h5, h6 {
            color: #111111 !important;
        }

        /* Restore button text colors */
        button[kind="primary"] span,
        button[kind="primary"] p,
        [data-testid="stBaseButton-primary"] span,
        [data-testid="stBaseButton-primary"] p {
            color: #ffffff !important;
        }

        /* ===== Input fields: white, dark text, smooth corners ===== */
        input[type="text"], textarea {
            color: #000000 !important;
            background-color: #ffffff !important;
            border: 1.5px solid #aaa !important;
            border-radius: 6px !important;
        }
        /* Selectbox */
        [data-baseweb="select"] > div {
            background-color: #ffffff !important;
            border: 1.5px solid #aaa !important;
            border-radius: 6px !important;
            color: #000000 !important;
        }
        [data-baseweb="select"] span {
            color: #000000 !important;
        }

        /* Disabled fields — keep text dark and readable */
        input:disabled, textarea:disabled {
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            opacity: 1 !important;
            background-color: #f4f4f4 !important;
            border-color: #ccc !important;
        }
        [data-baseweb="select"][aria-disabled="true"] > div,
        [data-baseweb="select"][aria-disabled="true"] span {
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            opacity: 1 !important;
        }

        /* ===== Form container: white, clean border ===== */
        [data-testid="stForm"] {
            background-color: #ffffff !important;
            border: 1px solid #ddd !important;
            border-radius: 8px !important;
            padding: 1.2rem !important;
        }

        /* Compact vertical spacing in forms */
        .stForm [data-testid="stVerticalBlock"] > div {
            margin-bottom: -0.3rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_title(icon_text: str, title: str):
    """Render a consistent page title."""
    st.markdown(f"## {icon_text}")
    st.caption(title)


def star_rating(rating: int | None) -> str:
    """Return star string for a rating value."""
    if not rating:
        return ""
    return ":star:" * rating


def hotel_badges(hotels: list[str] | None) -> str:
    """Return hotel names as a comma-separated string."""
    if not hotels:
        return ""
    return ", ".join(hotels)
