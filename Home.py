# Home.py

import streamlit as st
import streamlit.components.v1 as components

# --- Setup is commented out as it relies on external file ---
# from config import app_setup
# app_setup("Forecasters' Tools")

# ---------------------------
# 0. PAGE CONFIG (safe wrapper)
# ---------------------------
try:
    st.set_page_config(
        page_title="Forecasters' Tools",
        page_icon="🗺️",
        layout="wide"
    )
    _page_config_ok = True
except Exception as e:
    _page_error = str(e)
    _page_config_ok = False

# ---------------------------
# 1. HIDE STREAMLIT UI (Toolbar, Menu, Footer) + Custom CSS
# ---------------------------
hide_streamlit_style = """
    <style>
    /* Hide Streamlit default UI elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden !important;}
    [data-testid="stDecoration"] {visibility: hidden !important;}
    [data-testid="stStatusWidget"] {visibility: hidden !important;}
    div[data-testid="stActionButton"] {visibility: hidden !important;}
    
    /* Center and style the login form container */
    .login-container {
        display: flex;
        justify-content: center;
        margin-top: 50px;
    }
    .login-box {
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        width: 100%;
        max-width: 300px; /* NARROWER WIDTH FOR INPUTS */
        background-color: white; 
    }
    .login-box label {
        font-weight: bold;
    }
    /* Style for the Sign In button within the form */
    .login-box .stButton button {
        background-color: #1E90FF;
        color: white;
        width: 100%;
        margin-top: 15px;
        border: none;
    }
    .login-box .stButton button:hover {
        background-color: #1a7ae2;
        color: white;
    }
    
    /* General styles from previous versions */
    .main-header {
        background-color: #1E90FF;
        color: white;
        padding: 10px 0;
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 1000;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
    }
    .logout-link {
        position: absolute;
        right: 20px;
        top: 12px;
        font-size: 14px;
        color: white;
        text-decoration: none;
    }
    .logout-link:hover { text-decoration: underline; }
    .stApp > .main > div {
        padding-top: 84px;
    }
    /* This generic button style is now only for the main page buttons, not login */
    div.stButton {
        display: flex;
        justify-content: center;
        margin-bottom: 6px;
    }
    .stButton > button {
        width: 250px;
        height: 40px;
        margin: 5px 0;
        font-size: 16px;
        border: 1px solid #1E90FF;
        color: #1E90FF;
        background-color: white;
        border-radius: 6px;
    }
    .stButton > button:hover {
        background-color: #1E90FF;
        color: white;
    }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ---------------------------
# 2. HEADER + STATIC COMPONENT
# ---------------------------
HEADER_HTML = """
<div class="main-header" id="mainHeader">
  Forecasters' Tools
  <span class="logout-link" id="logoutAnchor"></span>
</div>
"""
components.html(HEADER_HTML, height=10)


# ---------------------------
# 3. PAGE CONFIG ERROR HANDLER
# ---------------------------
if not _page_config_ok:
    st.warning(
        "⚠️ Page configuration failed. Check 'Manage app → Logs' for details."
    )
    st.caption(f"Error detail: {_page_error}")

# ---------------------------
# 4. LOGIN SYSTEM
# ---------------------------
# Using hardcoded credentials as requested by user
USER_CREDENTIALS = {"forecaster": "Maldives123"} 

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

def do_login(username, password):
    username = (username or "").strip()
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.rerun()
    else:
        st.error("Invalid username or password")

def do_logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

# ---------------------------
# 5. LOGIN PAGE (ENHANCED UI)
# ---------------------------
if not st.session_state.logged_in:
    # Title and subtitle
    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>🔒 Forecasters' Tools — Sign In</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; margin-top:-10px; color:#555;'>Please sign in to access MMS tools.</p>", unsafe_allow_html=True)

    # Centering the login box
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        
        # Streamlit Form
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Sign In")
            
            if submitted:
                do_login(username, password)
        
        st.markdown('</div>', unsafe_allow_html=True) # Close login-box
    st.markdown('</div>', unsafe_allow_html=True) # Close login-container
    
    st.stop()

# ---------------------------
# 6. MAIN APP (After Login)
# ---------------------------
header_cols = st.columns([1, 9, 1])
with header_cols[2]:
    if st.button(f"Log Out ({st.session_state.username})"):
        do_logout()

col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    st.markdown("<h3 style='text-align: center; margin-top: 8px;'>Select a Tool from the Sidebar Menu on the Left</h3>", unsafe_allow_html=True)
    st.markdown("---")

    # Placeholder buttons (updated list)
    st.button("Tide Chart")
    st.button("Alert Graphic")
    st.button("Forecast Graphic")
    st.button("Weekend Forecast")
    st.button("Satellite Image")
    st.button("Forecast App (Testing)")
    st.button("Weather News")
    st.button("Cloud Sketch") # <-- NEW BUTTON ADDED HERE

    st.markdown("---")
    st.info("Your custom map tools are available as **'Rainfall Outlook'** and **'Temperature Outlook'** in the sidebar.")
