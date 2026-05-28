import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="HockeyAI Studio", page_icon="🏑", layout="wide")

# Dein Token bleibt fest drin
HF_TOKEN = "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"
client = InferenceClient(token=HF_TOKEN)

st.title("🏑 HockeyAI Studio")
st.caption("Feldhockey Content Creator | 100% Freigeschaltete Version")

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
        with st.spinner("Generiere Stories mit DreamShaper..."):
            base_prompt = f"Action shot of a field hockey match, final score {score} vs {opponent}, green artificial turf, professional sports photography, instagram story format, portrait orientation"
            
            styles = [
                "dynamic match action, intense atmosphere", 
                "players celebrating a goal, emotional victory moment", 
                "epic lighting, stadium atmosphere", 
                "dramatic focus on the field hockey ball and stick"
            ]
            
            for i in range(4):
                prompt = f"{base_prompt}, {styles[i]}, highly detailed, sharp focus, 8k"
                
                try:
                    # DreamShaper 8 ist komplett offen und blockiert keine Token
                    image = client.text_to_image(
                        prompt=prompt,
                        model="Lykon/dreamshaper-8"
                    )
                    st.image(image, caption=f"Story {i+1} — {styles[i].split(',')[0]}", use_container_width=True)
                except Exception as e:
                    st.error(f"Story {i+1} fehlgeschlagen. HF-Meldung: {str(e)[:120]}...")

with tab2:
    st.subheader("Highlight Creator")
    uploaded_file = st.file_uploader("Foto hochladen", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        st.image(uploaded_file, caption="Original Foto", width=600)
        extra = st.text_input("Zusätzlicher Stil", "dramatic cinematic lighting, action shot, epic")
        
        if st.button("Episch machen"):
            with st.spinner("Transformiere dein Bild..."):
                prompt = f"Professional field hockey scene, {extra}, green artificial turf stadium, hyper-realistic"
                try:
                    image = client.text_to_image(prompt, model="Lykon/dreamshaper-8")
                    st.image(image, caption="Dein generiertes Highlight")
                except Exception as e:
                    st.error(f"Fehler: {str(e)[:120]}...")

with tab3:
    st.subheader("Reel & Content Ideen")
    if st.button("Ideen generieren"):
        with st.spinner("Llama denkt nach..."):
            try:
                response = client.text_generation(
                    f"Erstelle 8 kreative und kurze Instagram Reel und Story Ideen für ein Feldhockey Spiel. Ergebnis: {score} gegen {opponent}.",
                    model="meta-llama/Llama-3.1-8B-Instruct",
                    max_tokens=600
                )
                st.write(response)
            except Exception as e:
                st.error(f"Fehler bei der Textgenerierung: {str(e)}")

st.caption("HockeyAI Studio • Powered by DreamShaper & Llama")
