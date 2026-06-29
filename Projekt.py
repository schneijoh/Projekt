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
    page_title="LBV Phoenix Command Center v4.0", 
    page_icon="🦅", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- SESSION STATE INITIALISIERUNG ---
if "app_geladen" not in st.session_state: 
    st.session_state["app_geladen"] = False
if "kader_liste" not in st.session_state:
    st.session_state["kader_liste"] = [
        "Torwart Max", "Anna", "Lisa", "Tom", "Ben", "Felix", 
        "Marie", "Lukas", "Emma", "Tim", "Jan", "Laura", "Sam"
    ]
if "strafen" not in st.session_state: 
    st.session_state["strafen"] = []
if "tore_phönix" not in st.session_state: 
    st.session_state["tore_phönix"] = 0
if "tore_gegner" not in st.session_state: 
    st.session_state["tore_gegner"] = 0
if "spielbericht_events" not in st.session_state: 
    st.session_state["spielbericht_events"] = []
if "match_momentum" not in st.session_state: 
    st.session_state["match_momentum"] = [50]
if "verletzungen" not in st.session_state:
    st.session_state["verletzungen"] = [
        {"Spieler": "Tom", "Verletzung": "Oberschenkelzerrung", "Status": "Ausfall", "Rückkehr": "In 2 Wochen"}
    ]
if "trainingsplan" not in st.session_state:
    st.session_state["trainingsplan"] = []

