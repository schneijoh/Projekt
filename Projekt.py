import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="HockeyAI Studio", page_icon="🏑", layout="wide")

HF_TOKEN = "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"

client = InferenceClient(token=HF_TOKEN)

st.title("🏑 HockeyAI Studio")
st.caption("Stabile Version • Stable Diffusion XL")

tab1, tab2, tab3 = st.tabs(["🎮 GameDay Blitz", "📸 Highlight Creator", "💡 Ideen"])

with tab1:
    st.subheader("GameDay Blitz")
    
    col1, col2 = st.columns(2)
    with col1:
        score = st.text_input("Ergebnis", "4:2")
        opponent = st.text_input("Gegner", "Mannheimer HC")
    with col2:
        scorers = st.text_area("Torschützen", "Lisa Müller - 2\nAnna Schmidt - 1")

    if st.button("🚀 Stories generieren", type="primary", use_container_width=True):
        with st.spinner("Generiere Bilder..."):
            base = f"field hockey match, score {score} vs {opponent}, {scorers}, green artificial turf, dynamic action, instagram story"
            
            for i in range(4):
                prompt = f"{base}, cinematic lighting, professional sports photo, high quality"
                
                image = client.text_to_image(
                    prompt=prompt,
                    model="stabilityai/stable-diffusion-xl-base-1.0",   # Stabileres Modell
                    width=576,
                    height=1024,
                    num_inference_steps=30,
                    guidance_scale=7.5
                )
                st.image(image, caption=f"Story {i+1}", use_column_width=True)

with tab2:
    st.subheader("Highlight Creator")
    if st.button("Test Bild generieren"):
        with st.spinner("Generiere..."):
            image = client.text_to_image(
                "dramatic field hockey goal celebration on green turf, cinematic lighting",
                model="stabilityai/stable-diffusion-xl-base-1.0",
                width=576,
                height=1024
            )
            st.image(image)

with tab3:
    st.subheader("Reel Ideen")
    if st.button("Ideen generieren"):
        response = client.text_generation(
            "Gib mir 6 gute Reel-Ideen für ein gewonnenes Feldhockey-Spiel",
            model="meta-llama/Llama-3.1-8B-Instruct"
        )
        st.write(response)

st.caption("Stabile Version mit SDXL")
