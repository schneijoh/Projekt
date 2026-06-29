import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image, ImageDraw, ImageEnhance
import io
import time
import numpy as np
import cv2

# ==========================================
# 1. STREAMLIT CONFIGURATION (MUST BE FIRST)
# ==========================================
st.set_page_config(
    page_title="LBV Phoenix Command Center v5.0",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. SESSION STATE INITIALIZATION
# ==========================================
if "app_geladen" not in st.session_state:
    st.session_state["app_geladen"] = False

if "kader_liste" not in st.session_state:
    st.session_state["kader_liste"] = [
        "Torwart Max", "Anna Müller", "Lisa Schmidt", "Tom Becker", 
        "Ben Fischer", "Felix Weber", "Marie Meyer", "Lukas Wagner", 
        "Emma Schulz", "Tim Becker", "Jan Hoffmann", "Laura Koch", "Sam Bauer"
    ]

if "spieler_daten" not in st.session_state:
    st.session_state["spieler_daten"] = pd.DataFrame([
        {"Spieler": "Torwart Max", "Nummer": 1, "Position": "Torwart", "Status": "Fit", "Tore": 0, "Karten": 0},
        {"Spieler": "Anna Müller", "Nummer": 2, "Position": "Verteidigung", "Status": "Fit", "Tore": 1, "Karten": 0},
        {"Spieler": "Lisa Schmidt", "Nummer": 4, "Position": "Verteidigung", "Status": "Fit", "Tore": 0, "Karten": 1},
        {"Spieler": "Tom Becker", "Nummer": 6, "Position": "Mittelfeld", "Status": "Angeschlagen", "Tore": 2, "Karten": 0},
        {"Spieler": "Ben Fischer", "Nummer": 7, "Position": "Mittelfeld", "Status": "Fit", "Tore": 4, "Karten": 2},
        {"Spieler": "Felix Weber", "Nummer": 9, "Position": "Sturm", "Status": "Fit", "Tore": 12, "Karten": 0},
        {"Spieler": "Marie Meyer", "Nummer": 10, "Position": "Sturm", "Status": "Fit", "Tore": 8, "Karten": 1},
        {"Spieler": "Lukas Wagner", "Nummer": 11, "Position": "Verteidigung", "Status": "Fit", "Tore": 0, "Karten": 0},
        {"Spieler": "Emma Schulz", "Nummer": 13, "Position": "Mittelfeld", "Status": "Ausfall", "Tore": 3, "Karten": 0},
        {"Spieler": "Tim Becker", "Nummer": 14, "Position": "Sturm", "Status": "Fit", "Tore": 5, "Karten": 0},
        {"Spieler": "Jan Hoffmann", "Nummer": 17, "Position": "Verteidigung", "Status": "Fit", "Tore": 1, "Karten": 3},
        {"Spieler": "Laura Koch", "Nummer": 19, "Position": "Mittelfeld", "Status": "Fit", "Tore": 2, "Karten": 0},
        {"Spieler": "Sam Bauer", "Nummer": 22, "Position": "Torwart", "Status": "Fit", "Tore": 0, "Karten": 0}
    ])

if "strafen_db" not in st.session_state:
    st.session_state["strafen_db"] = []

if "tore_phönix" not in st.session_state:
    st.session_state["tore_phönix"] = 0

if "tore_gegner" not in st.session_state:
    st.session_state["tore_gegner"] = 0

if "ticker_events" not in st.session_state:
    st.session_state["ticker_events"] = []

if "match_momentum" not in st.session_state:
    st.session_state["match_momentum"] = [50]

if "trainingsuebungen" not in st.session_state:
    st.session_state["trainingsuebungen"] = [
        {"Titel": "Warm-up Pass-Dreieck", "Dauer": 15, "Fokus": "Technik", "Intensitaet": "Mittel"},
        {"Titel": "Umschaltspiel 4vs4", "Dauer": 25, "Fokus": "Taktik", "Intensitaet": "Hoch"}
    ]

if "logistik_inventar" not in st.session_state:
    st.session_state["logistik_inventar"] = [
        {"Gegenstand": "Bälle (Größe 5)", "Soll": 20, "Ist": 18, "Status": "Korrekt"},
        {"Gegenstand": "Markierungshemden (Rot)", "Soll": 15, "Ist": 15, "Status": "Korrekt"},
        {"Gegenstand": "Markierungshemden (Gelb)", "Soll": 15, "Ist": 12, "Status": "Fehlbestand"},
        {"Gegenstand": "Medizin-Koffer komplett", "Soll": 1, "Ist": 1, "Status": "Korrekt"},
        {"Gegenstand": "Hütchen (Set)", "Soll": 2, "Ist": 2, "Status": "Korrekt"}
    ]

# ==========================================
# 3. HIGH-CONTRAST TERMINAL LOADING SCREEN
# ==========================================
if not st.session_state["app_geladen"]:
    st.markdown("""
        <style>
        .loading-frame {
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            height: 85vh; background-color: #000000; border: 5px solid #ffcc00; text-align: center;
            font-family: 'Courier New', monospace; padding: 40px;
        }
        .pulse-box {
            width: 80px; height: 80px; background-color: #ffcc00; margin-bottom: 40px;
            animation: block-pulse 1s infinite steps(2, start);
        }
        @keyframes block-pulse {
            0% { transform: scale(1); background-color: #ffcc00; }
            100% { transform: scale(1.15); background-color: #ff0000; }
        }
        .loading-title { color: #ffffff; font-size: 50px; font-weight: 900; letter-spacing: 6px; margin: 0; }
        .loading-sub { color: #ffcc00; font-size: 16px; margin-top: 15px; font-weight: bold; }
        </style>
        <div class="loading-frame">
            <div class="pulse-box"></div>
            <h1 class="loading-title">LBV PHOENIX SYSTEM</h1>
            <p class="loading-sub">CRITICAL TACTICAL ENGINE: INITIALIZING ALL MODULES...</p>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(1.6)
    st.session_state["app_geladen"] = True
    st.rerun()

# ==========================================
# 4. ULTRA-CONTRAST CORPORATE STYLING (CSS)
# ==========================================
st.markdown("""
    <style>
    /* Global Hard Contrast Overrides */
    .stApp { 
        background-color: #000000 !important; 
        color: #ffffff !important; 
        font-family: 'Segoe UI', -apple-system, sans-serif; 
    }
    
    /* Global Font Color Reset for standard Streamlit Elements */
    p, span, label, h1, h2, h3, h4, h5, h6, li {
        color: #ffffff !important;
    }
    
    /* Input Elements Contrast Fixing */
    div[data-baseweb="select"] *, div[data-baseweb="input"] *, div[data-testid="stMarkdownContainer"] * {
        color: #ffffff !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #0f141c !important;
        border: 2px solid #ffffff !important;
    }
    
    /* Hard Core Metric Containers */
    .metric-container {
        background-color: #0f141c !important;
        padding: 25px; 
        border-radius: 4px; 
        border: 3px solid #ffcc00 !important;
        margin-bottom: 25px;
    }
    
    .metric-container h3, .metric-container h4 {
        color: #ffcc00 !important;
        font-weight: 900 !important;
        margin-top: 0px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Navigation Tabs - Maximum Visibility */
    .stTabs [data-baseweb="tab"] { 
        color: #ffffff !important; 
        font-weight: 900 !important; 
        font-size: 16px !important; 
        padding: 18px 25px !important; 
        background-color: #0f141c !important; 
        border-radius: 0px !important; 
        margin-right: 5px !important;
        border: 3px solid #ffffff !important;
        border-bottom: none !important;
    }
    .stTabs [aria-selected="true"] { 
        color: #000000 !important; 
        background-color: #ffcc00 !important; 
        border-color: #ffcc00 !important;
    }
    
    /* Main Header Element */
    .app-header {
        text-align: center; 
        padding: 35px; 
        background-color: #0f141c;
        border: 4px solid #ffffff;
        margin-bottom: 35px;
    }
    .app-header h1 { 
        color: #ffffff !important; 
        font-size: 42px !important; 
        font-weight: 900 !important; 
        letter-spacing: 4px; 
        margin: 0; 
    }
    .app-header p {
        color: #ffcc00 !important;
        margin-top: 5px;
        font-weight: bold;
        letter-spacing: 2px;
    }
    
    /* Rigid High-Contrast Buttons */
    div.stButton > button {
        width: 100% !important; 
        border-radius: 0px !important; 
        font-weight: 900 !important; 
        font-size: 16px !important;
        padding: 15px !important;
        background-color: #000000 !important;
        color: #ffffff !important; 
        border: 3px solid #ffffff !important;
        text-transform: uppercase !important;
        letter-spacing: 1px;
    }
    div.stButton > button:hover { 
        background-color: #ffcc00 !important; 
        border-color: #ffcc00 !important; 
        color: #000000 !important;
    }
    
    /* Sidebar Overrides */
    section[data-testid="stSidebar"] {
        background-color: #0f141c !important;
        border-right: 4px solid #ffcc00 !important;
    }
    
    /* Expander Layout Contrast */
    .stExpander {
        border: 2px solid #ffffff !important;
        background-color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- POSTER STRING REPLACEMENT UTILITY ---
def clean_umlauts_for_render(text):
    if not isinstance(text, str): return text
    mappings = {'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue', 'ß': 'ss'}
    for k, v in mappings.items():
        text = text.replace(k, v)
    return text

# ==========================================
# 5. HEADER RENDER
# ==========================================
st.markdown('<div class="app-header"><h1>🦅 PHOENIX COMMAND CENTER v5.0</h1><p>HIGH-CONTRAST AM OLED TACTICAL ENGINE</p></div>', unsafe_allow_html=True)

# ==========================================
# 6. SIDEBAR ENGINE
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color:#ffcc00 !important; font-weight:900;'>🎛️ CORE CONSOLE</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    with st.expander("📝 QUICK SQUAD ROSTER EDITOR", expanded=False):
        edited_kader = st.data_editor(
            st.session_state["kader_liste"], 
            num_rows="dynamic", 
            placeholder="Spielername...", 
            use_container_width=True
        )
        st.session_state["kader_liste"] = [x for x in edited_kader if x]
    
    current_kader = st.session_state["kader_liste"]
    
    st.markdown("---")
    st.markdown("### 🧮 SYSTEMMETRIKEN")
    st.metric("Verfügbare Akteure", f"{len(current_kader)} Spieler")
    
    if len(current_kader) < 11:
        st.error("🚨 CRITICAL ERROR: System benötigt mindestens 11 Spieler für Match-Zuweisung.")
        st.stop()
    else:
        st.markdown("<p style='color:#00ff00 !important; font-weight:bold;'>🟢 VALIDATION SUCCESSFUL: Kader spielbereit.</p>", unsafe_allow_html=True)

# ==========================================
# 7. MAIN INTERFACE TABS (9 FULL MODULES)
# ==========================================
tabs = st.tabs([
    "⚽ Taktik & Grid", 
    "📸 UHD Poster Export", 
    "📝 Live Ticker Pro", 
    "💰 Kassenbuch Engine", 
    "👁️ Vision Studio", 
    "📊 Analytics & xG", 
    "📋 Training Architect",
    "🍏 Hydration Coach",
    "🎒 Logistics & Kits"
])

# ------------------------------------------
# TAB 1: TAKTIK & ADVANCED FORMATION GRID
# ------------------------------------------
with tabs[0]:
    st.markdown('<div class="metric-container"><h3>⚽ Advanced Formation & Tactical Blueprint</h3>', unsafe_allow_html=True)
    
    c_tact1, c_tact2 = st.columns([1, 2])
    with c_tact1:
        system_select = st.selectbox("Taktisches System:", [
            "4-3-3 (Offensiver Drang)", "3-4-3 (Variables Flügelspiel)", 
            "3-5-2 (Kompakte Zentrale)", "4-4-2 (Klassische Raute)", "2-4-4 (All-In)"
        ])
        pressing_line = st.select_slider("Pressing-Linie:", options=["Tiefer Block", "Mittelfeldpressing", "Angriffspressing", "Extremes Gegenpressing"])
    with c_tact2:
        st.markdown("#### Taktische Vorgabe")
        st.write(f"Das System **{system_select}** agiert heute mit einer **{pressing_line}** Ausrichtung. Schnelles Umschaltspiel über die Halbräume wird erzwungen.")
    
    form_clean = system_select.split(" ")[0]
    def_count, mid_count, sturm_count = map(int, form_clean.split("-"))
    
    st.markdown("---")
    st.markdown("### 🏃‍♂️ Matchday Lineup Konstruktor")
    
    col_g1, col_g2, col_g3 = st.columns(3)
    squad_assigned = []
    
    with col_g1:
        st.markdown("<b style='color:#ffcc00; font-size:16px;'>🧤 GOALKEEPING</b>", unsafe_allow_html=True)
        tw_player = st.selectbox("Torwart (TW)", current_kader, index=0, key="sel_tw")
        squad_assigned.append(tw_player)
        
        st.markdown(f"<b style='color:#ffffff; font-size:16px;'>🛡️ DEFENSIVE LINE ({def_count})</b>", unsafe_allow_html=True)
        def_players = []
        for i in range(def_count):
            p = st.selectbox(f"Verteidiger Position {i+1}", current_kader, index=min(1+i, len(current_kader)-1), key=f"sel_def_{i}")
            def_players.append(p)
            squad_assigned.append(p)

    with col_g2:
        st.markdown(f"<b style='color:#ffcc00; font-size:16px;'>🧠 CORE MIDFIELD ({mid_count})</b>", unsafe_allow_html=True)
        mid_players = []
        for i in range(mid_count):
            p = st.selectbox(f"Mittelfeld Position {i+1}", current_kader, index=min(1+def_count+i, len(current_kader)-1), key=f"sel_mid_{i}")
            mid_players.append(p)
            squad_assigned.append(p)

    with col_g3:
        st.markdown(f"<b style='color:#ff0000; font-size:16px;'>⚡ OFFENSIVE STRIKER ({sturm_count})</b>", unsafe_allow_html=True)
        sturm_players = []
        for i in range(sturm_count):
            p = st.selectbox(f"Stürmer Position {i+1}", current_kader, index=min(1+def_count+mid_count+i, len(current_kader)-1), key=f"sel_sturm_{i}")
            sturm_players.append(p)
            squad_assigned.append(p)

    bench_players = [pl for pl in current_kader if pl not in squad_assigned]
    
    st.markdown("---")
    st.markdown("#### 🔄 Matchday-Auswechselbank (Verfügbares Ergänzungspersonal)")
    if bench_players:
        st.markdown(f"<h3 style='color:#ffcc00 !important;'>{'  •  '.join(bench_players)}</h3>", unsafe_allow_html=True)
    else:
        st.warning("Keine Auswechselspieler verfügbar. Risikoszenario bei Verletzung.")
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# TAB 2: HIGH-RES SOCIAL MEDIA ENGINE
# ------------------------------------------
with tabs[1]:
    st.markdown('<div class="metric-container"><h3>📸 UHD Social Media Poster Engine (4K Story Format)</h3>', unsafe_allow_html=True)
    
    col_post1, col_post2 = st.columns(2)
    with col_post1:
        input_opponent = st.text_input("Gegnerischer Verein:", "UHC Hamburg Pro", key="p_opp")
        input_pitch = st.text_input("Austragungsort:", "Buniamshof Hamburg", key="p_pitch")
        input_kickoff = st.text_input("Anstoßzeit:", "Sonntag, 15:00 Uhr", key="p_kick")
    with col_post2:
        st.write("Die Render-Engine generiert ein unkomprimiertes PNG im Hochkantformat (2160x3840 Pixel), optimiert für Monitore, Tablets und Social-Media-Kanäle.")
        st.write("Alle Sonderzeichen und Umlaute werden zur Vermeidung von Font-Glitches automatisch normalisiert.")

    if st.button("⚡ GENERATE HIGH-RES MATCHDAY POSTER"):
        # Create full 4K Canvas
        img_canvas = Image.new("RGB", (2160, 3840), color="#000000")
        canvas_draw = ImageDraw.Draw(img_canvas)
        
        # Geometric Rigid Frames
        canvas_draw.rectangle([50, 50, 2110, 3790], outline="#ffcc00", width=25)
        canvas_draw.rectangle([80, 80, 2080, 3760], outline="#ffffff", width=8)
        canvas_draw.line([1080, 600, 1080, 3300], fill="#ffcc00", width=10)
        
        # Header Typography Block
        canvas_draw.text((1080, 300), "LBV PHOENIX LUEBECK", fill="#ffffff", anchor="mm", font_size=140)
        canvas_draw.text((1080, 480), f"MATCHDAY vs {input_opponent.upper()}", fill="#ffcc00", anchor="mm", font_size=95)
        canvas_draw.text((1080, 620), f"LOCATION: {input_pitch.upper()} | KICKOFF: {input_kickoff.upper()}", fill="#ffffff", anchor="mm", font_size=50)
        
        # Lineup Data Blocks
        canvas_draw.text((1080, 1000), clean_umlauts_for_render(f"🧤 TOR: {tw_player}"), fill="#ffffff", anchor="mm", font_size=90)
        canvas_draw.text((1080, 1400), clean_umlauts_for_render(f"🛡️ DEF ({def_count}): {' • '.join(def_players)}"), fill="#ffffff", anchor="mm", font_size=75)
        canvas_draw.text((1080, 1900), clean_umlauts_for_render(f"🧠 MID ({mid_count}): {' • '.join(mid_players)}"), fill="#ffffff", anchor="mm", font_size=75)
        canvas_draw.text((1080, 2400), clean_umlauts_for_render(f"⚡ OFF ({sturm_count}): {' • '.join(sturm_players)}"), fill="#ffffff", anchor="mm", font_size=80)
        
        # Footer
        canvas_draw.text((1080, 3000), clean_umlauts_for_render(f"🔄 BANK: {', '.join(bench_players) if bench_players else 'Keine'}"), fill="#ffcc00", anchor="mm", font_size=70)
        canvas_draw.text((1080, 3620), "🦅 PHOENIX COMMAND AUTOMATION v5.0", fill="#ffffff", anchor="mm", font_size=50)
        
        st.image(img_canvas, width=380, caption="Gerendertes Ergebnis-Vorschau")
        
        buffer = io.BytesIO()
        img_canvas.save(buffer, format="PNG")
        st.download_button(
            label="📥 DOWNLOAD UHD GRAPHIC (PNG)", 
            data=buffer.getvalue(), 
            file_name="phoenix_4k_matchday.png", 
            mime="image/png"
        )
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# TAB 3: LIVE TICKER PRO & EVENT DATABASE
# ------------------------------------------
with tabs[2]:
    st.markdown('<div class="metric-container"><h3>📝 High-Contrast Match Ticker Engine</h3>', unsafe_allow_html=True)
    
    col_sc1, col_sc2 = st.columns(2)
    with col_sc1:
        st.markdown(f"<div style='background-color:#000000; padding:25px; text-align:center; border:4px solid #ffcc00;'><h2 style='color:#ffffff !important; margin:0;'>🦅 PHOENIX</h2><span style='font-size:80px; font-weight:900; color:#ffcc00;'>{st.session_state['tore_phönix']}</span></div>", unsafe_allow_html=True)
    with col_sc2:
        st.markdown(f"<div style='background-color:#000000; padding:25px; text-align:center; border:4px solid #ffffff;'><h2 style='color:#ffffff !important; margin:0;'>🆚 GEGNER</h2><span style='font-size:80px; font-weight:900; color:#ffffff;'>{st.session_state['tore_gegner']}</span></div>", unsafe_allow_html=True)
        
    st.markdown("---")
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("⚽ TOR FÜR PHOENIX LOGGEN", key="b_inc_p"):
            st.session_state["tore_phönix"] += 1
            st.session_state["ticker_events"].append(f"[{datetime.now().strftime('%H:%M:%S')}] ⚽ TOR! PHOENIX ERHÖHT DIE FÜHRUNG.")
            st.session_state["match_momentum"].append(min(100, st.session_state["match_momentum"][-1] + 15))
            st.rerun()
    with col_btn2:
        if st.button("❌ GEGENTOR LOGGEN", key="b_inc_o"):
            st.session_state["tore_gegner"] += 1
            st.session_state["ticker_events"].append(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ GEGENTOR. Defensive unkonzentriert.")
            st.session_state["match_momentum"].append(max(0, st.session_state["match_momentum"][-1] - 15))
            st.rerun()
            
    st.markdown("---")
    st.markdown("#### Spezifisches Matchday-Event detektieren")
    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        tick_sp = st.selectbox("Akteur:", current_kader, key="t_sp")
    with col_t2:
        tick_ev = st.selectbox("Aktion:", ["Grüne Karte (2 Min)", "Gelbe Karte", "Zeitstrafe 5 Min", "Ecke herausgeholt", "Ballverlust folgenschwer"])
    with col_t3:
        tick_comm = st.text_input("Zusatznotiz:", placeholder="Zuschauerprotest / Schiedsrichterentscheidung...")
        
    if st.button("EVENT IN SPIELBERICHT EINSPEISEN"):
        full_string = f"[{datetime.now().strftime('%H:%M')}] • {tick_sp} -> {tick_ev} | {tick_comm if tick_comm else 'Kein Kommentar'}"
        st.session_state["ticker_events"].append(full_string)
        st.success("Event erfolgreich verarbeitet.")
        st.rerun()
        
    st.markdown("---")
    st.markdown("#### 📜 Chronologisches Event-Logbuch")
    if st.session_state["ticker_events"]:
        for e in reversed(st.session_state["ticker_events"]):
            st.markdown(f"<div style='padding:5px; border-bottom:1px solid #2c3e50;'><code style='color:#ffcc00; font-size:15px;'>{e}</code></div>", unsafe_allow_html=True)
            
        # Export Option
        df_export = pd.DataFrame(st.session_state["ticker_events"], columns=["Match Event Log"])
        csv_data = df_export.to_csv(index=False).encode('utf-8')
        st.download_button("📥 SPIELBERICHT ALS CSV EXPORTIEREN", csv_data, "phoenix_match_log.csv", "text/csv")
    else:
        st.caption("Bisher keine Vorkommnisse aufgezeichnet.")
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# TAB 4: KASSENBUCH ENGINE & FINANCES
# ------------------------------------------
with tabs[3]:
    st.markdown('<div class="metric-container"><h3>💰 Financial Penalty Ledger (Strafenkatalog)</h3>', unsafe_allow_html=True)
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.markdown("#### Transaktion aufzeichnen")
        f_spieler = st.selectbox("Spieler auswählen:", current_kader, key="f_sp")
        f_vergehen = st.selectbox("Delikt laut Satzung:", [
            "Zu spät zum Treffpunkt (10€)", 
            "Unsportliches Verhalten (25€)",
            "Ausrüstung unvollständig (5€)", 
            "Gelbe Karte wegen Meckern (15€)", 
            "Kasten vergessen (15€)"
        ])
        f_status = st.radio("Zahlungsstatus bei Erfassung:", ["Offen", "Direkt Bar bezahlt"])
        
        if st.button("BETRAG RECHTSKRÄFTIG BUCHEN"):
            money_val = int(f_vergehen.split("(")[1].split("€")[0])
            st.session_state["strafen_db"].append({
                "Spieler": f_spieler,
                "Vergehen": f_vergehen.split(" (")[0],
                "Betrag (EUR)": money_val,
                "Status": f_status,
                "Datum": datetime.now().strftime("%d.%m.%Y - %H:%M")
            })
            st.success("Kassenbucheintrag erfolgreich verarbeitet.")
            st.rerun()
            
    with col_f2:
        st.markdown("#### 📊 Kassenstand & Offene Posten")
        if st.session_state["strafen_db"]:
            df_money = pd.DataFrame(st.session_state["strafen_db"])
            st.dataframe(df_money, use_container_width=True)
            
            sum_total = df_money["Betrag (EUR)"].sum()
            sum_offen = df_money[df_money["Status"] == "Offen"]["Betrag (EUR)"].sum()
            
            st.metric("Gesamtvolumen erfasster Strafen", f"{sum_total} €")
            st.metric("Davon ausstehend (Soll-Überschuss)", f"{sum_offen} €", delta=f"{sum_offen} € offen", delta_color="inverse")
        else:
            st.info("Kassenbuch weist aktuell keine Einträge auf.")
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# TAB 5: VISION STUDIO (IMAGE PROCESSING)
# ------------------------------------------
with tabs[4]:
    st.markdown('<div class="metric-container"><h3>👁️ Phoenix AI Core: Vision & Grid Processing Studio</h3>', unsafe_allow_html=True)
    st.write("Verarbeitung von Bilddaten zur Konturen- und Taktikanalyse mittels modularer OpenCV Filter-Pipelines.")
    
    uploaded_img = st.file_uploader("Taktikboard-Foto oder Screenshot einlesen...", type=["jpg", "png", "jpeg"], key="v_img")
    
    if uploaded_img is not None:
        raw_bytes = np.asarray(bytearray(uploaded_img.read()), dtype=np.uint8)
        cv_matrix = cv2.imdecode(raw_bytes, 1)
        
        st.markdown("---")
        st.markdown("#### 🛠️ Filter-Konfiguration für Bild-Prozessierung")
        
        col_cv_sel, col_cv_val = st.columns(2)
        with col_cv_sel:
            cv_filter = st.selectbox("Auszuführende Matrix-Operation:", ["Canny Edge Detection", "Binary Thresholding", "Invert Color Matrix", "Gaussian Blur"])
        with col_cv_val:
            p_val1 = st.slider("Parameter-Intensität 1:", 1, 255, 100)
            
        st.markdown("---")
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            st.image(uploaded_img, caption="Originaler Kamera-Input", use_container_width=True)
            
        with col_v2:
            with st.spinner("Prozessiere Matrixvariablen..."):
                gray_base = cv2.cvtColor(cv_matrix, cv2.COLOR_BGR2GRAY)
                
                if cv_filter == "Canny Edge Detection":
                    processed = cv2.Canny(gray_base, p_val1, p_val1 * 2)
                    st.image(processed, caption="Ergebnis: Canny Edge Matrix", use_container_width=True, channels="GRAY")
                elif cv_filter == "Binary Thresholding":
                    _, processed = cv2.threshold(gray_base, p_val1, 255, cv2.THRESH_BINARY)
                    st.image(processed, caption="Ergebnis: Binärer Schwellenwert", use_container_width=True, channels="GRAY")
                elif cv_filter == "Invert Color Matrix":
                    processed = cv2.bitwise_not(cv_matrix)
                    st.image(processed, caption="Ergebnis: Invertierter Farbraum", use_container_width=True)
                elif cv_filter == "Gaussian Blur":
                    kernel_sz = p_val1 if p_val1 % 2 != 0 else p_val1 + 1
                    processed = cv2.GaussianBlur(cv_matrix, (kernel_sz, kernel_sz), 0)
                    st.image(processed, caption="Ergebnis: Weichgezeichnete Matrix", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# TAB 6: ANALYTICS & xG ENGINE
# ------------------------------------------
with tabs[5]:
    st.markdown('<div class="metric-container"><h3>📊 Advanced Analytics & Match Probability Matrix</h3>', unsafe_allow_html=True)
    
    st.markdown("#### 📈 Momentum Tracker (Echtzeitverlauf)")
    st.line_chart(st.session_state["match_momentum"])
    
    st.markdown("---")
    st.markdown("#### 📐 Mathematischer Expected Goals (xG) Rechner")
    
    col_an1, col_an2 = st.columns(2)
    with col_an1:
        calc_dist = st.slider("Entfernung zum Tor (in Metern):", 1, 45, 15)
        calc_angle = st.slider("Schusswinkel (90 Grad = Absolut Zentral):", 10, 90, 75)
    with col_an2:
        calc_gk = st.selectbox("Torhüter-Positionierung:", ["Zentral blockierend", "Ermüdungserscheinung / In Bewegung", "Tor verwaist"])
        calc_press = st.selectbox("Verteidigungsdruck:", ["Keiner (Freier Raum)", "Mäßiger Körperkontakt", "Extremer Block (Zustellt)"])
        
    # Multi-Faktor xG Algorithmus
    base_xg = 0.98 if calc_dist < 4 else (1.8 / (calc_dist * 0.2))
    angle_mod = calc_angle / 90
    gk_mod = 1.0 if calc_gk == "Zentral blockierend" else (1.5 if calc_gk == "Ermüdungserscheinung / In Bewegung" else 2.8)
    press_mod = 1.0 if calc_press == "Keiner (Freier Raum)" else (0.40 if calc_press == "Mäßiger Körperkontakt" else 0.08)
    
    computed_xg = min(0.999, max(0.001, base_xg * angle_mod * gk_mod * press_mod))
    
    st.metric("Statistischer xG-Wert (Wahrscheinlichkeit)", f"{computed_xg:.4f}")
    if computed_xg > 0.65:
        st.success("🔥 KLASSISCHE GROSSCHANCE: Abschluss dringend empfohlen.")
    elif computed_xg > 0.30:
        st.warning("⚠️ RISK SHOT: Mittlere Erfolgswahrscheinlichkeit.")
    else:
        st.error("🛑 LOW PROBABILITY: Ein Zuspiel wäre taktisch sinnvoller gewesen.")
        
    st.markdown("---")
    st.markdown("#### 🔮 Monte-Carlo Saison-Punktrechner (Prognose)")
    st.write("Simuliere den Saisonverlauf basierend auf deiner aktuellen Siegwahrscheinlichkeit.")
    
    prob_win = st.slider("Durchschnittliche Siegwahrscheinlichkeit pro Match (%):", 10, 90, 50)
    remaining_games = st.number_input("Verbleibende Ligaspiele:", min_value=1, max_value=38, value=10)
    
    if st.button("SAISON-ENDSTAND PROGNOSTIZIEREN"):
        sim_points = []
        for _ in range(1000): # 1000 Simulationsdurchläufe
            run_pts = 0
            for _ in range(remaining_games):
                rand_val = np.random.randint(1, 101)
                if rand_val <= prob_win:
                    run_pts += 3
                elif rand_val <= prob_win + 20: # 20% Unentschieden-Chance
                    run_pts += 1
            sim_points.append(run_pts)
            
        mean_prediction = np.mean(sim_points)
        st.markdown(f"<h3 style='color:#ffcc00 !important;'>Erwartete Punkteausbeute: ca. {mean_prediction:.1f} Punkte aus {remaining_games} Spielen</h3>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# TAB 7: TRAINING ARCHITECT
# ------------------------------------------
with tabs[6]:
    st.markdown('<div class="metric-container"><h3>📋 Tactical Training Session Planner</h3>', unsafe_allow_html=True)
    
    col_tr1, col_tr2 = st.columns(2)
    with col_tr1:
        st.markdown("#### Übungsmodul hinzufügen")
        tr_title = st.text_input("Übungsname:", "Überzahl-Shuttle 3vs2", key="tr_t")
        tr_duration = st.number_input("Zeitaufwand (Minuten):", min_value=5, max_value=90, value=20, key="tr_d")
        tr_focus = st.selectbox("Fokus-Areal:", ["Taktik", "Technik", "Kondition", "Standardsituationen"], key="tr_f")
        tr_intensity = st.select_slider("Belastungsstufe:", options=["Niedrig", "Mittel", "Hoch", "Maximal-Limit"])
        
        if st.button("ÜBUNG IN TRAININGSPROTOKOLL REGISTER"):
            st.session_state["trainingsuebungen"].append({
                "Titel": tr_title, "Dauer": tr_duration, "Fokus": tr_focus, "Intensitaet": tr_intensity
            })
            st.success("Übung erfolgreich für die nächste Einheit eingeplant.")
            st.rerun()
            
    with col_tr2:
        st.markdown("#### 📋 Geplanter Ablauf")
        df_training = pd.DataFrame(st.session_state["trainingsuebungen"])
        st.dataframe(df_training, use_container_width=True)
        
        total_time = df_training["Dauer"].sum()
        st.metric("Gesamtdauer der Trainingseinheit", f"{total_time} Minuten")
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# TAB 8: NUTRITION & MATCHDAY HYDRATION COACH
# ------------------------------------------
with tabs[7]:
    st.markdown('<div class="metric-container"><h3>🍏 Nutrition & Matchday Hydration Coach</h3>', unsafe_allow_html=True)
    st.write("Kalkuliert den Flüssigkeits- und Kohlenhydratbedarf der Mannschaft am Spieltag basierend auf Umweltbedingungen und Spielminuten.")
    
    col_nut1, col_nut2 = st.columns(2)
    with col_nut1:
        weather_temp = st.slider("Außentemperatur am Spielort (°C):", 0, 40, 22)
        match_intensity = st.select_slider("Erwartete Spielintensität:", options=["Regenerativ", "Normal", "Sehr Hoch (Pressinggegner)"])
        individual_weight = st.number_input("Durchschnittliches Spielergewicht (kg):", min_value=50, max_value=110, value=75)
        
    with col_nut2:
        st.markdown("#### 📊 Berechnete Richtwerte pro Spieler:")
        
        # Hydration & Carb Calculation Algorithm
        base_fluid = 600 # ml pro Stunde Basis
        if weather_temp > 25: base_fluid += 300
        if match_intensity == "Sehr Hoch (Pressinggegner)": base_fluid += 200
        
        carb_need = 60 # Gramm pro Stunde Basis
        if match_intensity == "Sehr Hoch (Pressinggegner)": carb_need += 20
        
        st.subheader(f"💧 Wasser/Elektrolyte: {base_fluid} ml / Spielstunde")
        st.subheader(f"🍌 Kohlenhydrat-Bedarf: {carb_need} g / Spieltag-Zufuhr")
        st.info("Empfehlung: Zufuhr von schnellen Kohlenhydraten (Gele/Isotonische Getränke) ca. 35 Minuten vor Anpfiff und unmittelbar in der Halbzeitpause.")
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# TAB 9: EQUIPMENT & LOGISTICS MANAGER
# ------------------------------------------
with tabs[8]:
    st.markdown('<div class="metric-container"><h3>🎒 Equipment & Logistics Manager</h3>', unsafe_allow_html=True)
    st.write("Überwachung der mitzuführenden Teamausrüstung für Heim- und Auswärtsspiele, um Fehlbestände am Platz zu verhindern.")
    
    col_log1, col_log2 = st.columns(2)
    with col_log1:
        st.markdown("#### 🔄 Inventar-Status aktualisieren")
        log_item = st.selectbox("Gegenstand auswählen:", [x["Gegenstand"] for x in st.session_state["logistik_inventar"]])
        log_ist = st.number_input("Aktuell gezählte Menge (Ist):", min_value=0, max_value=100, value=15)
        
        if st.button("BESTAND IN DATENBANK SPEICHERN"):
            for idx, item in enumerate(st.session_state["logistik_inventar"]):
                if item["Gegenstand"] == log_item:
                    st.session_state["logistik_inventar"][idx]["Ist"] = log_ist
                    if log_ist >= item["Soll"]:
                        st.session_state["logistik_inventar"][idx]["Status"] = "Korrekt"
                    else:
                        st.session_state["logistik_inventar"][idx]["Status"] = "Fehlbestand"
            st.success("Logistikdaten erfolgreich aktualisiert.")
            st.rerun()
            
    with col_log2:
        st.markdown("#### 🎒 Aktuelle Packliste & Fehlbestände")
        df_logistik = pd.DataFrame(st.session_state["logistik_inventar"])
        
        # Custom coloring style override via data_editor or just display
        st.dataframe(df_logistik, use_container_width=True)
        
        missing_items = df_logistik[df_logistik["Status"] == "Fehlbestand"]
        if not missing_items.empty:
            st.error(f"🚨 WARNUNG: Unvollständiges Equipment am Platz! Folgende Gegenstände fehlen: {', '.join(missing_items['Gegenstand'].tolist())}")
        else:
            st.success("🟢 LOGISTIK CHECK ERFOLGREICH: Alle Ausrüstungsgegenstände vollzählig am Platz.")
    st.markdown('</div>', unsafe_allow_html=True)
