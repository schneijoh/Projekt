import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image, ImageDraw
import io
import time

# --- STREAMLIT CONFIG (Muss ganz oben stehen) ---
st.set_page_config(page_title="LBV Phoenix Command Center", page_icon="🦅", layout="wide")

# --- LADESCREEN (Zentraler Einstieg) ---
if "app_geladen" not in st.session_state:
    st.session_state["app_geladen"] = False

if not st.session_state["app_geladen"]:
    # Edles Phönix-Design für das Intro
    st.markdown("""
        <style>
        .loading-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 70vh;
            font-family: 'Arial', sans-serif;
            color: #002147;
        }
        .spinner {
            border: 8px solid #f4f6f9;
            border-top: 8px solid #cc0000;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            animation: spin 1s linear infinite;
            margin-bottom: 20px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        </style>
        <div class="loading-container">
            <div class="spinner"></div>
            <h1 style="font-size: 40px; letter-spacing: 2px;">LBV PHOENIX LUEBECK</h1>
            <p style="font-size: 18px; color: #555;">Command Center wird initialisiert...</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Künstliche kurze Verzögerung für den "App-Lade-Effekt"
    time.sleep(2.0)
    st.session_state["app_geladen"] = True
    st.rerun()

# --- HILFSFUNKTION FÜR UMLAUTE ---
def umlaute_ersetzen(text):
    if not isinstance(text, str):
        return text
    ersetzungen = {
        'ä': 'ae', 'ö': 'oe', 'ü': 'ue',
        'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue',
        'ß': 'ss'
    }
    for umlaut, ersetzung in ersetzungen.items():
        text = text.replace(umlaut, ersetzung)
    return text

# --- DESIGN & CSS NACH DEM LADEN ---
st.markdown("""
    <style>
    .main { background-color: #f4f6f9; }
    .stTabs [data-baseweb="tab"] { color: #002147; font-weight: bold; font-size: 16px; }
    .stTabs [aria-selected="true"] { color: #cc0000 !important; border-bottom-color: #cc0000 !important; }
    h1, h2, h3 { color: #002147; font-family: 'Arial', sans-serif; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 8px; border-left: 5px solid #002147; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSIONS STATE INITIALISIERUNG ---
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

# --- SIDEBAR: KADER ---
st.sidebar.title("🦅 LBV Phoenix Luebeck")
st.sidebar.caption("Hockey-Zentrale • Gegruendet 1903")
st.sidebar.markdown("---")

st.sidebar.markdown("### 👥 Kader-Schnellbearbeitung")
neuer_kader = st.sidebar.data_editor(
    st.session_state["kader_liste"],
    num_rows="dynamic",
    placeholder="Name eintippen...",
    use_container_width=True
)
st.session_state["kader_liste"] = [x for x in neuer_kader if x]
kader = st.session_state["kader_liste"]

if len(kader) < 11:
    st.error("⚠️ Mindestens 11 Spieler benoetigt (1 TW + 10 Feldspieler).")
    st.stop()

# --- HAUPTBEREICH ---
st.title("🏑 PHOENIX HOCKEY COMMAND CENTER")
st.write("Die All-in-One Verwaltung für Aufstellung, Social Media und Spielbetrieb.")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Aufstellung (Dynamisch)", 
    "📸 Kader-Grafik",
    "🎨 Weitere Grafiken",
    "📝 Live-Scout & Bericht",
    "💰 Kasse & Strafen"
])

# --- TAB 1: DYNAMISCHE AUFSTELLUNG ---
with tab1:
    st.subheader("Spielsystem & Aufstellung")
    formation = st.selectbox("Wähle das Spielsystem:", ["4-3-3", "3-4-3", "3-5-2", "2-4-4"])
    
    anzahl_def = int(formation.split("-")[0])
    anzahl_mid = int(formation.split("-")[1])
    anzahl_sturm = int(formation.split("-")[2])
    
    stamm_aufstellung = []
    c_tw, c_def, c_mid, c_sturm = st.columns(4)
    
    with c_tw:
        st.markdown("**🧤 Tor**")
        tw_val = st.selectbox("Torwart", kader, index=0)
        stamm_aufstellung.append(tw_val)
        
    with c_def:
        st.markdown(f"**🛡️ Abwehr ({anzahl_def})**")
        def_spieler = []
        for i in range(anzahl_def):
            val = st.selectbox(f"Verteidiger {i+1}", kader, index=min(1 + i, len(kader)-1), key=f"def_{i}")
            def_spieler.append(val)
            stamm_aufstellung.append(val)
            
    with c_mid:
        st.markdown(f"**🧠 Mittelfeld ({anzahl_mid})**")
        mid_spieler = []
        for i in range(anzahl_mid):
            val = st.selectbox(f"Mittelfeld {i+1}", kader, index=min(1 + anzahl_def + i, len(kader)-1), key=f"mid_{i}")
            mid_spieler.append(val)
            stamm_aufstellung.append(val)
            
    with c_sturm:
        st.markdown(f"**⚡ Sturm ({anzahl_sturm})**")
        sturm_spieler = []
        for i in range(anzahl_sturm):
            val = st.selectbox(f"Stürmer {i+1}", kader, index=min(1 + anzahl_def + anzahl_mid + i, len(kader)-1), key=f"sturm_{i}")
            sturm_spieler.append(val)
            stamm_aufstellung.append(val)

    moegliche_bank = [p for p in kader if p not in list(set(stamm_aufstellung))]
    
    st.write("---")
    st.markdown("### 🔄 Aktuelle Auswechselbank")
    if moegliche_bank:
        st.info(", ".join(moegliche_bank))
    else:
        st.caption("Keine Auswechselspieler verfügbar.")

# --- TAB 2: SOCIAL MEDIA EXPORT (KADER GRAFIK) ---
with tab2:
    st.subheader("📸 Startelf-Grafik für Instagram")
    gegner_media = st.text_input("Gegner:", "UHC Hamburg", key="gegner_tab2")
    design_typ = st.radio("Wähle dein Phönix Vereins-Design:", [
        "🔵 Falkenstraße Homefield (Blauer Kunstrasen!)", 
        "🔵⚪🔴 Phönix Matchday Classic (Dunkelblau dominant)", 
        "⚪🔵🔴 Phönix Clean White (Auswärts-Look)"
    ])
    
    if st.button("🚀 Kader-Grafik erstellen"):
        img = Image.new("RGB", (2160, 3840))
        draw = ImageDraw.Draw(img)
        
        if "Blauer Kunstrasen" in design_typ:
            bg, accent, text = "#004B87", "#cc0000", "#ffffff"
            draw.rectangle([0, 0, 2160, 3840], fill=bg)
            draw.rectangle([100, 100, 2060, 3740], outline="#ffffff", width=16)
            draw.line([100, 1920, 2060, 1920], fill="#ffffff", width=12)
            draw.arc([680, 100, 1480, 700], start=0, end=180, fill="#ffffff", width=12)
        elif "Classic" in design_typ:
            bg, accent, text = "#001530", "#cc0000", "#ffffff"
            draw.rectangle([0, 0, 2160, 3840], fill=bg)
            draw.rectangle([0, 0, 2160, 520], fill=accent)
        else:
            bg, accent, text = "#ffffff", "#002147", "#002147"
            draw.rectangle([0, 0, 2160, 3840], fill=bg)
            draw.rectangle([80, 80, 2080, 3760], outline=accent, width=16)

        box_fill = "#000e21" if "Clean White" not in design_typ else "#f4f6f9"
        box_outline = "#cc0000" if "Clean White" not in design_typ else "#002147"
        
        for y_box in [1000, 1440, 1880, 2320, 2920]:
            draw.rectangle([150, y_box, 2010, y_box+280], fill=box_fill, outline=box_outline, width=4)

        header_top = umlaute_ersetzen("LBV PHOENIX LUEBECK")
        header_sub = umlaute_ersetzen(f"STARTING XI vs {gegner_media}")
        system_str = umlaute_ersetzen(f"System: {formation}")
        
        tw_str = umlaute_ersetzen(f"🧤 TW:  {tw_val}")
        def_str = umlaute_ersetzen(f"🛡️ DEF:  {'  •  '.join(def_spieler)}")
        mid_str = umlaute_ersetzen(f"🧠 MID:  {'  •  '.join(mid_spieler)}")
        sturm_str = umlaute_ersetzen(f"⚡ STURM:  {'  •  '.join(sturm_spieler)}")
        
        bank_raw = ", ".join(moegliche_bank) if moegliche_bank else "Keine"
        bank_str = umlaute_ersetzen(f"🔄 BANK:  {bank_raw}")

        draw.text((1080, 260), header_top, fill="#ffffff" if "Clean White" not in design_typ else "#002147", anchor="mm", font_size=116)
        draw.text((1080, 640), header_sub, fill=accent if "Classic" not in design_typ else "#ffcc00", anchor="mm", font_size=92)
        draw.text((1080, 780), system_str, fill=text, anchor="mm", font_size=64)
        
        draw.text((1080, 1140), tw_str, fill=text, anchor="mm", font_size=78)
        draw.text((1080, 1580), def_str, fill=text, anchor="mm", font_size=74)
        draw.text((1080, 2020), mid_str, fill=text, anchor="mm", font_size=74)
        draw.text((1080, 2460), sturm_str, fill=text, anchor="mm", font_size=74)
        draw.text((1080, 3060), bank_str, fill=text, anchor="mm", font_size=70)
        
        draw.text((1080, 3640), "ADLER FLIEGEN HOCH • SEIT 1903", fill="#aaaaaa", anchor="mm", font_size=52)
        
        st.image(img, width=350)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.download_button(label="📥 Kader-Story herunterladen", data=buf.getvalue(), file_name="phoenix_kader.png", mime="image/png", type="primary")

# --- TAB 3: WEITERE GRAFIKEN (MAXIMAL ERWEITERT AUF 8 TYPEN) ---
with tab3:
    st.subheader("🎨 Weitere nützliche Grafiken erstellen")
    st.write("Wähle das passende Event-Format. Alle Grafiken werden hochauflösend (4K UHD) ausgegeben.")
    
    # Riesige Auswahl an Grafiktypen
    g_type = st.selectbox("Welche Grafik brauchst du?", [
        "Match-Ankündigung (Plakat)", 
        "Halbzeitstand-Post", 
        "Endergebnis-Post", 
        "Spieler des Tages (MVP)",
        "Mannschaftskasse / Strafen-Summary",
        "Absage / Spielverlegung", 
        "Sponsoring / Danke-Post",
        "Freitext-Info-Post (z.B. Event/Party)"
    ])
    
    # Basisdaten-Felder
    c_g1, c_g2 = st.columns(2)
    with c_g1:
        gegner_g = st.text_input("Gegner:", "UHC Hamburg", key="gegner_tab3_new") if g_type in ["Match-Ankündigung (Plakat)", "Halbzeitstand-Post", "Endergebnis-Post", "Absage / Spielverlegung"] else ""
        ort_g = st.text_input("Spielort / Location:", "Falkenstrasse (Blau)", key="ort_tab3") if g_type != "Mannschaftskasse / Strafen-Summary" else ""
    with c_g2:
        datum_g = st.text_input("Datum:", datetime.now().strftime("%d.%m.%Y"), key="datum_tab3") if g_type != "Mannschaftskasse / Strafen-Summary" else ""
        zeit_g = st.text_input("Uhrzeit / Frist:", "14:00 Uhr", key="zeit_tab3") if g_type != "Mannschaftskasse / Strafen-Summary" else ""
        
    # Dynamische Variablen initialisieren
    tore_p, tore_g = 0, 0
    freitext_titel = ""
    freitext_inhalt = ""
    info_g = ""
    mvp_spieler = ""
    mvp_begruendung = ""
    
    # Spezifische Inputs je nach Auswahl
    if g_type in ["Endergebnis-Post", "Halbzeitstand-Post"]:
        c_e1, c_e2 = st.columns(2)
        with c_e1: tore_p = st.number_input("Tore Phönix:", value=st.session_state["tore_phönix"], min_value=0, step=1)
        with c_e2: tore_g = st.number_input("Tore Gegner:", value=st.session_state["tore_gegner"], min_value=0, step=1)
    
    if g_type == "Match-Ankündigung (Plakat)":
        info_g = st.text_input("Zusatz-Info (z.B. 'Topspiel', 'Eintritt frei'):", "Heimspiel", key="info_tab3")
    elif g_type == "Absage / Spielverlegung":
        info_g = st.text_input("Grund / Info (z.B. 'Nachholtermin folgt'):", "Spiel faellt witterungsbedingt aus!", key="absage_tab3")
    elif g_type == "Spieler des Tages (MVP)":
        mvp_spieler = st.selectbox("Wähle den MVP:", kader)
        mvp_begruendung = st.text_input("Kurze Begründung (z.B. '3 Tore & Traum-Performance'):", "Starke Parade in der Schlussminute!")
    elif g_type == "Sponsoring / Danke-Post":
        freitext_inhalt = st.text_area("Danksagungstext:", "Vielen Dank an alle Zuschauer und Sponsoren fuer den sensationellen Support am Spielfeldrand!")
    elif g_type == "Freitext-Info-Post (z.B. Event/Party)":
        freitext_titel = st.text_input("Überschrift des Posts:", "MANNSCHAFTSABEND")
        freitext_inhalt = st.text_area("Inhalt / Beschreibung:", "Kommt alle vorbei! Fuer kalte Getraenke und Grillgut ist gesorgt. Start nach dem Training.")

    if st.button("🚀 Grafik jetzt generieren"):
        # 4K UHD QUALITÄT (2160 x 3840)
        img_g = Image.new("RGB", (2160, 3840), color="#002147")
        draw_g = ImageDraw.Draw(img_g)
        
        # Gebrandeter Vereins-Rahmen
        draw_g.rectangle([80, 80, 2080, 3760], outline="#ffffff", width=12)
        draw_g.rectangle([80, 80, 2080, 480], fill="#cc0000")
        
        club_title = umlaute_ersetzen("LBV PHOENIX LUEBECK")
        draw_g.text((1080, 280), club_title, fill="#ffffff", anchor="mm", font_size=110)
        
        # Clean-Strings vorbereiten
        gegner_clean = umlaute_ersetzen(gegner_g)
        ort_clean = umlaute_ersetzen(ort_g)
        datum_clean = umlaute_ersetzen(datum_g)
        zeit_clean = umlaute_ersetzen(zeit_g)
        info_clean = umlaute_ersetzen(info_g)

        # --- 1. MATCH ANKÜNDIGUNG ---
        if g_type == "Match-Ankündigung (Plakat)":
            draw_g.text((1080, 1100), "NAECHSTES SPIEL", fill="#ffcc00", anchor="mm", font_size=140)
            draw_g.rectangle([250, 1350, 1910, 2050], fill="#001124", outline="#ffffff", width=6)
            draw_g.text((1080, 1530), "LBV PHOENIX", fill="#ffffff", anchor="mm", font_size=96)
            draw_g.text((1080, 1720), "VS", fill="#cc0000", anchor="mm", font_size=70)
            draw_g.text((1080, 1890), gegner_clean, fill="#ffffff", anchor="mm", font_size=96)
            
            draw_g.rectangle([250, 2250, 1910, 2900], fill="#001a3a", outline="#ffcc00", width=4)
            draw_g.text((1080, 2370), f"PLATZ:  {ort_clean}", fill="#ffffff", anchor="mm", font_size=76)
            draw_g.text((1080, 2520), f"DATUM:  {datum_clean}", fill="#ffffff", anchor="mm", font_size=76)
            draw_g.text((1080, 2670), f"ANPFIFF:  {zeit_clean}", fill="#ffffff", anchor="mm", font_size=76)
            if info_clean:
                draw_g.rectangle([350, 3100, 1810, 3280], fill="#cc0000")
                draw_g.text((1080, 3190), info_clean.upper(), fill="#ffffff", anchor="mm", font_size=72)
            
        # --- 2. HALBZEITSTAND ---
        elif g_type == "Halbzeitstand-Post":
            draw_g.text((1080, 1100), "HALBZEITSTAND", fill="#ffcc00", anchor="mm", font_size=140)
            draw_g.rectangle([250, 1350, 1910, 2250], fill="#001124", outline="#ffffff", width=8)
            draw_g.text((1080, 1510), "LBV Phoenix", fill="#ffffff", anchor="mm", font_size=86)
            draw_g.text((1080, 1790), f"{int(tore_p)} : {int(tore_g)}", fill="#ffffff", anchor="mm", font_size=210)
            draw_g.text((1080, 2070), gegner_clean, fill="#ffffff", anchor="mm", font_size=86)
            draw_g.text((1080, 2500), "Gleich geht's weiter!", fill="#ffffff", anchor="mm", font_size=76)

        # --- 3. ENDERGEBNIS ---
        elif g_type == "Endergebnis-Post":
            draw_g.text((1080, 1100), "ENDERGEBNIS", fill="#ffcc00", anchor="mm", font_size=140)
            draw_g.rectangle([250, 1350, 1910, 2250], fill="#001124", outline="#cc0000", width=8)
            draw_g.text((1080, 1510), "LBV Phoenix", fill="#ffffff", anchor="mm", font_size=86)
            draw_g.text((1080, 1790), f"{int(tore_p)} : {int(tore_g)}", fill="#ffffff", anchor="mm", font_size=210)
            draw_g.text((1080, 2070), gegner_clean, fill="#ffffff", anchor="mm", font_size=86)
            
            if st.session_state["spielbericht_events"]:
                draw_g.rectangle([250, 2450, 1910, 3150], fill="#001a3a", outline="#ffffff", width=3)
                draw_g.text((1080, 2540), "MATCH HIGHLIGHTS", fill="#ffcc00", anchor="mm", font_size=68)
                y_offset = 2660
                for ev in st.session_state["spielbericht_events"][:5]:
                    draw_g.text((1080, y_offset), umlaute_ersetzen(ev), fill="#ffffff", anchor="mm", font_size=58)
                    y_offset += 90

        # --- 4. SPIELER DES TAGES (MVP) ---
        elif g_type == "Spieler des Tages (MVP)":
            draw_g.text((1080, 1100), "SPIELER DES TAGES", fill="#ffcc00", anchor="mm", font_size=130)
            draw_g.text((1080, 1220), "🔥 MVP 🔥", fill="#ffffff", anchor="mm", font_size=80)
            
            draw_g.rectangle([200, 1450, 1960, 1950], fill="#cc0000", outline="#ffffff", width=6)
            draw_g.text((1080, 1700), umlaute_ersetzen(mvp_spieler).upper(), fill="#ffffff", anchor="mm", font_size=110)
            
            draw_g.rectangle([200, 2150, 1960, 2650], fill="#001124", outline="#ffcc00", width=4)
            draw_g.text((1080, 2400), umlaute_ersetzen(mvp_begruendung), fill="#ffffff", anchor="mm", font_size=60)
            draw_g.text((1080, 2900), f"Match vom {datum_clean}", fill="#aaaaaa", anchor="mm", font_size=56)

        # --- 5. MANNSCHAFTSKASSE SUMMARY ---
        elif g_type == "Mannschaftskasse / Strafen-Summary":
            draw_g.text((1080, 1050), "MANNSCHAFTSKASSE", fill="#ffcc00", anchor="mm", font_size=130)
            draw_g.text((1080, 1180), "OFFENE STRAFEN & KASSENSTAND", fill="#ffffff", anchor="mm", font_size=64)
            
            # Kassenstand holen
            gesamt = sum(item['Betrag'] for item in st.session_state["strafen"]) if st.session_state["strafen"] else 0
            
            draw_g.rectangle([350, 1350, 1710, 1650], fill="#001124", outline="#cc0000", width=6)
            draw_g.text((1080, 1500), f"AKTEULLER STAND: {gesamt} EUR", fill="#ffffff", anchor="mm", font_size=86)
            
            # Die letzten Einträge auflisten
            draw_g.rectangle([200, 1800, 1960, 3100], fill="#001a3a", outline="#ffffff", width=4)
            draw_g.text((1080, 1900), "LETZTE BUCHUNGEN:", fill="#ffcc00", anchor="mm", font_size=64)
            
            if st.session_state["strafen"]:
                y_s = 2050
                for s in st.session_state["strafen"][-8:]: # Letzten 8 anzeigen
                    s_line = f"{s['Spieler']} - {s['Grund']} ({s['Datum']})"
                    draw_g.text((1080, y_s), umlaute_ersetzen(s_line), fill="#ffffff", anchor="mm", font_size=54)
                    y_s += 110
            else:
                draw_g.text((1080, 2400), "Keine offenen Strafen registriert!", fill="#aaaaaa", anchor="mm", font_size=58)

        # --- 6. ABSAGE / SPIELVERLEGUNG ---
        elif g_type == "Absage / Spielverlegung":
            draw_g.text((1080, 1100), "SPIELABSAGE", fill="#cc0000", anchor="mm", font_size=140)
            draw_g.rectangle([250, 1350, 1910, 1850], fill="#001124", outline="#ffffff", width=6)
            draw_g.text((1080, 1500), "LBV Phoenix", fill="#ffffff", anchor="mm", font_size=86)
            draw_g.text((1080, 1680), f"vs  {gegner_clean}", fill="#ffffff", anchor="mm", font_size=86)
            
            draw_g.rectangle([250, 2050, 1910, 2650], fill="#cc0000", outline="#ffffff", width=4)
            draw_g.text((1080, 2350), info_clean.upper(), fill="#ffffff", anchor="mm", font_size=70)

        # --- 7. SPONSORING & DANKE ---
        elif g_type == "Sponsoring / Danke-Post":
            draw_g.text((1080, 1100), "VIELEN DANK", fill="#ffcc00", anchor="mm", font_size=140)
            draw_g.rectangle([200, 1350, 1960, 2500], fill="#001a3a", outline="#ffffff", width=6)
            
            lines = umlaute_ersetzen(freitext_inhalt).split("\n")
            y_o = 1600
            for l in lines:
                draw_g.text((1080, y_o), l, fill="#ffffff", anchor="mm", font_size=64)
                y_o += 120

        # --- 8. FREITEXT INFOPPOST ---
        elif g_type == "Freitext-Info-Post (z.B. Event/Party)":
            titel_clean = umlaute_ersetzen(freitext_titel).upper()
            inhalt_clean = umlaute_ersetzen(freitext_inhalt)
            
            draw_g.text((1080, 1000), titel_clean, fill="#ffcc00", anchor="mm", font_size=120)
            draw_g.rectangle([200, 1200, 1960, 2600], fill="#001a3a", outline="#ffffff", width=6)
            
            lines = inhalt_clean.split("\n")
            y_text_offset = 1400
            for line in lines:
                draw_g.text((1080, y_text_offset), line, fill="#ffffff", anchor="mm", font_size=64)
                y_text_offset += 110
                
            draw_g.text((1080, 2800), f"WANN: {datum_clean} um {zeit_clean}", fill="#ffffff", anchor="mm", font_size=70)
            draw_g.text((1080, 2950), f"WO: {ort_clean}", fill="#ffffff", anchor="mm", font_size=70)

        # Footer
        draw_g.text((1080, 3520), "🦅 NUR DER LBV!", fill="#ffffff", anchor="mm", font_size=85)
        
        st.image(img_g, width=350)
        buf_g = io.BytesIO()
        img_g.save(buf_g, format="PNG")
        st.download_button(label="📥 Diese Grafik herunterladen", data=buf_g.getvalue(), file_name=f"phoenix_{g_type.lower().replace(' ', '_')}.png", mime="image/png", type="primary")

# --- TAB 4: LIVE SCOUT & REPORT ---
with tab4:
    st.subheader("📝 Live-Match-Scout & Bericht-Generator")
    sc1, sc2 = st.columns(2)
    with sc1:
        st.markdown("### 📊 Aktueller Spielstand")
        c_p, c_g = st.columns(2)
        with c_p:
            if st.button("⚽ Tor für Phönix"): st.session_state["tore_phönix"] += 1
        with c_g:
            if st.button("❌ Tor für Gegner"): st.session_state["tore_gegner"] += 1
        st.metric("Spielstand", f"LBV Phönix {st.session_state['tore_phönix']} : {st.session_state['tore_gegner']} {gegner_media}")
        if st.button("🔄 Spielstand resetten"):
            st.session_state["tore_phönix"], st.session_state["tore_gegner"], st.session_state["spielbericht_events"] = 0, 0, []
            st.rerun()
    with sc2:
        st.markdown("### 🎙️ Event Ticker")
        event_spieler = st.selectbox("Spieler:", kader, key="scout_sp")
        event_typ = st.selectbox("Event:", ["Tor erzielt", "Ecke verwandelt", "Grüne Karte", "Gelbe Karte"])
        if st.button("Event speichern"):
            st.session_state["spielbericht_events"].append(f"• {event_spieler} ({event_typ})")
            st.success("Event geloggt!")
            st.rerun()

    bericht_text = f"🏑 MATCH-REPORT - LBV PHÖNIX LÜBECK\n" \
                   f"Ergebnis: LBV Phönix {st.session_state['tore_phönix']} : {st.session_state['tore_gegner']} {gegner_media}\n" \
                   f"-----------------------------------------\n" + "\n".join(st.session_state["spielbericht_events"]) + \
                   f"\n-----------------------------------------\n🦅 Nur der LBV!"
    st.text_area("WhatsApp-Bericht kopieren:", bericht_text, height=150)

# --- TAB 5: MANNSCHAFTSKASSE ---
with tab5:
    st.subheader("💰 Phönix Mannschaftskasse")
    s_col1, s_col2, s_col3 = st.columns([2, 2, 1])
    with s_col1: s_spieler = st.selectbox("Spieler", kader, key="money_sp")
    with s_col2: grund = st.selectbox("Vergehen", ["Zu spät (5€)", "Grüne Karte (2€)", "Gelbe Karte (5€)", "Kasten vergessen (10€)"])
    with s_col3:
        if st.button("Buchen"):
            betrag = grund.split("(")[1].split("€")[0]
            st.session_state["strafen"].append({"Spieler": s_spieler, "Grund": grund, "Betrag": int(betrag), "Datum": datetime.now().strftime("%d.%m.%y")})
    if st.session_state["strafen"]:
        st.table(pd.DataFrame(st.session_state["strafen"]))
        st.metric("Kassenstand aktuell", f"{pd.DataFrame(st.session_state['strafen'])['Betrag'].sum()} €")
