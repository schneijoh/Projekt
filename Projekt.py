import streamlit as st
from diffusers import FluxPipeline
import torch

st.set_page_config(page_title="HockeyAI Studio", page_icon="🏑", layout="wide")

st.title("🏑 HockeyAI Studio")
st.caption("FLUX.1-schnell lokal auf Spaces")

@st.cache_resource
def load_flux():
    with st.spinner("Lade FLUX.1-schnell... Dies kann beim ersten Mal 3-8 Minuten dauern"):
        pipe = FluxPipeline.from_pretrained(
            "black-forest-labs/FLUX.1-schnell",
            torch_dtype=torch.bfloat16,
            device_map="balanced",
            low_cpu_mem_usage=True,
        )
        pipe.enable_model_cpu_offload()
        return pipe

pipe = load_flux()

st.success("✅ FLUX erfolgreich geladen!")

tab1, tab2 = st.tabs(["GameDay Stories", "Freie Generierung"])

with tab1:
    st.subheader("GameDay Story Generator")
    score = st.text_input("Ergebnis", "4:2")
    opponent = st.text_input("Gegner", "Mannheimer HC")
    scorers = st.text_area("Torschützen", "Lisa Müller - 2")

    if st.button("4 Stories generieren", type="primary"):
        with st.spinner("FLUX generiert Bilder..."):
            base_prompt = f"field hockey, score {score} vs {opponent}, {scorers}, green turf, dynamic action, instagram story 9:16"
            
            for i in range(4):
                image = pipe(
                    prompt=base_prompt,
                    height=1024,
                    width=576,
                    num_inference_steps=4,
                    guidance_scale=3.5,
                    max_sequence_length=512,
                ).images[0]
                
                st.image(image, caption=f"Story {i+1} — {score} vs {opponent}", use_column_width=True)

with tab2:
    st.subheader("Eigenen Prompt")
    prompt = st.text_area("Dein Prompt", 
        "dramatic field hockey penalty corner goal, green artificial turf, cinematic lighting, dynamic", 
        height=120)
    
    if st.button("Bild generieren"):
        with st.spinner("Generiere..."):
            image = pipe(
                prompt=prompt,
                height=1024,
                width=576,
                num_inference_steps=4,
                guidance_scale=3.5,
            ).images[0]
            st.image(image, use_column_width=True)
