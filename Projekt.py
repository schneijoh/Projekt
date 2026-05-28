import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="HockeyAI Studio", page_icon="🏑", layout="wide")

HF_TOKEN = "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"

client = InferenceClient(token=HF_TOKEN)

st.title("🏑 HockeyAI Studio")
st.caption("Stabile Version - Working Model")

tab1, tab2 = st.tabs(["🎮 GameDay Blitz", "Test"])

with tab1:
    st.subheader("GameDay Blitz")
    
    col1, col2 = st.columns(2)
    with col1:
        score = st.text_input("Ergebnis", "4:2")
        opponent = st.text_input("Gegner", "Mannheimer HC")
    with col2:
        scorers = st.text_area("Torschützen", "Lisa Müller - 2\nAnna Schmidt - 1")

    if st.button("🚀 2 Stories generieren", type="primary", use_container_width=True):
        with st.spinner("Generiere mit stabilem Modell..."):
            base = f"field hockey, score {score} vs {opponent}, {scorers}, green turf, dynamic action, instagram story"

            for i in range(2):
                prompt = f"{base}, cinematic lighting, professional sports photography, high quality"
                
                try:
                    image = client.text_to_image(
                        prompt=prompt,
                        model="runwayml/stable-diffusion-v1-5",   # Sehr bekanntes & stabiles Modell
                        width=512,
                        height=768,
                        num_inference_steps=25,
                        guidance_scale=7.5
                    )
                    st.image(image, caption=f"Story {i+1} — {score} vs {opponent}", use_column_width=True)
                except Exception as e:
                    st.error(f"Fehler bei Bild {i+1}")
                    st.write(str(e)[:150])

with tab2:
    st.subheader("Schnelltest")
    if st.button("Test-Bild generieren"):
        with st.spinner("Test läuft..."):
            try:
                image = client.text_to_image(
                    "field hockey player celebrating goal on green turf, cinematic",
                    model="runwayml/stable-diffusion-v1-5",
                    width=512,
                    height=768
                )
                st.image(image)
            except Exception as e:
                st.error(str(e)[:200])

st.caption("Stabile Version mit stable-diffusion-v1-5")
