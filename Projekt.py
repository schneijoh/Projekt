import streamlit as st
from PIL import Image
import torch
import os

# ------------------- Page Config -------------------
st.set_page_config(
    page_title="HockeyAI Studio - Feldhockey Content",
    page_icon="🏑",
    layout="wide"
)

st.title("🏑 HockeyAI Studio")
st.caption("All-in-One Content Creator für Feldhockey Instagram & Co.")

# ------------------- Sidebar -------------------
with st.sidebar:
    st.header("Einstellungen")
    model_choice = st.selectbox(
        "LLM wählen",
        ["meta-llama/Llama-3.1-8B-Instruct", "mistralai/Mistral-7B-Instruct-v0.3"]
    )
    
    use_flux = st.checkbox("FLUX.1-schnell verwenden", value=True)
    st.info("Lade Modelle beim ersten Start (kann 5-20 Min dauern)")

# ------------------- Tabs -------------------
tab1, tab2, tab3, tab4 = st.tabs(["🎮 GameDay Blitz", "📸 Highlight Creator", "💡 Reel & Video Ideen", "❓ Frage der Woche"])

# ------------------- Tab 1: GameDay Blitz -------------------
with tab1:
    st.subheader("GameDay Blitz - Story Pack Generator")
    
    col1, col2 = st.columns(2)
    with col1:
        score = st.text_input("Endergebnis (z.B. 4:2)", "3:1")
        opponent = st.text_input("Gegner", "TSV Mannheim")
    
    with col2:
        scorers = st.text_area("Torschützen (ein pro Zeile)", "Lisa Müller - 2\nAnna Schmidt - 1")
        match_info = st.text_area("Weitere Infos / Besonderheiten", "Starke Strafecken + 2. Halbzeit dominiert")

    if st.button("🚀 Story Pack generieren", type="primary"):
        with st.spinner("LLM analysiert Spiel + generiert Prompts..."):
            # Hier kommt später der LLM-Aufruf
            st.success("Prompts generiert!")
        
        st.subheader("Generierte Story-Ideen")
        # Platzhalter für FLUX-Bilder
        for i in range(6):
            st.image("https://via.placeholder.com/512x512/00ff00/000000?text=Story+" + str(i+1), 
                    caption=f"Story {i+1} - {score} vs {opponent}", width=400)

# ------------------- Tab 2: Highlight Creator -------------------
with tab2:
    st.subheader("Highlight Creator (Foto → Episch)")
    uploaded_file = st.file_uploader("Foto hochladen (Spielszene, Tor, Spieler...)", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Hochgeladenes Bild", width=500)
        
        prompt = st.text_input("Zusätzlicher Prompt (optional)", 
                              "dramatic field hockey action, golden hour, green turf, cinematic lighting")
        
        if st.button("✨ Epische Version generieren"):
            st.info("Florence-2 analysiert Bild + FLUX generiert neue Version...")
            # Hier kommen Florence + FLUX + IP-Adapter später hin
            st.success("Bild generiert! (Platzhalter)")

# ------------------- Tab 3: Reel & Video Ideen -------------------
with tab3:
    st.subheader("Reel & Video Ideen Generator")
    match_summary = st.text_area("Kurze Spiel-Zusammenfassung", 
                                "Heimsieg 4:2 gegen starken Gegner. Zwei wunderschöne Strafeckentore.")
    
    if st.button("Ideen generieren"):
        st.write("**Top 5 Reel-Ideen:**")
        st.write("1. Slow-Mo Strafecken + epischer Hook")
        st.write("2. Torschützen Montage mit Text-Overlays")
        # etc.

# ------------------- Tab 4: Frage der Woche -------------------
with tab4:
    st.subheader("Frage der Woche")
    if st.button("Frage generieren"):
        st.success("**Frage der Woche:** Wer war euer Spieler des Spiels gegen Mannheim?")
        st.write("Direkt als Story-Vorlage nutzbar")

# ------------------- Footer -------------------
st.divider()
st.caption("HockeyAI Studio • Powered by Hugging Face • Llama-3.1 + FLUX.1-schnell + Florence-2")
