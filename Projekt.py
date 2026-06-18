import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image, ImageDraw
import io

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

# --- STREAMLIT CONFIG & DESIGN ---
st.set_page_config(page_title="LBV Phoenix Command Center", page_icon="🦅", layout="wide")

# Zentrales, sauberes Phönix-Design für die App-Oberfläche
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
        # 4K UHD QUALITÄT (2160 x 3840) für extreme Schärfe
        img = Image.new("RGB", (2160, 3840))
        draw = ImageDraw.Draw(img)
        
        # Farbwelten zuweisen
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
        else: # Clean White
            bg, accent, text = "#ffffff", "#002147", "#002147"
            draw.rectangle([0, 0, 2160, 3840], fill=bg)
            draw.rectangle([80, 80, 2080, 3760], outline=accent, width=16)

        # Größere Boxen für bessere Lesbarkeit
        box_fill = "#000e21" if "Clean White" not in design_typ else "#f4f6f9"
        box_outline = "#cc0000" if "Clean White" not in design_typ else "#002147"
        
        for y_box in [1000, 1440, 1880, 2320, 2920]:
            draw.rectangle([150, y_box, 2010, y_box+280], fill=box_fill, outline=box_outline, width=4)

        # Texte vorbereiten und Umlaute ausschreiben
        header_top = umlaute_ersetzen("LBV PHOENIX LUEBECK")
        header_sub = umlaute_ersetzen(f"STARTING XI vs {gegner_media}")
        system_str = umlaute_ersetzen(f"System: {formation}")
        
        tw_str = umlaute_ersetzen(f"🧤 TW:  {tw_val}")
        def_str = umlaute_ersetzen(f"🛡️ DEF:  {'  •  '.join(def_spieler)}")
        mid_str = umlaute_ersetzen(f"🧠 MID:  {'  •  '.join(mid_spieler)}")
        sturm_str = umlaute_ersetzen(f"⚡ STURM:  {'  •  '.join(sturm_spieler)}")
        
        bank_raw = ", ".join(moegliche_bank) if moegliche_bank else "Keine"
        bank_str = umlaute_ersetzen(f"🔄 BANK:  {bank_raw}")

        # Texte rendern (Schriftgrößen angepasst für perfekte Lesbarkeit in 4K)
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

