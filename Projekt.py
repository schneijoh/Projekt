import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="HockeyAI Studio", page_icon="🏑", layout="wide")

HF_TOKEN = "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"

client = InferenceClient(token=HF_TOKEN)

st.title("🏑 HockeyAI Studio")
st.caption("Test mit offiziellem Modell")

tab1, tab2 = st.tabs(["🎮 GameDay", "Test"])

with tab1:
    st.subheader("GameDay Blitz")
    
    col1, col2 = st.columns(2)
    with col1:
        score = st.text_input("Ergebnis", "4:2")
        opponent = st.text_input("Gegner", "Mannheimer HC")
    with col2:
        scorers = st.text_area("Torschützen", "Lisa Müller - 2\nAnna Schmidt - 1")

    if st.button("🚀 Stories generieren", type="primary"):
        with st.spinner("Versuche mit stabilem Modell..."):
            base = f"Feldhockey Spiel, Ergebnis {score} gegen {opponent}, Torschützen {scorers}, grüner Rasen, Action"

            for i in range(2):   # Nur 2 Bilder zum Testen
                prompt = f"{base}, professionelle Sportfotografie, cinematic, hochqualitativ, dynamisch"
                
                try:
                    image = client.text_to_image(
                        prompt=prompt,
                        model="black-forest-labs/FLUX.1-schnell",   # Versuch mit FLUX
                        width=576,
                        height=1024
                    )
                    st.image(image, caption=f"Story {i+1}", use_column_width=True)
                    st.success("Bild erfolgreich generiert!")
                except Exception as e:
                    st.error(f"Fehler bei Bild {i+1}")
                    st.write(str(e)[:150])

with tab2:
    st.subheader("Schnelltest")
    if st.button("Ein Test-Bild generieren"):
        with st.spinner("Test läuft..."):
            try:
                image = client.text_to_image(
                    "field hockey goal celebration, green turf, cinematic lighting",
                    model="black-forest-labs/FLUX.1-schnell"
                )
                st.image(image)
            except Exception as e:
                st.error("Fehler:")
                st.write(str(e)[:300])

st.caption("Letzter Versuch mit FLUX.1-schnell")
