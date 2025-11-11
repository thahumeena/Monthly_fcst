# config.py — shared setup for all pages
import streamlit as st

def app_setup(page_title="Forecasters' Tools"):
    try:
        st.set_page_config(page_title=page_title, page_icon="🗺️", layout="wide")
    except Exception:
        pass

    # Hide Streamlit default toolbar/menu/footer
    hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden !important;}
    [data-testid="stDecoration"] {visibility: hidden !important;}
    [data-testid="stStatusWidget"] {visibility: hidden !important;}
    div[data-testid="stActionButton"] {visibility: hidden !important;}
    </style>
    """
    st.markdown(hide_style, unsafe_allow_html=True)

