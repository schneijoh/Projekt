import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image, ImageDraw, ImageEnhance
import io
import time
import numpy as np
import cv2

# --- STREAMLIT CONFIG (Muss ganz oben stehen) ---
st.set_page_config(page_title="LBV Phoenix CC", page_icon="🦅", layout="wide")

# --- LADESCREEN ---
if "app_geladen" not in st.session_state:
    st.session_state["app_geladen"] = False

if not st.session_state["app_geladen"]:
    st.markdown("""
        <style>
        .loading-container {
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            height: 70vh; font-family: 'Segoe UI', sans-serif; color: #002147; text-align: center;
        }
        .spinner {
            border: 6px solid #f4f6f9; border-top: 6px solid #cc0000; border-radius: 50%;
            width: 60px; height: 60px; animation: spin 1s linear infinite; margin-bottom: 25px;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        </style>
        <div class="loading-container">
            <div class="spinner"></div>
            <h1 style="font-size: 36px; letter-spacing: 2px;">LBV PHOENIX</h1>
            <p style="font-size: 18px; color: #666;">Mobile Command Center wird optimiert...</p>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(1.2)
    st.session_state["app_geladen"] = True
    st.rerun()

# --- HILFSFUNKTION FÜR UMLAUTE ---
def umlaute_ersetzen(text):
    if not isinstance(text, str): return text
    ersetzungen = {'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue', 'ß': 'ss'}
    for umlaut, ersetzung in ersetzungen.items():
        text = text.replace(umlaut, ersetzung)
    return text

# --- MODERNES BRANDING & CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #f7f9fc; font-family: 'Segoe UI', sans-serif; }
    .stTabs [data-baseweb="tab"] { 
        color: #002147; font-weight: 700; font-size: 15px; padding: 12px 20px; 
        background-color: #ffffff; border-radius: 8px 8px 0px 0px; margin-right: 4px;
        border: 1px solid #e1e4e8;
    }
    .stTabs [aria-selected="true"] { 
        color: #ffffff !important; background-color: #002147 !important; 
    }
    .main-title { text-align: center; color: #002147; font-weight: 800; font-size: 32px; margin-bottom: 20px; }
    .custom-card {
        background-color: #ffffff; padding: 20px; border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-left: 6px solid #cc0000; margin-bottom: 20px;
    }
    div.stButton > button { width: 100%; border-radius: 8px; font-weight: bold; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSIONS STATE INITIALISIERUNG ---
if "kader_liste" not in st.session_state:
    st.session_state["kader_liste"] = ["Torwart Max", "Anna", "Lisa", "Tom", "Ben", "Felix", "Marie", "Lukas", "Emma", "Tim", "Jan", "Laura", "Sam"]
if "strafen" not in st.session_state: st.session_state["strafen"] = []
if "tore_phönix" not in st.session_state: st.session_state["tore_phönix"] = 0
if "tore_gegner" not in st.session_state: st.session_state["tore_gegner"] = 0
if "spielbericht_events" not in st.session_state: st.session_state["spielbericht_events"] = []

# --- HEADER ---
st.markdown('<h1 class="main-title">🦅 LBV PHOENIX COMMAND CENTER</h1>', unsafe_allow_html=True)

# --- KADER SIDEBAR / EXPANDER ---
with st.expander("👥 Kader-Verwaltung (Klicken zum Bearbeiten)", expanded=False):
    neuer_kader = st.data_editor(st.session_state["kader_liste"], num_rows="dynamic", placeholder="Name...", use_container_width=True)
    st.session_state["kader_liste"] = [x for x in neuer_kader if x]
kader = st.session_state["kader_liste"]

if len(kader) < 11:
    st.error("⚠️ Mindestens 11 Spieler benötigt.")
    st.stop()

# --- TABS ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📋 Aufstellung", "📸 Aufst.-Grafik", "🎨 Content-Gen", 
    "📝 Live-Ticker", "💰 Mannschaftskasse", "👁️ Bild-Analyse (KI)", "📊 Taktik & xG"
])

# --- TAB 1: AUFSTELLUNG ---
with tab1:
    st.markdown('<div class="custom-card"><h3>⚽ System & Startelf festlegen</h3>', unsafe_allow_html=True)
    formation = st.selectbox("Spielsystem:", ["4-3-3", "3-4-3", "3-5-2", "2-4-4"])
    anzahl_def, anzahl_mid, anzahl_sturm = map(int, formation.split("-"))
    stamm_aufstellung = []
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**🧤 Tor**")
        tw_val = st.selectbox("Torwart", kader, index=0, key="tw_m")
        stamm_aufstellung.append(tw_val)
        st.markdown(f"**🛡️ Abwehr ({anzahl_def})**")
        def_spieler = [st.selectbox(f"Verteidiger {i+1}", kader, index=min(1 + i, len(kader)-1), key=f"def_{i}") for i in range(anzahl_def)]
        stamm_aufstellung.extend(def_spieler)
    with col2:
        st.markdown(f"**🧠 Mittelfeld ({anzahl_mid})**")
        mid_spieler = [st.selectbox(f"Mittelfeld {i+1}", kader, index=min(1 + anzahl_def + i, len(kader)-1), key=f"mid_{i}") for i in range(anzahl_mid)]
        stamm_aufstellung.extend(mid_spieler)
    with col3:
        st.markdown(f"**⚡ Sturm ({anzahl_sturm})**")
        sturm_spieler = [st.selectbox(f"Stürmer {i+1}", kader, index=min(1 + anzahl_def + anzahl_mid + i, len(kader)-1), key=f"sturm_{i}") for i in range(anzahl_sturm)]
        stamm_aufstellung.extend(sturm_spieler)

    moegliche_bank = [p for p in kader if p not in stamm_aufstellung]
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card"><h3>🔄 Auswechselbank</h3>', unsafe_allow_html=True)
    if moegliche_bank: st.success(", ".join(moegliche_bank))
    else: st.caption("Keine Auswechselspieler verfügbar.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 2: GRAFIK ---
with tab2:
    st.subheader("📸 Startelf-Story exportieren")
    gegner_media = st.text_input("Gegner:", "UHC Hamburg", key="gegner_tab2")
    
    if st.button("🚀 Aufstellungs-Grafik generieren"):
        img = Image.new("RGB", (1080, 1920), color="#002147")
        draw = ImageDraw.Draw(img)
        draw.rectangle([40, 40, 1040, 1880], outline="#ffffff", width=8)
        
        draw.text((540, 150), "LBV PHOENIX LUEBECK", fill="#ffffff", anchor="mm", font_size=50)
        draw.text((540, 250), f"vs {gegner_media}", fill="#cc0000", anchor="mm", font_size=40)
        draw.text((540, 450), f"🧤 TW: {tw_val}", fill="#ffffff", anchor="mm", font_size=35)
        draw.text((540, 650), f"🛡️ DEF: {' • '.join(def_spieler)}", fill="#ffffff", anchor="mm", font_size=32)
        draw.text((540, 850), f"🧠 MID: {' • '.join(mid_spieler)}", fill="#ffffff", anchor="mm", font_size=32)
        draw.text((540, 1050), f"⚡ STURM: {' • '.join(sturm_spieler)}", fill="#ffffff", anchor="mm", font_size=32)
        
        st.image(img, width=300)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.download_button("📥 Grafik herunterladen", data=buf.getvalue(), file_name="phoenix_lineup.png", mime="image/png")

# --- TAB 3: CONTENT GENERATOR ---
with tab3:
    st.subheader("🎨 Content & Story Generator")
    st.info("Nutze die Grafik-Exporte aus Tab 2, um Content für Instagram direkt im Web-View zu speichern.")

# --- TAB 4: LIVE TICKER ---
with tab4:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.metric("🦅 LBV Phoenix", st.session_state['tore_phönix'])
    with c2: st.metric("🆚 Gegner", st.session_state['tore_gegner'])
    
    b1, b2 = st.columns(2)
    with b1: 
        if st.button("⚽ Tor für Phönix"): 
            st.session_state["tore_phönix"] += 1
            st.rerun()
    with b2: 
        if st.button("❌ Tor für Gegner"): 
            st.session_state["tore_gegner"] += 1
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 5: KASSE ---
with tab5:
    st.subheader("💰 Mannschaftskasse")
    s_spieler = st.selectbox("Spieler:", kader, key="kasse_s")
    grund = st.selectbox("Vergehen:", ["Zu spät (5€)", "Grüne Karte (2€)", "Gelbe Karte (5€)", "Kasten vergessen (10€)"])
    if st.button("Euro buchen 💶"):
        betrag = grund.split("(")[1].split("€")[0]
        st.session_state["strafen"].append({"Spieler": s_spieler, "Grund": grund, "Betrag": int(betrag), "Datum": datetime.now().strftime("%d.%m.%y")})
        st.success("Erfolgreich gebucht!")
        st.rerun()
    if st.session_state["strafen"]:
        st.table(pd.DataFrame(st.session_state["strafen"]))

# --- TAB 6: COMPUTER VISION BILD-ANALYSE (Sicher & Leichtgewichtig) ---
with tab6:
    st.markdown('<div class="custom-card"><h3>👁️ Phoenix Tactical Image Analyzer</h3>', unsafe_allow_html=True)
    st.write("Analysiere Fotos von Taktikboards oder Spielszenen auf Qualität, Kontraste und Lesbarkeit.")
    
    uploaded_file = st.file_uploader("Bild auswählen...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        opencv_img = cv2.imdecode(file_bytes, 1)
        
        st.image(uploaded_file, caption="Hochgeladenes Taktikfoto", width=350)
        
        with st.spinner("Computer Vision Analyse läuft..."):
            # Berechnung von Bildstatistiken via OpenCV
            gray = cv2.cvtColor(opencv_img, cv2.COLOR_BGR2GRAY)
            schaerfe = cv2.Laplacian(gray, cv2.CV_64F).var()
            helligkeit = np.mean(gray)
            
            st.markdown("#### 📊 Analyseergebnis der KI:")
            if schaerfe < 100:
                st.error(f"⚠️ **Bild ist unscharf** ({schaerfe:.1f} Var). Details auf Taktikboards könnten verschwommen sein.")
            else:
                st.success(f"✅ **Gute Schärfe** ({schaerfe:.1f} Var). Linien und Spielernamen sind gut lesbar.")
                
            if helligkeit < 50:
                st.warning(f"🌙 **Bild ist zu dunkel** ({helligkeit:.1f}/255). Erhöhe die Belichtung für bessere Analyse.")
            elif helligkeit > 200:
                st.warning(f"☀️ **Bild ist überbelichtet** ({helligkeit:.1f}/255). Details könnten verloren gehen.")
            else:
                st.success(f"☀️ **Optimale Belichtung** ({helligkeit:.1f}/255).")
    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 7: EXTRA TAKTIK FEATURE ---
with tab7:
    st.markdown('<div class="custom-card"><h3>📊 Live-Chance & xG-Analyse</h3>', unsafe_allow_html=True)
    distanz = st.slider("Entfernung zum Tor (in Metern):", 1, 50, 12)
    winkel = st.slider("Schusswinkel (90° = Zentral vor dem Tor):", 10, 90, 90)
    verteidiger = st.radio("Druck durch Gegenspieler:", ["Keine (Freie Bahn)", "Mäßig", "Stark"])
    
    base_xg = 0.85 if distanz < 7 else (1 / (distanz * 0.15))
    def_factor = 1.0 if verteidiger == "Keine (Freie Bahn)" else (0.5 if verteidiger == "Mäßig" else 0.15)
    final_xg = min(0.99, max(0.01, base_xg * (winkel / 90) * def_factor))
    
    st.metric("Expected Goal Wert (xG-Wahrscheinlichkeit)", f"{final_xg:.2f}")
    if final_xg > 0.5: st.success("🔥 Erstklassige Torchance!")
    else: st.error("🛑 Geringe Erfolgsaussicht. Ein Pass wäre klüger.")
    st.markdown('</div>', unsafe_allow_html=True)
