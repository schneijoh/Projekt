import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="HockeyAI Studio", page_icon="🏑", layout="wide")

HF_TOKEN = "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"   

client = InferenceClient(token=HF_TOKEN)

st.title("🏑 HockeyAI Studio")
st.caption("Feldhockey Content Creator | FLUX.1-schnell")

tab1, tab2, tab3 = st.tabs(["🎮 GameDay Blitz", "📸 Highlight Creator", "💡 Ideen Generator"])

with tab1:
    st.subheader("GameDay Blitz - Story Pack")
    
    col1, col2 = st.columns(2)
    with col1:
        score = st.text_input("Ergebnis", "4:2")
        opponent = st.text_input("Gegner", "Mannheimer HC")
    with col2:
        scorers = st.text_area("Torschützen", "Lisa Müller - 2\nAnna Schmidt - 1")
        moments = st.text_area("Besondere Momente", "Starke Strafecken • Comeback")

    if st.button("🚀 6 Stories generieren", type="primary", use_container_width=True):
        with st.spinner("FLUX generiert 6 Stories..."):
            base = f"field hockey, score {score} vs {opponent}, {scorers}, green artificial turf, dynamic action, instagram story"
            
            for i in range(6):
                styles = ["golden hour lighting", "epic goal celebration", "intense action", "team spirit", "dramatic atmosphere", "victory moment"]
                prompt = f"{base}, {styles[i]}, cinematic, high quality, vibrant colors"
                
                image = client.text_to_image(
                    prompt=prompt,
                    model="black-forest-labs/FLUX.1-schnell",
                    width=576,
                    height=1024
                )
                st.image(image, caption=f"Story {i+1} - {score} vs {opponent}", use_column_width=True)

with tab2:
    st.subheader("Highlight Creator")
    uploaded_file = st.file_uploader("Foto hochladen", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        st.image(uploaded_file, caption="Original Foto", width=600)
        extra = st.text_input("Extra Stil-Beschreibung", "dramatic cinematic lighting, epic")
        
        if st.button("Episch machen mit FLUX"):
            with st.spinner("Generiere..."):
                prompt = f"field hockey action, {extra}, green turf, high quality"
                image = client.text_to_image(prompt, model="black-forest-labs/FLUX.1-schnell")
                st.image(image, caption="Generiertes Highlight")

with tab3:
    st.subheader("Reel & Content Ideen")
    if st.button("Ideen generieren"):
        with st.spinner("Llama denkt nach..."):
            response = client.text_generation(
                f"Gib mir 8 kreative Instagram Reel und Story Ideen für ein Feldhockey Spiel {score} gegen {opponent}",
                model="meta-llama/Llama-3.1-8B-Instruct",
                max_tokens=600
            )
            st.write(response)

st.caption("HockeyAI Studio • Funktioniert ✓")
