# Home.py

import streamlit as st

# --- Configuration ---
st.set_page_config(
    page_title="Forecasters' Tools",
    page_icon="🗺️",
    layout="wide"
)

# Hardcoded Credentials (You should use your own secure method for production)
USERNAME = "forecaster"
PASSWORD = "Maldives123"

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None

# Inject Custom CSS for the Blue Header Bar and Button Styling
st.markdown(
    """
    <style>
    /* CUSTOM BLUE HEADER BAR */
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
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    /* Push main content down to account for the fixed header */
    .st-emotion-cache-1g8i5u7, .st-emotion-cache-6qob1r, .st-emotion-cache-1y4pm5r {
        padding-top: 80px; 
    }
    
    /* CUSTOM BUTTON STYLING (Kept for consistency but no longer used in body) */
    div.stButton {
        display: flex;
        justify-content: center;
        margin-bottom: 5px; 
    }
    .stButton > button {
        width: 250px;
        height: 40px;
        margin: 5px 0;
        font-size: 16px;
        border: 1px solid #1E90FF; 
        color: #1E90FF;
        background-color: white;
    }
    .st-emotion-cache-1629p8f { /* Hide hamburger menu icon */
        display: none !important;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

def logout():
    """Clears authentication state and reruns the app to show login."""
    st.session_state['authenticated'] = False
    st.session_state['username'] = None
    st.rerun()

# --- Authentication Logic ---
if st.session_state['authenticated']:
    # --- LOGGED IN VIEW ---
    with st.sidebar:
        st.title("Navigation")
        st.markdown("---")
        st.button("Log Out", on_click=logout)

    st.markdown('<div class="main-header">Forecasters\' Tools</div>', unsafe_allow_html=True)

    # Main Page Content (Below the Header)
    col_left, col_center, col_right = st.columns([1, 2, 1])

    with col_center:
        st.markdown(f"<h3 style='text-align: center; margin-top: 20px;'>Welcome, {st.session_state['username']}! Select a Tool from the Sidebar Menu on the Left</h3>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Placeholder buttons removed as requested.

        st.info("Your custom map tools are now available as **'Rainfall Outlook'** and **'Temperature Outlook'** in the Streamlit sidebar menu.")

else:
    # --- LOGIN FORM VIEW ---
    st.markdown('<div class="main-header">Forecasters\' Tools - Login</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.5, 1])

    with col2:
        st.subheader("Sign In")
        with st.form("login_form"):
            username_input = st.text_input("Username")
            password_input = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Sign In")

            if submitted:
                if username_input == USERNAME and password_input == PASSWORD:
                    st.session_state['authenticated'] = True
                    st.session_state['username'] = username_input
                    st.success("Login successful! Redirecting to the main page...")
                    st.rerun()
                else:
                    st.error("Invalid Username or Password. Please try again.")

    # Stop the execution of the home page until the user is authenticated
    st.stop()
