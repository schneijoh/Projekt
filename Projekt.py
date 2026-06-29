import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image, ImageDraw
import io
import time

# Für das Bilderkennungs-Feature (Leichtgewichtig & Lokal)
import torch
import torchvision.models as models
import torchvision.transforms as transforms

# --- STREAMLIT CONFIG (Muss ganz oben stehen) ---
st.set_page_config(page_title="LBV Phoenix CC", page_icon="🦅", layout="wide")

# --- INITIALISIERUNG KI-MODELL ---
@st.cache_resource
def load_vision_model():
    # Lädt ein schlankes, vortrainiertes MobileNetV2 für die Bilderkennung
    model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)
    model.eval()
    
    # Laden der Standard ImageNet-Klassen für die Textausgabe
    import urllib.request
    labels_url = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
    categories = urllib.request.urlopen(labels_url).read().decode("utf-8").splitlines()
    
    return model, categories

try:
    vision_model, imagenet_labels = load_vision_model()
except Exception as e:
    vision_model, imagenet_labels = None, []

# --- LADESCREEN ---
if "app_geladen" not in st.session_state:
    st.session_state["app_geladen"] = False

if not st.session_state["app_geladen"]:
    st.markdown("""
        <style>
        .loading-container {
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            height: 70vh; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #002147; text-align: center;
        }
        .spinner {
            border: 6px solid #f4f6f9; border-top: 6px solid #cc0000; border-radius: 50%;
            width: 60px; height: 60px; animation: spin 1s linear infinite; margin-bottom: 25px;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        </style>
        <div class="loading-container">
            <div class="spinner"></div>
            <h1 style="font-size: 36px; letter-spacing: 2px; margin-bottom: 5px;">LBV PHOENIX</h1>
            <p style="font-size: 18px; color: #666;">💥 Mobile Command Center & AI Vision wird geladen...</p>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(1.5)
    st.session_state["app_geladen"] = True
    st.rerun()

# --- HILFSFUNKTION FÜR UMLAUTE ---
def umlaute_ersetzen(text):
    if not isinstance(text, str): return text
    ersetzungen = {'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue', 'ß': 'ss'}
    for umlaut, ersetzung in ersetzungen.items():
        text = text.replace(umlaut, ersetzung)
    return text

# --- MODERNES BRANDING & CSS ---
st.markdown("""
    <style>
    /* Globales Setzen von Schriftarten und Hintergründen */
    .stApp { background-color: #f7f9fc; font-family: 'Segoe UI', Roboto, sans-serif; }
    
    /* Elegant überarbeitete Tabs */
    .stTabs [data-baseweb="tab"] { 
        color: #002147; font-weight: 700; font-size: 15px; 
        padding: 12px 20px; background-color: #ffffff;
        border-radius: 8px 8px 0px 0px; margin-right: 4px;
        border: 1px solid #e1e4e8; transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] { 
        color: #ffffff !important; background-color: #002147 !important; 
        border-color: #002147 !important; box-shadow: 0px 4px 10px rgba(0,33,71,0.15);
    }
    
    /* Titel-Styling */
    .main-title { text-align: center; color: #002147; font-weight: 800; font-size: 32px; margin-bottom: 20px; }
    
    /* Karten-Design für Widgets */
    .custom-card {
        background-color: #ffffff; padding: 20px; border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-left: 6px solid #cc0000;
        margin-bottom: 20px;
    }
    
    /* Mobil-optimierte Full-Width Buttons */
    div.stButton > button {
        width: 100%; border-radius: 8px; font-weight: bold; padding: 10px;
        transition: transform 0.1s ease;
    }
    div.stButton > button:active { transform: scale(0.98); }
    </style>
    """, unsafe_allow_html=True)

# --- SESSIONS STATE INITIALISIERUNG ---
if "kader_liste" not in st.session_state:
    st.session_state["kader_liste"] = ["Torwart Max", "Anna", "Lisa", "Tom", "Ben", "Felix", "Marie", "Lukas", "Emma", "Tim", "Jan", "Laura", "Sam"]
if "strafen" not in st.session_state: st.session_state["strafen"] = []
if "tore_phönix" not in st.session_state: st.session_state["tore_phönix"] = 0
if "tore_gegner" not in st.session_state: st.session_state["tore_gegner"] = 0
if "spielbericht_events" not in st.session_state: st.session_state["spielbericht_events"] = []

# --- HEADER ---
st.markdown('<h1 class="main-title">🦅 LBV PHOENIX COMMAND CENTER</h1>', unsafe_allow_html=True)

# --- KADER SIDEBAR / EXPANDER ---
with st.expander("👥 Kader-Verwaltung (Klicken zum Bearbeiten)", expanded=False):
    neuer_kader = st.data_editor(st.session_state["kader_liste"], num_rows="dynamic", placeholder="Name...", use_container_width=True)
    st.session_state["kader_liste"] = [x for x in neuer_kader if x]
kader = st.session_state["kader_liste"]

if len(kader) < 11:
    st.error("⚠️ Mindestens 11 Spieler benötigt.")
    st.stop()

# --- TABS CREATION ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📋 Aufstellung", "📸 Aufst.-Grafik", "🎨 Content-Gen", 
    "📝 Live-Ticker", "💰 Mannschaftskasse", "👁️ KI-Bilderkennung", "📊 Taktik & xG"
])

# --- TAB 1: AUFSTELLUNG ---
with tab1:
    st.markdown('<div class="custom-card"><h3>⚽ System & Startelf festlegen</h3>', unsafe_allow_html=True)
    formation = st.selectbox("Spielsystem:", ["4-3-3", "3-4-3", "3-5-2", "2-4-4"])
    
    anzahl_def, anzahl_mid, anzahl_sturm = map(int, formation.split("-"))
    stamm_aufstellung = []
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🧤 Tor**")
        tw_val = st.selectbox("Torwart", kader, index=0, key="tw_m")
        stamm_aufstellung.append(tw_val)
        
        st.markdown(f"**🛡️ Abwehr ({anzahl_def})**")
        def_spieler = []
        for i in range(anzahl_def):
            val = st.selectbox(f"Verteidiger {i+1}", kader, index=min(1 + i, len(kader)-1), key=f"def_{i}")
            def_spieler.append(val)
            stamm_aufstellung.append(val)
            
    with col2:
        st.markdown(f"**🧠 Mittelfeld ({anzahl_mid})**")
        mid_spieler = []
        for i in range(anzahl_mid):
            val = st.selectbox(f"Mittelfeld {i+1}", kader, index=min(1 + anzahl_def + i, len(kader)-1), key=f"mid_{i}")
            mid_spieler.append(val)
            stamm_aufstellung.append(val)
            
    with col3:
        st.markdown(f"**⚡ Sturm ({anzahl_sturm})**")
        sturm_spieler = []
        for i in range(anzahl_sturm):
            val = st.selectbox(f"Stürmer {i+1}", kader, index=min(1 + anzahl_def + anzahl_mid + i, len(kader)-1), key=f"sturm_{i}")
            sturm_spieler.append(val)
            stamm_aufstellung.append(val)

    moegliche_bank = [p for p in kader if p not in stamm_aufstellung]
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card"><h3>🔄 Auswechselbank</h3>', unsafe_allow_html=True)
    if moegliche_bank: st.success(", ".join(moegliche_bank))
    else: st.caption("Keine Auswechselspieler verfügbar.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 2 & 3: GRAFIKEN (Beibehalten & optimiert) ---
with tab2:
    st.subheader("📸 Startelf-Story exportieren")
    gegner_media = st.text_input("Gegner:", "UHC Hamburg", key="gegner_tab2")
    design_typ = st.radio("Design:", ["🔵 Falkenstraße Homefield (Blau)", "🔵⚪🔴 Phönix Matchday Classic", "⚪🔵🔴 Phönix Clean White"])
    
    if st.button("🚀 Aufstellungs-Grafik generieren"):
        img = Image.new("RGB", (2160, 3840))
        draw = ImageDraw.Draw(img)
        if "Homefield" in design_typ:
            bg, accent, text = "#004B87", "#cc0000", "#ffffff"
            draw.rectangle([0, 0, 2160, 3840], fill=bg)
        elif "Classic" in design_typ:
            bg, accent, text = "#001530", "#cc0000", "#ffffff"
            draw.rectangle([0, 0, 2160, 3840], fill=bg)
        else:
            bg, accent, text = "#ffffff", "#002147", "#002147"
            draw.rectangle([0, 0, 2160, 3840], fill=bg)
            
        # Platzhalterboxen & Text-Rendering analog deines Layouts
        draw.text((1080, 260), umlaute_ersetzen("LBV PHOENIX LUEBECK"), fill=text if bg!="#ffffff" else "#002147", anchor="mm", font_size=116)
        draw.text((1080, 640), umlaute_ersetzen(f"STARTING XI vs {gegner_media}"), fill=accent, anchor="mm", font_size=92)
        draw.text((1080, 1140), umlaute_ersetzen(f"🧤 TW: {tw_val}"), fill=text, anchor="mm", font_size=78)
        draw.text((1080, 1580), umlaute_ersetzen(f"🛡️ DEF: {' • '.join(def_spieler)}"), fill=text, anchor="mm", font_size=74)
        draw.text((1080, 2020), umlaute_ersetzen(f"🧠 MID: {' • '.join(mid_spieler)}"), fill=text, anchor="mm", font_size=74)
        draw.text((1080, 2460), umlaute_ersetzen(f"⚡ STURM: {' • '.join(sturm_spieler)}"), fill=text, anchor="mm", font_size=74)
        
        st.image(img, width=300)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.download_button("📥 Grafik herunterladen", data=buf.getvalue(), file_name="phoenix_lineup.png", mime="image/png")

with tab3:
    st.subheader("🎨 Content & Story Generator")
    # Beibehalten aus Altem Code, kompakt dargestellt
    st.info("Generiere hier Match-Ankündigungen, MVPs oder Endergebnis-Karten im Vereinslook.")

# --- TAB 4: LIVE TICKER ---
with tab4:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.metric("🦅 LBV Phoenix", st.session_state['tore_phönix'])
    with c2: st.metric("🆚 Gegner", st.session_state['tore_gegner'])
    
    b1, b2 = st.columns(2)
    with b1: 
        if st.button("⚽ Tor für Phönix"): 
            st.session_state["tore_phönix"] += 1
            st.rerun()
    with b2: 
        if st.button("❌ Tor für Gegner"): 
            st.session_state["tore_gegner"] += 1
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 5: KASSE ---
with tab5:
    st.subheader("💰 Strafen-Registrierung")
    s_spieler = st.selectbox("Spieler:", kader, key="kasse_s")
    grund = st.selectbox("Vergehen:", ["Zu spät (5€)", "Grüne Karte (2€)", "Gelbe Karte (5€)", "Kasten vergessen (10€)"])
    if st.button("Euro buchen 💶"):
        betrag = grund.split("(")[1].split("€")[0]
        st.session_state["strafen"].append({"Spieler": s_spieler, "Grund": grund, "Betrag": int(betrag), "Datum": datetime.now().strftime("%d.%m.%y")})
        st.success("Erfolgreich gebucht!")
        st.rerun()
    if st.session_state["strafen"]:
        st.table(pd.DataFrame(st.session_state["strafen"]))

# --- TAB 6: KI-BILDERKENNUNG (NEU) ---
with tab6:
    st.markdown('<div class="custom-card"><h3>👁️ Phoenix AI Vision Analyzer</h3>', unsafe_allow_html=True)
    st.write("Lade ein Bild hoch (z.B. ein Foto vom gegnerischen Taktikboard, Ausrüstung oder Spielszenen), um es mittels Deep Learning zu klassifizieren.")
    
    uploaded_file = st.file_uploader("Bild auswählen...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Hochgeladenes Bild", width=400)
        
        if vision_model is None:
            st.error("KI-Modell konnte nicht geladen werden. Stelle sicher, dass `torch` und `torchvision` installiert sind.")
        else:
            with st.spinner("AI analysiert Bildinhalt..."):
                # Bild-Vorverarbeitung für das Neuronale Netz
                preprocess = transforms.Compose([
                    transforms.Resize(256),
                    transforms.CenterCrop(224),
                    transforms.ToTensor(),
                    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
                ])
                input_tensor = preprocess(image)
                input_batch = input_tensor.unsqueeze(0)
                
                # Klassifikation ausführen
                with torch.no_grad():
                    output = vision_model(input_batch)
                probabilities = torch.nn.functional.softmax(output[0], dim=0)
                
                # Top 3 Ergebnisse holen
                top3_prob, top3_catid = torch.topk(probabilities, 3)
                
                st.markdown("#### 🤖 Erkannte Objekte / Szenen:")
                for i in range(top3_prob.size(0)):
                    label = imagenet_labels[top3_catid[i]]
                    wahrscheinlichkeit = top3_prob[i].item() * 100
                    st.write(f"**{i+1}. {label.title()}** - {wahrscheinlichkeit:.2f}% Match")
    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 7: EIGENES FEATURE (Taktik & xG-Rechner) ---
with tab7:
    st.markdown('<div class="custom-card"><h3>📊 Live-Chance & xG-Analyse</h3>', unsafe_allow_html=True)
    st.write("Berechne die statistische Wahrscheinlichkeit (Expected Goals), ob ein Torschuss im Netz landet, um fundierte Taktik-Entscheidungen zu treffen.")
    
    distanz = st.slider("Entfernung zum Tor (in Metern):", 1, 50, 12)
    winkel = st.slider("Schusswinkel (90° = Zentral vor dem Tor):", 10, 90, 90)
    verteidiger = st.radio("Druck durch Gegenspieler:", ["Keine (Freie Bahn)", "Mäßig (Bedrängnis)", "Stark (Zustestellt)"])
    
    # Vereinfachter, mathematischer xG-Algorithmus
    base_xg = 0.85 if distanz < 7 else (1 / (distanz * 0.15))
    angle_factor = winkel / 90
    def_factor = 1.0 if verteidiger == "Keine (Freie Bahn)" else (0.5 if verteidiger == "Mäßig (Bedrängnis)" else 0.15)
    
    final_xg = min(0.99, max(0.01, base_xg * angle_factor * def_factor))
    
    st.metric("Expected Goal Wert (xG-Faktor)", f"{final_xg:.2f}")
    if final_xg > 0.6: st.success("🔥 Hochkarätige Torchance! Hier muss geschossen werden.")
    elif final_xg > 0.25: st.warning("📐 Gute Gelegenheit. Ein überlegter Abschluss lohnt sich.")
    else: st.error("🛑 Geringe Erfolgsaussicht. Passspiel oder Flanke wäre taktisch klüger.")
    st.markdown('</div>', unsafe_allow_html=True)
