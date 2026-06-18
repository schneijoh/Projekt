import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image, ImageDraw
import io

# Seiteneinstellungen
st.set_page_config(page_title="Hockey Command Center", page_icon="🏑", layout="wide")

# --- INITIALISIERUNG DES KADERS (EINFACHE TABELLE) ---
if "kader_liste" not in st.session_state:
    st.session_state["kader_liste"] = [
        "Max (TW)", "Anna", "Lisa", "Tom", "Ben", "Felix", 
        "Marie", "Lukas", "Emma", "Tim", "Jan", "Laura", "Sam"
    ]
if "strafen" not in st.session_state:
    st.session_state["strafen"] = []

# --- SIDEBAR: ULTRA LEICHTE KADER-VERWALTUNG ---
st.sidebar.title("🏑 Kader-Verwaltung")
team_name = st.sidebar.text_input("Dein Team-Name", "Mein Hockey Club")

st.sidebar.markdown("### 👥 Spieler bearbeiten")
# Data Editor für extrem einfaches Ändern und Löschen
neuer_kader = st.sidebar.data_editor(
    st.session_state["kader_liste"],
    num_rows="dynamic",
    placeholder="Spielername eingeben...",
    use_container_width=True
)
# Speichern, wenn Änderungen vorgenommen wurden
st.session_state["kader_liste"] = [x for x in neuer_kader if x]

kader = st.session_state["kader_liste"]

# Sicherstellen, dass genügend Spieler da sind
if len(kader) < 11:
    st.error("⚠️ Dein Kader muss mindestens 11 Spieler enthalten (1 TW + 10 Feldspieler)! Bitte füge in der Sidebar Spieler hinzu.")
    st.stop()

# --- HAUPTBEREICH ---
st.title(f"🏆 {team_name} - Command Center")
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Aufstellung (1+10)", 
    "🎯 Corner Master", 
    "📸 Social Media Export",
    "⏱️ Karten & Zeitstrafen", 
    "💰 Mannschaftskasse"
])

# --- TAB 1: AUFSTELLUNG (REIN 1+10) ---
with tab1:
    st.subheader("Match-Aufstellung (1 Torwart + 10 Feldspieler)")
    
    col_sys, col_press = st.columns(2)
    with col_sys:
        formation = st.selectbox("Spielsystem:", [
            "3-4-3 (Klassisch)", "4-3-3 (Kompakt)", "3-5-2 (Mittelfeld-Dominanz)", "2-4-4 (Offensiv-Pressing)"
        ])
    with col_press:
        pressing = st.select_slider("Pressing-Zone:", options=["Viertel", "Halbfeld", "Dreiviertel", "Voll-Pressing"])

    st.write("---")
    
    st.markdown("### 🏃‍♂️ Start-Aufstellung festlegen")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.info("🧤 Tor & Abwehr (4)")
        tw = st.selectbox("Torwart (TW)", kader, index=0)
        def1 = st.selectbox("Verteidiger Links (VL)", kader, index=1)
        def2 = st.selectbox("Verteidiger Zentrum (VZ)", kader, index=2)
        def3 = st.selectbox("Verteidiger Rechts (VR)", kader, index=3)
        
    with c2:
        st.success("🧠 Mittelfeld (3 oder 4)")
        m1 = st.selectbox("Mittelfeld Links (ML)", kader, index=4)
        m2 = st.selectbox("Mittelfeld Zentrum (MZ)", kader, index=5)
        m3 = st.selectbox("Mittelfeld Rechts (MR)", kader, index=6)
        # Je nach System optional der 4. Mittelfeldspieler
        m4 = st.selectbox("Zusatz Mittelfeld / Halbraum", kader, index=7)

    with c3:
        st.warning("⚡ Sturm (2 oder 3)")
        s1 = st.selectbox("Stürmer Links (SL)", kader, index=8)
        s2 = st.selectbox("Stürmer Zentrum (SZ)", kader, index=9)
        s3 = st.selectbox("Stürmer Rechts (SR)", kader, index=10)
    
    # Berechne gewählte Stammspieler, um die Bank automatisch zu füllen
    stammspieler = [tw, def1, def2, def3, m1, m2, m3, m4, s1, s2, s3]
    # Entferne Duplikate für die Anzeige der Bank
    einzigartige_stamm = list(set(stammspieler))
    moegliche_bank = [p for p in kader if p not in einzigartige_stamm]
    
    st.write("---")
    st.markdown("### 🔄 Verfügbare Wechselspieler für die Bank")
    if moegliche_bank:
        st.info(", ".join(moegliche_bank))
    else:
        st.caption("Keine Auswechselspieler übrig. Alle im Kader befindlichen Personen starten.")

