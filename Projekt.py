import streamlit as st
from PIL import Image

st.set_page_config(page_title="HockeyAI Studio", page_icon="🏑", layout="wide")

st.title("🏑 HockeyAI Studio")
st.caption("Feldhockey Content AI • Vereinfachte Version")

with st.sidebar:
    st.warning("⚠️ Vereinfachte Version aktiv\nTorch & FLUX sind deaktiviert")
    st.info("Die App läuft jetzt stabil. Schwere Modelle kommen später.")

tab1, tab2, tab3, tab4 = st.tabs(["🎮 GameDay Blitz", "📸 Highlight Creator", "💡 Reel Ideen", "❓ Frage der Woche"])

with tab1:
    st.subheader("GameDay Blitz")
    score = st.text_input("Endstand", "4:2")
    opponent = st.text_input("Gegner", "Mannheimer HC")
    scorers = st.text_area("Torschützen", "Lisa Müller - 2\nAnna Schmidt - 1")
    
    if st.button("Story Pack generieren", type="primary"):
        st.success("✅ Demo-Modus")
        st.write("Hier würden normal FLUX-Bilder erscheinen.")
        for i in range(1, 5):
            st.image("https://via.placeholder.com/600x800/006400/white?text=Story+"+str(i), 
                     caption=f"Story {i}", width=400)

with tab2:
    st.subheader("Highlight Creator")
    uploaded = st.file_uploader("Foto hochladen", type=["jpg","png"])
    if uploaded:
        st.image(uploaded, width=500)
        st.info("Florence-2 + FLUX kommen in der nächsten Version")

with tab3:
    st.subheader("Reel & Video Ideen")
    if st.button("Ideen generieren"):
        st.write("1. Strafecken Highlight Reel")
        st.write("2. Torschützen Montage")
        st.write("3. Spieler des Spiels")

with tab4:
    st.subheader("Frage der Woche")
    if st.button("Frage generieren"):
        st.success("Wer war euer Spieler des Spiels heute? 🏑")

st.caption("Aktuell im Demo-Modus | Schwere Modelle werden später über Inference Endpoints geladen")