# --- LADESCREEN ---
if not st.session_state["app_geladen"]:
    st.markdown("""
        <style>
        .loading-wrapper {
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            height: 80vh; font-family: 'Segoe UI', sans-serif; text-align: center; background: #02060c;
            border-radius: 20px; border: 3px solid #cc0000;
        }
        .phoenix-pulse {
            width: 120px; height: 120px; background: #cc0000; border-radius: 50%;
            animation: pulse 1.2s infinite ease-in-out; margin-bottom: 30px;
            box-shadow: 0 0 40px #cc0000;
        }
        @keyframes pulse {
            0% { transform: scale(0.8); opacity: 0.5; }
            50% { transform: scale(1.1); opacity: 1; box-shadow: 0 0 60px #ff3333; }
            100% { transform: scale(0.8); opacity: 0.5; }
        }
        .glitch-text {
            color: #ffffff; font-size: 45px; font-weight: 900; letter-spacing: 5px;
            margin: 0; text-transform: uppercase;
        }
        </style>
        <div class="loading-wrapper">
            <div class="phoenix-pulse"></div>
            <h1 class="glitch-text">LBV Phoenix</h1>
            <p style="color: #ffcc00; font-size: 18px; font-weight: bold; margin-top: 10px;">QUANTUM TACTICAL CORE SYSTEM LOADING...</p>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(1.5)
    st.session_state["app_geladen"] = True
    st.rerun()

# --- HILFSFUNKTION FÜR UMLAUTE (POSTER RENDERING) ---
def umlaute_ersetzen(text):
    if not isinstance(text, str): return text
    ersetzungen = {'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue', 'ß': 'ss'}
    for umlaut, ersetzung in ersetzungen.items():
        text = text.replace(umlaut, ersetzung)
    return text

# --- HIGH-CONTRAST NEON SPORT DESIGN STYLE (CSS) ---
st.markdown("""
    <style>
    /* Global Overrides für maximalen Kontrast */
    .stApp { background-color: #04080f; color: #ffffff; font-family: 'Segoe UI', sans-serif; }
    
    /* Input-Elemente Textfarbe erzwingen */
    div[data-baseweb="select"] *, div[data-baseweb="input"] * {
        color: #ffffff !important;
    }
    
    /* Hard-Contrast Containers */
    .metric-container {
        background-color: #0b1320;
        padding: 25px; 
        border-radius: 12px; 
        border: 2px solid #2c3e50;
        box-shadow: 0 8px 16px rgba(0,0,0,0.6); 
        margin-bottom: 25px;
    }
    
    .metric-container h3 {
        color: #ffcc00 !important;
        font-weight: 800 !important;
        margin-top: 0px;
    }
    
    /* Navigation Tabs Restyling mit klaren Trennungen */
    .stTabs [data-baseweb="tab"] { 
        color: #ffffff !important; 
        font-weight: 800; 
        font-size: 15px; 
        padding: 16px 24px; 
        background: #111d30; 
        border-radius: 8px 8px 0 0; 
        margin-right: 4px;
        border: 2px solid #2c3e50;
        border-bottom: none;
    }
    .stTabs [aria-selected="true"] { 
        color: #ffffff !important; 
        background: #cc0000 !important; 
        border-color: #ff3333 !important;
        box-shadow: 0 -4px 15px rgba(254, 0, 0, 0.4);
    }
    
    /* Header Style */
    .app-header {
        text-align: center; 
        padding: 30px; 
        background: linear-gradient(90deg, #00152f 0%, #cc0000 100%);
        border: 3px solid #ffffff;
        border-radius: 12px; 
        margin-bottom: 30px;
    }
    .app-header h1 { color: #ffffff !important; font-size: 38px !important; font-weight: 900 !important; letter-spacing: 3px; margin: 0; }
    
    /* High-Contrast Buttons */
    div.stButton > button {
        width: 100%; 
        border-radius: 8px; 
        font-weight: 900; 
        font-size: 16px;
        padding: 14px;
        background: #16253d;
        color: #ffffff !important; 
        border: 2px solid #ffffff;
        text-transform: uppercase;
    }
    div.stButton > button:hover { 
        background: #cc0000 !important; 
        border-color: #ffcc00 !important; 
        color: #ffffff !important;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #080f1a !important;
        border-right: 3px solid #2c3e50;
    }
    </style>
    """, unsafe_allow_html=True)

# --- APP HEADER ---
st.markdown('<div class="app-header"><h1>🦅 PHOENIX COMMAND CENTER v4.0</h1></div>', unsafe_allow_html=True)

# --- SIDEBAR: KADERMANAGEMENT & SYSTEMSTATUS ---
with st.sidebar:
    st.header("⚡ System-Konfiguration")
    st.markdown("---")
    with st.expander("📋 Live-Kader-Datenbank", expanded=True):
        neuer_kader = st.data_editor(st.session_state["kader_liste"], num_rows="dynamic", placeholder="Spieler hinzufügen...", use_container_width=True)
        st.session_state["kader_liste"] = [x for x in neuer_kader if x]
    
    kader = st.session_state["kader_liste"]
    
    st.markdown("---")
    st.markdown("### 📊 Live-Status")
    st.metric("Registrierte Spieler", f"{len(kader)} Akteure")
    
    if len(kader) < 11:
        st.error("🚨 KRITISCHER FEHLER: Unter 11 Spieler verfügbar!")
        st.stop()
    else:
        st.success("🟢 Kaderstärke einsatzbereit.")

# --- NAVIGATION TABS ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "⚽ Formation Pro", "📸 High-Res Export", "📝 Live-Ticker Pro", 
    "🏥 Medizin & Fitness", "💰 Finanz-Kasse", "👁️ Computer Vision", 
    "📊 Analytics Engine", "📋 Training Planner"
])

# --- TAB 1: FORMATION PRO & TAKTIK-ROLES ---
with tab1:
    st.markdown('<div class="metric-container"><h3>⚽ Taktische Ausrichtung & Spielerprofile</h3>', unsafe_allow_html=True)
    
    col_f1, col_f2 = st.columns([1, 2])
    with col_f1:
        formation = st.selectbox("Taktische Grundordnung:", [
            "4-3-3 (Offensiv)", "3-4-3 (Flügelspiel)", "3-5-2 (Kompakt)", 
            "4-4-2 (Klassisch)", "2-4-4 (All-In)", "5-3-2 (Defensiv)"
        ])
        ausrichtung = st.select_slider("Mannschafts-Mentalität:", options=["Ultra-Defensiv", "Konter", "Ausgeglichen", "Pressing", "All-Out Attack"])
        match_typ = st.radio("Match-Typ:", ["Punktspiel", "Pokalmatch", "Freundschaftsspiel / Test"])
    
    with col_f2:
        st.markdown("#### 🎯 Taktische Marschroute")
        st.info(f"Gewähltes System: **{formation}** mit Ausrichtung **{ausrichtung}** im **{match_typ}**. Die Abfangleistung im Mittelfeld hat oberste Priorität.")

    form_clean = formation.split(" ")[0]
    anzahl_def, anzahl_mid, anzahl_sturm = map(int, form_clean.split("-"))
    stamm_aufstellung = []
    spieler_rollen = {}
    
    st.markdown("---")
    st.markdown("### 🏃‍♂️ Positionsbezogene Rollenverteilung")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<b style='color:#ffcc00; font-size:18px;'>🧤 TOR (TW)</b>", unsafe_allow_html=True)
        tw_val = st.selectbox("Torwart", kader, index=0, key="tw_pro")
        stamm_aufstellung.append(tw_val)
        spieler_rollen[tw_val] = st.selectbox("Rolle TW:", ["Klassischer Linienrichter", "Mitspielender Torwart (Sweeper Keeper)"])
        
        st.markdown(f"<b style='color:#ffffff; font-size:18px;'>🛡️ DEFENSIVE ({anzahl_def})</b>", unsafe_allow_html=True)
        def_spieler = []
        for i in range(anzahl_def):
            sp = st.selectbox(f"Verteidiger {i+1}", kader, index=min(1 + i, len(kader)-1), key=f"def_pro_{i}")
            def_spieler.append(sp)
            stamm_aufstellung.append(sp)
            spieler_rollen[sp] = st.selectbox(f"Rolle Def {i+1}:", ["Innenverteidiger", "Flügelverteidiger (Inverted)", "Zerstörer"], key=f"roll_d_{i}")

    with c2:
        st.markdown(f"<b style='color:#ffcc00; font-size:18px;'>🧠 ZENTRUM & STRATEGIE ({anzahl_mid})</b>", unsafe_allow_html=True)
        mid_spieler = []
        for i in range(anzahl_mid):
            sp = st.selectbox(f"Mittelfeld {i+1}", kader, index=min(1 + anzahl_def + i, len(kader)-1), key=f"mid_pro_{i}")
            mid_spieler.append(sp)
            stamm_aufstellung.append(sp)
            spieler_rollen[sp] = st.selectbox(f"Rolle Mid {i+1}:", ["Box-to-Box", "Tiefer Spielmacher", "Abkippende Sechs", "Zehner / Regisseur"], key=f"roll_m_{i}")

    with c3:
        st.markdown(f"<b style='color:#ff3333; font-size:18px;'>⚡ STURM ({anzahl_sturm})</b>", unsafe_allow_html=True)
        sturm_spieler = []
        for i in range(anzahl_sturm):
            sp = st.selectbox(f"Stürmer {i+1}", kader, index=min(1 + anzahl_def + anzahl_mid + i, len(kader)-1), key=f"sturm_pro_{i}")
            sturm_spieler.append(sp)
            stamm_aufstellung.append(sp)
            spieler_rollen[sp] = st.selectbox(f"Rolle Sturm {i+1}:", ["Stoßstürmer", "Falsche Neun", "Flügelstürmer (Inside Forward)"], key=f"roll_s_{i}")

    moegliche_bank = [p for p in kader if p not in stamm_aufstellung]
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="metric-container"><h3>🔄 Matchday Bank (Verfügbare Einwechselspieler)</h3>', unsafe_allow_html=True)
    if moegliche_bank: 
        st.markdown(f"<h4 style='color:#ffcc00;'>{'  •  '.join(moegliche_bank)}</h4>", unsafe_allow_html=True)
    else: 
        st.caption("Keine Auswechselspieler auf der Bank.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 2: HIGH-RES POSTER GENERATOR ---
with tab2:
    st.markdown('<div class="metric-container"><h3>📸 Social Media Matchday Poster (4K Story Format)</h3>', unsafe_allow_html=True)
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        gegner = st.text_input("Gegnerischer Verein:", "UHC Hamburg", key="gegner_pro")
        spiel_ort = st.text_input("Spielort / Platzanlage:", "Buniamshof (Heimspiel)", key="ort_pro")
        trainer_name = st.text_input("Verantwortlicher Coach:", "Headcoach Coach Phoenix", key="coach_pro")
    
    with col_p2:
        st.markdown("#### Grafik-Spezifikation")
        st.write("- Auflösung: 2160 x 3840 (Ultra HD Story Format)")
        st.write("- Farbraum: High-Contrast RGB")
        st.write("- Branding: LBV Phoenix Corporate Design")

    if st.button("⚡ HIGH-RES GRAPHIC POSTER RENDERN"):
        img = Image.new("RGB", (2160, 3840), color="#04080f")
        draw = ImageDraw.Draw(img)
        
        # Design-Rahmen
        draw.rectangle([40, 40, 2120, 3800], outline="#cc0000", width=20)
        draw.rectangle([65, 65, 2095, 3775], outline="#ffffff", width=6)
        draw.line([1080, 500, 1080, 3400], fill="#2c3e50", width=8)
        
        # Text-Stile & Positionierungen
        draw.text((1080, 280), "LBV PHOENIX LUEBECK", fill="#ffffff", anchor="mm", font_size=130)
        draw.text((1080, 440), f"MATCHDAY vs {gegner.upper()}", fill="#ffcc00", anchor="mm", font_size=90)
        draw.text((1080, 560), f"ORT: {spiel_ort.upper()} | CO: {trainer_name.upper()}", fill="#ffffff", anchor="mm", font_size=55)
        
        # Aufstellung
        draw.text((1080, 950), umlaute_ersetzen(f"🧤 TOR: {tw_val}"), fill="#ffffff", anchor="mm", font_size=90)
        draw.text((1080, 1350), umlaute_ersetzen(f"🛡️ ABWEHR ({anzahl_def}): {' • '.join(def_spieler)}"), fill="#ffffff", anchor="mm", font_size=75)
        draw.text((1080, 1850), umlaute_ersetzen(f"🧠 MITTELFELD ({anzahl_mid}): {' • '.join(mid_spieler)}"), fill="#ffffff", anchor="mm", font_size=75)
        draw.text((1080, 2350), umlaute_ersetzen(f"⚡ ANGRIFF ({anzahl_sturm}): {' • '.join(sturm_spieler)}"), fill="#ff3333", anchor="mm", font_size=80)
        
        draw.text((1080, 2950), umlaute_ersetzen(f"🔄 BANK: {', '.join(moegliche_bank) if moegliche_bank else 'Keine'}"), fill="#ffffff", anchor="mm", font_size=65)
        draw.text((1080, 3600), "🦅 AUTOMATED BY PHOENIX COMMAND CORE v4.0", fill="#ffcc00", anchor="mm", font_size=55)
        
        st.image(img, width=400)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.download_button("📥 High-Res Poster herunterladen (PNG)", data=buf.getvalue(), file_name="phoenix_matchday_4k.png", mime="image/png")
    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 3: LIVE-TICKER PRO & MOMENTUM ---
with tab3:
    st.markdown('<div class="metric-container"><h3>📝 Advanced Live-Ticker & Event Log</h3>', unsafe_allow_html=True)
    
    col_s1, col_s2 = st.columns(2)
    with col_s1: 
        st.markdown(f"<div style='background:#cc0000; padding:20px; text-align:center; border-radius:10px; border:2px solid white;'><h2 style='color:white; margin:0;'>🦅 PHOENIX</h2><span style='font-size:70px; font-weight:900; color:white;'>{st.session_state['tore_phönix']}</span></div>", unsafe_allow_html=True)
    with col_s2: 
        st.markdown(f"<div style='background:#111d30; padding:20px; text-align:center; border-radius:10px; border:2px solid white;'><h2 style='color:white; margin:0;'>🆚 GEGNER</h2><span style='font-size:70px; font-weight:900; color:white;'>{st.session_state['tore_gegner']}</span></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    b_l, b_r = st.columns(2)
    with b_l:
        if st.button("⚽ TOR FÜR PHOENIX EINLOGGEN"):
            st.session_state["tore_phönix"] += 1
            st.session_state["spielbericht_events"].append(f"[{datetime.now().strftime('%H:%M:%S')}] ⚽ TOR FÜR PHOENIX LÜBECK!")
            st.session_state["match_momentum"].append(min(100, st.session_state["match_momentum"][-1] + 20))
            st.rerun()
    with b_r:
        if st.button("❌ GEGENTOR EINLOGGEN"):
            st.session_state["tore_gegner"] += 1
            st.session_state["spielbericht_events"].append(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Tor für den Gegner.")
            st.session_state["match_momentum"].append(max(0, st.session_state["match_momentum"][-1] - 20))
            st.rerun()
            
    st.markdown("---")
    st.markdown("#### Spezifisches Match-Event loggen")
    ev_c1, ev_c2, ev_c3 = st.columns(3)
    with ev_c1:
        ticker_spieler = st.selectbox("Involvierter Spieler:", kader, key="tick_sp")
    with ev_c2:
        ticker_event = st.selectbox("Ereignis-Typ:", ["Grüne Karte (2 Min)", "Gelbe Karte", "Gelb-Rot (Ausfall)", "Strafecke erzielt", "Ecke abgewehrt", "Führungswechsel"])
    with ev_c3:
        ticker_kommentar = st.text_input("Zusatz-Kommentar (Optional):")
        
    if st.button("PRO-EVENT IN SPiELBERICHT SPEICHERN"):
        log_entry = f"[{datetime.now().strftime('%H:%M')}] • {ticker_spieler} -> {ticker_event} ({ticker_kommentar if ticker_kommentar else 'Keine Angabe'})"
        st.session_state["spielbericht_events"].append(log_entry)
        st.success("Event erfolgreich verarbeitet!")
        st.rerun()
        
    st.markdown("---")
    st.markdown("#### 📜 Chronologischer Live-Spielbericht")
    if st.session_state["spielbericht_events"]:
        for ev in reversed(st.session_state["spielbericht_events"]):
            st.markdown(f"<code style='font-size:16px; color:#ffcc00;'>{ev}</code>", unsafe_allow_html=True)
    else:
        st.caption("Noch keine Spielereignisse dokumentiert.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 4: MEDICAL DEPARTMENT & FITNESS ---
with tab4:
    st.markdown('<div class="metric-container"><h3>🏥 Medizinische Abteilung & Belastungs-Steuerung</h3>', unsafe_allow_html=True)
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("#### 🩹 Neue Verletzung eintragen")
        v_spieler = st.selectbox("Spieler:", kader, key="med_sp")
        v_art = st.text_input("Diagnose / Befund:", "Muskuläre Probleme")
        v_status = st.selectbox("Einsatzfähigkeit:", ["Ausfall", "Angeschlagen (Teiltraining)", "Spielfähig mit Einschränkung"])
        v_back = st.text_input("Voraussichtliche Rückkehr:", "10 Tage")
        
        if st.button("MEDIZINISCHEN STATUS AKTUALISIEREN"):
            st.session_state["verletzungen"].append({
                "Spieler": v_spieler, "Verletzung": v_art, "Status": v_status, "Rückkehr": v_back
            })
            st.success("Datenbank-Eintrag geschrieben!")
            st.rerun()
            
    with col_m2:
        st.markdown("#### 📈 Aktuelle Patientenakte & Lazarett")
        if st.session_state["verletzungen"]:
            df_med = pd.DataFrame(st.session_state["verletzungen"])
            st.dataframe(df_med, use_container_width=True)
        else:
            st.success("Alle Spieler sind zu 100% fit!")
            
    st.markdown("---")
    st.markdown("#### 🏃‍♂️ Belastungs-Analyse (RPE - Rate of Perceived Exertion)")
    st.write("Ermittlung des Ermüdungskoeffizienten der Mannschaft vor dem Spiel.")
    rpe_score = st.slider("Durchschnittlicher Erschöpfungsgrad (1 = Topfit, 10 = Absolutes Limit):", 1, 10, 4)
    if rpe_score > 7:
        st.error("🚨 WARNUNG: Erhöhte Verletzungsgefahr detektiert. Intensität im Training drosseln!")
    else:
        st.success("🟢 Belastungskoeffizient im grünen Bereich. Volle Intensität möglich.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 5: FINANZ-KASSE & STRAFEN ---
with tab5:
    st.markdown('<div class="metric-container"><h3>💰 Digitales Kassenbuch & Mannschaftskasse</h3>', unsafe_allow_html=True)
    
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        st.markdown("#### 📝 Vergehen verbuchen")
        k_spieler = st.selectbox("Spieler:", kader, key="kasse_pro")
        k_vergehen = st.selectbox("Katalog-Auswahl:", [
            "Zu spät zum Treffpunkt (10€)", 
            "Unsportliches Verhalten (20€)", 
            "Ausrüstung vergessen (5€)", 
            "Rote Karte (50€)", 
            "Trikot nicht gewaschen (15€)"
        ])
        
        if st.button("BETRAG UNWIDERRUFLICH BUCHEN"):
            extracted_betrag = k_vergehen.split("(")[1].split("€")[0]
            st.session_state["strafen"].append({
                "Spieler": k_spieler, 
                "Vergehen": k_vergehen.split(" (")[0], 
                "Betrag (EUR)": int(extracted_betrag), 
                "Timestamp": datetime.now().strftime("%d.%m.%Y - %H:%M")
            })
            st.success("Finanztransaktion erfolgreich abgeschlossen!")
            st.rerun()
            
    with col_k2:
        st.markdown("#### 📊 Offene Posten & Bilanz")
        if st.session_state["strafen"]:
            df_strafen_pro = pd.DataFrame(st.session_state["strafen"])
            st.dataframe(df_strafen_pro, use_container_width=True)
            total_cash = df_strafen_pro["Betrag (EUR)"].sum()
            st.metric("Gesamtguthaben Mannschaftskasse", f"{total_cash} EUR", delta=f"+{df_strafen_pro.iloc[-1]['Betrag (EUR)']} EUR (Letzte Buchung)")
        else:
            st.info("Die Kasse ist leer. Keine Strafen offen.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 6: KI COMPUTER VISION (ERWEITERT) ---
with tab6:
    st.markdown('<div class="metric-container"><h3>👁️ Phoenix AI Core: Tactical Computer Vision</h3>', unsafe_allow_html=True)
    st.write("Modul zur Echtzeitanalyse von Spielszenen, Taktikboards oder gegnerischen Formationen mittels OpenCV Matrix-Transformationen.")
    
    cv_file = st.file_uploader("Bild zur Taktikanalyse hochladen (PNG/JPG)...", type=["jpg", "png", "jpeg"], key="cv_file_pro")
    
    if cv_file is not None:
        file_bytes = np.asarray(bytearray(cv_file.read()), dtype=np.uint8)
        img_cv = cv2.imdecode(file_bytes, 1)
        
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            st.image(cv_file, caption="Eingelesenes Originalbild", use_container_width=True)
            
        with col_c2:
            st.markdown("#### ⚙️ OpenCV Graustufen- & Kantenerkennung")
            gray_img = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            edges_img = cv2.Canny(gray_img, 60, 180)
            st.image(edges_img, caption="Prozessierte Struktur-Matrix (Canny)", use_container_width=True, channels="GRAY")
            
        with col_c3:
            st.markdown("#### 🔬 Statistische Bild-DNA")
            small_p = cv2.resize(img_cv, (40, 40)).reshape(-1, 3)
            mean_colors = np.mean(small_p, axis=0)
            rgb_fix = (int(mean_colors[2]), int(mean_colors[1]), int(mean_colors[0]))
            
            st.write(f"• Pixel-Dimensionen: {img_cv.shape[1]}x{img_cv.shape[0]}")
            st.write(f"• Farb-Cluster Mittelwert (RGB): {rgb_fix}")
            st.markdown(f"""
                <div style="width:100%; height:50px; background-color:rgb{rgb_fix}; 
                border:2px solid white; border-radius:6px; text-align:center; line-height:50px; font-weight:900;">
                    ANALYSIERTE JERSEY-FARBE
                </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 7: ADVANCED ANALYTICS ENGINE & XG ---
with tab7:
    st.markdown('<div class="metric-container"><h3>📊 Predictive Analytics & Match-Momentum Tracker</h3>', unsafe_allow_html=True)
    
    st.markdown("#### 📈 Live Match-Momentum Kurve")
    st.line_chart(st.session_state["match_momentum"])
    
    st.markdown("---")
    st.markdown("#### 📐 Mathematisches xG-Wahrscheinlichkeitsmodell (Expected Goals)")
    
    col_an1, col_an2 = st.columns(2)
    with col_an1:
        x_dist = st.slider("Schuss-Entfernung zum Tor (Meter):", 1, 50, 12, key="an_dist")
        x_winkel = st.slider("Winkel zum Gehäuse (90° = Zentral frontal):", 5, 90, 80, key="an_wink")
    with col_an2:
        x_gk = st.select_slider("Stellungsspiel Torhüter:", options=["Deplatziert", "In Bewegung", "Optimal positioniert"])
        x_press = st.selectbox("Defensiver Druck durch Gegner:", ["Kein Druck (Freistehend)", "Mäßiger Druck", "Extremer Raumverlust (Doppeldeckung)"])
        
    # xG Algorithmische Berechnung
    base_calc = 0.95 if x_dist < 5 else (1.5 / (x_dist * 0.15))
    w_factor = x_winkel / 90
    gk_factor = 2.0 if x_gk == "Deplatziert" else (1.2 if x_gk == "In Bewegung" else 0.8)
    press_factor = 1.0 if x_press == "Kein Druck (Freistehend)" else (0.50 if x_press == "Mäßiger Druck" else 0.10)
    
    final_xg = min(0.99, max(0.01, base_calc * w_factor * gk_factor * press_factor))
    
    st.metric("Berechneter xG-Wert für Abschluss", f"{final_xg:.4f}")
    if final_xg > 0.70:
        st.success("🔥 KLASSISCHE GROSSCHANCE! Ein Fehlschuss wäre statistisch unwahrscheinlich.")
    elif final_xg > 0.35:
        st.warning("⚠️ PROBABLE GOAL! Gute Abschluss-Positionierung.")
    else:
        st.error("🛑 WENIG ERFOLGVERSPRECHEND! Taktische Empfehlung: Neuaufbau oder Abgabe.")
        
    st.markdown("---")
    st.markdown("#### 🔮 Live-Tabellen-Kalkulator (Simulations-Rechner)")
    st.write("Berechne die Punkteausbeute der nächsten Spiele im fiktiven Ligaszenario.")
    s_sieg = st.number_input("Erwartete Siege:", min_value=0, max_value=20, value=3)
    s_remis = st.number_input("Erwartete Unentschieden:", min_value=0, max_value=20, value=1)
    
    berechnete_punkte = (s_sieg * 3) + (s_remis * 1)
    st.markdown(f"<h3 style='color:#ffcc00;'>Prognostizierter Punktgewinn: {berechnete_punkte} Zähler</h3>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 8: TRAINING PLANNER & DRILLS ---
with tab8:
    st.markdown('<div class="metric-container"><h3>📋 Training Planner & Drill Konstruktor</h3>', unsafe_allow_html=True)
    
    col_tr1, col_tr2 = st.columns(2)
    with col_tr1:
        st.markdown("#### 🛠️ Neue Übungseinheit entwerfen")
        t_titel = st.text_input("Bezeichnung der Übung:", "Überzahlspiel 3vs2 am Kreis")
        t_dauer = st.number_input("Dauer der Einheit (Minuten):", min_value=5, max_value=120, value=20)
        t_fokus = st.selectbox("Schwerpunkt:", ["Taktik / Verschieben", "Physis / Kondition", "Technik / Stockarbeit", "Torschuss-Varianten"])
        t_beschreibung = st.text_area("Detaillierter Ablauf & Coaching Points:")
        
        if st.button("ÜBUNG IN TRAININGSPROTOKOLL SPEICHERN"):
            st.session_state["trainingsplan"].append({
                "Übung": t_titel, "Dauer (Min)": t_dauer, "Fokus": t_fokus, "Details": t_beschreibung
            })
            st.success("Übung erfolgreich für die nächste Einheit eingeplant!")
            st.rerun()
            
    with col_tr2:
        st.markdown("#### 📋 Geplante Übungen für die nächste Session")
        if st.session_state["trainingsplan"]:
            df_train = pd.DataFrame(st.session_state["trainingsplan"])
            st.dataframe(df_train, use_container_width=True)
            gesamtdauer = df_train["Dauer (Min)"].sum()
            st.metric("Gesamtdauer der Trainingseinheit", f"{gesamtdauer} Minuten")
        else:
            st.caption("Noch keine Übungen für das anstehende Training definiert.")
    st.markdown('</div>', unsafe_allow_html=True)
