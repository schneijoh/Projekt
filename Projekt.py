import streamlit as st
import pandas as pd
import time
from datetime import datetime

# Seiteneinstellungen
st.set_page_config(page_title="Hockey Command Center", page_icon="🏑", layout="wide")

# Styling für Hockey-Vibe
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE INITIALISIERUNG ---
if "players" not in st.session_state:
    st.session_state["players"] = ["TW (Name hier)"] + [f"Spieler {i}" for i in range(1, 15)]
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

# --- HAUPTBEREICH: TABS ---
st.title(f"🏆 {team_name} - Command Center")
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Taktik & Lineup", 
    "🎯 Corner Master", 
    "⏱️ Karten & Zeitstrafen", 
    "💰 Mannschaftskasse"
])

# --- TAB 1: TAKTIK & LINEUP ---
with tab1:
    st.subheader("Match-Aufstellung & System")
    
    col_sys, col_press = st.columns(2)
    with col_sys:
        formation = st.selectbox("Grundformation:", [
            "3-4-3 (Klassisches System)",
            "3-4-3 (Doppel-Sechs)",
            "4-3-3 (Defensiv-Stabilität)",
            "3-5-2 (Überzahl Mittelfeld)",
            "2-4-4 (Extremes Pressing)",
            "5-3-2 (Schotten-Dicht)"
        ])
    with col_press:
        pressing = st.select_slider("Pressing-Linie:", options=["Viertel", "Halbfeld", "Dreiviertel", "Voll-Pressing"])

    st.write("---")
    kader = st.session_state["players"]
    
    # Positionen visuell gruppiert
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### 🧤 Defensive")
        tw = st.selectbox("Torwart", kader, key="tw")
        def1 = st.selectbox("VL", kader, index=1, key="vl")
        def2 = st.selectbox("VZ", kader, index=2, key="vz")
        def3 = st.selectbox("VR", kader, index=3, key="vr")
        
    with c2:
        st.markdown("#### 🧠 Mittelfeld")
        m1 = st.selectbox("ML", kader, index=4, key="ml")
        m2 = st.selectbox("MZ (Zentrum)", kader, index=5, key="mz")
        m3 = st.selectbox("MR", kader, index=6, key="mr")
        m4 = st.selectbox("MA (Aufbau)", kader, index=7, key="ma")

    with c3:
        st.markdown("#### ⚡ Sturm")
        s1 = st.selectbox("SL", kader, index=8, key="sl")
        s2 = st.selectbox("SZ", kader, index=9, key="sz")
        s3 = st.selectbox("SR", kader, index=10, key="sr")
    
    st.multiselect("🔄 Wechselspieler (Bank):", kader, default=kader[11:min(15, len(kader))])

# --- TAB 2: CORNER MASTER ---
with tab1: # Wir fügen Corner-Info direkt im Taktik Tab hinzu für den Aushang
    st.write("---")
    st.subheader("🎯 Strafecken & Standards")
    e_col1, e_col2 = st.columns(2)
    with e_col1:
        st.info("Eigene Ecken (Offensiv)")
        raus = st.selectbox("Rausgeber", kader, key="raus")
        stop = st.selectbox("Stopper", kader, key="stop")
        schuss = st.multiselect("Schützen (Schlag/Schlenz)", kader, default=[kader[2]])
    with e_col2:
        st.error("Gegnerische Ecken (Defensiv)")
        st.selectbox("Abläufer (1. Welle)", kader, key="w1")
        st.selectbox("2. Welle / Posten", kader, key="w2")

# --- TAB 3: KARTEN-TIMER ---
with tab3:
    st.subheader("⏱️ Live Karten-Strafen Timer")
    st.write("Verwalte die Zeitstrafen während des Spiels.")
    
    t_col1, t_col2, t_col3 = st.columns(3)
    with t_col1:
        karten_typ = st.radio("Karten-Typ", ["🟢 Grün (2 Min)", "🟡 Gelb (5 Min)", "🟡 Gelb (10 Min)"])
    with t_col2:
        straf_spieler = st.selectbox("Spieler auf der Bank", kader, key="straf_sp")
    with t_col3:
        if st.button("Strafe starten"):
            st.warning(f"Timer für {straf_spieler} läuft! (In der Kabine bitte Uhr beachten)")
            # In einer echten App würde man hier Zeit berechnen, hier als Info:
            finish_time = "2 Min" if "Grün" in karten_typ else ("5 Min" if "5" in karten_typ else "10 Min")
            st.write(f"Wieder rein um: **{finish_time} nach Absitzen**")

# --- TAB 4: MANNSCHAFTSKASSE ---
with tab4:
    st.subheader("💰 Team-Strafenkatalog")
    
    s_col1, s_col2, s_col3 = st.columns([2, 2, 1])
    with s_col1:
        s_spieler = st.selectbox("Wer hat gesündigt?", kader, key="money_sp")
    with s_col2:
        grund = st.selectbox("Grund", [
            "Zu spät zum Treff (5€)", 
            "Grüne Karte (2€)", 
            "Gelbe Karte (5€)", 
            "Ausrüstung vergessen (3€)", 
            "Handy in der Kabine (2€)",
            "Kasten vergessen (10€)"
        ])
    with s_col3:
        if st.button("Eintragen"):
            betrag = grund.split("(")[1].split("€")[0]
            st.session_state["strafen"].append({"Spieler": s_spieler, "Grund": grund, "Betrag": int(betrag), "Datum": datetime.now().strftime("%d.%m.%y")})

    if st.session_state["strafen"]:
        df_strafen = pd.DataFrame(st.session_state["strafen"])
        st.table(df_strafen)
        st.metric("Gesamtstand Kasse", f"{df_strafen['Betrag'].sum()} €")
        if st.button("Kasse leeren (Saisonende)"):
            st.session_state["strafen"] = []
            st.rerun()

# Footer
st.write("---")
st.caption(f"Hockey Command Center v2.0 | Entwickelt für {team_name} | Läuft stabil ohne API-Token")
