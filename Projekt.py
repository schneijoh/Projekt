import streamlit as st
from PIL import Image
import torch
from diffusers import FluxPipeline
import os

# ====================== CONFIG ======================
st.set_page_config(page_title="HockeyAI Studio", page_icon="🏑", layout="wide")

st.title("🏑 HockeyAI Studio - Lokale Version")
st.caption("FLUX.1-schnell läuft lokal auf deinem PC")

# ====================== MODEL LADEN ======================
@st.cache_resource
def load_flux():
    with st.spinner("Lade FLUX.1-schnell... (das kann beim ersten Mal 2-5 Minuten dauern)"):
        pipe = FluxPipeline.from_pretrained(
            "black-forest-labs/FLUX.1-schnell",
            torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
            device_map="balanced" if torch.cuda.is_available() else None,
        )
        if torch.cuda.is_available():
            pipe.enable_model_cpu_offload()   # Spart VRAM
        return pipe

pipe = load_flux()

# ====================== TABS ======================
tab1, tab2 = st.tabs(["🎮 GameDay Story Generator", "📸 Freie Bildgenerierung"])

with tab1:
    st.subheader("GameDay Story Generator")
    
    col1, col2 = st.columns(2)
    with col1:
        score = st.text_input("Ergebnis", "4:2")
        opponent = st.text_input("Gegner", "Mannheimer HC")
    with col2:
        scorers = st.text_area("Torschützen", "Lisa Müller - 2\nAnna Schmidt - 1")
        style = st.selectbox("Stil", ["Dramatisch", "Energetisch", "Clean & Modern", "Cinematic"])

    prompt_base = f"Feldhockey Spiel, {score} Sieg gegen {opponent}, Torschützen: {scorers}, grüner Kunstrasen, Action"

    if st.button("🚀 Stories mit FLUX generieren", type="primary"):
        with st.spinner("FLUX generiert Bilder..."):
            for i in range(4):
                full_prompt = f"{prompt_base}, {style.lower()} style, instagram story format, high quality"
                
                image = pipe(
                    prompt=full_prompt,
                    height=1024,
                    width=576,      # 9:16 für Stories
                    num_inference_steps=4,   # Schnell-Modell braucht nur wenige Steps
                    guidance_scale=3.5,
                ).images[0]
                
                st.image(image, caption=f"Story {i+1} - {score} vs {opponent}", use_column_width=True)

with tab2:
    st.subheader("Freie Bildgenerierung")
    custom_prompt = st.text_area("Dein Prompt", 
        "Dramatisches Strafeckentor im Feldhockey, grüner Kunstrasen, golden hour, cinematic lighting, dynamic action",
        height=100)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        height = st.selectbox("Höhe", [1024, 768, 512], index=0)
    with col2:
        width = st.selectbox("Breite", [576, 1024, 768], index=0)
    with col3:
        steps = st.slider("Inference Steps", 1, 8, 4)
    
    if st.button("Bild mit FLUX generieren"):
        with st.spinner("Generiere Bild..."):
            image = pipe(
                prompt=custom_prompt,
                height=height,
                width=width,
                num_inference_steps=steps,
                guidance_scale=3.5,
            ).images[0]
            
            st.image(image, caption="Generiert mit FLUX.1-schnell", use_column_width=True)

st.divider()
st.caption("Lokale Version • FLUX.1-schnell • GPU benötigt")
