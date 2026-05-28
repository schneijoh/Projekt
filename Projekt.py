import streamlit as st

st.set_page_config(page_title="HockeyAI Studio", page_icon="🏑", layout="wide")

st.title("🏑 HockeyAI Studio")
st.caption("Stabile kostenlose Version (ohne API-Probleme)")

tab1, tab2, tab3 = st.tabs(["🎮 GameDay Blitz", "💡 Ideen", "📝 Captions"])

with tab1:
    st.subheader("GameDay Blitz")
    
    col1, col2 = st.columns(2)
    with col1:
        score = st.text_input("Ergebnis", "4:2")
        opponent = st.text_input("Gegner", "Mannheimer HC")
    with col2:
        scorers = st.text_area("Torschützen", "Thore Waaden - 1\nJohan Schneider - 3")
        moments = st.text_area("Besondere Momente", "Starke Strafecken • Comeback")

    if st.button("🚀 GameDay Zusammenfassung erstellen", type="primary"):
        st.success("✅ Zusammenfassung (Demo)")
        st.write(f"**Spielbericht:**")
        st.write(f"Starker Sieg mit {score} gegen {opponent}!")
        st.write(f"Torschützen: {scorers}")
        st.write(f"Highlight: {moments}")
        st.write("\n**Mögliche Caption:**")
        st.write(f"Unglaublicher Kampf! 🔥 {score} Sieg gegen {opponent}! Die Jungs haben alles gegeben! #Feldhockey")

with tab2:
    st.subheader("Reel & Story Ideen")
    if st.button("Ideen anzeigen"):
        st.write("**8 Reel / Story Ideen:**")
        ideas = [
            "1. Slow-Motion der besten Strafecken",
            "2. Torschützen Montage mit Torjubel",
            "3. Before & After Comeback",
            "4. Fan-Reaktionen auf der Tribüne",
            "5. Spieler des Spiels Interview",
            "6. Top 5 Saves des Torwarts",
            "7. Team-Huddle nach dem Sieg",
            "8. Next Game Teaser"
        ]
        for idea in ideas:
            st.write(idea)

with tab3:
    st.subheader("Caption Generator")
    if st.button("Captions generieren"):
        st.write("**6 mögliche Captions:**")
        captions = [
            f"💪 {score} Sieg gegen {opponent}! Die Mannschaft hat gekämpft wie Löwen! 🔥",
            f"Strafecken-Monster! {scorers} – was für ein Spiel! 🏑",
            f"Von Rückstand zum Sieg! Starkes Comeback heute! ❤️",
            f"Der Rasen brannte heute! Unglaubliche Leistung! #Feldhockey",
            f"Next one loading... Wir sind bereit! 🔥",
            f"Danke an alle Fans für die Unterstützung! Ihr wart der 12. Mann!"
        ]
        for cap in captions:
            st.write(cap)

st.caption("Kostenlose stabile Version – ohne externe API")
st.info("Sobald du einen guten Endpoint oder lokale Installation hast, können wir Bilder hinzufügen.")
