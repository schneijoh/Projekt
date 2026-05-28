import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="HockeyAI Studio", page_icon="🏑", layout="wide")

HF_TOKEN = "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"
client = InferenceClient(token=HF_TOKEN)

st.title("🏑 HockeyAI Studio")
st.caption("Stabile Version")

tab1, tab2 = st.tabs(["🎮 GameDay Blitz", "💡 Ideen"])

with tab1:
    st.subheader("GameDay Blitz")
    
    col1, col2 = st.columns(2)
    with col1:
        score = st.text_input("Ergebnis", "4:2")
        opponent = st.text_input("Gegner", "Mannheimer HC")
    with col2:
        scorers = st.text_area("Torschützen", "Thore Waaden - 1\nJohan Schneider - 3")
        moments = st.text_area("Besondere Momente", "Starke Strafecken • Comeback")

    if st.button("🚀 Zusammenfassung generieren", type="primary"):
        with st.spinner("Generiere..."):
            prompt = f"""Erstelle eine gute Instagram-Zusammenfassung für dieses Feldhockey-Spiel:

Ergebnis: {score} gegen {opponent}
Torschützen: {scorers}
Besondere Momente: {moments}

Schreibe:
- Eine starke Caption
- 5 Hashtags
- 3 Story-Ideen"""

            try:
                response = client.text_generation(
                    prompt,
                    model="mistralai/Mistral-7B-Instruct-v0.3",
                    max_new_tokens=600,      # <-- korrigiert
                    temperature=0.7
                )
                st.success("✅ Fertig!")
                st.write(response)
            except Exception as e:
                st.error("Fehler bei der Generierung")
                st.write(str(e)[:200])

with tab2:
    st.subheader("Schnelltest")
    if st.button("Test-Text generieren"):
        with st.spinner("Test läuft..."):
            try:
                response = client.text_generation(
                    "Schreibe eine kurze Begrüßung für einen Feldhockey Instagram-Account.",
                    model="mistralai/Mistral-7B-Instruct-v0.3",
                    max_new_tokens=100
                )
                st.write(response)
            except Exception as e:
                st.error(str(e)[:150])

st.caption("Stabile Version mit Mistral-7B")
