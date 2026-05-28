import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="HockeyAI Studio", page_icon="🏑", layout="wide")

# Dein Token
HF_TOKEN = "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"
client = InferenceClient(token=HF_TOKEN)

# Liste von Modellen, die wir nacheinander durchprobieren, falls keins antwortet
IMAGE_MODELS = [
    "stabilityai/stable-diffusion-2-1",
    "runwayml/stable-diffusion-v1-5",
    "CompVis/stable-diffusion-v1-4"
]

def generate_hockey_image(prompt):
    """Versucht ein Bild zu generieren. Wenn ein Modell offline ist, wird das nächste probiert."""
    for model in IMAGE_MODELS:
        try:
            image = client.text_to_image(prompt=prompt, model=model)
            return image, model
        except Exception:
            continue  # Probiere das nächste Modell
    return None, None

st.title("🏑 HockeyAI Studio")
st.caption("Feldhockey Content Creator | Fail-Safe Bildgenerierung")

tab1, tab2, tab3 = st.tabs(["🎮 GameDay Blitz", "📸 Highlight Creator", "💡 Ideen & Reels"])

with tab1:
    st.subheader("GameDay Blitz - Story Pack")
    
    col1, col2 = st.columns(2)
    with col1:
        score = st.text_input("Ergebnis", "4:2")
        opponent = st.text_input("Gegner", "Mannheimer HC")
    with col2:
        scorers = st.text_area("Torschützen", "Lisa Müller - 2\nAnna Schmidt - 1")
        moments = st.text_area("Besondere Momente", "Starke Strafecken • Comeback")
        
    if st.button("🚀 4 Stories generieren", type="primary", use_container_width=True):
        with st.spinner("Suche freies KI-Modell und generiere Bilder..."):
            base_prompt = f"field hockey action, match score {score} vs {opponent}, green artificial turf, dynamic sports photography, instagram story format"
            
            for i in range(4):
                styles = ["golden hour lighting", "epic celebration", "intense action", "victory moment"]
                prompt = f"{base_prompt}, {styles[i]}, cinematic, highly detailed"
                
                image, used_model = generate_hockey_image(prompt)
                
                if image:
                    st.image(image, caption=f"Story {i+1} ({used_model})", use_container_width=True)
                else:
                    st.error(f"Story {i+1} konnte nicht generiert werden. Alle Hugging Face Server sind gerade überlastet.")

with tab2:
    st.subheader("Highlight Creator")
    uploaded_file = st.file_uploader("Foto hochladen", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        st.image(uploaded_file, caption="Original Foto", width=600)
        extra = st.text_input("Zusätzlicher Stil", "dramatic cinematic lighting, professional sports photography")
        
        if st.button("Episch machen"):
            with st.spinner("Generiere..."):
                prompt = f"field hockey action player, {extra}, green turf, high quality"
                image, used_model = generate_hockey_image(prompt)
                if image:
                    st.image(image, caption=f"Generiertes Highlight (Modell: {used_model})")
                else:
                    st.error("Bild-Server überlastet. Bitte gleich nochmal versuchen.")

with tab3:
    st.subheader("Reel & Content Ideen")
    if st.button("Ideen generieren"):
        with st.spinner("Llama generiert Ideen..."):
            try:
                response = client.text_generation(
                    f"Erstelle 8 kreative und kurze Instagram Reel und Story Ideen für ein Feldhockey Spiel. Ergebnis: {score} gegen {opponent}.",
                    model="meta-llama/Llama-3.1-8B-Instruct",
                    max_tokens=600
                )
                st.write(response)
            except Exception as e:
                st.error(f"Fehler bei der Textgenerierung: {str(e)}")

st.caption("HockeyAI Studio • Smart Fallback Aktiviert")
