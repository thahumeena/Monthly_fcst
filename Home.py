# Home.py
import os
import streamlit as st
import streamlit.components.v1 as components

# ---------------------------
# 0. Defensive: wrap set_page_config to avoid Cloud crashes
# ---------------------------
try:
    st.set_page_config(
        page_title="Forecasters' Tools",
        page_icon="🗺️",
        layout="wide"
    )
    _page_config_ok = True
except Exception as e:
    # If set_page_config fails (some Cloud environments restrict or raise),
    # keep going but surface a helpful message to the developer in the UI.
    _page_config_ok = False
    _page_config_error = str(e)

# ---------------------------
# 1. Header + CSS via components.html
# ---------------------------
HEADER_HTML = """
<style>
/* Hide default Streamlit menu + footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* MAIN HEADER */
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

/* Logout link placeholder (visual only) */
.logout-link {
    position: absolute;
    right: 20px;
    top: 12px;
    font-size: 14px;
    color: white;
    text-decoration: none;
}
.logout-link:hover { text-decoration: underline; }

/* Push main content down to account for the fixed header */
.stApp > .main > div {
    padding-top: 84px;
}

/* Centered stacked buttons styling */
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

<div class="main-header" id="mainHeader">
  Forecasters' Tools
  <span class="logout-link" id="logoutAnchor"></span>
</div>
"""

# components.html rarely fails on Cloud; small height to avoid big blank area.
components.html(HEADER_HTML, height=10)

# ---------------------------
# 2. If set_page_config failed, show a visible banner for troubleshooting
# ---------------------------
if not _page_config_ok:
    st.warning(
        "Note: `st.set_page_config()` raised an exception in this environment. "
        "The app will still run, but page configuration was not applied. "
        "If you're on Streamlit Cloud, check **Manage app → Logs** for the full error."
    )
    # Optional: show the short error for quick debugging (safe to reveal here)
    st.caption(f"set_page_config error (short): {_page_config_error}")

# ---------------------------
# 3. Simple authentication (session-state)
# ---------------------------
USER_CREDENTIALS = {"forecaster": "mms123"}  # demo only — replace with secure backend

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

def do_login(username: str, password: str):
    username = (username or "").strip()
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        # Rerun to load main UI
        try:
            st.experimental_rerun()
        except Exception:
            # fallback: just continue and let UI refresh naturally
            pass
    else:
        st.error("Invalid username or password")

def do_logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    try:
        st.experimental_rerun()
    except Exception:
        pass

# ---------------------------
# 4. LOGIN PAGE
# ---------------------------
if not st.session_state.logged_in:
    # Vertical spacing
    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>🔒 Forecasters' Tools — Sign In</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; margin-top:-10px;'>Please sign in to access MMS tools.</p>", unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("Username", key="form_username")
        password = st.text_input("Password", type="password", key="form_password")
        submitted = st.form_submit_button("Sign In")
        if submitted:
            do_login(username, password)

    st.info("Demo credentials — Username: `forecaster`  Password: `mms123`")
    st.stop()

# ---------------------------
# 5. MAIN APP (after login)
# ---------------------------

# Show a small logout button at top-right region (invisible headerAnchor not easily hookable)
header_cols = st.columns([1, 9, 1])
with header_cols[2]:
    if st.button(f"Log Out ({st.session_state.username})"):
        do_logout()

# Buttons layout
col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    st.markdown("<h3 style='text-align: center; margin-top: 8px;'>Select a Tool from the Sidebar Menu on the Left</h3>", unsafe_allow_html=True)
    st.markdown("---")

    # Buttons (wire these to pages or callbacks later)
    if st.button("Tide Chart"):
        st.info("Tide Chart clicked — wire this to a page or callback.")
    if st.button("Alert Graphic"):
        st.info("Alert Graphic clicked — wire this to a page or callback.")
    if st.button("Forecast Graphic"):
        st.info("Forecast Graphic clicked — wire this to a page or callback.")
    if st.button("Weekend Forecast"):
        st.info("Weekend Forecast clicked — wire this to a page or callback.")
    if st.button("Satellite Image"):
        st.info("Satellite Image clicked — wire this to a page or callback.")
    if st.button("Forecast App (Testing)"):
        st.info("Forecast App (Testing) clicked — wire this to a page or callback.")
    if st.button("Weather News"):
        st.info("Weather News clicked — wire this to a page or callback.")

    st.markdown("---")
    st.info("Your custom map tools are available as **'Rainfall Outlook'** and **'Temperature Outlook'** in the sidebar menu (add them under pages/ or via sidebar components).")

# Small footer logout link
st.markdown("<br><center><a href='#' style='color:#1E90FF;' onclick='window.location.reload();'>🔓 Log Out</a></center>", unsafe_allow_html=True)
