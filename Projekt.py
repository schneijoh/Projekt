import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="HockeyAI Studio", page_icon="🏑", layout="wide")

st.title("🏑 HockeyAI Studio")

HF_TOKEN = "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"   

if HF_TOKEN and HF_TOKEN.startswith("hf_"):
    client = InferenceClient(token=HF_TOKEN)
    st.success("✅ Token geladen - App ist bereit!")
    
    if st.button("Test-Bild mit FLUX generieren"):
        with st.spinner("FLUX.1-schnell generiert..."):
            image = client.text_to_image(
                "field hockey player celebrating a goal on green turf, cinematic lighting, dynamic action",
                model="black-forest-labs/FLUX.1-schnell"
            )
            st.image(image, caption="Test Bild - FLUX.1-schnell")
else:
    st.error("Token fehlt oder ist ungültig.")

st.caption("HockeyAI Studio • Test Version")
