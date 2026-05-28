import streamlit as st
from huggingface_hub import InferenceClient
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="HockeyAI Studio", page_icon="🏑", layout="wide")

# Dein Token (aktiv für Llama)
HF_TOKEN = "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"
client = InferenceClient(token=HF_TOKEN)

def create_placeholder_image(title, score, opponent, scorers, style_name):
    """Generiert lokal ein schickes Teambild/Grafik ohne externe API."""
    # Instagram Story Format (576x1024)
    img = Image.new("RGB", (576, 1024), "#1E4620")  # Dunkles Feldhockey-Grün
    draw = ImageDraw.Draw(img)
    
    # Einfache Formen für den sportlichen Look zeichnen
    draw.rectangle([20, 20, 556, 1004], outline="#E5A93C", width=5) # Goldener Rahmen
    draw.ellipse([188, 412, 388, 612], outline="#FFFFFF", width=3) # Anstoßkreis
    draw.line([20, 512, 556, 512], fill="#FFFFFF", width=3) # Mittellinie
    
    # Textplatzierung (Nutzt Standard-Schriftart, da plattformunabhängig)
    draw.text((40, 60), "🏑 HOCKEY AI STUDIO", fill="#FFFFFF")
    draw.text((40, 120), f"STORY: {title.upper()}", fill="#E5A93C")
    
    draw.text((40, 250), f"Match: {score}", fill="#FFFFFF")
    draw.text((40, 290), f"vs. {opponent}", fill="#FFFFFF")
    
    draw.text((40, 400), "Torschuetzen:", fill="#E5A93C")
    # Einfaches Splitten für die Darstellung
    for idx, line in enumerate(scorers.split('\n')[:4]):
        draw.text((40, 440 + (idx * 30)), line, fill="#FFFFFF")
        
    draw.text((40, 700), f"Vibe: {style_name}", fill="#E5A93C")
    draw.text((40, 950), "Bereit fuer Instagram Stories ✅", fill="#FFFFFF")
    
    # In Bytes konvertieren, damit Streamlit es anzeigen kann
    byte_im = io.BytesIO()
    img.save(byte_im, format="PNG")
    return byte_im.getvalue()

st.title("🏑 HockeyAI Studio")
st.caption("Feldhockey Content Creator | 100% Ausfallsichere Version")

tab1, tab2, tab3 = st.tabs(["🎮 GameDay Blitz", "📸 Highlight Creator", "💡 Ideen & Reels"])

with tab1:
    st.subheader("GameDay Blitz - Story Pack")
    
    col1, col2 = col1, col2 = st.columns(2)
    with col1:
        score = st.text_input("Ergebnis", "4:2")
        opponent = st.text_input("Gegner", "Mannheimer HC")
    with col2:
        scorers = st.text_area("Torschützen", "Lisa Müller - 2\nAnna Schmidt - 1")
        moments = st.text_area("Besondere Momente", "Starke Strafecken • Comeback")
        
    if st.button("🚀 4 Stories generieren", type="primary", use_container_width=True):
        with st.spinner("Erstelle Grafiken lokal im System..."):
            styles = ["Golden Hour", "Epic Celebration", "Intense Action", "Victory Moment"]
            
            for i in range(4):
                # Generiert die Grafik direkt auf deinem Server ohne HF-Bild-API
                img_data = create_placeholder_image(f"Story {i+1}", score, opponent, scorers, styles[i])
                st.image(img_data, caption=f"Story {i+1} — {styles[i]}", use_container_width=True)

with tab2:
    st.subheader("Highlight Creator")
    uploaded_file = st.file_uploader("Foto hochladen", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        st.image(uploaded_file, caption="Original Foto", width=600)
        extra = st.text_input("Zusätzlicher Stil", "Dramatisch, Episch")
        
        if st.button("Episch machen"):
            with st.spinner("Verarbeite..."):
                img_data = create_placeholder_image("Highlight", score, opponent, "Match-Highlight", extra)
                st.image(img_data, caption="Dein optimiertes Highlight-Layout")

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

st.caption("HockeyAI Studio • Lokale Grafik-Engine aktiv")
