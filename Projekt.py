import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io

# Seiteneinstellungen
st.set_page_config(page_title="Hockey Command Center", page_icon="🏑", layout="wide")

# --- SESSION STATE INITIALISIERUNG ---
if "players" not in st.session_state:
    st.session_state["players"] = ["TW (Max)"] + [f"Spieler {i}" for i in range(1, 15)]
if "strafen" not in st.session_state:
    st.session_state["strafen"] = []

# --- SIDEBAR: TEAM MANAGEMENT ---
st.sidebar.title("🏑 Team Management")
team_name = st.sidebar.text_input("Dein Team-Name", "Mein Hockey Club")
st.sidebar.markdown("---")

with st.sidebar.expander("👥 Kader bearbeiten"):
    player_input = st.text_area("Spielernamen (einer pro Zeile)", "\n".join(st.session_state["players"]))
    if st.button("Kader aktualisieren"):
        st.session_state["players"] = [p.strip() for p in player_input.split("\n") if p.strip()]
        st.success("Kader gespeichert!")

# --- HAUPTBEREICH ---
st.title(f"🏆 {team_name} - Command Center")
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Aufstellung & System", 
    "🎯 Corner Master", 
    "📸 Social Media Export",
    "⏱️ Karten & Zeitstrafen", 
    "💰 Mannschaftskasse"
])

# --- TAB 1: TAKTIK & LINEUP ---
with tab1:
    st.subheader("Match-Aufstellung & System")
    
    col_sys, col_press = st.columns(2)
    with col_sys:
        formation = st.selectbox("Grundformation:", [
            "3-4-3 (Klassisch)", "3-4-3 (Doppel-Sechs)", "4-3-3 (Defensiv)", 
            "3-5-2 (Mittelfeld-Dominanz)", "2-4-4 (Voll-Pressing)"
        ])
    with col_press:
        pressing = st.select_slider("Pressing-Linie:", options=["Viertel", "Halbfeld", "Dreiviertel", "Voll-Pressing"])

    st.write("---")
    kader = st.session_state["players"]
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### 🧤 Defensive")
        tw = st.selectbox("Torwart", kader, key="tw")
        def1 = st.selectbox("Verteidiger Links (VL)", kader, index=min(1, len(kader)-1), key="vl")
        def2 = st.selectbox("Verteidiger Zentrum (VZ)", kader, index=min(2, len(kader)-1), key="vz")
        def3 = st.selectbox("Verteidiger Rechts (VR)", kader, index=min(3, len(kader)-1), key="vr")
        
    with c2:
        st.markdown("#### 🧠 Mittelfeld")
        m1 = st.selectbox("Mittelfeld Links (ML)", kader, index=min(4, len(kader)-1), key="ml")
        m2 = st.selectbox("Mittelfeld Zentrum (MZ)", kader, index=min(5, len(kader)-1), key="mz")
        m3 = st.selectbox("Mittelfeld Rechts (MR)", kader, index=min(6, len(kader)-1), key="mr")

    with c3:
        st.markdown("#### ⚡ Sturm")
        s1 = st.selectbox("Stürmer Links (SL)", kader, index=min(7, len(kader)-1), key="sl")
        s2 = st.selectbox("Stürmer Zentrum (SZ)", kader, index=min(8, len(kader)-1), key="sz")
        s3 = st.selectbox("Stürmer Rechts (SR)", kader, index=min(9, len(kader)-1), key="sr")
    
    bench = st.multiselect("🔄 Wechselspieler (Bank):", kader, default=kader[10:min(14, len(kader))])

# --- TAB 2: CORNER MASTER (JETZT KORREKT IM EIGENEN TAB) ---
with tab2:
    st.subheader("🎯 Strafecken & Standardsituationen")
    st.write("Plane hier eure Ecken-Varianten für das nächste Match.")
    
    e_col1, e_col2 = st.columns(2)
    with e_col1:
        st.markdown("### 🟢 Eigene Ecken (Offensiv)")
        raus = st.selectbox("Rausgeber", kader, key="raus")
        stop = st.selectbox("Stopper", kader, key="stop")
        schuss = st.multiselect("Schützen", kader, default=[kader[min(2, len(kader)-1)]])
        variante = st.text_area("Ablauf / Variante", "Direkter Schlenzer oben rechts oder Ablage auf den Rechtsstecher.")
        
    with e_col2:
        st.markdown("### 🔴 Gegnerische Ecken (Defensiv)")
        w1 = st.selectbox("1. Welle (Abläufer)", kader, key="w1")
        w2 = st.selectbox("2. Welle", kader, key="w2")
        posten = st.selectbox("Linien-Posten", kader, key="posten")
        def_info = st.text_area("Defensiv-Notiz", "Torwart sichert die Stockseite, 1. Welle läuft voll auf den Schützen.")

