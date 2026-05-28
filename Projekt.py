import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="HockeyAI Studio", page_icon="🏑", layout="wide")

st.title("🏑 HockeyAI Studio")

# Sicherer Token-Laden
if "HF_TOKEN" in st.secrets:
    token = st.secrets["HF_TOKEN"]
    st.success("✅ Token geladen!")
else:
    token = None
    st.error("❌ Token nicht gefunden in secrets.toml")

if token:
    client = InferenceClient(token=token)
    
    tab1, tab2 = st.tabs(["GameDay", "Test"])

    with tab1:
        st.write("Test - Wenn du das siehst, funktioniert der Token.")
        if st.button("FLUX Test Bild generieren"):
            with st.spinner("Generiere Test-Bild..."):
                image = client.text_to_image(
                    "field hockey player celebrating goal, green turf, cinematic",
                    model="black-forest-labs/FLUX.1-schnell"
                )
                st.image(image)
else:
    st.info("Bitte überprüfe die secrets.toml Datei")
