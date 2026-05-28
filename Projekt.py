import streamlit as st

st.title("🏑 HockeyAI Studio - Final Test")

try:
    token = st.secrets["HF_TOKEN"]
    st.success("✅ Token erfolgreich geladen!")
    st.write("Token beginnt mit:", token[:20] + "...")
except Exception as e:
    st.error("❌ Fehler beim Laden des Tokens")
    st.write("Fehlermeldung:", str(e))
    st.write("Verfügbare Secrets:", list(st.secrets.keys()))