# --- TAB 3: SOCIAL MEDIA EXPORT (GENERIEREN ALS BILD) ---
with tab3:
    st.subheader("📸 Matchday-Grafik für Instagram & Co.")
    st.write("Generiere eine saubere Grafik im Story-Format zum direkten Download.")
    
    gegner_media = st.text_input("Gegner für die Grafik:", "Mannheimer HC")
    
    if st.button("🚀 Grafik generieren"):
        # Erstelle ein leeres Bild (Instagram Story Format: 1080 x 1920)
        img = Image.new("RGB", (1080, 1920), color="#1e3d2f") # Hockey-Grün
        draw = ImageDraw.Draw(img)
        
        # Einfache Formen zeichnen (Spielfeld-Look)
        draw.rectangle([40, 40, 1040, 1880], outline="#ffffff", width=8) # Außenlinie
        draw.line([40, 960, 1040, 960], fill="#ffffff", width=5) # Mittellinie
        draw.arc([340, 40, 740, 300], start=0, end=180, fill="#ffffff", width=5) # Schusskreis oben
        draw.arc([340, 1660, 740, 1920], start=180, end=0, fill="#ffffff", width=5) # Schusskreis unten
        
        # Text auf das Bild schreiben (Nutzt Standard-Schriftart, falls keine TrueType verfügbar)
        draw.text((540, 150), f"MATCHDAY", fill="#ffffff", anchor="mm", font_size=70)
        draw.text((540, 240), f"{team_name} vs {gegner_media}", fill="#ffcc00", anchor="mm", font_size=45)
        
        # Aufstellung aufschreiben
        draw.text((540, 400), "--- AUFSTELLUNG ---", fill="#ffffff", anchor="mm", font_size=40)
        draw.text((540, 500), f"🧤 TW: {tw}", fill="#ffffff", anchor="mm", font_size=35)
        draw.text((540, 600), f"🛡️ ABWEHR: {def1} | {def2} | {def3}", fill="#ffffff", anchor="mm", font_size=35)
        draw.text((540, 700), f"🧠 MITTELFLD: {m1} | {m2} | {m3}", fill="#ffffff", anchor="mm", font_size=35)
        draw.text((540, 800), f"⚡ STURM: {s1} | {s2} | {s3}", fill="#ffffff", anchor="mm", font_size=35)
        
        # Corner Master Infos hinzufügen
        draw.text((540, 1050), "--- CORNER MASTER ---", fill="#ffffff", anchor="mm", font_size=40)
        draw.text((540, 1150), f"📥 Rausgabe: {raus}  |  🛑 Stop: {stop}", fill="#ffffff", anchor="mm", font_size=32)
        schuetzen_str = ", ".join(schusch) if 'schusch' in locals() else ", ".join(schuss)
        draw.text((540, 1230), f"🎯 Schützen: {schuetzen_str}", fill="#ffffff", anchor="mm", font_size=32)
        draw.text((540, 1310), f"🏃‍♂️ 1. Welle (Defensiv): {w1}", fill="#ffffff", anchor="mm", font_size=32)
        
        # Bank
        bank_str = ", ".join(bench) if bench else "Keine"
        draw.text((540, 1550), f"🔄 Bank: {bank_str}", fill="#aaaaaa", anchor="mm", font_size=30)
        
        draw.text((540, 1800), "Generiert mit HockeyAI Command Center", fill="#ffffff", anchor="mm", font_size=25)
        
        # Bild in Streamlit anzeigen
        st.image(img, caption="Deine fertige Story-Grafik", width=400)
        
        # Download Button vorbereiten
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.download_button(
            label="💾 Grafik für Instagram herunterladen",
            data=byte_im,
            file_name="hockey_matchday_story.png",
            mime="image/png",
            type="primary"
        )

# --- TAB 4: KARTEN-TIMER ---
with tab4:
    st.subheader("⏱️ Live Karten-Strafen")
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        karten_typ = st.radio("Karten-Typ", ["🟢 Grün (2 Min)", "🟡 Gelb (5 Min)", "🟡 Gelb (10 Min)"])
        straf_spieler = st.selectbox("Spieler", kader, key="straf_sp")
    with t_col2:
        if st.button("Strafe auf Bank absitzen"):
            st.warning(f"Zeitstrafe läuft für {straf_spieler}!")
            st.info("Bitte die Hallen-/Platz-Uhr entsprechend im Auge behalten.")

# --- TAB 5: MANNSCHAFTSKASSE ---
with tab5:
    st.subheader("💰 Team-Strafenkatalog")
    s_col1, s_col2, s_col3 = st.columns([2, 2, 1])
    with s_col1:
        s_spieler = st.selectbox("Spieler", kader, key="money_sp")
    with s_col2:
        grund = st.selectbox("Grund", [
            "Zu spät zum Treff (5€)", "Grüne Karte (2€)", "Gelbe Karte (5€)", 
            "Ausrüstung vergessen (3€)", "Kasten vergessen (10€)"
        ])
    with s_col3:
        if st.button("Eintragen"):
            betrag = grund.split("(")[1].split("€")[0]
            st.session_state["strafen"].append({"Spieler": s_spieler, "Grund": grund, "Betrag": int(betrag), "Datum": datetime.now().strftime("%d.%m.%y")})

    if st.session_state["strafen"]:
        df_strafen = pd.DataFrame(st.session_state["strafen"])
        st.table(df_strafen)
        st.metric("Gesamtstand Kasse", f"{df_strafen['Betrag'].sum()} €")
        if st.button("Kasse leeren"):
            st.session_state["strafen"] = []
            st.rerun()

st.write("---")
st.caption(f"Hockey Command Center v3.0 | 100% verlässlich und ohne API-Sperren")
