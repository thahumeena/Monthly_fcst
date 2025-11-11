# Home.py

import streamlit as st

# --- Configuration ---
st.set_page_config(
    page_title="Forecasters' Tools",
    page_icon="🗺️",
    layout="wide"
)

# Hardcoded Credentials
USERNAME = "forecaster"
PASSWORD = "Maldives123"

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None

# Custom CSS for Header and Styling
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
    /* Hide the default Streamlit footer and hamburger menu */
    .st-emotion-cache-1629p8f {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Authentication Logic ---
if st.session_state['authenticated']:
    # --- LOGGED IN VIEW ---
    st.markdown('<div class="main-header">Forecasters\' Tools</div>', unsafe_allow_html=True)

    def logout():
        """Clears authentication state and reruns the app to show login."""
        st.session_state['authenticated'] = False
        st.session_state['username'] = None
        st.rerun()

    with st.sidebar:
        st.title("Navigation")
        # Links appear automatically due to files in the 'pages' folder.
        st.markdown("---")
        st.button("Log Out", on_click=logout)

    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        st.markdown(
            f"<h3 style='text-align: center; margin-top: 20px;'>Welcome, {st.session_state['username']}!</h3>", 
            unsafe_allow_html=True
        )
        st.markdown(
            "<h4 style='text-align: center;'>Please select a map from the sidebar menu to view the outlook.</h4>", 
            unsafe_allow_html=True
        )

else:
    # --- LOGIN FORM VIEW ---
    st.markdown('<div class="main-header">Forecasters\' Tools - Login</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.5, 1])

    with col2:
        st.subheader("Sign In")
        with st.form("login_form"):
            username_input = st.text_input("Username")
            # Use the requested username and password
            # username: forecaster. password Maldives123
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
