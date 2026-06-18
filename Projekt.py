import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image, ImageDraw
import io

# Seiteneinstellungen
st.set_page_config(page_title="LBV Phönix Command Center", page_icon="🏑", layout="wide")

# --- INITIALISIERUNG DES KADERS & STATS ---
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
st.sidebar.subheader("Tradition seit 1903")

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

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 Dynamische Aufstellung", 
    "🎯 Corner Master", 
    "📸 Phönix Social Export",
    "📝 Live-Scout & Bericht",
    "⏱️ Karten-Timer", 
    "💰 Mannschaftskasse"
])

# --- TAB 1: DYNAMISCHE AUFSTELLUNG (1+10) ---
with tab1:
    st.subheader("Match-Aufstellung & System-Konfigurator")
    formation = st.selectbox("Wähle das Spielsystem:", ["4-3-3", "3-4-3", "3-5-2", "2-4-4"])
    
    anzahl_def = int(formation.split("-")[0])
    anzahl_mid = int(formation.split("-")[1])
    anzahl_sturm = int(formation.split("-")[2])
    
    st.write(f"System benötigt: **1** TW | **{anzahl_def}** Abwehr | **{anzahl_mid}** Mittelfeld | **{anzahl_sturm}** Sturm.")
    st.write("---")
    
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

# --- TAB 3: SOCIAL MEDIA EXPORT (NUR KADER, MEHR PHÖNIX-DESIGNS) ---
with tab3:
    st.subheader("📸 LBV Phönix Matchday Grafik-Generator")
    gegner_media = st.text_input("Gegner:", "UHC Hamburg")
    design_typ = st.radio("Wähle dein Phönix Vereins-Design:", [
        "🔵⚪🔴 Phönix Heim-Trikot (Dunkelblau dominant)", 
        "⚪🔵🔴 Phönix Auswärts (Weiß dominant)", 
        "🔴🔵⚪ Phönix Retro (Rot-Blau gestreift)", 
        "🦅 Adler Black Gold Edition",
        "🏑 Kunstrasen Falkenstraße"
    ])
    
    if st.button("🚀 Phönix Grafik generieren"):
        img = Image.new("RGB", (1080, 1920))
        draw = ImageDraw.Draw(img)
        
        # 5 Vereins-Farbwelten ausarbeiten
        if "Heim-Trikot" in design_typ:
            bg, accent, text, line = "#002147", "#cc0000", "#ffffff", "#ffffff" # Dunkelblau & Rot
            draw.rectangle([0, 0, 1080, 1920], fill=bg)
            draw.rectangle([0, 0, 1080, 240], fill=accent) # Rote Schärpe oben
            draw.rectangle([40, 40, 1040, 1880], outline=line, width=6)
        elif "Auswärts" in design_typ:
            bg, accent, text, line = "#ffffff", "#002147", "#002147", "#cc0000" # Weiß & Blau
            draw.rectangle([0, 0, 1080, 1920], fill=bg)
            draw.rectangle([0, 0, 1080, 240], fill=accent)
            draw.rectangle([40, 40, 1040, 1880], outline=line, width=6)
            text_header = "#ffffff"
        elif "Retro" in design_typ:
            bg, accent, text, line = "#002147", "#cc0000", "#ffffff", "#ffffff"
            draw.rectangle([0, 0, 1080, 1920], fill=bg)
            # Vertikale Retro-Streifen
            for x in range(0, 1080, 120):
                draw.rectangle([x, 0, x+60, 1920], fill=accent)
            draw.rectangle([100, 100, 980, 1820], fill="#001530") # Dunkler Kasten für Text-Lesbarkeit
        elif "Black Gold" in design_typ:
            bg, accent, text, line = "#111111", "#d4af37", "#ffffff", "#d4af37" # Schwarz & Gold
            draw.rectangle([0, 0, 1080, 1920], fill=bg)
            draw.rectangle([40, 40, 1040, 1880], outline=accent, width=4)
        else: # Kunstrasen
            bg, accent, text, line = "#1b4d3e", "#002147", "#ffffff", "#ffffff"
            draw.rectangle([0, 0, 1080, 1920], fill=bg)
            draw.rectangle([40, 40, 1040, 1880], outline=line, width=6)
            draw.line([40, 960, 1040, 960], fill=line, width=4)

        # Farb-Korrektur für Header-Text bei weißem Hintergrund
        h_color = "#ffffff" if "Auswärts" in design_typ else ("#111111" if "Black Gold" in design_typ else "#ffffff")
        if "Auswärts" in design_typ: h_color = "#ffffff"
        if "Black Gold" in design_typ: accent = "#d4af37"

        # Adler-Wappen Andeutung (Phönix-Logo-Symbolik)
        draw.polygon([(540, 50), (490, 110), (590, 110)], fill=accent if "Auswärts" not in design_typ else "#ffffff")
        
        # Texte (NUR KADER, KEINE Short-Corner Infos mehr!)
        draw.text((540, 150), "LBV PHÖNIX LÜBECK", fill=h_color, anchor="mm", font_size=55)
        draw.text((540, 320), f"STARTING XI vs {gegner_media}", fill=accent if "Heim" not in design_typ else "#ffcc00", anchor="mm", font_size=42)
        draw.text((540, 390), f"System: {formation}", fill="#ffffff" if bg != "#ffffff" else "#555555", anchor="mm", font_size=30)
        
        # Aufstellung
        draw.text((540, 520), "🧤 TORWART", fill=accent if "Heim" not in design_typ else "#ffcc00", anchor="mm", font_size=35)
        draw.text((540, 580), tw_val, fill=text, anchor="mm", font_size=42)
        
        draw.text((540, 720), "🛡️ ABWEHR", fill=accent if "Heim" not in design_typ else "#ffcc00", anchor="mm", font_size=35)
        draw.text((540, 790), "  •  ".join(def_spieler), fill=text, anchor="mm", font_size=36)
        
        draw.text((540, 960), "🧠 MITTELFELD", fill=accent if "Heim" not in design_typ else "#ffcc00", anchor="mm", font_size=35)
        draw.text((540, 1030), "  •  ".join(mid_spieler), fill=text, anchor="mm", font_size=36)
        
        draw.text((540, 1200), "⚡ STURM", fill=accent if "Heim" not in design_typ else "#ffcc00", anchor="mm", font_size=35)
        draw.text((540, 1270), "  •  ".join(sturm_spieler), fill=text, anchor="mm", font_size=36)
        
        # Bank
        bank_str = ", ".join(moegliche_bank) if moegliche_bank else "Keine Auswechselspieler"
        draw.text((540, 1500), "🔄 WECHSELBANK", fill="#aaaaaa", anchor="mm", font_size=32)
        draw.text((540, 1580), bank_str, fill=text, anchor="mm", font_size=30)
        
        draw.text((540, 1840), "Adler fliegen hoch • LBV Phönix Hockey", fill="#aaaaaa", anchor="mm", font_size=24)
        
        st.image(img, width=360)
        
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.download_button(label="📥 Phönix-Kader-Story herunterladen", data=byte_im, file_name="phoenix_kader_story.png", mime="image/png", type="primary")

