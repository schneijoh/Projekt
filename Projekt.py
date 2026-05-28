import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="HockeyAI Studio - Debug", page_icon="🏑", layout="wide")

st.title("🏑 HockeyAI Studio - System Check")

# 1. Diagnose-Bereich anzeigen
st.subheader("🔍 Secret-Diagnose")
verfuegbare_keys = list(st.secrets.keys())

st.write(f"**Gefundene Secret-Namen in deiner App:** `{verfuegbare_keys}`")

if "HF_TOKEN" in st.secrets:
    st.success("✅ HF_TOKEN wurde im System registriert!")
    # Zeigt nur die ersten 4 Zeichen zur Sicherheit
    st.write(f"Token-Vorschau: `{st.secrets['HF_TOKEN'][:4]}...`")
else:
    st.error("❌ Das System sieht das Secret 'HF_TOKEN' aktuell nicht.")
    st.info("Hinweis: Prüfe in den Space-Settings, ob das Secret exakt 'HF_TOKEN' heißt (alles großgeschrieben, keine Leerzeichen).")

st.markdown("---")

# 2. Die normale App startet hier, falls das Secret da ist
if "HF_TOKEN" in st.secrets:
    HF_TOKEN = st.secrets["HF_TOKEN"]
    client = InferenceClient(token=HF_TOKEN)
    
    tab1, tab2 = st.tabs(["🎮 GameDay Blitz", "💡 Ideen & Reels"])
    
    with tab1:
        st.subheader("GameDay Blitz")
        score = st.text_input("Ergebnis", "4:2")
        opponent = st.text_input("Gegner", "Mannheimer HC")
        
        if st.button("🚀 Test-Bild generieren"):
            with st.spinner("FLUX startet..."):
                try:
                    image = client.text_to_image(
                        prompt=f"Field hockey match action, score {score} vs {opponent}, green turf, photorealistic",
                        model="black-forest-labs/FLUX.1-schnell"
                    )
                    st.image(image, caption="Es funktioniert!")
                except Exception as e:
                    st.error(f"Fehler: {str(e)[:150]}")
                    
    with tab2:
        st.subheader("Ideen")
        if st.button("Ideen generieren"):
            response = client.text_generation(
                f"Erstelle 3 kurze Instagram Ideen für Feldhockey {score} gegen {opponent}.",
                model="meta-llama/Llama-3.1-8B-Instruct"
            )
            st.write(response)
else:
    st.warning("⚠️ Die App pausiert, bis das Secret 'HF_TOKEN' erkannt wird.")