# --- TAB 2: CORNER MASTER ---
with tab2:
    st.subheader("🎯 Strafecken-Zuweisung")
    
    e_col1, e_col2 = st.columns(2)
    with e_col1:
        st.markdown("### 🟢 Eigene Ecken (Offensiv)")
        raus = st.selectbox("Rausgeber", kader, index=1, key="raus")
        stop = st.selectbox("Stopper", kader, index=2, key="stop")
        schuss = st.multiselect("Schützen", kader, default=[kader[3]])
        variante = st.text_area("Taktischer Ablauf", "Schlenzer auf die Stockseite oder Ablage Linksstecher.")
        
    with e_col2:
        st.markdown("### 🔴 Gegnerische Ecken (Defensiv)")
        w1 = st.selectbox("1. Welle (Abläufer)", kader, index=4, key="w1")
        w2 = st.selectbox("2. Welle", kader, index=5, key="w2")
        posten = st.selectbox("Linien-Posten", kader, index=2, key="posten")

# --- TAB 3: SOCIAL MEDIA EXPORT (MIT MULTI-DESIGN) ---
with tab3:
    st.subheader("📸 Social Media Grafik-Generator")
    st.write("Wähle ein Design aus und lade deine Matchday-Grafik direkt herunter.")
    
    gegner_media = st.text_input("Gegnerischer Verein:", "Mannheimer HC")
    design_typ = st.radio("🎨 Grafik-Stil auswählen:", ["Klassisch Grün (Spielfeld)", "Premium Black Edition", "Minimalistisches Lineup-Board"])
    
    if st.button("🚀 Grafik erstellen"):
        # Basis-Bild (1080x1920 - Instagram Story)
        img = Image.new("RGB", (1080, 1920))
        draw = ImageDraw.Draw(img)
        
        # FARB-THEMEN DEFINIEREN
        if design_typ == "Klassisch Grün (Spielfeld)":
            bg_color = "#1e3d2f"
            line_color = "#ffffff"
            accent_color = "#ffcc00"
            img = Image.new("RGB", (1080, 1920), color=bg_color)
            draw = ImageDraw.Draw(img)
            # Spielfeldlinien zeichnen
            draw.rectangle([40, 40, 1040, 1880], outline=line_color, width=8)
            draw.line([40, 960, 1040, 960], fill=line_color, width=5)
            draw.arc([340, 40, 740, 300], start=0, end=180, fill=line_color, width=5)
            draw.arc([340, 1660, 740, 1920], start=180, end=0, fill=line_color, width=5)
            
        elif design_typ == "Premium Black Edition":
            bg_color = "#111111"
            line_color = "#333333"
            accent_color = "#ff4444"
            img = Image.new("RGB", (1080, 1920), color=bg_color)
            draw = ImageDraw.Draw(img)
            # Moderner Tech-Look
            draw.rectangle([30, 30, 1050, 1890], outline=line_color, width=3)
            draw.rectangle([50, 50, 1030, 250], fill="#222222")
            
        else: # Minimalistisches Lineup-Board
            bg_color = "#f4f4f6"
            line_color = "#111111"
            accent_color = "#1e3d2f"
            img = Image.new("RGB", (1080, 1920), color=bg_color)
            draw = ImageDraw.Draw(img)
            draw.line([100, 280, 980, 280], fill=accent_color, width=8)

        # TEXT ZEICHNEN (Unabhängig vom Design mit angepassten Farben)
        text_main_color = "#ffffff" if design_typ != "Minimalistisches Lineup-Board" else "#111111"
        text_sub_color = "#aaaaaa" if design_typ != "Minimalistisches Lineup-Board" else "#555555"
        
        # Header
        draw.text((540, 120), "MATCHDAY", fill=accent_color, anchor="mm", font_size=75)
        draw.text((540, 210), f"{team_name} vs {gegner_media}", fill=text_main_color, anchor="mm", font_size=45)
        
        # System
        draw.text((540, 320), f"System: {formation}", fill=text_sub_color, anchor="mm", font_size=30)
        
        # Die 1+10 Aufstellung auf dem Bild platzieren
        draw.text((540, 450), "🧤 TORWART", fill=accent_color, anchor="mm", font_size=35)
        draw.text((540, 510), tw, fill=text_main_color, anchor="mm", font_size=40)
        
        draw.text((540, 640), "🛡️ ABWEHR", fill=accent_color, anchor="mm", font_size=35)
        draw.text((540, 710), f"{def1}   •   {def2}   •   {def3}", fill=text_main_color, anchor="mm", font_size=38)
        
        draw.text((540, 840), "🧠 MITTELFELD", fill=accent_color, anchor="mm", font_size=35)
        draw.text((540, 910), f"{m1}  •  {m2}  •  {m3}  •  {m4}", fill=text_main_color, anchor="mm", font_size=38)
        
        draw.text((540, 1040), "⚡ STURM", fill=accent_color, anchor="mm", font_size=35)
        draw.text((540, 1110), f"{s1}   •   {s2}   •   {s3}", fill=text_main_color, anchor="mm", font_size=38)
        
        # Corner Infos unten einblenden
        draw.text((540, 1280), "🎯 SHORT CORNER", fill=accent_color, anchor="mm", font_size=35)
        draw.text((540, 1340), f"Rausgabe: {raus}  |  Stopper: {stop}", fill=text_main_color, anchor="mm", font_size=32)
        draw.text((540, 1400), f"Schützen: {', '.join(schuss)}", fill=text_sub_color, anchor="mm", font_size=30)
        
        # Bank
        bank_str = ", ".join(moegliche_bank) if moegliche_bank else "Keine"
        draw.text((540, 1600), "🔄 WECHSELBANK", fill=accent_color, anchor="mm", font_size=32)
        draw.text((540, 1660), bank_str, fill=text_sub_color, anchor="mm", font_size=30)
        
        draw.text((540, 1840), f"Created via HockeyAI Studio", fill=text_sub_color, anchor="mm", font_size=22)
        
        # Bild-Vorschau in verkleinerter Form anzeigen
        st.image(img, caption=f"Vorschau: {design_typ}", width=380)
        
        # Download-Verarbeitung
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.download_button(
            label=f"💾 {design_typ} herunterladen",
            data=byte_im,
            file_name=f"hockey_{design_typ.lower().replace(' ', '_')}.png",
            mime="image/png",
            type="primary"
        )

