import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="HockeyAI Studio", page_icon="🏑", layout="wide")

HF_TOKEN = "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"
client = InferenceClient(token=HF_TOKEN)

st.title("🏑 HockeyAI Studio")
st.caption("Kostenlose stabile Version")

tab1, tab2, tab3 = st.tabs(["🎮 GameDay Blitz", "💡 Ideen", "📝 Captions"])

with tab1:
    st.subheader("GameDay Blitz")
    
    col1, col2 = st.columns(2)
    with col1:
        score = st.text_input("Ergebnis", "4:2")
        opponent = st.text_input("Gegner", "Mannheimer HC")
    with col2:
        scorers = st.text_area("Torschützen", "Lisa Müller - 2\nAnna Schmidt - 1")
        moments = st.text_area("Besondere Momente", "Starke Strafecken • Comeback")

    if st.button("🚀 Zusammenfassung generieren", type="primary"):
        with st.spinner("Generiere..."):
            prompt = f"""Erstelle eine gute Instagram Zusammenfassung für ein Feldhockey Spiel.

Spiel: {score} gegen {opponent}
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
                    max_tokens=700,
                    temperature=0.7
                )
                st.write(response)
            except Exception as e:
                st.error("Fehler bei der Generierung")
                st.write(str(e)[:150])

with tab2:
    st.subheader("Reel & Story Ideen")
    if st.button("Ideen generieren"):
        with st.spinner("Generiere Ideen..."):
            response = client.text_generation(
                f"Gib mir 8 kreative Reel und Story Ideen für ein Feldhockey Spiel {score} gegen {opponent}",
                model="mistralai/Mistral-7B-Instruct-v0.3",
                max_tokens=600
            )
            st.write(response)

with tab3:
    st.subheader("Caption Generator")
    if st.button("Captions generieren"):
        with st.spinner("Generiere Captions..."):
            response = client.text_generation(
                f"Schreibe 6 gute Instagram Captions für ein Feldhockey Spiel. Ergebnis: {score} vs {opponent}",
                model="mistralai/Mistral-7B-Instruct-v0.3",
                max_tokens=600
            )
            st.write(response)

st.caption("Kostenlose Version mit Mistral-7B")
