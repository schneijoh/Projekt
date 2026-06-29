import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image, ImageDraw, ImageEnhance
import io
import time
import numpy as np
import cv2

# --- STREAMLIT CONFIG (Muss zwingend ganz oben stehen) ---
st.set_page_config(
    page_title="LBV Phoenix Mobile CC", 
    page_icon="🦅", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- SESSIONS STATE INITIALISIERUNG ---
if "app_geladen" not in st.session_state: st.session_state["app_geladen"] = False
if "kader_liste" not in st.session_state:
    st.session_state["kader_liste"] = [
        "Torwart Max", "Anna", "Lisa", "Tom", "Ben", "Felix", 
        "Marie", "Lukas", "Emma", "Tim", "Jan", "Laura", "Sam"
    ]
if "strafen" not in st.session_state: st.session_state["strafen"] = []
if "tore_phönix" not in st.session_state: st.session_state["tore_phönix"] = 0
if "tore_gegner" not in st.session_state: st.session_state["tore_gegner"] = 0
if "spielbericht_events" not in st.session_state: st.session_state["spielbericht_events"] = []
if "match_momentum" not in st.session_state: st.session_state["match_momentum"] = [50]

# --- ELEGANTNER AUDIO-VISUELLER LADESCREEN ---
if not st.session_state["app_geladen"]:
    st.markdown("""
        <style>
        .loading-wrapper {
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            height: 80vh; font-family: 'Segoe UI', sans-serif; text-align: center; background: #001124;
            border-radius: 20px; box-shadow: inset 0 0 100px rgba(0,0,0,0.5);
        }
        .phoenix-pulse {
            width: 100px; height: 100px; background: #cc0000; border-radius: 50%;
            animation: pulse 1.5s infinite ease-in-out; margin-bottom: 30px;
            box-shadow: 0 0 30px #cc0000;
        }
        @keyframes pulse {
            0% { transform: scale(0.9); opacity: 0.6; }
            50% { transform: scale(1.1); opacity: 1; box-shadow: 0 0 50px #ff3333; }
            100% { transform: scale(0.9); opacity: 0.6; }
        }
        .glitch-text {
            color: #ffffff; font-size: 40px; font-weight: 900; letter-spacing: 4px;
            margin: 0; text-transform: uppercase;
        }
        </style>
        <div class="loading-wrapper">
            <div class="phoenix-pulse"></div>
            <h1 class="glitch-text">LBV Phoenix</h1>
            <p style="color: #8a99ad; font-size: 16px; margin-top: 10px;">TACTICAL INTELLIGENCE CENTER CORE LOADED...</p>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(1.8)
    st.session_state["app_geladen"] = True
    st.rerun()

# --- HILFSFUNKTION FÜR UMLAUTE ---
def umlaute_ersetzen(text):
    if not isinstance(text, str): return text
    ersetzungen = {'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue', 'ß': 'ss'}
    for umlaut, ersetzung in ersetzungen.items():
        text = text.replace(umlaut, ersetzung)
    return text

# --- ULTRA-MODERN NEON SPORT DESIGN STYLE (CSS) ---
st.markdown("""
    <style>
    /* Global Overrides */
    .stApp { background-color: #0b131f; color: #f0f4f8; font-family: 'Segoe UI', -apple-system, sans-serif; }
    
    /* Custom Metric Cards */
    .metric-container {
        background: linear-gradient(135deg, #111c2e 0%, #080f1a 100%);
        padding: 22px; border-radius: 16px; border: 1px solid #1e2d42;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3); margin-bottom: 18px;
    }
    
    /* Navigation Tabs Restyling */
    .stTabs [data-baseweb="tab"] { 
        color: #9cb0c9 !important; font-weight: 700; font-size: 14px; padding: 14px 22px; 
        background: #111c2e; border-radius: 10px 10px 0 0; margin-right: 6px;
        border: 1px solid #1e2d42; border-bottom: none; transition: all 0.25s ease;
    }
    .stTabs [aria-selected="true"] { 
        color: #ffffff !important; background: #cc0000 !important; 
        border-color: #cc0000 !important; box-shadow: 0 -5px 15px rgba(204,0,0,0.3);
    }
    
    /* Header Style */
    .app-header {
        text-align: center; padding: 25px; background: linear-gradient(90deg, #002147 0%, #cc0000 100%);
        border-radius: 16px; margin-bottom: 25px; box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    }
    .app-header h1 { color: #ffffff !important; font-size: 34px !important; font-weight: 900 !important; letter-spacing: 2px; margin: 0; }
    
    /* Buttons Customization */
    div.stButton > button {
        width: 100%; border-radius: 10px; font-weight: 800; padding: 12px;
        background: linear-gradient(135deg, #1f3554 0%, #111c2e 100%);
        color: #ffffff; border: 1px solid #314d73; transition: all 0.2s ease;
    }
    div.stButton > button:hover { background: #cc0000; border-color: #ff3333; box-shadow: 0 0 15px rgba(204,0,0,0.4); }
    </style>
    """, unsafe_allow_html=True)

# --- APP HEADER ---
st.markdown('<div class="app-header"><h1>🦅 PHOENIX COMMAND CENTER v3.0</h1></div>', unsafe_allow_html=True)

# --- CONTROL EXPANDER FOR ROSTER ---
with st.expander("📋 Live-Kader & Spieler-Datenbank verwalten", expanded=False):
    neuer_kader = st.data_editor(st.session_state["kader_liste"], num_rows="dynamic", placeholder="Neuer Spieler...", use_container_width=True)
    st.session_state["kader_liste"] = [x for x in neuer_kader if x]
kader = st.session_state["kader_liste"]

if len(kader) < 11:
    st.error("🚨 System-Fehler: Mindestens 11 spielfähige Akteure im Kader benötigt.")
    st.stop()

# --- MAIN NAVIGATION TABS ---
tab1, tab2, tab4, tab5, tab6, tab7 = st.tabs([
    "📋 Match-Formation", "📸 High-Res Export", 
    "📝 Live-Ticker Pro", "💰 Finanz-Kasse", "👁️ KI Computer Vision", "📊 Advanced Analytics"
])

# --- TAB 1: FORMATION & STRATEGIE ---
with tab1:
    st.markdown('<div class="metric-container"><h3>⚽ Taktisches System & Match-Zuordnung</h3>', unsafe_allow_html=True)
    formation = st.selectbox("Taktische Grundordnung:", ["4-3-3 (Offensiv)", "3-4-3 (Flügelspiel)", "3-5-2 (Kompakt)", "4-4-2 (Diamond)", "2-4-4 (All-In)"])
    
    form_clean = formation.split(" ")[0]
    anzahl_def, anzahl_mid, anzahl_sturm = map(int, form_clean.split("-"))
    stamm_aufstellung = []
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<b style='color:#ffcc00;'>🧤 RÜCKHALT (TW)</b>", unsafe_allow_html=True)
        tw_val = st.selectbox("Torwart", kader, index=0, key="tw_v3")
        stamm_aufstellung.append(tw_val)
        
        st.markdown(f"<b style='color:#9cb0c9;'>🛡️ DEFENSIVE ({anzahl_def})</b>", unsafe_allow_html=True)
        def_spieler = [st.selectbox(f"Verteidiger Position {i+1}", kader, index=min(1 + i, len(kader)-1), key=f"def_v3_{i}") for i in range(anzahl_def)]
        stamm_aufstellung.extend(def_spieler)
    with c2:
        st.markdown(f"<b style='color:#9cb0c9;'>🧠 STRATEGIE & ZENTRUM ({anzahl_mid})</b>", unsafe_allow_html=True)
        mid_spieler = [st.selectbox(f"Mittelfeld Position {i+1}", kader, index=min(1 + anzahl_def + i, len(kader)-1), key=f"mid_v3_{i}") for i in range(anzahl_mid)]
        stamm_aufstellung.extend(mid_spieler)
    with c3:
        st.markdown(f"<b style='color:#ff3333;'>⚡ STURMSPITZE ({anzahl_sturm})</b>", unsafe_allow_html=True)
        sturm_spieler = [st.selectbox(f"Stürmer Position {i+1}", kader, index=min(1 + anzahl_def + anzahl_mid + i, len(kader)-1), key=f"sturm_v3_{i}") for i in range(anzahl_sturm)]
        stamm_aufstellung.extend(sturm_spieler)

    moegliche_bank = [p for p in kader if p not in stamm_aufstellung]
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="metric-container"><h3>🔄 Matchday Auswechselbank (Verfügbar)</h3>', unsafe_allow_html=True)
    if moegliche_bank: st.success(" ✔️ " + "  •  ".join(moegliche_bank))
    else: st.caption("Keine Auswechselspieler registriert.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 2: HIGH-RES EXPORT ---
with tab2:
    st.subheader("📸 Social Media Matchday Poster (4K Story Format)")
    gegner = st.text_input("Gegnerischer Verein:", "UHC Hamburg", key="g_v3")
    
    if st.button("⚡ High-Res Poster rendern & kompilieren"):
        img = Image.new("RGB", (2160, 3840), color="#001124")
        draw = ImageDraw.Draw(img)
        
        # Geometrische Design-Elemente (Premium-Vereins-Branding)
        draw.rectangle([60, 60, 2100, 3780], outline="#cc0000", width=16)
        draw.rectangle([80, 80, 2080, 3760], outline="#ffffff", width=4)
        draw.line([1100, 400, 1100, 3400], fill="#1e2d42", width=6)
        
        # Schriften & Datenplatzierung
        draw.text((1080, 250), "LBV PHOENIX LUEBECK", fill="#ffffff", anchor="mm", font_size=120)
        draw.text((1080, 420), f"MATCHDAY vs {gegner.upper()}", fill="#ffcc00", anchor="mm", font_size=80)
        
        draw.text((1080, 900), umlaute_ersetzen(f"🧤 TOR: {tw_val}"), fill="#ffffff", anchor="mm", font_size=85)
        draw.text((1080, 1300), umlaute_ersetzen(f"🛡️ ABWEHR: {' • '.join(def_spieler)}"), fill="#f0f4f8", anchor="mm", font_size=70)
        draw.text((1080, 1700), umlaute_ersetzen(f"🧠 MITTELFLD: {' • '.join(mid_spieler)}"), fill="#f0f4f8", anchor="mm", font_size=70)
        draw.text((1080, 2100), umlaute_ersetzen(f"⚡ ANGRIFF: {' • '.join(sturm_spieler)}"), fill="#ff3333", anchor="mm", font_size=75)
        draw.text((1080, 2700), umlaute_ersetzen(f"🔄 BANK: {', '.join(moegliche_bank) if moegliche_bank else 'Keine'}"), fill="#8a99ad", anchor="mm", font_size=65)
        
        draw.text((1080, 3550), "🦅 COORD CENTER AUTOMATION", fill="#314d73", anchor="mm", font_size=50)
        
        st.image(img, width=320)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.download_button("📥 Story-Grafik sichern (PNG)", data=buf.getvalue(), file_name="phoenix_matchday_4k.png", mime="image/png")

# --- TAB 4: TICKER PRO ---
with tab4:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    col_t1, col_t2 = st.columns(2)
    with col_t1: st.markdown(f"<h2 style='text-align:center; color:#ffffff;'>🦅 PHOENIX<br><span style='font-size:48px; color:#ff3333;'>{st.session_state['tore_phönix']}</span></h2>", unsafe_allow_html=True)
    with col_t2: st.markdown(f"<h2 style='text-align:center; color:#ffffff;'>🆚 GEGNER<br><span style='font-size:48px; color:#9cb0c9;'>{st.session_state['tore_gegner']}</span></h2>", unsafe_allow_html=True)
    
    btn_l, btn_r = st.columns(2)
    with btn_l:
        if st.button("⚽ TOR FÜR PHOENIX LOGGEN"):
            st.session_state["tore_phönix"] += 1
            st.session_state["spielbericht_events"].append(f"[{datetime.now().strftime('%H:%M')}] ⚽ TOR für Phoenix!")
            st.session_state["match_momentum"].append(min(100, st.session_state["match_momentum"][-1] + 15))
            st.rerun()
    with btn_r:
        if st.button("❌ TOR FÜR GEGNER LOGGEN"):
            st.session_state["tore_gegner"] += 1
            st.session_state["spielbericht_events"].append(f"[{datetime.now().strftime('%H:%M')}] ❌ Gegentor.")
            st.session_state["match_momentum"].append(max(0, st.session_state["match_momentum"][-1] - 15))
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("---")
    ev_spieler = st.selectbox("Akteur auswählen:", kader, key="ev_s")
    ev_art = st.selectbox("Ereignis-Kategorie:", ["Tor erzielt", "Karte Gelb", "Karte Grün", "Zeitstrafe 5 Min", "Ecke herausgeholt"])
    if st.button("Event fest in Spielbericht einschreiben"):
        st.session_state["spielbericht_events"].append(f"• {ev_spieler} ({ev_art})")
        st.success("Event erfolgreich registriert!")
        st.rerun()

# --- TAB 5: FINANZ-KASSE ---
with tab5:
    st.subheader("💰 Digitales Kassenbuch & Strafen-Katalog")
    s_spieler = st.selectbox("Spieler auswählen:", kader, key="kasse_v3")
    grund = st.selectbox("Katalog-Vergehen:", ["Zu spät zum Treffpunkt (5€)", "Grüne Karte (2€)", "Gelbe Karte (5€)", "Gelb-Rot / Unsportlichkeit (15€)", "Kasten vergessen (10€)"])
    
    if st.button("Betrag unwiderruflich buchen"):
        betrag = grund.split("(")[1].split("€")[0]
        st.session_state["strafen"].append({
            "Spieler": s_spieler, "Vergehen": grund.split(" (")[0], "Betrag (EUR)": int(betrag), "Datum": datetime.now().strftime("%d.%m.%Y - %H:%M")
        })
        st.success("Transaktion erfolgreich abgeschlossen!")
        st.rerun()
        
    if st.session_state["strafen"]:
        df_strafen = pd.DataFrame(st.session_state["strafen"])
        st.dataframe(df_strafen, use_container_width=True)
        st.metric("Gesamtguthaben Mannschaftskasse", f"{df_strafen['Betrag (EUR)'].sum()} €")

# --- TAB 6: KI COMPUTER VISION & IMAGE PROCESSING (NEU & ERWEITERT) ---
with tab6:
    st.markdown('<div class="metric-container"><h3>👁️ Phoenix AI Core: Advanced Computer Vision</h3>', unsafe_allow_html=True)
    st.write("Lade Bilder hoch, um komplexe visuelle Analysen durchzuführen (Taktikboard-Geometrie oder Farb-Cluster der Ausrüstung).")
    
    uploaded_file = st.file_uploader("Strategie-Dokument oder Szenenbild einlesen...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img_cv = cv2.imdecode(file_bytes, 1)
        
        col_cv1, col_cv2 = st.columns(2)
        with col_cv1:
            st.image(uploaded_file, caption="Original-Eingabe der Kamera", use_container_width=True)
            
        with col_cv2:
            with st.spinner("Führe CV-Algorithmen und Matrix-Transformationen aus..."):
                # 1. Geometrische Linien- und Taktikboard-Erkennung via Hough-Transformation
                gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
                edges = cv2.Canny(gray, 50, 150, apertureSize=3)
                lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)
                
                line_count = len(lines) if lines is not None else 0
                
                # 2. Farb-Cluster-Analyse (Bestimmung der dominanten Ausrüstungsfarben)
                # Wir skalieren das Bild herunter, um Rechenleistung zu sparen
                small_img = cv2.resize(img_cv, (50, 50))
                pixels = small_img.reshape(-1, 3)
                
                # Ermittlung der Durchschnittsfarbe (RGB)
                avg_color_bgr = np.mean(pixels, axis=0)
                avg_color_rgb = (int(avg_color_bgr[2]), int(avg_color_bgr[1]), int(avg_color_bgr[0]))
                
                # Visuelle Ausgabe des Ergebnisses
                st.markdown("#### ⚙️ Computer Vision Analysedaten:")
                st.write(f"📈 **Erkannte Feldlinien / Konturen:** {line_count}")
                if line_count > 8:
                    st.success("🎯 Taktikboard-Struktur / Spielfeld-Layout erfolgreich identifiziert.")
                else:
                    st.warning("ℹ️ Wenige klare Linien detektiert. Möglicherweise ein Foto einer Spielszene oder Freifläche.")
                
                # Anzeige der dominanten Farb-DNA
                st.write("🎨 **Dominante Farb-DNA des Bildes (RGB):**", avg_color_rgb)
                st.markdown(f"""
                    <div style="width:100%; height:40px; background-color:rgb{avg_color_rgb}; 
                    border-radius:8px; border:1px solid #ffffff; text-align:center; line-height:40px; color:#ffffff; font-weight:bold;">
                        Farb-Cluster Vorschau
                    </div>
                """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 7: ADVANCED ANALYTICS (NEU & ERWEITERT) ---
with tab7:
    st.markdown('<div class="metric-container"><h3>📊 Advanced Scouting & Match-Momentum Engine</h3>', unsafe_allow_html=True)
    
    st.write("#### 📈 Echtzeit Match-Momentum Tracker")
    st.write("Die Kurve visualisiert die Dominanz-Verschiebung basierend auf deinen Ticker-Eingaben.")
    st.line_chart(st.session_state["match_momentum"])
    
    st.write("---")
    st.write("#### 📐 Mathematische xG-Wahrscheinlichkeits-Matrix")
    
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        dist = st.slider("Schuss-Distanz zum Gehäuse (Meter):", 1, 45, 14)
        winkel = st.slider("Schusswinkel zum Tor (90° = Zentral):", 10, 90, 75)
    with col_a2:
        keeper_pos = st.radio("Torwart-Stellungsspiel:", ["Optimal positioniert", "In Bewegung / Erwischt", "Tor leer / Verlassen"])
        def_pressure = st.selectbox("Gegnerischer Verteidigungsdruck:", ["Keiner (Freistehend)", "Mäßig (Bedrängnis)", "Extrem (Zustestellt)"])
        
    # Erweiterter xG-Algorithmus
    base_calc = 0.90 if dist < 6 else (1 / (dist * 0.12))
    w_factor = winkel / 90
    
    k_factor = 1.0 if keeper_pos == "Optimal positioniert" else (1.4 if keeper_pos == "In Bewegung / Erwischt" else 2.5)
    d_factor = 1.0 if def_pressure == "Keiner (Freistehend)" else (0.45 if def_pressure == "Mäßig (Bedrängnis)" else 0.12)
    
    xg_score = min(0.99, max(0.01, base_calc * w_factor * k_factor * d_factor))
    
    st.metric("Berechneter Expected Goals Wert (xG-Faktor)", f"{xg_score:.3f}")
    if xg_score > 0.65:
        st.success("🔥 ABSOLUTE GROSSCHANCE! Statistischer Pflicht-Treffer.")
    elif xg_score > 0.30:
        st.warning("⚠️ GUTE GELEGENHEIT! Abschluss aus vielversprechender Position.")
    else:
        st.error("🛑 LOW-PERCENTAGE SHOT! Ein Zuspiel wäre taktisch ertragreicher gewesen.")
    st.markdown('</div>', unsafe_allow_html=True)