# --- TAB 4: KARTEN-TIMER ---
with tab4:
    st.subheader("⏱️ Live Bank-Zeitstrafen")
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        karten_typ = st.radio("Karte:", ["🟢 Grün (2 Min)", "🟡 Gelb (5 Min)", "🟡 Gelb (10 Min)"])
        straf_spieler = st.selectbox("Spieler", kader, key="straf_sp")
    with t_col2:
        if st.button("Zeitstrafe registrieren"):
            st.warning(f"Uhr läuft für {straf_spieler}! Bitte Hallen-/Platzzeit beachten.")

# --- TAB 5: MANNSCHAFTSKASSE ---
with tab5:
    st.subheader("💰 Team-Strafenkatalog")
    s_col1, s_col2, s_col3 = st.columns([2, 2, 1])
    with s_col1:
        s_spieler = st.selectbox("Spieler", kader, key="money_sp")
    with s_col2:
        grund = st.selectbox("Vergehen", [
            "Zu spät zum Treff (5€)", "Grüne Karte (2€)", "Gelbe Karte (5€)", 
            "Ausrüstung vergessen (3€)", "Kasten vergessen (10€)"
        ])
    with s_col3:
        if st.button("Buchen"):
            betrag = grund.split("(")[1].split("€")[0]
            st.session_state["strafen"].append({"Spieler": s_spieler, "Grund": grund, "Betrag": int(betrag), "Datum": datetime.now().strftime("%d.%m.%y")})

    if st.session_state["strafen"]:
        df_strafen = pd.DataFrame(st.session_state["strafen"])
        st.table(df_strafen)
        st.metric("Kassenstand aktuell", f"{df_strafen['Betrag'].sum()} €")
        if st.button("Kasse zurücksetzen"):
            st.session_state["strafen"] = []
            st.rerun()

st.write("---")
st.caption("Hockey Command Center v4.0 • Pro Lineup-Builder & Multi-Export")
