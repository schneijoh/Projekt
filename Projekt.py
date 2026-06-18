import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image, ImageDraw
import io

# Seiteneinstellungen
st.set_page_config(page_title="LBV Phönix Command Center", page_icon="🏑", layout="wide")

# Styling für den LBV Phönix Look (Blau-Weiß-Rot)
st.markdown("""
    <style>
    .main { background-color: #0a1f33; }
    h1, h2, h3 { color: #003366; }
    .stButton>button { background-color: #cc0000; color: white; border-radius: 5px; }
    .stButton>button:hover { background-color: #990000; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALISIERUNG DES KADERS ---
if "kader_liste" not in st.session_state:
    st.session_state["kader_liste"] = [
        "Torwart Max", "Anna", "Lisa", "Tom", "Ben", "Felix", 
        "Marie", "Lukas", "Emma", "Tim", "Jan", "Laura", "Sam"
    ]
if "strafen" not in st.session_state:
    st.session_state["strafen"] = []

# --- SIDEBAR: KADER ---
st.sidebar.title("🦅 LBV Phönix Lübeck")
st.sidebar.subheader("Abteilung Hockey seit 1909")

st.sidebar.markdown("### 👥 Kader bearbeiten (Ändern/Löschen)")
neuer_kader = st.sidebar.data_editor(
    st.session_state["kader_liste"],
    num_rows="dynamic",
    placeholder="Name eingeben...",
    use_container_width=True
)
st.session_state["kader_liste"] = [x for x in neuer_kader if x]
kader = st.session_state["kader_liste"]

if len(kader) < 11:
    st.error("⚠️ Phönix-Kader zu klein! Mindestens 11 Spieler benötigt (1 TW + 10 Feldspieler).")
    st.stop()

# --- HAUPTBEREICH ---
st.title("🏑 LBV PHÖNIX – HOCKEY COMMAND CENTER")
st.caption("Blau-Weiß-Rot • Tradition seit 1903 am Travekanal")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Dynamische Aufstellung", 
    "🎯 Corner Master", 
    "📸 Phönix Social Export",
    "⏱️ Karten-Timer", 
    "💰 Mannschaftskasse"
])

# --- TAB 1: DYNAMISCHE AUFSTELLUNG (1+10) ---
with tab1:
    st.subheader("Match-Aufstellung & System-Konfigurator")
    
    formation = st.selectbox("Wähle das Spielsystem:", ["4-3-3", "3-4-3", "3-5-2", "2-4-4"])
    
    # Aufteilen der Feldspieler basierend auf der gewählten Formation
    anzahl_def = int(formation.split("-")[0])
    anzahl_mid = int(formation.split("-")[1])
    anzahl_sturm = int(formation.split("-")[2])
    
    st.write(f"Ausgewähltes System benötigt: **1** Torwart | **{anzahl_def}** Verteidiger | **{anzahl_mid}** Mittelfeldspieler | **{anzahl_sturm}** Stürmer.")
    st.write("---")
    
    # Dropdowns dynamisch generieren
    stamm_aufstellung = []
    
    c_tw, c_def, c_mid, c_sturm = st.columns(4)
    
    with c_tw:
        st.info("🧤 Tor")
        tw_val = st.selectbox("Torwart (TW)", kader, index=0)
        stamm_aufstellung.append(tw_val)
        
    with c_def:
        st.error(f"🛡️ Abwehr ({anzahl_def})")
        def_spieler = []
        for i in range(anzahl_def):
            idx = min(1 + i, len(kader)-1)
            val = st.selectbox(f"Verteidiger {i+1}", kader, index=idx, key=f"def_{i}")
            def_spieler.append(val)
            stamm_aufstellung.append(val)
            
    with c_mid:
        st.success(f"🧠 Mittelfeld ({anzahl_mid})")
        mid_spieler = []
        for i in range(anzahl_mid):
            idx = min(1 + anzahl_def + i, len(kader)-1)
            val = st.selectbox(f"Mittelfeld {i+1}", kader, index=idx, key=f"mid_{i}")
            mid_spieler.append(val)
            stamm_aufstellung.append(val)
            
    with c_sturm:
        st.warning(f"⚡ Sturm ({anzahl_sturm})")
        sturm_spieler = []
        for i in range(anzahl_sturm):
            idx = min(1 + anzahl_def + anzahl_mid + i, len(kader)-1)
            val = st.selectbox(f"Stürmer {i+1}", kader, index=idx, key=f"sturm_{i}")
            sturm_spieler.append(val)
            stamm_aufstellung.append(val)

    # Bank berechnen
    einzigartige_stamm = list(set(stamm_aufstellung))
    moegliche_bank = [p for p in kader if p not in einzigartige_stamm]
    
    st.write("---")
    st.markdown("### 🔄 Auswechselbank")
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

# --- TAB 3: SOCIAL MEDIA EXPORT (PHÖNIX BRANDING) ---
with tab3:
    st.subheader("📸 LBV Phönix Matchday Grafik-Generator")
    gegner_media = st.text_input("Gegner:", "UHC Hamburg")
    design_typ = st.radio("Style:", ["Phönix Blau-Rot Classic", "Falkenstraße Homefield (Grün)", "Adler Black Edition"])
    
    if st.button("🚀 Phönix Grafik generieren"):
        img = Image.new("RGB", (1080, 1920))
        draw = ImageDraw.Draw(img)
        
        # Designs im Vereins-Branding
        if design_typ == "Phönix Blau-Rot Classic":
            bg_color = "#002b49"  # Dunkelblau
            accent_color = "#cc0000"  # Phönix Rot
            text_color = "#ffffff"
            draw.rectangle([0, 0, 1080, 1920], fill=bg_color)
            draw.rectangle([0, 0, 1080, 260], fill=accent_color)  # Roter Balken oben
            draw.rectangle([40, 40, 1040, 1880], outline="#ffffff", width=6)
        elif design_typ == "Falkenstraße Homefield (Grün)":
            bg_color = "#123524"
            accent_color = "#002b49"
            text_color = "#ffffff"
            draw.rectangle([0, 0, 1080, 1920], fill=bg_color)
            draw.rectangle([40, 40, 1040, 1880], outline="#ffffff", width=8)
            draw.line([40, 960, 1040, 960], fill="#ffffff", width=5)
        else:  # Adler Black Edition
            bg_color = "#111111"
            accent_color = "#ffffff"
            text_color = "#ffffff"
            draw.rectangle([0, 0, 1080, 1920], fill=bg_color)
            draw.rectangle([50, 50, 1030, 1870], outline="#cc0000", width=4)

        # Wappen / Adler Symbol andeuten
        draw.polygon([(540, 60), (510, 110), (570, 110)], fill="#ffffff" if design_typ != "Adler Black Edition" else "#cc0000") # Minimalistischer Adler-Kopf
        
        # Texte platzierten
        draw.text((540, 160), "LBV PHÖNIX LÜBECK", fill="#ffffff", anchor="mm", font_size=55)
        draw.text((540, 320), f"vs  {gegner_media}", fill="#ffffff" if design_typ == "Falkenstraße Homefield (Grün)" else "#ffcc00", anchor="mm", font_size=45)
        draw.text((540, 400), f"System: {formation}", fill="#aaaaaa", anchor="mm", font_size=32)
        
        # Aufstellung auf dem Bild
        draw.text((540, 520), "🧤 TORWART", fill=accent_color if design_typ != "Phönix Blau-Rot Classic" else "#ffcc00", anchor="mm", font_size=32)
        draw.text((540, 580), tw_val, fill=text_color, anchor="mm", font_size=42)
        
        draw.text((540, 720), "🛡️ ABWEHR", fill=accent_color if design_typ != "Phönix Blau-Rot Classic" else "#ffcc00", anchor="mm", font_size=32)
        draw.text((540, 780), "  •  ".join(def_spieler), fill=text_color, anchor="mm", font_size=36)
        
        draw.text((540, 940), "🧠 MITTELFELD", fill=accent_color if design_typ != "Phönix Blau-Rot Classic" else "#ffcc00", anchor="mm", font_size=32)
        draw.text((540, 1000), "  •  ".join(mid_spieler), fill=text_color, anchor="mm", font_size=36)
        
        draw.text((540, 1160), "⚡ STURM", fill=accent_color if design_typ != "Phönix Blau-Rot Classic" else "#ffcc00", anchor="mm", font_size=32)
        draw.text((540, 1220), "  •  ".join(sturm_spieler), fill=text_color, anchor="mm", font_size=36)
        
        # Strafecken
        draw.text((540, 1400), "🎯 STRAFECKE", fill=accent_color if design_typ != "Phönix Blau-Rot Classic" else "#ffcc00", anchor="mm", font_size=32)
        draw.text((540, 1460), f"Rausgabe: {raus} | Stop: {stop}", fill=text_color, anchor="mm", font_size=32)
        
        # Bank
        bank_str = ", ".join(moegliche_bank) if moegliche_bank else "Voller Kader auf dem Feld"
        draw.text((540, 1640), "🔄 WECHSELBANK", fill="#aaaaaa", anchor="mm", font_size=30)
        draw.text((540, 1700), bank_str, fill=text_color, anchor="mm", font_size=28)
        
        draw.text((540, 1850), "Phönix Go! • Hockey Command Center", fill="#aaaaaa", anchor="mm", font_size=24)
        
        st.image(img, width=360)
        
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.download_button(label="📥 Phönix-Story herunterladen", data=byte_im, file_name="phoenix_matchday.png", mime="image/png", type="primary")

# --- TAB 4 & 5: TIMER & KASSE (UNVERÄNDERT STABIL) ---
with tab4:
    st.subheader("⏱️ Live Bank-Zeitstrafen (Grün / Gelb)")
    karten_typ = st.radio("Karte:", ["🟢 Grün (2 Min)", "🟡 Gelb (5 Min)", "🟡 Gelb (10 Min)"])
    straf_spieler = st.selectbox("Spieler", kader, key="straf_sp")
    if st.button("Zeitstrafe für Phönix aktivieren"):
        st.warning(f"Strafe läuft für {straf_spieler}!")

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
