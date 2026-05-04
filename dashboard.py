import streamlit as st
import os

# Simple Streamlit Auth
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if password == os.environ.get("STREAMLIT_PASSWORD"):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Wrong password")
    st.stop()

# Pages
# dashboard.py
pg = st.navigation([
    st.Page("overview.py", title="Dashboard"),
    st.Page("review_form.py", title="Weekly Review"),
])
pg.run()

