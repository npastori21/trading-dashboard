import streamlit as st
import hashlib


def check_password():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.subheader("🔒 Enter Password to Access App")
        password_input = st.text_input("Password", type="password")
        if st.button("Submit"):
            hashed_input = hashlib.sha256(password_input.encode()).hexdigest()
            if hashed_input == st.secrets["PW"]:
                st.session_state["authenticated"] = True
                st.success("✅ Access Granted")
                st.experimental_rerun()
            else:
                st.error("❌ Incorrect Password")
        st.stop()

def check_auth():
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.warning("🔒 Please log in to access this page.")
        st.switch_page("pages/home.py")