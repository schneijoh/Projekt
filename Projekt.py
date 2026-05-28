import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="HockeyAI Studio", page_icon="🏑", layout="wide")

HF_TOKEN = "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"

client = InferenceClient(token=HF_TOKEN)

st.title("🏑 HockeyAI Studio")
st.caption("Stabile Version • DreamShaper-8")

tab1, tab2, tab3 = st.tabs(["🎮 GameDay Blitz", "📸 Highlight Creator", "💡 Ideen"])

with tab1:
    st.subheader("GameDay Blitz")
    
    col1, col2 = st.columns(2)
    with col1:
        score = st.text_input("Ergebnis", "4:2")
        opponent = st.text_input("Gegner", "Mannheimer HC")
    with col2:
        scorers = st.text_area("Torschützen", "Lisa Müller - 2\nAnna Schmidt - 1")

    if st.button("🚀 3 Stories generieren", type="primary", use_container_width=True):
        with st.spinner("Generiere Bilder mit DreamShaper-8..."):
            base = f"field hockey match, score {score} vs {opponent}, {scorers}, green artificial turf, dynamic action, instagram story"

            for i in range(3):
                prompt = f"{base}, cinematic lighting, professional sports photo, high quality, vibrant colors"
                
                try:
                    image = client.text_to_image(
                        prompt=prompt,
                        model="Lykon/dreamshaper-8",   # Stabileres Modell
                        width=576,
                        height=1024,
                        num_inference_steps=25,
                        guidance_scale=7.5
                    )
                    st.image(image, caption=f"Story {i+1} — {score} vs {opponent}", use_column_width=True)
                    st.success(f"Story {i+1} fertig!")
                except Exception as e:
                    st.error(f"Fehler bei Bild {i+1}")
                    st.write(str(e)[:120])

with tab2:
    st.subheader("Highlight Creator")
    uploaded_file = st.file_uploader("Foto hochladen", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, width=600)
        if st.button("Episch machen"):
            with st.spinner("Generiere..."):
                image = client.text_to_image(
                    "dramatic field hockey goal celebration on green turf, cinematic lighting, high quality",
                    model="Lykon/dreamshaper-8",
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

st.caption("Stabile Version mit DreamShaper-8")
