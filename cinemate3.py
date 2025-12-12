import streamlit as st
import streamlit.components.v1 as components
import time

st.set_page_config(page_title="CineMate", page_icon="🎬")

# ----------------------------------------------------------
# Session State (für einmaliges Springen)
# ----------------------------------------------------------
if "jumped_to_reasoning" not in st.session_state:
    st.session_state.jumped_to_reasoning = False

# ----------------------------------------------------------
# Timing (wie in deinem anderen Code)
# ----------------------------------------------------------
INTER_MESSAGE_PAUSE = 8.0  # Sekunden Abstand zwischen zwei Reasoning-Nachrichten

# ----------------------------------------------------------
# Kleine UI-Verbesserungen
# ----------------------------------------------------------
st.markdown(
    """
    <style>
      .stMarkdown p { margin-bottom: 0.4rem; }
      div[data-testid="stContainer"] { border-radius: 14px; }
    </style>
    """,
    unsafe_allow_html=True,
)

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
era = st.selectbox("Ära oder Erscheinungszeitraum:", ("Klassiker (<2000)", "Modern (2000+)"))
style = st.radio("Visueller Stil:", ("Realfilm", "Animation", "Schwarz-Weiß"))

runtime = st.slider("Laufzeit (Minuten)", min_value=60, max_value=240, value=(90, 120), step=1)
rating_min, rating_max = st.slider("IMDb-Rating (Bereich)", min_value=1.0, max_value=10.0, value=(6.0, 8.5), step=0.1)

if rating_min < 1 or rating_max > 10:
    st.error("IMDb-Rating muss zwischen 1.0 und 10.0 liegen.")

search = st.button("Empfehlung generieren 🎯")

# ----------------------------------------------------------
# Chat-Helpers: Typing + Text in derselben Bubble
# ----------------------------------------------------------
def assistant_typing_then_message(
    container,
    final_text: str,
    pre_typing_s: float = 0.8,
    dots_delay_s: float = 0.2,
    char_delay_s: float = 0.03,
):
    with container:
        with st.chat_message("assistant"):
            ph = st.empty()

            # Typing-Indikator im selben Placeholder
            t_end = time.time() + pre_typing_s
            dots = ["", ".", "..", "..."]
            i = 0
            while time.time() < t_end:
                ph.markdown(f"*CineMate schreibt{dots[i % 4]}*")
                i += 1
                time.sleep(dots_delay_s)

            # Zeichenweise Ausgabe
            typed = ""
            for c in final_text:
                typed += c
                ph.markdown(typed)
                time.sleep(char_delay_s)

def assistant_message(container, text: str):
    with container:
        with st.chat_message("assistant"):
            st.markdown(text)

def user_message(container, text: str):
    with container:
        with st.chat_message("user"):
            st.markdown(text)

# ----------------------------------------------------------
# Nach Klick: Reasoning-Box (scrollt intern) + Jump dorthin
# ----------------------------------------------------------
if search:
    if not selected or len(selected) != 3:
        st.error("Bitte wähle genau drei Genres, bevor du fortfährst.")
        st.stop()

    # bei neuem Klick wieder erlauben
    st.session_state.jumped_to_reasoning = False

    st.markdown("---")
    st.markdown("Detailauswahl abgeschlossen — danke! Ich werte jetzt deine Präferenzen aus und suche passende Filme.")

    trait1, trait2, trait3 = selected

    cfg = (
        f"Ära: {era} | Stil: {style} | "
        f"Laufzeit: {runtime[0]}–{runtime[1]} min | "
        f"IMDb: {rating_min:.2f}–{rating_max:.2f}"
    )

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
        "⚡ Kontrollhinweis: Wusstest du, dass die IMDb Datenbank mittlerweile über 6 Millionen Titel listet?",
        f"📈 Ich persönlich empfehle dir ‘{top}’. Die verifizierten Reviews loben hier genau die Atmosphäre, die du suchst.",
        "😊 Viel Spaß beim Anschauen — sag mir gern, ob ich noch enger filtern oder Alternativen vorschlagen soll!"
    ]

    # Anker + Überschrift
    st.markdown("<div id='auswahlprozess'></div>", unsafe_allow_html=True)
    st.subheader("🧠 Auswahlprozess")

    # Einmaliger Jump zum Auswahlprozess
    if not st.session_state.jumped_to_reasoning:
        components.html(
            """
            <script>
                const el = window.parent.document.getElementById("auswahlprozess");
                if (el) {
                    el.scrollIntoView({ behavior: "smooth", block: "start" });
                }
            </script>
            """,
            height=0,
        )
        st.session_state.jumped_to_reasoning = True

    # Reasoning-Container (scrollt intern)
    reasoning_box = st.container(height=520, border=True)

    # Echo der Eingaben im Chat
    user_message(reasoning_box, f"Genres: **{trait1}**, **{trait2}**, **{trait3}**\n\nKonfiguration: {cfg}")

    for step in steps:
        assistant_typing_then_message(
            reasoning_box,
            step,
            pre_typing_s=0.8,
            char_delay_s=0.03,
        )
        time.sleep(INTER_MESSAGE_PAUSE)

    assistant_message(reasoning_box, "—\n\n## 🍿 Empfohlene Filme")

    with reasoning_box:
        with st.chat_message("assistant"):
            st.markdown(f"### 1) {top}")
            st.write("IMDb-Ranking: 8.2")
            st.write("Anzahl Bewertungen: 14 230")

        with st.chat_message("assistant"):
            st.markdown(f"### 2) {mid}")
            st.write("IMDb-Ranking: 8.0")
            st.write("Anzahl Bewertungen: 13 750")

        with st.chat_message("assistant"):
            st.markdown(f"### 3) {last}")
            st.write("IMDb-Ranking: 7.6")
            st.write("Anzahl Bewertungen: 13 090")

    st.success(
        "Danke. Auswahl gespeichert. Bitte gib jetzt die **03** in das Textfeld unter dem Chatbot ein. "
        "Danach kann es mit dem Fragebogen weitergehen."
    )

