import streamlit as st
from journal_db import init_db

# Must be called first in Streamlit apps
st.set_page_config(
    page_title="Fadeaway Flow Engine",
    page_icon="💜",
    layout="wide"
)

# Initialize application configuration states
if 'brand_handle' not in st.session_state:
    st.session_state['brand_handle'] = "FadeawayFlow"

# Initialize local SQLite engine
init_db()

# Custom UI Theme Overrides: Purple, Gold, Dark Grey
st.markdown("""
    <style>
        /* Primary app background architecture */
        .stApp {
            background-color: #0F0F12 !important;
            color: #FFFFFF !important;
        }
        /* Custom Title or Headers containing brand styling elements */
        h1, h2, h3 {
            color: #FDB927 !important; /* Premium Gold */
            font-family: 'Helvetica Neue', sans-serif;
            font-weight: 800;
        }
        /* Metric block styling adjustments */
        div[data-testid="stMetricValue"] {
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }
        /* Left navigation sidebar panel color adjustments */
        section[data-testid="stSidebar"] {
            background-color: #16161A !important;
            border-right: 1px solid #2D2D34;
        }
        /* Custom border/div styles */
        hr {
            border-top: 1px solid #552583 !important; /* Deep Master Purple */
        }
    </style>
""", unsafe_allowed_code=True)

# Main Application Imports
from modules.dashboard import render_dashboard
from modules.journal import render_journal
from modules.analytics import render_analytics

# Navigation controls mapped to sidebar configuration choices
st.sidebar.title(f"@{st.session_state['brand_handle']}")
st.sidebar.markdown("`Technical Master Architecture` v1.0")
st.sidebar.markdown("---")

menu_selection = st.sidebar.radio(
    "Navigation Menu",
    ["Performance Dashboard", "Journal Entry Log", "Runner Metrics Analytics"]
)

# Handle modular app traffic routing based on active choice
if menu_selection == "Performance Dashboard":
    render_dashboard()
elif menu_selection == "Journal Entry Log":
    render_journal()
elif menu_selection == "Runner Metrics Analytics":
    render_analytics()
