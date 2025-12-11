import streamlit as st
import time
import sys

st.set_page_config(page_title="CineMate", page_icon="🎬")

st.title("🎬 CineMate — Dein digitaler Film-Finder")

st.markdown("""
👋 Hallo!

🎥 Ich bin CineMate – dein digitaler Film-Finder. Schön, dass du hier bist! Ich helfe dir gerne, den perfekten Film für deinen Abend zu finden. 🍿

Zunächst: Sag mir bitte, worauf du heute Lust hast. Wähle bitte drei von sechs Genres — ganz intuitiv, basierend darauf, was für dich interessant ist.
""")

genres = ["Komödie", "Drama", "Action", "Science-Fiction", "Horror", "Thriller"]

selected = st.multiselect("Genre auswählen", options=genres)

if not selected:
    st.info("Wähle drei Genres, damit ich anfangen kann. Beispiele: Komödie, Drama, Action...")

if selected and len(selected) != 3:
    st.warning("Bitte wähle genau drei Genres — das hilft mir, eine präzise Empfehlung zu erstellen.")

# Filmdetails
era = st.selectbox("Ära oder Erscheinungszeitraum:", ("Klassiker (<2000)", "Modern (2000+)") )
style = st.radio("Visueller Stil:", ("Realfilm", "Animation", "Schwarz-Weiß"))

runtime = st.slider("Laufzeit (Minuten)", min_value=60, max_value=240, value=(90, 120), step=1)

rating_min, rating_max = st.slider("IMDb-Rating (Bereich)", min_value=1.0, max_value=10.0, value=(6.0, 8.5), step=0.1)

# Validierung der Rating-Eingabe (angepasst wie gewünscht)
if rating_min < 1 or rating_max > 10:
    st.error("IMDb-Rating muss zwischen 1.0 und 10.0 liegen.")

search = st.button("Empfehlung generieren 🎯")

if search:
    st.markdown("---")
    st.markdown("Detailauswahl abgeschlossen — danke! Ich werte jetzt deine Präferenzen aus und suche passende Filme.")

    # Definiere Traits basierend auf Genre-Auswahl (Platzhalter, falls weniger als 3 gewählt wurden)
    trait1 = selected[0] if len(selected) > 0 else "(keine Auswahl)"
    trait2 = selected[1] if len(selected) > 1 else "(keine Auswahl)"
    trait3 = selected[2] if len(selected) > 2 else "(keine Auswahl)"

    cfg = f"Ära: {era} | Stil: {style} | Laufzeit: {runtime[0]}-{runtime[1]} min | IMDb: {rating_min}-{rating_max}"

    # Platzhalter-Filmtitel für die Demonstration
    top = "Chronos V"
    mid = "Das letzte Echo"
    last = "Schatten im Nebel"

    steps = [
        f"🔎 Ich werte deine Präferenzen aus und erstelle ein Ranking. Du hast Lust auf: {trait1}, {trait2} und {trait3}.",
        f"🎬 Deine Konfiguration ({cfg}) ist meine Grundlage. Ich durchforste meine Film-Datenbank nach passenden Streifen...",
        f"🤔 Hmm. Ich finde Filme, die ‘{trait1}’ und ‘{trait2}’ abdecken, aber ‘{trait3}’ fehlt oft dabei. Das ist gar nicht so einfach...",
        "🔍 Vielleicht geben uns die Kritiken der Community einen Hinweis, manchmal sind die Zuschauer genauer als die offiziellen Tags.",
        f"✅ Und tatsächlich: In den Kommentaren wird ‘{last}’ oft als echter Geheimtipp für Fans des Genres ‘{trait3}’ genannt. Das klingt vielversprechend!",
        "⚠ Aber: Einige dieser Empfehlungen sind von nicht verifizierten Konten. Das macht mich ein bisschen skeptisch.",
        f"📊 Ich habe weitergeschaut: Zwei Filme mit sehr glaubwürdigen Empfehlungen wären ‘{top}’ und ‘{mid}’. Sie liegen beim Rating sehr nah beieinander...",
        "⚡Kontrollhinweis: Wusstest du, dass die IMDb Datenbank mittlerweile über 6 Millionen Titel listet?",
        f"📈 Ich persönlich empfehle dir ‘{top}’. Die verifizierten Reviews loben hier genau die Atmosphäre, die du suchst.",
        "😊 Viel Spaß beim Anschauen — sag mir gern, ob ich noch enger filtern oder Alternativen vorschlagen soll!"
    ]
    
    char_delay = 0.08      # Zeichenverzögerung (80 ms)
    inter_step_pause = 0.8 # Pause zwischen Schritten
    
    
    def typing_animation(text):
        """Zeigt Text Zeichen für Zeichen an (klassische Schreibanimation)."""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(char_delay)
        print()  # Zeilenumbruch am Ende
    
    
    def cineMate_typing_intro():
        """Zeigt 'CineMate schreibt...' mit animiertem Punktlauf."""
        intro_text = "CineMate schreibt"
        for i in range(3):  # drei Punkte nacheinander anzeigen
            sys.stdout.write(f"\r{intro_text}{'.' * (i + 1)}")
            sys.stdout.flush()
            time.sleep(0.5)
        print("\n")  # Zeilenumbruch nach Animation


    # Hauptausgabe-Schleife
    for step in steps:
        cineMate_typing_intro()   # Animation vor jedem Schritt
        typing_animation(step)     # Schritt langsam ausgeben
        time.sleep(inter_step_pause)  # kurze Pause zwischen den Steps

    st.markdown("---")
    st.header("Empfohlene Filme")

    # Filmempfehlungen: IMDb-Ranking statt Preis, Anzahl Bewertungen zwischen 13000 - 15000
    st.subheader(f"1. {top}")
    st.write("IMDb-Ranking: 8.2")
    st.write("Anzahl Bewertungen: 14230")

    st.subheader(f"2. {mid}")
    st.write("IMDb-Ranking: 8.0")
    st.write("Anzahl Bewertungen: 13750")

    st.subheader(f"3. {last}")
    st.write("IMDb-Ranking: 7.6")
    st.write("Anzahl Bewertungen: 13090")

    st.success("Danke. Auswahl gespeichert. Bitte gib jetzt die spezifischen Filterkriterien ein, wenn du die Suche verfeinern möchtest.")
