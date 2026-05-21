import streamlit as st

st.title("🏑 HockeyAI Studio - Token Test")

# Token aus secrets.toml laden
token = st.secrets.get("HF_TOKEN")

if token and token.startswith("hf_"):
    st.success("✅ Token wurde erfolgreich geladen!")
    st.write("Token beginnt mit:", token[:15] + "...")
else:
    st.error("❌ Token konnte nicht geladen werden")
    st.write("Aktueller Token-Wert:", token)

st.write("---")
st.info("Stelle sicher, dass die Datei `.streamlit/secrets.toml` existiert")
