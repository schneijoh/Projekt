import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image, ImageDraw
import io

# --- STREAMLIT CONFIG & DESIGN ---
st.set_page_config(page_title="LBV Phönix Command Center", page_icon="🦅", layout="wide")

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
st.sidebar.title("🦅 LBV Phönix Lübeck")
st.sidebar.caption("Hockey-Zentrale • Gegründet 1903")
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
    st.error("⚠️ Mindestens 11 Spieler benötigt (1 TW + 10 Feldspieler).")
    st.stop()

# --- HAUPTBEREICH ---
st.title("🏑 PHÖNIX HOCKEY COMMAND CENTER")
st.write("Die All-in-One Verwaltung für Aufstellung, Social Media und Spielbetrieb.")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 Aufstellung (Dynamisch)", 
    "🎯 Corner Master", 
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

# --- TAB 2: CORNER MASTER ---
with tab2:
    st.subheader("🎯 Strafecken-Zuweisung")
    e_col1, e_col2 = st.columns(2)
    with e_col1:
        st.markdown("### 🟢 Eigene Ecken (Offensiv)")
        raus = st.selectbox("Rausgeber", kader, index=1, key="raus")
        stop = st.selectbox("Stopper", kader, index=2, key="stop")
        schuss = st.multiselect("Schützen", kader, default=[kader[min(3, len(kader)-1)]])
    with e_col2:
        st.markdown("### 🔴 Gegnerische Ecken (Defensiv)")
        w1 = st.selectbox("1. Welle (Abläufer)", kader, index=min(4, len(kader)-1), key="w1")
        w2 = st.selectbox("2. Welle", kader, index=min(5, len(kader)-1), key="w2")
        posten = st.selectbox("Linien-Posten", kader, index=min(2, len(kader)-1), key="posten")

# --- TAB 3: SOCIAL MEDIA EXPORT (KADER GRAFIK) ---
with tab3:
    st.subheader("📸 Startelf-Grafik für Instagram")
    gegner_media = st.text_input("Gegner:", "UHC Hamburg", key="gegner_tab3")
    design_typ = st.radio("Wähle dein Phönix Vereins-Design:", [
        "🔵 Falkenstraße Homefield (Blauer Kunstrasen!)", 
        "🔵⚪🔴 Phönix Matchday Classic (Dunkelblau dominant)", 
        "⚪🔵🔴 Phönix Clean White (Auswärts-Look)"
    ])
    
    if st.button("🚀 Kader-Grafik erstellen"):
        img = Image.new("RGB", (1080, 1920))
        draw = ImageDraw.Draw(img)
        
        # Farbwelten zuweisen
        if "Blauer Kunstrasen" in design_typ:
            bg, accent, text = "#004B87", "#cc0000", "#ffffff" # Phönix Blau & Rot
            draw.rectangle([0, 0, 1080, 1920], fill=bg)
            # Feldlinien weiß einzeichnen
            draw.rectangle([50, 50, 1030, 1870], outline="#ffffff", width=8)
            draw.line([50, 960, 1030, 960], fill="#ffffff", width=6)
            draw.arc([340, 50, 740, 350], start=0, end=180, fill="#ffffff", width=6)
        elif "Classic" in design_typ:
            bg, accent, text = "#001530", "#cc0000", "#ffffff"
            draw.rectangle([0, 0, 1080, 1920], fill=bg)
            draw.rectangle([0, 0, 1080, 260], fill=accent) # Rote Kopfzeile
        else: # Clean White
            bg, accent, text = "#ffffff", "#002147", "#002147"
            draw.rectangle([0, 0, 1080, 1920], fill=bg)
            draw.rectangle([40, 40, 1040, 1880], outline=accent, width=8)

        # Dunkle Boxen im Hintergrund für maximale Text-Lesbarkeit
        if "Clean White" not in design_typ:
            for y_box in [500, 720, 940, 1160, 1460]:
                draw.rectangle([100, y_box, 980, y_box+130], fill="#000e21", outline="#cc0000", width=2)
        else:
            for y_box in [500, 720, 940, 1160, 1460]:
                draw.rectangle([100, y_box, 980, y_box+130], fill="#f4f6f9", outline="#002147", width=2)

        # Header Text
        draw.text((540, 130), "LBV PHÖNIX LÜBECK", fill="#ffffff" if "Clean White" not in design_typ else "#002147", anchor="mm", font_size=58)
        draw.text((540, 320), f"STARTING XI vs {gegner_media}", fill=accent if "Classic" not in design_typ else "#ffcc00", anchor="mm", font_size=46)
        draw.text((540, 390), f"System: {formation}", fill=text, anchor="mm", font_size=32)
        
        # Aufstellungs-Text (Groß und extrem gut lesbar)
        draw.text((540, 530), f"🧤 TW:  {tw_val}", fill=text, anchor="mm", font_size=38)
        draw.text((540, 750), f"🛡️ DEF:  {'  •  '.join(def_spieler)}", fill=text, anchor="mm", font_size=36)
        draw.text((540, 970), f"🧠 MID:  {'  •  '.join(mid_spieler)}", fill=text, anchor="mm", font_size=36)
        draw.text((540, 1190), f"⚡ STURM:  {'  •  '.join(sturm_spieler)}", fill=text, anchor="mm", font_size=36)
        
        # Bank
        bank_str = ", ".join(moegliche_bank) if moegliche_bank else "Keine"
        draw.text((540, 1490), f"🔄 BANK:  {bank_str}", fill=text, anchor="mm", font_size=34)
        
        draw.text((540, 1820), "🦅 Adler fliegen hoch • Seit 1903", fill="#aaaaaa", anchor="mm", font_size=26)
        
        st.image(img, width=350)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.download_button(label="📥 Kader-Story herunterladen", data=buf.getvalue(), file_name="phoenix_kader.png", mime="image/png", type="primary")

