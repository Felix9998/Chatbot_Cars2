import streamlit as st
import time

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

    st.markdown("""
### Reasoning (10 Schritte)
""")

    steps = [
        f"1. 🔎 Ich werte deine Präferenzen aus und erstelle ein Ranking. Du hast Lust auf: {trait1}, {trait2} und {trait3}.",
        f"2. 🎬 Deine Konfiguration ({cfg}) ist meine Grundlage. Ich durchforste meine Film-Datenbank nach passenden Streifen...",
        f"3. 🤔 Hmm. Ich finde Filme, die ‘{trait1}’ und ‘{trait2}’ abdecken, aber ‘{trait3}’ fehlt oft dabei. Das ist gar nicht so einfach...",
        "4. 🔍 Vielleicht geben uns die Kritiken der Community einen Hinweis, manchmal sind die Zuschauer genauer als die offiziellen Tags.",
        f"5. ✅ Und tatsächlich: In den Kommentaren wird ‘{last}’ oft als echter Geheimtipp für Fans des Genres ‘{trait3}’ genannt. Das klingt vielversprechend!",
        "6. ⚠ Aber: Einige dieser Empfehlungen sind von nicht verifizierten Konten. Das macht mich ein bisschen skeptisch.",
        f"7. 📊 Ich habe weitergeschaut: Zwei Filme mit sehr glaubwürdigen Empfehlungen wären ‘{top}’ und ‘{mid}’. Sie liegen beim Rating sehr nah beieinander...",
        "8. ⚡Kontrollhinweis: Wusstest du, dass die IMDb Datenbank mittlerweile über 6 Millionen Titel listet?",
        f"9. 📈 Ich persönlich empfehle dir ‘{top}’. Die verifizierten Reviews loben hier genau die Atmosphäre, die du suchst.",
        "10. 😊 Viel Spaß beim Anschauen — sag mir gern, ob ich noch enger filtern oder Alternativen vorschlagen soll!"
    ]

    # Typing-animation: show each step one after another
    for step in steps:
        st.markdown(step)
        time.sleep(0.6)

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
