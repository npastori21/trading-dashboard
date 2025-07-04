import streamlit as st
import hashlib

def verify_password(password_input: str, stored_hash: str) -> bool:
    return hashlib.sha256(password_input.encode()).hexdigest() == stored_hash

def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        with st.form("login_form"):
            password = st.text_input("Enter password", type="password")
            submitted = st.form_submit_button("Login")

            if submitted:
                stored_hash = st.secrets["PW"]
                if verify_password(password, stored_hash):
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("❌ Incorrect password")
        st.stop()

def check_auth():
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.warning("🔒 Please log in to access this page.")
        st.switch_page("pages/home.py")