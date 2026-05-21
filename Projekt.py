import streamlit as st
from huggingface_hub import InferenceClient
import os

st.set_page_config(page_title="HockeyAI Studio", page_icon="🏑", layout="wide")

hf_token = os.getenv("HF_TOKEN")
client = InferenceClient(token=hf_token) if hf_token else None

st.title("🏑 HockeyAI Studio")
st.caption("Feldhockey Content Creator • FLUX.1-schnell")

if not hf_token:
    st.error("HF_TOKEN fehlt noch in den Secrets!")
    st.stop()

tab1, tab2, tab3 = st.tabs(["🎮 GameDay Blitz", "📸 Highlight Creator", "💡 Ideen Generator"])

with tab1:
    st.subheader("GameDay Blitz - Story Pack")
    
    col1, col2 = st.columns(2)
    with col1:
        score = st.text_input("Endergebnis", "4:2")
        opponent = st.text_input("Gegner", "Mannheimer HC")
    with col2:
        scorers = st.text_area("Torschützen (ein pro Zeile)", "Lisa Müller - 2\nAnna Schmidt - 1")
        moments = st.text_area("Besondere Momente", "2 starke Strafecken • Comeback in H2")

    if st.button("🚀 6 Stories generieren", type="primary", use_container_width=True):
        with st.spinner("FLUX.1-schnell generiert deine Stories..."):
            base_prompt = f"field hockey match, final score {score} vs {opponent}, {scorers}, green artificial turf, dynamic action, high quality, instagram story"
            
            for i in range(6):
                style = ["golden hour lighting", "epic celebration", "intense action shot", 
                        "team spirit", "dramatic atmosphere", "victory moment"][i]
                
                prompt = f"{base_prompt}, {style}, cinematic, vibrant colors"
                
                try:
                    image = client.text_to_image(
                        prompt=prompt,
                        model="black-forest-labs/FLUX.1-schnell",
                        width=576,
                        height=1024
                    )
                    st.image(image, caption=f"Story {i+1} — {score} vs {opponent}", use_column_width=True)
                except Exception as e:
                    st.error(f"Fehler bei Bild {i+1}")

with tab2:
    st.subheader("Highlight Creator")
    uploaded = st.file_uploader("Foto hochladen (Tor, Spieler, Strafecke...)", type=["jpg","png","jpeg"])
    if uploaded:
        st.image(uploaded, width=600)
        extra = st.text_input("Extra Beschreibung / Stil", "dramatic cinematic lighting, epic")
        if st.button("Epische Version erstellen"):
            with st.spinner("Generiere..."):
                image = client.text_to_image(
                    f"field hockey action, {extra}, green turf, high quality",
                    model="black-forest-labs/FLUX.1-schnell"
                )
                st.image(image)

with tab3:
    st.subheader("Reel & Content Ideen")
    if st.button("Gute Ideen für diesen Spieltag generieren"):
        with st.spinner("Llama denkt nach..."):
            response = client.text_generation(
                f"Gib mir 8 kreative Instagram Reel und Story Ideen für ein Feldhockey Spiel. Ergebnis: {score} gegen {opponent}.",
                model="meta-llama/Llama-3.1-8B-Instruct",
                max_tokens=600
            )
            st.write(response)

st.caption("HockeyAI Studio • Powered by FLUX.1-schnell")
