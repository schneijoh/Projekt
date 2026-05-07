import streamlit as st
from PIL import Image
import torch
import os

# ====================== PAGE CONFIG ======================
st.set_page_config(
    page_title="HockeyAI Studio",
    page_icon="🏑",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏑 HockeyAI Studio")
st.caption("Feldhockey Content Creator | Llama + FLUX + Florence-2")

# ====================== SIDEBAR ======================
with st.sidebar:
    st.header("⚙️ Einstellungen")
    
    llm_model = st.selectbox(
        "LLM Modell",
        ["meta-llama/Llama-3.1-8B-Instruct", 
         "mistralai/Mistral-7B-Instruct-v0.3"],
        index=0
    )
    
    use_flux = st.checkbox("FLUX.1-schnell verwenden", value=True)
    use_florence = st.checkbox("Florence-2 verwenden", value=True)
    
    st.divider()
    st.caption("**Tipp:** Beim ersten Start laden die Modelle (kann 1-3 Minuten dauern).")

# ====================== TABS ======================
tab1, tab2, tab3, tab4 = st.tabs([
    "🎮 GameDay Blitz", 
    "📸 Highlight Creator", 
    "💡 Reel & Video Ideen", 
    "❓ Frage der Woche"
])

# ====================== TAB 1: GAMEDAY BLITZ ======================
with tab1:
    st.subheader("GameDay Blitz - Automatisches Story Pack")
    
    col1, col2 = st.columns(2)
    with col1:
        score = st.text_input("Endstand", "4:2")
        opponent = st.text_input("Gegner", "Mannheimer HC")
    
    with col2:
        scorers = st.text_area("Torschützen (ein pro Zeile)", 
                              "Lisa Müller - 2 Tore\nAnna Schmidt - 1 Tor")
        special = st.text_area("Besondere Momente", "2 starke Strafecken + Comeback in H2")

    if st.button("🚀 Komplettes Story Pack generieren", type="primary", use_container_width=True):
        with st.spinner("Lade LLM und generiere Inhalte..."):
            # Hier kommt später der echte LLM-Aufruf
            st.success("✅ Prompts generiert!")
            
            st.subheader("Vorschau der Stories")
            for i in range(1, 7):
                st.image(
                    "https://via.placeholder.com/512x512/006400/FFFFFF?text=Story+"+str(i),
                    caption=f"Story {i} - {score} vs {opponent}",
                    width=380
                )

# ====================== TAB 2: HIGHLIGHT CREATOR ======================
with tab2:
    st.subheader("Highlight Creator - Foto → Episch")
    
    uploaded_file = st.file_uploader("Spiel-Foto hochladen", 
                                   type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Originalbild", width=500)
        
        custom_prompt = st.text_input(
            "Zusätzlicher Stil-Prompt (optional)",
            "dramatic field hockey action, green turf, golden hour lighting, cinematic"
        )
        
        if st.button("✨ Epische Version erstellen"):
            with st.spinner("Florence-2 analysiert Bild + FLUX generiert..."):
                st.success("Bild wurde generiert! (Platzhalter)")
                st.image(image, caption="Generiertes Bild (Demo)", width=500)

# ====================== TAB 3: REEL IDEEN ======================
with tab3:
    st.subheader("Reel & Video Ideen")
    summary = st.text_area("Kurze Spielzusammenfassung", 
                          "Heimsieg 4:2. Starke zweite Halbzeit und zwei wunderschöne Strafeckentore.")
    
    if st.button("Ideen generieren"):
        st.subheader("🔥 Empfohlene Reel-Ideen")
        ideas = [
            "1. Top 3 Tore Slow-Motion Montage",
            "2. Strafecken Highlight Reel (15s)",
            "3. Spieler des Spiels Portrait + Stats",
            "4. Fan Reaction + Torjubel",
            "5. Before/After Comeback Story"
        ]
        for idea in ideas:
            st.write(idea)

# ====================== TAB 4: FRAGE DER WOCHE ======================
with tab4:
    st.subheader("Frage der Woche Generator")
    
    if st.button("Frage der Woche erstellen"):
        st.success("**Frage der Woche:**")
        st.write("**Wer war für euch Spieler*in des Spiels gegen Mannheimer HC?** 🏑")
        st.write("Antwortet in den Kommentaren!")

# ====================== FOOTER ======================
st.divider()
st.caption("HockeyAI Studio • Powered by Hugging Face • Python 3.11")
