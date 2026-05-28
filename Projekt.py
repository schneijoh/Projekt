import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="HockeyAI Studio", page_icon="🏑", layout="wide")

HF_TOKEN = "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"

client = InferenceClient(token=HF_TOKEN)

st.title("🏑 HockeyAI Studio")
st.caption("Stabile Version • Realistisch & Schnell")

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
            base = f"field hockey match on green turf, final score {score} vs {opponent}, {scorers}, dynamic action, instagram story"
            
            for i in range(4):
                prompt = f"{base}, cinematic lighting, professional sports photography, high detail, vibrant"
                
                image = client.text_to_image(
                    prompt=prompt,
                    model="SG161222/RealVisXL_V5.0_Lightning",   # Sehr stabiles & gutes Modell
                    width=576,
                    height=1024,
                    num_inference_steps=6,
                    guidance_scale=7.0
                )
                st.image(image, caption=f"Story {i+1} — {score} vs {opponent}", use_column_width=True)

with tab2:
    st.subheader("Highlight Creator")
    uploaded_file = st.file_uploader("Foto hochladen", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        st.image(uploaded_file, caption="Original", width=600)
        if st.button("Episch machen"):
            with st.spinner("Generiere..."):
                image = client.text_to_image(
                    "dramatic field hockey goal celebration on green turf, cinematic lighting, high quality",
                    model="SG161222/RealVisXL_V5.0_Lightning",
                    width=576,
                    height=1024
                )
                st.image(image)

with tab3:
    st.subheader("Reel Ideen")
    if st.button("Ideen generieren"):
        response = client.text_generation(
            "Gib mir 6 kreative Reel und Story Ideen für ein Feldhockey Spiel",
            model="meta-llama/Llama-3.1-8B-Instruct"
        )
        st.write(response)

st.caption("Stabile Version mit RealVisXL Lightning")