# --- ✨ NEUES ZUSÄTZLICHES FENSTER: LIVE SCOUT & SPIELBERICHT ---
with tab4:
    st.subheader("📝 Live-Match-Scout & WhatsApp-Bericht")
    st.write("Trage während des Spiels Events ein, um am Ende einen fertigen Text für die Club-Medien zu haben.")
    
    sc1, sc2 = st.columns(2)
    with sc1:
        st.markdown("### 📊 Spielstand")
        c_p, c_g = st.columns(2)
        with c_p:
            if st.button("⚽ Tor für Phönix"): st.session_state["tore_phönix"] += 1
        with c_g:
            if st.button("❌ Tor für Gegner"): st.session_state["tore_gegner"] += 1
            
        st.metric("Aktueller Spielstand", f"LBV Phönix {st.session_state['tore_phönix']} : {st.session_state['tore_gegner']} {gegner_media}")
        if st.button("🔄 Spielstand zurücksetzen"):
            st.session_state["tore_phönix"] = 0
            st.session_state["tore_gegner"] = 0
            st.session_state["spielbericht_events"] = []
            st.rerun()

    with sc2:
        st.markdown("### 🎙️ Event-Ticker")
        event_spieler = st.selectbox("Beteiligter Spieler:", kader, key="scout_sp")
        event_typ = st.selectbox("Aktion:", ["Tor erzielt", "Strafecke verwandelt", "Grüne Karte", "Gelbe Karte", "Starke TW-Parade"])
        viertel = st.selectbox("Viertel:", ["1. Viertel", "2. Viertel", "3. Viertel", "4. Viertel"])
        
        if st.button("Event loggen"):
            log_text = f"[{viertel}] {event_spieler} -> {event_typ}"
            st.session_state["spielbericht_events"].append(log_text)
            st.success("Event gespeichert!")

    st.write("---")
    st.markdown("### 📋 Generierter Bericht-Entwurf (Kopierfertig)")
    
    bericht_text = f"🏑 SPIELBERICHT - LBV PHÖNIX LÜBECK\n" \
                   f"Endergebnis: LBV Phönix {st.session_state['tore_phönix']} : {st.session_state['tore_gegner']} {gegner_media}\n" \
                   f"-----------------------------------------\n" \
                   f"Spiel-Highlights:\n" + "\n".join(st.session_state["spielbericht_events"]) + \
                   f"\n-----------------------------------------\n🦅 Nur der LBV!"
                   
    st.text_area("Kopiere diesen Text für WhatsApp / Instagram-Story-Text:", bericht_text, height=200)

# --- TAB 5 & 6: TIMER & KASSE ---
with tab5:
    st.subheader("⏱️ Live Bank-Zeitstrafen")
    karten_typ = st.radio("Karte:", ["🟢 Grün (2 Min)", "🟡 Gelb (5 Min)", "🟡 Gelb (10 Min)"])
    straf_spieler = st.selectbox("Spieler", kader, key="straf_sp")
    if st.button("Zeitstrafe starten"):
        st.warning(f"Zeitstrafe aktiv für {straf_spieler}!")

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
