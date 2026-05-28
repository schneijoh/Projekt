import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="HockeyAI Studio", page_icon="🏑", layout="wide")

HF_TOKEN = "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"

client = InferenceClient(token=HF_TOKEN)

st.title("🏑 HockeyAI Studio")
st.caption("Stabile Version für Streamlit Cloud")

tab1, tab2 = st.tabs(["🎮 GameDay Blitz", "📸 Test"])

with tab1:
    st.subheader("GameDay Blitz")
    
    col1, col2 = st.columns(2)
    with col1:
        score = st.text_input("Ergebnis", "4:2")
        opponent = st.text_input("Gegner", "Mannheimer HC")
    with col2:
        scorers = st.text_area("Torschützen", "Lisa Müller - 2\nAnna Schmidt - 1")

    if st.button("🚀 Stories generieren", type="primary"):
        with st.spinner("Versuche Bilder zu generieren..."):
            base = f"field hockey match, score {score} vs {opponent}, {scorers}, green turf, dynamic action, instagram story"
            
            for i in range(2):
                prompt = f"{base}, cinematic lighting, professional sports photo, high quality"
                
                try:
                    image = client.text_to_image(
                        prompt=prompt,
                        model="Lykon/dreamshaper-8",
                        width=576,
                        height=1024,
                        num_inference_steps=20
                    )
                    st.image(image, caption=f"Story {i+1}", use_column_width=True)
                except Exception as e:
                    st.error(f"Fehler bei Bild {i+1}")
                    st.write(str(e)[:100])

with tab2:
    st.subheader("Schnelltest")
    if st.button("Test-Bild generieren"):
        with st.spinner("Generiere Test-Bild..."):
            try:
                image = client.text_to_image(
                    "field hockey player celebrating goal on green turf, cinematic lighting, high quality",
                    model="Lykon/dreamshaper-8",
                    width=576,
                    height=1024
                )
                st.image(image)
                st.success("Bild erfolgreich!")
            except Exception as e:
                st.error("Fehler bei der Generierung")
                st.write(str(e)[:200])

st.caption("HockeyAI Studio • Streamlit Cloud Version")
