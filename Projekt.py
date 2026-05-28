import streamlit as st
import os

st.title("🏑 HockeyAI Studio - Debug")

st.write("**Aktueller Ordnerinhalt:**")
try:
    files = os.listdir(".")
    st.write(files)
except:
    st.write("Konnte nicht lesen")

st.write("**Secrets vorhanden?**")
if "HF_TOKEN" in st.secrets:
    st.success("✅ HF_TOKEN gefunden!")
    st.write("Beginnt mit:", st.secrets["HF_TOKEN"][:15] + "...")
else:
    st.error("❌ HF_TOKEN nicht gefunden")
    st.write("Verfügbare Secrets Keys:", list(st.secrets.keys()))
