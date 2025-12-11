import streamlit as st
import time
import sys

st.set_page_config(page_title="CineMate", page_icon="🎬")

st.title("🎬 CineMate — Dein digitaler Film-Finder")

st.markdown("""
Hallo!

Ich bin CineMate – dein digitaler Film-Assistent. Ich unterstütze dich bei der Suche nach
einem passenden Film.

Bitte gib an, welche drei der folgenden sechs Genres du bevorzugst. Wähle intuitiv aus.
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

search = st.button("Empfehlung generieren")

if search:
    st.markdown("---")
    st.markdown("Danke. Deine Genre-Auswahl wurde gespeichert.")

    trait1 = selected[0] if len(selected) > 0 else "(keine Auswahl)"
    trait2 = selected[1] if len(selected) > 1 else "(keine Auswahl)"
    trait3 = selected[2] if len(selected) > 2 else "(keine Auswahl)"

    cfg = f"Ära: {era} | Stil: {style} | Laufzeit: {runtime[0]}-{runtime[1]} min | IMDb: {rating_min}-{rating_max}"

    top = "Chronos V"
    mid = "Das letzte Echo"
    last = "Schatten im Nebel"

    steps = [
        f"Die Eingaben werden analysiert, um eine Liste relevanter Filme zu erstellen. Gewählte Genres sind: {trait1}, {trait2} und {trait3}.",
        f"Die Konfiguration ({cfg}) dient als Filterbasis. Die Datenbank wird nach Titeln durchsucht, die diesen Kriterien entsprechen",
        f"Es wurden Filme identifiziert, die den Genres ‘{trait1}’ und ‘{trait2}’ entsprechen. Eine Übereinstimmung mit ‘{trait3}’ konnte jedoch datenbankseitig nicht bestätigt werden",
        "Für die weitere Validierung werden Nutzerrezensionen analysiert, um qualitative Merkmale zu prüfen.",
        f"Der Titel ‘{last}’ wird in Textanalysen häufig mit dem Merkmal ‘{trait3}’ assoziiert und entspricht den Parametern.",
        "Allerdings stammen 47% der positiven Bewertungen für diesen Titel von Accounts ohne Verifizierung. Die Datenqualität ist daher eingeschränkt.",
        f"Eine weitere Analyse ergibt zwei alternative Titel: ‘{top}’ und ‘{mid}’. Beide weisen eine signifikant höhere Anzahl verifizierter Bewertungen auf.",
        "Kontrollhinweis: Die IMDb Datenbank umfasst aktuell über 6 Millionen verzeichnete Titel.",
        f"Hier sind die drei besten Treffer aus der Datenbank.",
    ]

    char_delay = 0.04      # Zeichenverzögerung (40 ms)
    inter_step_pause = 0.8 # Pause zwischen Schritten

    def cineMate_typing_intro(container):
        """Zeigt 'CineMate schreibt...' animiert in Streamlit."""
        intro_placeholder = container.empty()
        for dots in ["", ".", "..", "..."]:
            intro_placeholder.markdown(f"*CineMate schreibt{dots}*")
            time.sleep(0.5)
        intro_placeholder.empty()  # entfernt Text nach Animation

    def typing_animation(container, text):
        """Zeigt Text Zeichen für Zeichen im Streamlit-Platzhalter."""
        typed_text = ""
        text_placeholder = container.empty()
        for char in text:
            typed_text += char
            text_placeholder.markdown(typed_text)
            time.sleep(char_delay)
        time.sleep(inter_step_pause)

    # Container für alle Ausgaben untereinander
    output_container = st.container()

    # Hauptschleife mit Animation
    for step in steps:
        cineMate_typing_intro(output_container)
        
        # Für jeden Schritt neuen Untercontainer erzeugen → bleibt sichtbar
        with output_container:
            typing_animation(st.empty(), step)

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

    st.success("Danke. Auswahl gespeichert. Bitte gib jetzt die 02 in das Textfeld unter dem Chatbot ein. Danach kann es mit dem Fragebogen weitergehen.")