# --- ✨ NEUES ZUSÄTZLICHES FENSTER: WEITERE NÜTZLICHE GRAFIKEN ---
with tab4:
    st.subheader("🎨 Weitere nützliche Grafiken erstellen")
    st.write("Generiere hier Grafiken für Ankündigungen oder Endergebnisse.")
    
    g_type = st.selectbox("Welche Grafik brauchst du?", ["Match-Ankündigung (Plakat)", "Endergebnis-Post"])
    gegner_g = st.text_input("Gegner:", "UHC Hamburg", key="gegner_tab4")
    
    if g_type == "Endergebnis-Post":
        c_e1, c_e2 = st.columns(2)
        with c_e1: tore_p = st.number_input("Tore Phönix:", value=st.session_state["tore_phönix"])
        with c_e2: tore_g = st.number_input("Tore Gegner:", value=st.session_state["tore_gegner"])
        
    if st.button("🚀 Grafik jetzt generieren"):
        img_g = Image.new("RGB", (1080, 1920), color="#002147") # Echtes Phönix Dunkelblau
        draw_g = ImageDraw.Draw(img_g)
        
        # Vereins-Rahmen zeichnen
        draw_g.rectangle([40, 40, 1040, 1880], outline="#ffffff", width=6)
        draw_g.rectangle([40, 40, 1040, 240], fill="#cc0000") # Roter Balken
        
        draw_g.text((540, 140), "LBV PHÖNIX LÜBECK", fill="#ffffff", anchor="mm", font_size=55)
        
        if g_type == "Match-Ankündigung (Plakat)":
            draw_g.text((540, 600), "NÄCHSTES SPIEL", fill="#ffcc00", anchor="mm", font_size=65)
            draw_g.rectangle([150, 750, 930, 1050], fill="#001124", outline="#ffffff", width=3)
            draw_g.text((540, 850), "LBV PHÖNIX", fill="#ffffff", anchor="mm", font_size=45)
            draw_g.text((540, 950), f"vs  {gegner_g}", fill="#ffffff", anchor="mm", font_size=45)
            
            draw_g.text((540, 1200), "📍 Heimplatz: Falkenstraße (Blau)", fill="#ffffff", anchor="mm", font_size=36)
            draw_g.text((540, 1300), f"📅 Datum: Heute", fill="#ffffff", anchor="mm", font_size=36)
            
        else: # Endergebnis-Post
            draw_g.text((540, 600), "ENDERGEBNIS", fill="#ffcc00", anchor="mm", font_size=70)
            
            # Ergebnis-Kasten
            draw_g.rectangle([150, 750, 930, 1150], fill="#001124", outline="#cc0000", width=4)
            draw_g.text((540, 830), "LBV Phönix", fill="#ffffff", anchor="mm", font_size=40)
            draw_g.text((540, 950), f"{int(tore_p)} : {int(tore_g)}", fill="#ffffff", anchor="mm", font_size=90)
            draw_g.text((540, 1070), gegner_g, fill="#ffffff", anchor="mm", font_size=40)
            
            # Match-Events aus dem Live-Scout einblenden falls vorhanden
            if st.session_state["spielbericht_events"]:
                draw_g.text((540, 1300), "Highlights:", fill="#aaaaaa", anchor="mm", font_size=32)
                y_offset = 1360
                for ev in st.session_state["spielbericht_events"][:5]: # Maximal 5 Zeilen anzeigen
                    draw_g.text((540, y_offset), ev, fill="#ffffff", anchor="mm", font_size=28)
                    y_offset += 50

        draw_g.text((540, 1750), "🦅 Nur der LBV!", fill="#ffffff", anchor="mm", font_size=40)
        
        st.image(img_g, width=350)
        buf_g = io.BytesIO()
        img_g.save(buf_g, format="PNG")
        st.download_button(label="📥 Diese Grafik herunterladen", data=buf_g.getvalue(), file_name=f"phoenix_{g_type.lower().replace(' ', '_')}.png", mime="image/png", type="primary")

# --- TAB 5: LIVE SCOUT & REPORT ---
with tab5:
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

# --- TAB 6: MANNSCHAFTSKASSE ---
with tab6:
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
