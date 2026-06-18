import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="HockeyAI Studio", page_icon="🏑", layout="wide")

# --- SIDEBAR: TOKEN FLEXIBEL EINGEBEN ---
st.sidebar.title("🔑 API-Konfiguration")
user_token = st.sidebar.text_input("Hugging Face Token (optional)", type="password", help="Ohne Token wird ein älteres Gratis-Modell genutzt. Mit Token kriegst du FLUX.")

if user_token:
    client = InferenceClient(token=user_token)
    st.sidebar.success("🔒 Eigener Token aktiv! (FLUX freigeschaltet)")
else:
    # Absolut Token-freier Client
    client = InferenceClient() 
    st.sidebar.warning("⚠️ Kein Token eingetragen. Nutze die 100% freie Basis-API.")

# --- APP HEADER ---
st.title("🏑 HockeyAI Studio")
st.caption("Feldhockey Content Creator • Premium Edition")

if "gameday_score" not in st.session_state:
    st.session_state["gameday_score"] = "4:2"
if "gameday_opponent" not in st.session_state:
    st.session_state["gameday_opponent"] = "Mannheimer HC"

tab1, tab2, tab3 = st.tabs(["🎮 GameDay Blitz", "📸 Highlight Creator", "💡 Ideen & Reels"])

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
        with st.spinner("Generiere Hockey-Bilder..."):
            base_prompt = f"Action shot of a field hockey match, score {score} vs {opponent}, green artificial turf, professional sports photography, instagram story format"
            
            styles = [
                "dynamic match action, intense atmosphere", 
                "players celebrating a goal, emotional victory moment", 
                "epic golden hour stadium lighting, cinematic wide shot", 
                "dramatic focus on the field hockey ball and stick"
            ]
            
            # WICHTIG: Wenn kein Token da ist, nutzen wir das klassische v1-5, das keinen 401-Fehler wirft
            model_to_use = "black-forest-labs/FLUX.1-schnell" if user_token else "runwayml/stable-diffusion-v1-5"
            
            for i in range(4):
                prompt = f"{base_prompt}, {styles[i]}, photorealistic, 8k"
                try:
                    image = client.text_to_image(prompt=prompt, model=model_to_use)
                    st.image(image, caption=f"Story {i+1} — {styles[i].split(',')[0]}", use_container_width=True)
                except Exception as e:
                    st.error(f"Story {i+1} Fehler: {str(e)[:120]}")

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
                model_to_use = "black-forest-labs/FLUX.1-schnell" if user_token else "runwayml/stable-diffusion-v1-5"
                try:
                    image = client.text_to_image(prompt, model=model_to_use)
                    st.image(image, caption="Dein generiertes Highlight")
                except Exception as e:
                    st.error(f"Fehler: {str(e)[:120]}")

# --- TAB 3: IDEEN & REELS ---
with tab3:
    st.subheader("Reel & Content Ideen")
    if st.button("Ideen generieren"):
        with st.spinner("Llama denkt nach..."):
            current_score = st.session_state["gameday_score"]
            current_opponent = st.session_state["gameday_opponent"]
            
            # Textgenerierung ohne Token klappt am besten mit universellen Modellen
            text_model = "meta-llama/Llama-3.1-8B-Instruct"
            try:
                response = client.text_generation(
                    f"Erstelle 8 kreative und kurze Instagram Reel und Story Ideen für ein Feldhockey Spiel. Ergebnis: {current_score} gegen {current_opponent}.",
                    model=text_model,
                    max_tokens=600
                )
                st.write(response)
            except Exception as e:
                # Kleiner Hinweis für den Nutzer falls auch Llama ohne Token blockiert
                st.error(f"Fehler: {str(e)[:100]}. Tipp: Trage links in der Sidebar einen kostenlosen HF-Token ein, falls das Limit erreicht ist.")

st.caption("HockeyAI Studio • Smart Fallback Edition")
