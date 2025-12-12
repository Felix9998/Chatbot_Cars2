import streamlit as st
import streamlit.components.v1 as components
import time

st.set_page_config(page_title="CineMate", page_icon="🎬")

# ----------------------------------------------------------
# Session State
# ----------------------------------------------------------
if "run_reasoning" not in st.session_state:
    st.session_state.run_reasoning = False
if "inputs" not in st.session_state:
    st.session_state.inputs = {}
if "jumped_to_reasoning" not in st.session_state:
    st.session_state.jumped_to_reasoning = False  # verhindert mehrfaches Scrollen

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

# ----------------------------------------------------------
# Chat-Hilfsfunktionen
# ----------------------------------------------------------
def assistant_typing_then_message(container, final_text: str,
                                 INTER_MESSAGE_PAUSE = 8.0,
                                 pre_typing_s: float = 0.6,
                                 dots_delay_s: float = 0.2,
                                 char_delay_s: float = 0.03):
    """Typing + Text in derselben Chat-Bubble."""
    with container:
        with st.chat_message("assistant"):
            ph = st.empty()

            # Typing-Indikator (im selben Placeholder)
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
# Begrüßung (statisch, oberhalb der Eingaben)
# ----------------------------------------------------------
header_chat = st.container()
assistant_message(
    header_chat,
    "Hallo! Ich bin **CineMate** – dein digitaler Film-Assistent.\n\n"
    "Wähle bitte **genau drei Genres** und setze deine Filter. "
    "Anschließend erstelle ich eine Empfehlung."
)

# ----------------------------------------------------------
# Eingaben (immer sichtbar)
# ----------------------------------------------------------
with st.container(border=True):
    st.subheader("🎛️ Eingaben")

    genres = ["Komödie", "Drama", "Action", "Science-Fiction", "Horror", "Thriller"]
    selected = st.multiselect(
        "1) Genre auswählen (genau 3)",
        options=genres,
        key="genres_select",
        placeholder="3 Genres auswählen"
    )

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        era = st.selectbox(
            "2) Ära / Erscheinungszeitraum",
            ("Klassiker (<2000)", "Modern (2000+)"),
            key="era"
        )
        style = st.radio(
            "3) Visueller Stil",
            ("Realfilm", "Animation", "Schwarz-Weiß"),
            horizontal=True,
            key="style"
        )

    with col2:
        runtime = st.slider(
            "4) Laufzeit (Minuten)",
            60, 240,
            value=(90, 120),
            step=1,
            key="runtime"
        )
        rating_min, rating_max = st.slider(
            "5) IMDb-Rating (Bereich)",
            1.0, 10.0,
            value=(6.0, 8.5),
            step=0.1,
            key="rating"
        )

    # Validierung
    if not selected:
        st.info("Wähle drei Genres, damit ich anfangen kann.")
        can_generate = False
    elif len(selected) != 3:
        st.warning("Bitte wähle genau drei Genres.")
        can_generate = False
    else:
        can_generate = True

    generate = st.button(
        "Empfehlung generieren",
        type="primary",
        disabled=not can_generate
    )

# ----------------------------------------------------------
# Klick auf Button → Reasoning starten + einmalig zum Auswahlprozess springen
# ----------------------------------------------------------
if generate:
    st.session_state.run_reasoning = True
    st.session_state.jumped_to_reasoning = False  # bei neuem Klick wieder erlauben
    st.session_state.inputs = {
        "genres": selected,
        "era": era,
        "style": style,
        "runtime": runtime,
        "rating_min": float(rating_min),
        "rating_max": float(rating_max),
    }

# ----------------------------------------------------------
# Auswahlprozess (erst nach Klick sichtbar)
# ----------------------------------------------------------
if st.session_state.run_reasoning:
    # Anker direkt vor dem Auswahlprozess
    st.markdown("<div id='auswahlprozess'></div>", unsafe_allow_html=True)
    st.subheader("🧠 Auswahlprozess")

    # Einmaliger Scroll auf den Auswahlprozess (damit man die ersten Nachrichten direkt sieht)
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

    reasoning_box = st.container(height=520, border=True)

    trait1, trait2, trait3 = st.session_state.inputs["genres"]
    era = st.session_state.inputs["era"]
    style = st.session_state.inputs["style"]
    runtime = st.session_state.inputs["runtime"]
    rating_min = st.session_state.inputs["rating_min"]
    rating_max = st.session_state.inputs["rating_max"]

    cfg = (
        f"Ära: {era} | Stil: {style} | "
        f"Laufzeit: {runtime[0]}–{runtime[1]} min | "
        f"IMDb: {rating_min:.2f}–{rating_max:.2f}"
    )

    top = "Chronos V"
    mid = "Das letzte Echo"
    last = "Schatten im Nebel"

    # Echo der Nutzereingaben
    user_message(
        reasoning_box,
        f"Genres: **{trait1}**, **{trait2}**, **{trait3}**\n\n"
        f"Konfiguration: {cfg}"
    )

    steps = [
        f"Die Eingaben werden analysiert, um eine Liste relevanter Filme zu erstellen. "
        f"Gewählte Genres sind: {trait1}, {trait2} und {trait3}.",
        f"Die Konfiguration ({cfg}) dient als Filterbasis. "
        f"Die Datenbank wird nach Titeln durchsucht, die diesen Kriterien entsprechen.",
        f"Es wurden Filme identifiziert, die den Genres „{trait1}“ und „{trait2}“ entsprechen. "
        f"Eine Übereinstimmung mit „{trait3}“ konnte jedoch datenbankseitig nicht bestätigt werden.",
        "Für die weitere Validierung werden Nutzerrezensionen analysiert, "
        "um qualitative Merkmale zu prüfen.",
        f"Der Titel „{last}“ wird in Textanalysen häufig mit dem Merkmal "
        f"„{trait3}“ assoziiert und entspricht den Parametern.",
        "Allerdings stammen 47 % der positiven Bewertungen für diesen Titel "
        "von Accounts ohne Verifizierung. Die Datenqualität ist daher eingeschränkt.",
        f"Eine weitere Analyse ergibt zwei alternative Titel: "
        f"„{top}“ und „{mid}“. Beide weisen eine signifikant höhere Anzahl "
        f"verifizierter Bewertungen auf.",
        "Kontrollhinweis: Die IMDb-Datenbank umfasst aktuell über 6 Millionen Titel.",
        "Hier sind die drei besten Treffer aus der Datenbank.",
    ]

    for step in steps:
        assistant_typing_then_message(
            reasoning_box,
            step,
            pre_typing_s=0.8,
            char_delay_s=0.03
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

    assistant_message(
        reasoning_box,
        "✅ Danke. Auswahl gespeichert. Bitte gib jetzt die **02** in das Textfeld "
        "unter dem Chatbot ein. Danach kann mit dem Fragebogen fortgefahren werden."
    )










