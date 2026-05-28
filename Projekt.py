import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="HockeyAI Studio", page_icon="🏑", layout="wide")

HF_TOKEN = "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"
client = InferenceClient(token=HF_TOKEN)

st.title("🏑 HockeyAI Studio")
st.caption("Kostenlose stabile Version")

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
            prompt = f"""Du bist ein guter Social Media Manager für Feldhockey.
Erstelle eine ansprechende Spieltags-Zusammenfassung.

Spiel: {score} gegen {opponent}
Torschützen: {scorers}
Besondere Momente: {moments}

Gib aus:
1. Eine starke Instagram Caption (max 2-3 Sätze)
2. 5 passende Hashtags
3. 3 Story-Ideen"""

            response = client.chat.completions.create(
                model="meta-llama/Llama-3.1-8B-Instruct",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.7
            )
            st.write(response.choices[0].message.content)

with tab2:
    st.subheader("Reel & Story Ideen")
    if st.button("Reel-Ideen generieren"):
        with st.spinner("Generiere..."):
            response = client.chat.completions.create(
                model="meta-llama/Llama-3.1-8B-Instruct",
                messages=[{"role": "user", "content": f"Gib mir 8 kreative Reel und Story Ideen für ein Feldhockey Spiel {score} gegen {opponent}"}],
                max_tokens=600
            )
            st.write(response.choices[0].message.content)

with tab3:
    st.subheader("Caption Generator")
    theme = st.text_input("Thema / Stimmung", "Sieg, Kampfgeist")
    if st.button("Captions generieren"):
        with st.spinner("Generiere Captions..."):
            response = client.chat.completions.create(
                model="meta-llama/Llama-3.1-8B-Instruct",
                messages=[{"role": "user", "content": f"Schreibe 6 gute Instagram Captions für Feldhockey. Thema: {theme}. Ergebnis: {score} vs {opponent}"}],
                max_tokens=700
            )
            st.write(response.choices[0].message.content)

with tab4:
    st.subheader("Frage der Woche")
    if st.button("Frage der Woche generieren"):
        with st.spinner("Generiere..."):
            response = client.chat.completions.create(
                model="meta-llama/Llama-3.1-8B-Instruct",
                messages=[{"role": "user", "content": "Erstelle eine gute 'Frage der Woche' für einen Feldhockey Instagram Account"}],
                max_tokens=300
            )
            st.success(response.choices[0].message.content)

st.caption("Kostenlose stabile Version mit Llama 3.1")

