import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="HockeyAI Studio", page_icon="🏑", layout="wide")

HF_TOKEN = "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"

client = InferenceClient(token=HF_TOKEN)

st.title("🏑 HockeyAI Studio")
st.caption("Test mit bekannt stabilem Modell")

tab1, tab2 = st.tabs(["🎮 GameDay Blitz", "Test"])

with tab1:
    st.subheader("GameDay Blitz")
    
    col1, col2 = st.columns(2)
    with col1:
        score = st.text_input("Ergebnis", "4:2")
        opponent = st.text_input("Gegner", "Mannheimer HC")
    with col2:
        scorers = st.text_area("Torschützen", "Lisa Müller - 2\nAnna Schmidt - 1")

    if st.button("🚀 2 Stories generieren", type="primary"):
        with st.spinner("Generiere mit stabilem Modell..."):
            base = f"field hockey match, score {score} vs {opponent}, {scorers}, green turf, dynamic action"

            for i in range(2):
                prompt = f"{base}, cinematic lighting, professional sports photo, high quality"
                
                try:
                    image = client.text_to_image(
                        prompt=prompt,
                        model="stabilityai/stable-diffusion-2-1",   # Oft stabiler
                        width=512,
                        height=768,
                        num_inference_steps=20
                    )
                    st.image(image, caption=f"Story {i+1}", use_column_width=True)
                except Exception as e:
                    st.error(f"Fehler bei Bild {i+1}")
                    st.write(str(e)[:150])

with tab2:
    st.subheader("Schnelltest")
    if st.button("Einzelnes Test-Bild"):
        with st.spinner("Test läuft..."):
            try:
                image = client.text_to_image(
                    "field hockey player scoring goal on green field, cinematic",
                    model="stabilityai/stable-diffusion-2-1"
                )
                st.image(image)
            except Exception as e:
                st.error("Fehler:")
                st.write(str(e)[:250])

st.caption("Test mit stable-diffusion-2-1")
