import streamlit as st
import pandas as pd

st.set_page_config(page_title="Hockey Tactical Studio", page_icon="🏑", layout="wide")

st.title("🏑 Hockey Tactical Studio")
st.caption("Professioneller Matchplaner & Lineup-Creator für Feldhockey")

# --- SESSIONS STATE FÜR SPIELER LISTE ---
if "players" not in st.session_state:
    st.session_state["players"] = [
        "Max (TW)", "Anna", "Lisa", "Tom", "Ben", 
        "Felix", "Marie", "Lukas", "Emma", "Tim", "Jan"
    ]

# --- SIDEBAR: KADERMANAGEMENT ---
st.sidebar.header("👥 Kader verwalten")
new_player = st.sidebar.text_input("Spieler hinzufügen")
if st.sidebar.button("Hinzufügen") and new_player:
    st.session_state["players"].append(new_player)
    st.rerun()

if st.sidebar.button("🗑️ Kader zurücksetzen"):
    st.session_state["players"] = ["Standard TW"] + [f"Feldspieler {i}" for i in range(1, 11)]
    st.rerun()

# --- HAUPTBEREICH: TABS FÜR STRATEGIE ---
tab1, tab2, tab3 = st.tabs(["📋 Aufstellung & Formation", "🎯 Matchplan & Taktik", "🖨️ Export & Drucken"])

# --- TAB 1: FORMATION ---
with tab1:
    st.subheader("Team-Aufstellung festlegen")
    
    col_form, col_opp = st.columns(2)
    with col_form:
        formation = st.selectbox(
            "Wähle deine Spielphilosophie (Formation):",
            ["3-4-3 (Klassisch)", "4-3-3 (Defensiver)", "3-5-2 (Mittelfeld-Dominanz)", "2-4-4 (Volles Pressing)"]
        )
    with col_opp:
        gegner = st.text_input("Gegnerischer Verein", "Mannheimer HC")

    st.write("---")
    st.markdown("### 🏃‍♂️ Positionen besetzen")
    
    # Dynamische Zuweisung basierend auf dem Kader
    kader = st.session_state["players"]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.info("🧤 Tor & Abwehr")
        tw = st.selectbox("Torwart (TW)", kader, index=0 if len(kader) > 0 else 0)
        def1 = st.selectbox("Verteidiger links", kader, index=min(1, len(kader)-1))
        def2 = st.selectbox("Verteidiger zentral", kader, index=min(2, len(kader)-1))
        def3 = st.selectbox("Verteidiger rechts", kader, index=min(3, len(kader)-1))

    with col2:
        st.success("🧠 Mittelfeld")
        mid1 = st.selectbox("Mittelfeld links", kader, index=min(4, len(kader)-1))
        mid2 = st.selectbox("Zentrales Mittelfeld", kader, index=min(5, len(kader)-1))
        mid3 = st.selectbox("Mittelfeld rechts", kader, index=min(6, len(kader)-1))

    with col3:
        st.warning("⚡ Sturm")
        sturm1 = st.selectbox("Stürmer links", kader, index=min(7, len(kader)-1))
        sturm2 = st.selectbox("Mittelstürmer", kader, index=min(8, len(kader)-1))
        sturm3 = st.selectbox("Stürmer rechts", kader, index=min(9, len(kader)-1))
        
    with col4:
        st.error("🔄 Bank / Wechselspieler")
        bench = st.multiselect("Auswechselspieler", kader, default=[kader[-1]] if len(kader) > 10 else None)

# --- TAB 2: TAKTIK ---
with tab2:
    st.subheader("Match-Strategie & Standardsituationen")
    
    col_taktik1, col_taktik2 = st.columns(2)
    
    with col_taktik1:
        st.markdown("### 🏑 Strafecken (Hausecken)")
        ecken_schuetze = st.text_input("Schütze (Rausgeber/Schlager)", "Anna (Rausgabe) • Tom (Schlag)")
        ecken_variante = st.text_area("Variante / Ablauf", "Direkter Schlenzer auf die passive Torwartseite oder Ablage auf den Rechtsstecher.")
        
        st.markdown("### 🛡️ Defensiv-Verhalten")
        def_style = st.radio("Defensiv-System:", ["Halbfeld-Pressing", "Viertel-Pressing", "Manndeckung (Aggressiv)", "Raumdeckung"])

    with col_taktik2:
        st.markdown("### 📝 Trainer-Notizen für die Kabinenansprache")
        ansprache = st.text_area(
            "Wichtige Punkte:", 
            "1. Schnelles Umschaltspiel nach Ballgewinn.\n2. Gegner bei eigenem Abschlag früh unter Druck setzen.\n3. Keine unnötigen Karten riskieren!"
        )
        
        st.markdown("### ⏱️ Viertel-Fokus")
        v1 = st.text_input("1. & 2. Viertel", "Konzentrierter Aufbau, Ball laufen lassen")
        v2 = st.text_input("3. & 4. Viertel", "Gegner müde spielen, Konter absichern")

# --- TAB 3: EXPORT ---
with tab3:
    st.subheader("📋 Fertiger Matchplan (Übersicht)")
    
    # HTML/Markdown-Tabelle für eine schöne Druckansicht
    matchplan_data = {
        "Kategorie": ["Gegner", "Formation", "Torwart", "Abwehr", "Mittelfeld", "Sturm", "Wechselbank", "Strafecke", "Defensiv-Taktik"],
        "Details":
