import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="HockeyAI Studio", page_icon="🏑", layout="wide")

# Token laden
client = InferenceClient(token=st.secrets["HF_TOKEN"])

st.title("🏑 HockeyAI Studio")
st.caption("Feldhockey Content AI • FLUX.1-schnell + Llama")

tab1, tab2, tab3 = st.tabs(["🎮 GameDay Blitz", "📸 Highlight Creator", "💡 Ideen & Reels"])

with tab1:
    st.subheader("GameDay Blitz - Story Pack")
    
    col1, col2 = st.columns(2)
    with col1:
        score = st.text_input("Endergebnis", "4:2")
        opponent = st.text_input("Gegner", "Mannheimer HC")
    with col2:
        scorers = st.text_area("Torschützen", "Lisa Müller - 2\nAnna Schmidt - 1")
        moments = st.text_area("Besondere Momente", "Starke Strafecken • Gutes Comeback")

    if st.button("🚀 6 Stories generieren", type="primary", use_container_width=True):
        with st.spinner("FLUX.1-schnell generiert deine Stories..."):
            base = f"field hockey match, final score {score} vs {opponent}, scorers {scorers}, green artificial turf, dynamic action, high quality, instagram story"
            
            for i in range(6):
                styles = ["golden hour", "epic celebration", "intense action", "team spirit", "dramatic", "victory moment"]
                prompt = f"{base}, {styles[i]}, cinematic lighting, vibrant"
                
                image = client.text_to_image(prompt, model="black-forest-labs/FLUX.1-schnell", width=576, height=1024)
                st.image(image, caption=f"Story {i+1} — {score} vs {opponent}", use_column_width=True)

with tab2:
    st.subheader("Highlight Creator")
    uploaded_file = st.file_uploader("Foto hochladen", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        st.image(uploaded_file, width=600)
        extra = st.text_input("Zusätzlicher Stil", "dramatic cinematic, epic goal")
        
        if st.button("Episch machen mit FLUX"):
            with st.spinner("Generiere..."):
                prompt = f"field hockey action, {extra}, green turf, high quality"
                image = client.text_to_image(prompt, model="black-forest-labs/FLUX.1-schnell")
                st.image(image, caption="Generiertes Bild")

with tab3:
    st.subheader("Reel & Content Ideen")
    if st.button("Ideen für diesen Spieltag generieren"):
        with st.spinner("Llama generiert Ideen..."):
            response = client.text_generation(
                f"Erstelle 8 gute Instagram Reel und Story Ideen für ein Feldhockey Spiel. Ergebnis: {score} gegen {opponent}. Kreativ und kurz.",
                model="meta-llama/Llama-3.1-8B-Instruct",
                max_tokens=700
            )
            st.write(response)

st.caption("HockeyAI Studio • Token funktioniert ✓")