# --- TAB 3: WEITERE GRAFIKEN (NEUES DESIGN & DETAILS) ---
with tab3:
    st.subheader("🎨 Weitere nützliche Grafiken erstellen")
    st.write("Generiere hier Plakate oder Endergebnisse in exzellenter 4K-Qualität.")
    
    g_type = st.selectbox("Welche Grafik brauchst du?", ["Match-Ankündigung (Plakat)", "Endergebnis-Post"])
    
    # Erweiterte Spieldetails für maximale Flexibilität
    c_g1, c_g2 = st.columns(2)
    with c_g1:
        gegner_g = st.text_input("Gegner:", "UHC Hamburg", key="gegner_tab3_new")
        ort_g = st.text_input("Spielort / Platz:", "Falkenstrasse (Blau)", key="ort_tab3")
    with c_g2:
        datum_g = st.text_input("Datum:", datetime.now().strftime("%d.%m.%Y"), key="datum_tab3")
        zeit_g = st.text_input("Uhrzeit / Anpfiff:", "14:00 Uhr", key="zeit_tab3")
        
    info_g = st.text_input("Zusatz-Info (z.B. 'Heimspiel', 'Eintritt frei' oder 'Topspiel'):", "Heimspiel", key="info_tab3")
    
    if g_type == "Endergebnis-Post":
        c_e1, c_e2 = st.columns(2)
        with c_e1: tore_p = st.number_input("Tore Phönix:", value=st.session_state["tore_phönix"])
        with c_e2: tore_g = st.number_input("Tore Gegner:", value=st.session_state["tore_gegner"])
        
    if st.button("🚀 Grafik jetzt generieren"):
        # 4K UHD QUALITÄT (2160 x 3840)
        img_g = Image.new("RGB", (2160, 3840), color="#002147")
        draw_g = ImageDraw.Draw(img_g)
        
        # Stabiler Kontrast-Rahmen
        draw_g.rectangle([80, 80, 2080, 3760], outline="#ffffff", width=12)
        draw_g.rectangle([80, 80, 2080, 480], fill="#cc0000")
        
        # Texte säubern & Umlaute ausschreiben
        club_title = umlaute_ersetzen("LBV PHOENIX LUEBECK")
        gegner_clean = umlaute_ersetzen(gegner_g)
        ort_clean = umlaute_ersetzen(ort_g)
        datum_clean = umlaute_ersetzen(datum_g)
        zeit_clean = umlaute_ersetzen(zeit_g)
        info_clean = umlaute_ersetzen(info_g).upper()
        
        draw_g.text((1080, 280), club_title, fill="#ffffff", anchor="mm", font_size=110)
        
        if g_type == "Match-Ankündigung (Plakat)":
            draw_g.text((1080, 1100), "NAECHSTES SPIEL", fill="#ffcc00", anchor="mm", font_size=140)
            
            # Match-Box (Massiv und kontrastreich)
            draw_g.rectangle([250, 1350, 1910, 2050], fill="#001124", outline="#ffffff", width=6)
            draw_g.text((1080, 1530), "LBV PHOENIX", fill="#ffffff", anchor="mm", font_size=96)
            draw_g.text((1080, 1720), "VS", fill="#cc0000", anchor="mm", font_size=70)
            draw_g.text((1080, 1890), gegner_clean, fill="#ffffff", anchor="mm", font_size=96)
            
            # Event-Details gut lesbar blockweise platziert
            draw_g.rectangle([250, 2250, 1910, 2900], fill="#001a3a", outline="#ffcc00", width=4)
            draw_g.text((1080, 2370), f"PLATZ:  {ort_clean}", fill="#ffffff", anchor="mm", font_size=76)
            draw_g.text((1080, 2520), f"DATUM:  {datum_clean}", fill="#ffffff", anchor="mm", font_size=76)
            draw_g.text((1080, 2670), f"ANPFIFF:  {zeit_clean}", fill="#ffffff", anchor="mm", font_size=76)
            
            if info_clean:
                draw_g.rectangle([350, 3100, 1810, 3280], fill="#cc0000")
                draw_g.text((1080, 3190), info_clean, fill="#ffffff", anchor="mm", font_size=72)
            
        else: # Endergebnis-Post
            draw_g.text((1080, 1100), "ENDERGEBNIS", fill="#ffcc00", anchor="mm", font_size=140)
            
            # Übergroßer Score-Kasten für maximalen Fokus
            draw_g.rectangle([250, 1350, 1910, 2250], fill="#001124", outline="#cc0000", width=8)
            draw_g.text((1080, 1510), "LBV Phoenix", fill="#ffffff", anchor="mm", font_size=86)
            draw_g.text((1080, 1790), f"{int(tore_p)} : {int(tore_g)}", fill="#ffffff", anchor="mm", font_size=210)
            draw_g.text((1080, 2070), gegner_clean, fill="#ffffff", anchor="mm", font_size=86)
            
            draw_g.text((1080, 2400), f"{datum_clean}  •  {ort_clean}", fill="#aaaaaa", anchor="mm", font_size=56)
            
            # Match-Highlights
            if st.session_state["spielbericht_events"]:
                draw_g.rectangle([250, 2550, 1910, 3250], fill="#001a3a", outline="#ffffff", width=3)
                draw_g.text((1080, 2640), "MATCH HIGHLIGHTS", fill="#ffcc00", anchor="mm", font_size=68)
                y_offset = 2760
                for ev in st.session_state["spielbericht_events"][:5]:
                    ev_clean = umlaute_ersetzen(ev)
                    draw_g.text((1080, y_offset), ev_clean, fill="#ffffff", anchor="mm", font_size=58)
                    y_offset += 100

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
