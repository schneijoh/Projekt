import streamlit as st
import requests
from io import BytesIO
from PIL import Image
from huggingface_hub import InferenceClient

st.set_page_config(page_title="HockeyAI Studio", page_icon="🏑", layout="wide")

# Client NUR noch für den Text in Tab 3 (Text klappt oft noch ohne Token)
client = InferenceClient()

st.title("🏑 HockeyAI Studio")
st.caption("Feldhockey Content Creator • Premium Edition (Token-Free Bilder)")

if "gameday_score" not in st.session_state:
    st.session_state["gameday_score"] = "4:2"
if "gameday_opponent" not in st.session_state:
    st.session_state["gameday_opponent"] = "Mannheimer HC"

tab1, tab2, tab3 = st.tabs(["🎮 GameDay Blitz", "📸 Highlight Creator", "💡 Ideen & Reels"])

# --- HILFSFUNKTION FÜR TOKEN-FREIE BILDER ---
def generate_free_image(prompt):
    # Nutzt die kostenlose, offene Pollinations-API (kein Token nötig!)
    url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}?width=1024&height=1024&enhance=true"
    response = requests.get(url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        raise Exception(f"Fehler beim Bild-Server (Status: {response.status_code})")

# --- TAB 1: GAMEDAY BLITZ ---
with tab1:
    st.subheader("GameDay Blitz - Story Pack")
    
    col1, col2 = st.columns(2)
    with col1:
        score = st.text_input("Ergebnis", value=st.session_state["gameday_score"], key="gameday_score")
        opponent = st.text_input("Gegner", value=st.session_state["gameday_opponent"], key="gameday_opponent")
    with col2:
        scorers = st.text_area("Torschützen", "Lisa Müller - 2\nAnna Schmidt - 1", key="gameday_scorers")
        moments = st.text_area("Besondere Momente", "Starke Strafecken • Comeback", key="gameday_moments")
        
    if st.button("🚀 4 Stories generieren", type="primary", use_container_width=True):
        with st.spinner("Generiere Hockey-Bilder über freien Server..."):
            base_prompt = f"Action shot of a field hockey match, final score {score} vs {opponent}, green artificial turf, professional sports photography, instagram story format"
            
            styles = [
                "dynamic match action, intense atmosphere", 
                "players celebrating a goal, emotional victory moment", 
                "epic golden hour stadium lighting, cinematic wide shot", 
                "dramatic focus on the field hockey ball and stick"
            ]
            
            for i in range(4):
                prompt = f"{base_prompt}, {styles[i]}, photorealistic, 8k"
                try:
                    # Aufruf der neuen, token-freien Funktion
                    image = generate_free_image(prompt)
                    st.image(image, caption=f"Story {i+1} — {styles[i].split(',')[0]}", use_container_width=True)
                except Exception as e:
                    st.error(f"Story {i+1} Fehler: {str(e)}")

# --- TAB 2: HIGHLIGHT CREATOR ---
with tab2:
    st.subheader("Highlight Creator")
    uploaded_file = st.file_uploader("Foto hochladen", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        st.image(uploaded_file, caption="Original Foto", width=600)
        extra = st.text_input("Zusätzlicher Stil", "cinematic dramatic lighting, action shot, epic")
        
        if st.button("Episch machen"):
            with st.spinner("Künstliche Intelligenz arbeitet..."):
                prompt = f"Professional field hockey scene, {extra}, green artificial turf stadium, hyper-realistic"
                try:
                    image = generate_free_image(prompt)
                    st.image(image, caption="Dein generiertes Highlight")
                except Exception as e:
                    st.error(f"Fehler: {str(e)}")

# --- TAB 3: IDEEN & REELS ---
with tab3:
    st.subheader("Reel & Content Ideen")
    if st.button("Ideen generieren"):
        with st.spinner("Llama denkt nach..."):
            current_score = st.session_state["gameday_score"]
            current_opponent = st.session_state["gameday_opponent"]
            
            text_model = "meta-llama/Llama-3.1-8B-Instruct"
            try:
                response = client.text_generation(
                    f"Erstelle 8 kreative und kurze Instagram Reel und Story Ideen für ein Feldhockey Spiel. Ergebnis: {current_score} gegen {current_opponent}.",
                    model=text_model,
                    max_new_tokens=600
                )
                st.write(response)
            except Exception as e:
                st.error(f"Fehler bei Textgenerierung: {str(e)}. (Hugging Face blockiert nun auch Text ohne Anmeldung).")

st.caption("HockeyAI Studio • 100% Token-Free Bild-Engine")
