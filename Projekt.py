import streamlit as st

st.set_page_config(page_title="HockeyAI Studio", page_icon="🏑", layout="wide")

st.title("🏑 HockeyAI Studio")
st.success("✅ Streamlit läuft endlich!")

st.write("Super! Die Basis funktioniert.")
st.write("Jetzt bauen wir FLUX schrittweise ein.")

if st.button("Test"):
    st.balloons()
    st.snow()
