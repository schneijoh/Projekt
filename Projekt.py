import streamlit as st
import os

st.title("Token Test")

token = os.getenv("HF_TOKEN")

if token:
    st.success("✅ Token wurde gefunden!")
    st.write("Token beginnt mit:", token[:10] + "...")
else:
    st.error("❌ Token wurde NICHT gefunden")
    st.write("os.getenv('HF_TOKEN') = None")

st.write("---")
st.write("Alle Secrets:", os.environ.keys())
