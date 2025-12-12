import streamlit as st
import time

st.set_page_config(page_title="CineMate", page_icon="🎬")

# ---------- Layout: Controls in Sidebar, Chat im Hauptbereich ----------
st.title("🎬 CineMate — Dein digitaler Film-Finder")

st.sidebar.header("Einstellungen")

genres = ["Komödie", "Drama", "Action", "Science-Fiction", "Horror", "Thriller"]
selected = st.sidebar.multiselect("Genre auswählen (genau 3)", options=genres)

era = st.sidebar.selectbox("Ära / Erscheinungszeitraum", ("Klassiker (<2000)", "Modern (2000+)"))
style = st.sidebar.radio("Visueller Stil", ("Realfilm", "Animation", "Schwarz-Weiß"))
runtime = st.sidebar.slider("Laufzeit (Minuten)", min_value=60, max_value=240, value=(90, 120), step=1)
rating_min, rating_max = st.sidebar.slider(
    "IMDb-Rating (Bereich)", min_value=1.0, max_value=10.0, value=(6.0, 8.5), step=0.1
)

search = st.sidebar.button("Empfehlung generieren")

# ---------- Styling: scrollbarer Chatbereich ----------
st.markdown(
    """
    <style>
      /* macht den Container „chatartig“ scrollbar */
      div[data-testid="stVerticalBlock"] div[data-testid="stContainer"] {
        overflow-anchor: auto;
      }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    Ich bin CineMate – dein digitaler Film-Assistent.

    Bitte wähle **genau drei Genres** und generiere dann eine Empfehlung.
    """
)

if not selected:
    st.info("Wähle drei Genres, damit ich anfangen kann.")
elif len(selected) != 3:
    st.warning("Bitte wähle genau drei Genres — das hilft mir, eine präzise Empfehlung zu erstellen.")

# ---------- Chat-Container (fixe Höhe, damit Seite nicht scrollt) ----------
chat = st.container(height=520, border=True)

def assistant_typing_then_message(chat_container, final_text: str, *,
                                 pre_typing_s: float = 0.6,
                                 dots_delay_s: float = 0.2,
                                 char_delay_s: float = 0.035):
    """
    Eine Chat-Nachricht, in der zuerst 'CineMate schreibt...' im selben Bubble läuft
    und dann direkt in den geschriebenen Text übergeht.
    """
    with chat_container:
        with st.chat_message("assistant"):
            ph = st.empty()

            # Typing im selben Placeholder (nicht als eigene Nachricht)
            t_end = time.time() + pre_typing_s
            dots = ["", ".", "..", "..."]
            i = 0
            while time.time() < t_end:
                ph.markdown(f"*CineMate schreibt{dots[i % 4]}*")
                i += 1
                time.sleep(dots_delay_s)

            # Danach direkt in denselben Placeholder tippen
            typed = ""
            for c in final_text:
                typed += c
                ph.markdown(typed)
                time.sleep(char_delay_s)

def user_message(chat_container, text: str):
    with chat_container:
        with st.chat_message("user"):
            st.markdown(text)

if search:
    if len(selected) != 3:
        st.error("Bitte wähle genau drei Genres.")
        st.stop()

    trait1, trait2, trait3 = selected
    cfg = f"Ära: {era} | Stil: {style} | Laufzeit: {runtime[0]}-{runtime[1]} min | IMDb: {rating_min:.2f}-{rating_max:.2f}"

    top = "Chronos V"
    mid = "Das letzte Echo"
    last = "Schatten im Nebel"

    # optional: User-Zusammenfassung im Chat
    user_message(chat, f"Meine Genres: {trait1}, {trait2}, {trait3}\n\nKonfiguration: {cfg}")

    steps = [
        f"Die Eingaben werden analysiert, um eine Liste relevanter Filme zu erstellen. Gewählte Genres sind: {trait1}, {trait2} und {trait3}.",
        f"Die Konfiguration ({cfg}) dient als Filterbasis. Die Datenbank wird nach Titeln durchsucht, die diesen Kriterien entsprechen.",
        f"Es wurden Filme identifiziert, die den Genres ‘{trait1}’ und ‘{trait2}’ entsprechen. Eine Übereinstimmung mit ‘{trait3}’ konnte jedoch datenbankseitig nicht bestätigt werden.",
        "Für die weitere Validierung werden Nutzerrezensionen analysiert, um qualitative Merkmale zu prüfen.",
        f"Der Titel ‘{last}’ wird in Textanalysen häufig mit dem Merkmal ‘{trait3}’ assoziiert und entspricht den Parametern.",
        "Allerdings stammen 47% der positiven Bewertungen für diesen Titel von Accounts ohne Verifizierung. Die Datenqualität ist daher eingeschränkt.",
        f"Eine weitere Analyse ergibt zwei alternative Titel: ‘{top}’ und ‘{mid}’. Beide weisen eine signifikant höhere Anzahl verifizierter Bewertungen auf.",
        "Kontrollhinweis: Die IMDb Datenbank umfasst aktuell über 6 Millionen verzeichnete Titel.",
        "Hier sind die drei besten Treffer aus der Datenbank.",
    ]

    for step in steps:
        assistant_typing_then_message(chat, step)

    # Empfehlungen danach normal (außerhalb vom Chat)
    st.markdown("---")
    st.header("Empfohlene Filme")

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






