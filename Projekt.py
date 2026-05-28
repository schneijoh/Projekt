import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="HockeyAI Studio", page_icon="🏑", layout="wide")

HF_TOKEN = "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"
client = InferenceClient(token=HF_TOKEN)

st.title("🏑 HockeyAI Studio")
st.caption("Kostenlose Version • Text + Ideen")

tab1, tab2, tab3, tab4 = st.tabs(["🎮 GameDay Blitz", "💡 Reel & Story Ideen", "📝 Captions", "❓ Frage der Woche"])

with tab1:
    st.subheader("GameDay Blitz")
    
    col1, col2 = st.columns(2)
    with col1:
        score = st.text_input("Ergebnis", "4:2")
        opponent = st.text_input("Gegner", "Mannheimer HC")
    with col2:
        scorers = st.text_area("Torschützen", "Lisa Müller - 2\nAnna Schmidt - 1")
        moments = st.text_area("Besondere Momente", "2 starke Strafecken • Comeback")

    if st.button("🚀 GameDay Zusammenfassung generieren", type="primary"):
        with st.spinner("Llama generiert..."):
            prompt = f"""Erstelle eine gute Spieltags-Zusammenfassung für Instagram für ein Feldhockey-Spiel.
Ergebnis: {score} gegen {opponent}
Torschützen: {scorers}
Besondere Momente: {moments}

Schreibe:
1. Eine kurze, starke Caption
2. 5 Hashtags
3. 3 Story-Ideen"""
            
            response = client.text_generation(prompt, model="meta-llama/Llama-3.1-8B-Instruct", max_tokens=800)
            st.write(response)

with tab2:
    st.subheader("Reel & Story Ideen")
    if st.button("Reel-Ideen generieren"):
        with st.spinner("Generiere Ideen..."):
            response = client.text_generation(
                f"Gib mir 8 kreative Instagram Reel und Story Ideen für ein Feldhockey Spiel {score} gegen {opponent}. Kurz und viral.",
                model="meta-llama/Llama-3.1-8B-Instruct"
            )
            st.write(response)

with tab3:
    st.subheader("Caption Generator")
    theme = st.text_input("Thema / Stimmung", "Sieg, Kampfgeist, Strafecken")
    if st.button("Captions generieren"):
        with st.spinner("Generiere Captions..."):
            response = client.text_generation(
                f"Schreibe 6 gute Instagram Captions für Feldhockey. Thema: {theme}. Ergebnis: {score} vs {opponent}",
                model="meta-llama/Llama-3.1-8B-Instruct"
            )
            st.write(response)

with tab4:
    st.subheader("Frage der Woche")
    if st.button("Frage der Woche generieren"):
        response = client.text_generation(
            "Erstelle eine gute 'Frage der Woche' für einen Feldhockey Instagram Account nach einem Spiel.",
            model="meta-llama/Llama-3.1-8B-Instruct"
        )
        st.success(response)

st.caption("Kostenlose Version • Llama 3.1 • Keine Bildkosten")
