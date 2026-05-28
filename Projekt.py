import streamlit as st
from huggingface_hub import InferenceClient
import os

st.set_page_config(page_title="HockeyAI Studio - Diagnostik", page_icon="🏑", layout="wide")

st.title("🏑 HockeyAI Studio - System-Analyse")

# --- DIAGNOSE START ---
st.subheader("🔍 Fehlersuche: Was sieht der Server?")

# Wir suchen unempfindlich gegen Groß-/Kleinschreibung nach dem Token
found_key_os = None
found_key_st = None

# Alle verfügbaren Keys einsammeln (ohne die echten Werte zu verraten!)
os_keys = [k.upper() for k in os.environ.keys()]
st_keys = [k.upper() for k in st.secrets.keys()]

st.write(f"**Verfügbare System-Variablen (OS):** `{list(os.environ.keys())}`")
st.write(f"**Verfügbare Streamlit-Secrets:** `{list(st.secrets.keys())}`")

# Versuchen, den Token zu greifen (egal wie er geschrieben wurde)
for k in os.environ.keys():
    if k.upper() == "HF_TOKEN":
        found_key_os = k

for k in st.secrets.keys():
    if k.upper() == "HF_TOKEN":
        found_key_st = k

HF_TOKEN = None
if found_key_st:
    HF_TOKEN = st.secrets[found_key_st]
    st.success(f"✅ Token in st.secrets gefunden! (Als `{found_key_st}`)")
elif found_key_os:
    HF_TOKEN = os.environ[found_key_os]
    st.success(f"✅ Token in os.environ gefunden! (Als `{found_key_os}`)")

# --- DIAGNOSE ENDE ---

if HF_TOKEN:
    # Wenn wir hier landen, haben wir IRGENDEINEN Token gefunden!
    client = InferenceClient(token=HF_TOKEN)
    st.balloons()
    
    tab1, tab2 = st.tabs(["🎮 GameDay Blitz", "💡 Ideen & Reels"])
    with tab1:
        st.subheader("GameDay Blitz")
        score = st.text_input("Ergebnis", "4:2")
        opponent = st.text_input("Gegner", "Mannheimer HC")
        
        if st.button("🚀 Test-Bild generieren"):
            with st.spinner("FLUX generiert..."):
                try:
                    image = client.text_to_image(
                        prompt=f"Field hockey match action, score {score} vs {opponent}, green turf, photorealistic",
                        model="black-forest-labs/FLUX.1-schnell"
                    )
                    st.image(image, caption="ES GEHT!")
                except Exception as e:
                    st.error(f"Fehler: {str(e)}")
                    
    with tab2:
        st.subheader("Ideen")
        if st.button("Ideen generieren"):
            response = client.text_generation(
                f"Erstelle 3 kurze Instagram Ideen für Feldhockey {score} gegen {opponent}.",
                model="meta-llama/Llama-3.1-8B-Instruct"
            )
            st.write(response)
else:
    st.error("❌ Absoluter Blindflug: Der Server liefert überhaupt kein Secret aus.")
    st.info("Bitte schau noch mal in deinen Space -> Settings -> 'Variables and secrets'. Steht das Secret dort wirklich unter 'Secrets' (nicht unter Variables) und ist der Name komplett ohne Leerzeichen?")
