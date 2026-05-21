import streamlit as st
from PIL import Image
from huggingface_hub import InferenceClient
import os

st.set_page_config(page_title="HockeyAI Studio", page_icon="🏑", layout="wide")

# Token laden
hf_token = os.getenv("HF_TOKEN")

st.title("🏑 HockeyAI Studio")
st.caption("Feldhockey Content AI | FLUX + Llama")

if not hf_token:
    st.warning("⚠️ HF_TOKEN noch nicht gesetzt. Gehe zu Settings → Secrets und füge 'HF_TOKEN' hinzu.")
else:
    client = InferenceClient(token=hf_token)

# Tabs
tab1, tab2, tab3 = st.tabs(["🎮 GameDay Stories", "📸 Highlight Generator", "💡 Reel Ideen"])

with tab1:
    st.subheader("GameDay Story Generator")
    score = st.text_input("Ergebnis", "4:2")
    opponent = st.text_input("Gegner", "Mannheimer HC")
    scorers = st.text_area("Torschützen", "Lisa Müller - 2\nAnna Schmidt - 1")
    
    if st.button("🚀 Stories mit FLUX generieren", type="primary"):
        with st.spinner("FLUX.1-schnell generiert 4 Stories..."):
            base = f"Feldhockey Spiel {score} gegen {opponent}, Torschützen: {scorers}, grüner Kunstrasen, dynamische Action"
            
            for i in range(4):
                prompt = f"{base}, Instagram Story Format, hohe Qualität, dramatisch, {['golden hour', 'epic celebration', 'intense action', 'team spirit'][i]}"
                try:
                    image = client.text_to_image(
                        prompt=prompt,
                        model="black-forest-labs/FLUX.1-schnell"
                    )
                    st.image(image, caption=f"Story {i+1}", use_column_width=True)
                except Exception as e:
                    st.error(f"Fehler bei Bild {i+1}: {e}")

with tab2:
    st.subheader("Highlight Generator")
    uploaded_file = st.file_uploader("Foto hochladen", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, caption="Original", width=500)
        
        extra = st.text_input("Zusätzlicher Stil", "dramatic cinematic lighting, epic")
        if st.button("Episch machen"):
            with st.spinner("Generiere..."):
                prompt = "dramatic field hockey action on green turf, " + extra
                image = client.text_to_image(prompt, model="black-forest-labs/FLUX.1-schnell")
                st.image(image, caption="Generiertes Bild")

with tab3:
    st.subheader("Reel & Content Ideen")
    if st.button("Ideen generieren"):
        ideas = client.text_generation(
            "Gib mir 6 gute Reel-Ideen für ein gewonnenes Feldhockey Spiel (kurz und kreativ)",
            model="meta-llama/Llama-3.1-8B-Instruct"
        )
        st.write(ideas)

st.caption("HockeyAI Studio • Läuft mit Hugging Face Inference")
