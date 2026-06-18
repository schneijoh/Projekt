import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image, ImageDraw
import io
import time

# --- STREAMLIT CONFIG (Muss ganz oben stehen) ---
st.set_page_config(page_title="LBV Phoenix CC", page_icon="🦅", layout="centered")

# --- LADESCREEN (Zentraler Einstieg) ---
if "app_geladen" not in st.session_state:
    st.session_state["app_geladen"] = False

if not st.session_state["app_geladen"]:
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
            text-align: center;
            padding: 20px;
        }
        .spinner {
            border: 6px solid #f4f6f9;
            border-top: 6px solid #cc0000;
            border-radius: 50%;
            width: 50px;
            height: 50px;
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
            <h1 style="font-size: 32px; letter-spacing: 1px;">LBV PHOENIX</h1>
            <p style="font-size: 16px; color: #555;">Mobile Command Center wird geladen...</p>
        </div>
    """, unsafe_allow_html=True)
    
    time.sleep(1.8)
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

# --- DESIGN & CSS FÜR HANDYFORMAT ---
st.markdown("""
    <style>
    .main { background-color: #f4f6f9; }
    /* Tabs für Daumenbedienung optimieren */
    .stTabs [data-baseweb="tab"] { 
        color: #002147; 
        font-weight: bold; 
        font-size: 14px; 
        padding: 8px 12px;
    }
    .stTabs [aria-selected="true"] { color: #cc0000 !important; border-bottom-color: #cc0000 !important; }
    h1 { color: #002147; font-family: 'Arial', sans-serif; font-size: 26px !important; text-align: center; }
    h2, h3 { color: #002147; font-family: 'Arial', sans-serif; font-size: 20px !important; }
    .stMetric { background-color: #ffffff; padding: 10px; border-radius: 8px; border-left: 5px solid #002147; }
    /* Buttons auf dem Handy vollflächig machen */
    div.stButton > button:first-child {
        width: 100%;
    }
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

# --- KADER-BEREICH OBEN ANHEFTEN FÜR MOBIL ---
with st.expander("👥 Kader bearbeiten (Ausklappbar)", expanded=False):
    neuer_kader = st.data_editor(
        st.session_state["kader_liste"],
        num_rows="dynamic",
        placeholder="Name...",
        use_container_width=True
    )
    st.session_state["kader_liste"] = [x for x in neuer_kader if x]
kader = st.session_state["kader_liste"]

if len(kader) < 11:
    st.error("⚠️ Mindestens 11 Spieler benoetigt.")
    st.stop()

# --- HAUPTBEREICH ---
st.title("🦅 PHOENIX COMMAND CENTER")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Aufstellung", 
    "📸 Aufst.-Grafik",
    "🎨 Mehr Grafiken",
    "📝 Ticker",
    "💰 Kasse"
])

# --- TAB 1: DYNAMISCHE AUFSTELLUNG ---
with tab1:
    st.subheader("Spielsystem & Aufstellung")
    formation = st.selectbox("Spielsystem:", ["4-3-3", "3-4-3", "3-5-2", "2-4-4"])
    
    anzahl_def = int(formation.split("-")[0])
    anzahl_mid = int(formation.split("-")[1])
    anzahl_sturm = int(formation.split("-")[2])
    
    stamm_aufstellung = []
    
    st.markdown("**🧤 Tor**")
    tw_val = st.selectbox("Torwart", kader, index=0, key="tw_mob")
    stamm_aufstellung.append(tw_val)
        
    st.markdown(f"**🛡️ Abwehr ({anzahl_def})**")
    def_spieler = []
    for i in range(anzahl_def):
        val = st.selectbox(f"Verteidiger {i+1}", kader, index=min(1 + i, len(kader)-1), key=f"def_m_{i}")
        def_spieler.append(val)
        stamm_aufstellung.append(val)
            
    st.markdown(f"**🧠 Mittelfeld ({anzahl_mid})**")
    mid_spieler = []
    for i in range(anzahl_mid):
        val = st.selectbox(f"Mittelfeld {i+1}", kader, index=min(1 + anzahl_def + i, len(kader)-1), key=f"mid_m_{i}")
        mid_spieler.append(val)
        stamm_aufstellung.append(val)
            
    st.markdown(f"**⚡ Sturm ({anzahl_sturm})**")
    sturm_spieler = []
    for i in range(anzahl_sturm):
        val = st.selectbox(f"Stürmer {i+1}", kader, index=min(1 + anzahl_def + anzahl_mid + i, len(kader)-1), key=f"sturm_m_{i}")
        sturm_spieler.append(val)
        stamm_aufstellung.append(val)

    moegliche_bank = [p for p in kader if p not in list(set(stamm_aufstellung))]
    
    st.write("---")
    st.markdown("### 🔄 Auswechselbank")
    if moegliche_bank:
        st.info(", ".join(moegliche_bank))
    else:
        st.caption("Keine Auswechselspieler.")

# --- TAB 2: KADER GRAFIK ---
with tab2:
    st.subheader("📸 Startelf-Story exportieren")
    gegner_media = st.text_input("Gegner:", "UHC Hamburg", key="gegner_tab2")
    design_typ = st.radio("Design:", [
        "🔵 Falkenstraße Homefield (Blau)", 
        "🔵⚪🔴 Phönix Matchday Classic", 
        "⚪🔵🔴 Phönix Clean White"
    ])
    
    if st.button("🚀 Aufstellungs-Grafik laden"):
        img = Image.new("RGB", (2160, 3840))
        draw = ImageDraw.Draw(img)
        
        if "Homefield" in design_typ:
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
        bank_str = umlaute_ersetzen(f"🔄 BANK:  {', '.join(moegliche_bank) if moegliche_bank else 'Keine'}")

        draw.text((1080, 260), header_top, fill="#ffffff" if "Clean White" not in design_typ else "#002147", anchor="mm", font_size=116)
        draw.text((1080, 640), header_sub, fill=accent if "Classic" not in design_typ else "#ffcc00", anchor="mm", font_size=92)
        draw.text((1080, 780), system_str, fill=text, anchor="mm", font_size=64)
        draw.text((1080, 1140), tw_str, fill=text, anchor="mm", font_size=78)
        draw.text((1080, 1580), def_str, fill=text, anchor="mm", font_size=74)
        draw.text((1080, 2020), mid_str, fill=text, anchor="mm", font_size=74)
        draw.text((1080, 2460), sturm_str, fill=text, anchor="mm", font_size=74)
        draw.text((1080, 3060), bank_str, fill=text, anchor="mm", font_size=70)
        draw.text((1080, 3640), "ADLER FLIEGEN HOCH • SEIT 1903", fill="#aaaaaa", anchor="mm", font_size=52)
        
        st.image(img, width=280)  # Perfekte Breite für Mobile Webview
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.download_button(label="📥 Bild speichern", data=buf.getvalue(), file_name="phoenix_kader.png", mime="image/png", type="primary")

# --- TAB 3: WEITERE GRAFIKEN ---
with tab3:
    st.subheader("🎨 Content Generator")
    g_type = st.selectbox("Format wählen:", [
        "Match-Ankündigung (Plakat)", 
        "Halbzeitstand-Post", 
        "Endergebnis-Post", 
        "Spieler des Tages (MVP)",
        "Mannschaftskasse / Strafen-Summary",
        "Absage / Spielverlegung", 
        "Sponsoring / Danke-Post",
        "Freitext-Info-Post (z.B. Event/Party)"
    ])
    
    gegner_g = st.text_input("Gegner:", "UHC Hamburg", key="gegner_tab3_m") if g_type in ["Match-Ankündigung (Plakat)", "Halbzeitstand-Post", "Endergebnis-Post", "Absage / Spielverlegung"] else ""
    ort_g = st.text_input("Ort:", "Falkenstrasse (Blau)", key="ort_tab3_m") if g_type != "Mannschaftskasse / Strafen-Summary" else ""
    datum_g = st.text_input("Datum:", datetime.now().strftime("%d.%m.%Y"), key="datum_tab3_m") if g_type != "Mannschaftskasse / Strafen-Summary" else ""
    zeit_g = st.text_input("Uhrzeit:", "14:00 Uhr", key="zeit_tab3_m") if g_type != "Mannschaftskasse / Strafen-Summary" else ""
        
    tore_p, tore_g = 0, 0
    freitext_titel, freitext_inhalt, info_g, mvp_spieler, mvp_begruendung = "", "", "", "", ""
    
    if g_type in ["Endergebnis-Post", "Halbzeitstand-Post"]:
        tore_p = st.number_input("Tore Phoenix:", value=st.session_state["tore_phönix"], min_value=0, step=1)
        tore_g = st.number_input("Tore Gegner:", value=st.session_state["tore_gegner"], min_value=0, step=1)
    
    if g_type == "Match-Ankündigung (Plakat)":
        info_g = st.text_input("Info:", "Heimspiel")
    elif g_type == "Absage / Spielverlegung":
        info_g = st.text_input("Grund:", "Spiel faellt aus!")
    elif g_type == "Spieler des Tages (MVP)":
        mvp_spieler = st.selectbox("MVP:", kader)
        mvp_begruendung = st.text_input("Grund:", "Starke Leistung!")
    elif g_type == "Sponsoring / Danke-Post":
        freitext_inhalt = st.text_area("Text:", "Vielen Dank an alle Zuschauer!")
    elif g_type == "Freitext-Info-Post (z.B. Event/Party)":
        freitext_titel = st.text_input("Titel:", "MANNSCHAFTSABEND")
        freitext_inhalt = st.text_area("Beschreibung:", "Kommt alle vorbei!")

    if st.button("🚀 Grafik erstellen"):
        img_g = Image.new("RGB", (2160, 3840), color="#002147")
        draw_g = ImageDraw.Draw(img_g)
        draw_g.rectangle([80, 80, 2080, 3760], outline="#ffffff", width=12)
        draw_g.rectangle([80, 80, 2080, 480], fill="#cc0000")
        
        club_title = umlaute_ersetzen("LBV PHOENIX LUEBECK")
        draw_g.text((1080, 280), club_title, fill="#ffffff", anchor="mm", font_size=110)
        
        gegner_clean = umlaute_ersetzen(gegner_g)
        ort_clean = umlaute_ersetzen(ort_g)
        datum_clean = umlaute_ersetzen(datum_g)
        zeit_clean = umlaute_ersetzen(zeit_g)
        info_clean = umlaute_ersetzen(info_g)

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
            
        elif g_type == "Halbzeitstand-Post":
            draw_g.text((1080, 1100), "HALBZEITSTAND", fill="#ffcc00", anchor="mm", font_size=140)
            draw_g.rectangle([250, 1350, 1910, 2250], fill="#001124", outline="#ffffff", width=8)
            draw_g.text((1080, 1510), "LBV Phoenix", fill="#ffffff", anchor="mm", font_size=86)
            draw_g.text((1080, 1790), f"{int(tore_p)} : {int(tore_g)}", fill="#ffffff", anchor="mm", font_size=210)
            draw_g.text((1080, 2070), gegner_clean, fill="#ffffff", anchor="mm", font_size=86)

        elif g_type == "Endergebnis-Post":
            draw_g.text((1080, 1100), "ENDERGEBNIS", fill="#ffcc00", anchor="mm", font_size=140)
            draw_g.rectangle([250, 1350, 1910, 2250], fill="#001124", outline="#cc0000", width=8)
            draw_g.text((1080, 1510), "LBV Phoenix", fill="#ffffff", anchor="mm", font_size=86)
            draw_g.text((1080, 1790), f"{int(tore_p)} : {int(tore_g)}", fill="#ffffff", anchor="mm", font_size=210)
            draw_g.text((1080, 2070), gegner_clean, fill="#ffffff", anchor="mm", font_size=86)
            if st.session_state["spielbericht_events"]:
                draw_g.rectangle([250, 2450, 1910, 3150], fill="#001a3a", outline="#ffffff", width=3)
                y_offset = 2660
                for ev in st.session_state["spielbericht_events"][:5]:
                    draw_g.text((1080, y_offset), umlaute_ersetzen(ev), fill="#ffffff", anchor="mm", font_size=58)
                    y_offset += 90

        elif g_type == "Spieler des Tages (MVP)":
            draw_g.text((1080, 1100), "SPIELER DES TAGES", fill="#ffcc00", anchor="mm", font_size=130)
            draw_g.rectangle([200, 1450, 1960, 1950], fill="#cc0000", outline="#ffffff", width=6)
            draw_g.text((1080, 1700), umlaute_ersetzen(mvp_spieler).upper(), fill="#ffffff", anchor="mm", font_size=110)
            draw_g.rectangle([200, 2150, 1960, 2650], fill="#001124", outline="#ffcc00", width=4)
            draw_g.text((1080, 2400), umlaute_ersetzen(mvp_begruendung), fill="#ffffff", anchor="mm", font_size=60)

        elif g_type == "Mannschaftskasse / Strafen-Summary":
            draw_g.text((1080, 1050), "MANNSCHAFTSKASSE", fill="#ffcc00", anchor="mm", font_size=130)
            gesamt = sum(item['Betrag'] for item in st.session_state["strafen"]) if st.session_state["strafen"] else 0
            draw_g.rectangle([350, 1350, 1710, 1650], fill="#001124", outline="#cc0000", width=6)
            draw_g.text((1080, 1500), f"STAND: {gesamt} EUR", fill="#ffffff", anchor="mm", font_size=86)
            draw_g.rectangle([200, 1800, 1960, 3100], fill="#001a3a", outline="#ffffff", width=4)
            if st.session_state["strafen"]:
                y_s = 2050
                for s in st.session_state["strafen"][-8:]:
                    s_line = f"{s['Spieler']} - {s['Grund']} ({s['Datum']})"
                    draw_g.text((1080, y_s), umlaute_ersetzen(s_line), fill="#ffffff", anchor="mm", font_size=54)
                    y_s += 110

        elif g_type == "Absage / Spielverlegung":
            draw_g.text((1080, 1100), "SPIELABSAGE", fill="#cc0000", anchor="mm", font_size=140)
            draw_g.rectangle([250, 1350, 1910, 1850], fill="#001124", outline="#ffffff", width=6)
            draw_g.text((1080, 1500), "LBV Phoenix", fill="#ffffff", anchor="mm", font_size=86)
            draw_g.text((1080, 1680), f"vs  {gegner_clean}", fill="#ffffff", anchor="mm", font_size=86)
            draw_g.rectangle([250, 2050, 1910, 2650], fill="#cc0000", outline="#ffffff", width=4)
            draw_g.text((1080, 2350), info_clean.upper(), fill="#ffffff", anchor="mm", font_size=70)

        elif g_type == "Sponsoring / Danke-Post":
            draw_g.text((1080, 1100), "VIELEN DANK", fill="#ffcc00", anchor="mm", font_size=140)
            draw_g.rectangle([200, 1350, 1960, 2500], fill="#001a3a", outline="#ffffff", width=6)
            lines = umlaute_ersetzen(freitext_inhalt).split("\n")
            y_o = 1600
            for l in lines:
                draw_g.text((1080, y_o), l, fill="#ffffff", anchor="mm", font_size=64)
                y_o += 120

        elif g_type == "Freitext-Info-Post (z.B. Event/Party)":
            titel_clean = umlaute_ersetzen(freitext_titel).upper()
            draw_g.text((1080, 1000), titel_clean, fill="#ffcc00", anchor="mm", font_size=120)
            draw_g.rectangle([200, 1200, 1960, 2600], fill="#001a3a", outline="#ffffff", width=6)
            lines = freitext_inhalt.split("\n")
            y_text_offset = 1400
            for line in lines:
                draw_g.text((1080, y_text_offset), line, fill="#ffffff", anchor="mm", font_size=64)
                y_text_offset += 110

        draw_g.text((1080, 3520), "🦅 NUR DER LBV!", fill="#ffffff", anchor="mm", font_size=85)
        
        st.image(img_g, width=280)
        buf_g = io.BytesIO()
        img_g.save(buf_g, format="PNG")
        st.download_button(label="📥 Grafik downloaden", data=buf_g.getvalue(), file_name="phoenix_post.png", mime="image/png", type="primary")

# --- TAB 4: LIVE SCOUT ---
with tab4:
    st.subheader("📝 Live Ticker")
    st.metric("Spielstand", f"LBV {st.session_state['tore_phönix']} : {st.session_state['tore_gegner']} Gegner")
    
    # Buttons auf Mobile übersichtlich untereinander
    if st.button("⚽ Tor für Phönix"): 
        st.session_state["tore_phönix"] += 1
        st.rerun()
    if st.button("❌ Tor für Gegner"): 
        st.session_state["tore_gegner"] += 1
        st.rerun()
        
    st.write("---")
    event_spieler = st.selectbox("Spieler:", kader)
    event_typ = st.selectbox("Event:", ["Tor erzielt", "Ecke verwandelt", "Grüne Karte", "Gelbe Karte"])
    if st.button("Event loggen"):
        st.session_state["spielbericht_events"].append(f"• {event_spieler} ({event_typ})")
        st.success("Geloggt!")
        st.rerun()

    if st.button("🔄 Reset"):
        st.session_state["tore_phönix"], st.session_state["tore_gegner"], st.session_state["spielbericht_events"] = 0, 0, []
        st.rerun()

    bericht_text = f"🏑 MATCH-REPORT\nLBV Phoenix {st.session_state['tore_phönix']}:{st.session_state['tore_gegner']}\n" + "\n".join(st.session_state["spielbericht_events"])
    st.text_area("Bericht kopieren:", bericht_text, height=120)

# --- TAB 5: MANNSCHAFTSKASSE ---
with tab5:
    st.subheader("💰 Mannschaftskasse")
    s_spieler = st.selectbox("Wer?", kader)
    grund = st.selectbox("Was?", ["Zu spät (5€)", "Grüne Karte (2€)", "Gelbe Karte (5€)", "Kasten vergessen (10€)"])
    
    if st.button("Buchen 💶"):
        betrag = grund.split("(")[1].split("€")[0]
        st.session_state["strafen"].append({"Spieler": s_spieler, "Grund": grund, "Betrag": int(betrag), "Datum": datetime.now().strftime("%d.%m.%y")})
        st.success("Gebucht!")
        st.rerun()
        
    if st.session_state["strafen"]:
        st.table(pd.DataFrame(st.session_state["strafen"]))
        st.metric("Gesamtstand", f"{pd.DataFrame(st.session_state['strafen'])['Betrag'].sum()} €")
