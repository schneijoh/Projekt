import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="HockeyAI Studio", page_icon="🏑", layout="wide")

HF_TOKEN = "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"

client = InferenceClient(token=HF_TOKEN)

st.title("🏑 HockeyAI Studio")
st.caption("Stabile Version - Versuch 4")

tab1, tab2 = st.tabs(["🎮 GameDay Blitz", "📸 Test"])

with tab1:
    st.subheader("GameDay Blitz")
    
    col1, col2 = st.columns(2)
    with col1:
        score = st.text_input("Ergebnis", "4:2")
        opponent = st.text_input("Gegner", "Mannheimer HC")
    with col2:
        scorers = st.text_area("Torschützen", "Lisa Müller - 2\nAnna Schmidt - 1")

    if st.button("🚀 Stories generieren", type="primary"):
        with st.spinner("Versuche Bilder zu generieren..."):
            base = f"field hockey, score {score} vs {opponent}, {scorers}, green turf, dynamic action"

            for i in range(3):
                prompt = f"{base}, professional sports photo, cinematic, high quality, vibrant"
                
                try:
                    image = client.text_to_image(
                        prompt=prompt,
                        model="runwayml/stable-diffusion-v1-5",   # Sehr altes aber stabiles Modell
                        width=512,
                        height=768,
                        num_inference_steps=25
                    )
                    st.image(image, caption=f"Story {i+1}", use_column_width=True)
                except Exception as e:
                    st.error(f"Fehler bei Bild {i+1}: {str(e)[:100]}...")

with tab2:
    st.subheader("Schnelltest")
    if st.button("Einzelnes Test-Bild"):
        with st.spinner("Generiere..."):
            try:
                image = client.text_to_image(
                    "field hockey player scoring a goal on green field, cinematic",
                    model="runwayml/stable-diffusion-v1-5",
                    width=512,
                    height=768
                )
                st.image(image)
            except Exception as e:
                st.error(str(e)[:200])

st.caption("Stabile Version mit stable-diffusion-v1-5")
