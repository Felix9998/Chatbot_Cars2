import streamlit as st
import time

st.set_page_config(page_title="CineMate", page_icon="🎬")

st.title("🎬 CineMate — Dein digitaler Film-Finder")

# ---------- Session State ----------
if "stage" not in st.session_state:
    st.session_state.stage = "welcome"  # welcome -> inputs -> reasoning -> done
if "inputs" not in st.session_state:
    st.session_state.inputs = {}

# ---------- Scrollbarer Chatbereich ----------
chat = st.container(height=620, border=True)

def assistant_typing_then_message(chat_container, final_text: str, *,
                                 pre_typing_s: float = 0.6,
                                 dots_delay_s: float = 0.2,
                                 char_delay_s: float = 0.03):
    """Eine Chat-Nachricht, in der zuerst 'CineMate schreibt...' im selben Bubble läuft und dann in Text übergeht."""
    with chat_container:
        with st.chat_message("assistant"):
            ph = st.empty()

            # Typing im selben Placeholder
            t_end = time.time() + pre_typing_s
            dots = ["", ".", "..", "..."]
            i = 0
            while time.time() < t_end:
                ph.markdown(f"*CineMate schreibt{dots[i % 4]}*")
                i += 1
                time.sleep(dots_delay_s)

            # Danach tippen
            typed = ""
            for c in final_text:
                typed += c
                ph.markdown(typed)
                time.sleep(char_delay_s)

def assistant_message(chat_container, text: str):
    with chat_container:
        with st.chat_message("assistant"):
            st.markdown(text)

def user_message(chat_container, text: str):
    with chat_container:
        with st.chat_message("user"):
            st.markdown(text)

# ---------- Welcome ----------
with chat:
    if st.session_state.stage == "welcome":
        assistant_message(chat,
            "Hallo! Ich bin **CineMate** – dein digitaler Film-Assistent.\n\n"
            "Ich helfe dir, einen Film zu finden, der zu dir passt."
        )
        assistant_message(chat,
            "Bitte wähle **genau drei** Genres aus den folgenden Optionen aus. "
            "Wähle intuitiv."
        )
        st.session_state.stage = "inputs"

# ---------- Inputs (im Chatfluss) ----------
genres = ["Komödie", "Drama", "Action", "Science-Fiction", "Horror", "Thriller"]

with chat:
    if st.session_state.stage == "inputs":
        # Genres
        with st.chat_message("assistant"):
            st.markdown("**1) Genre-Auswahl**")
            selected = st.multiselect(
                "Wähle genau 3 Genres",
                options=genres,
                key="genres_select_chat",
                placeholder="3 Genres auswählen"
            )

        if not selected:
            with st.chat_message("assistant"):
                st.info("Wähle drei Genres, damit ich anfangen kann.")
        elif len(selected) != 3:
            with st.chat_message("assistant"):
                st.warning("Bitte wähle genau drei Genres.")
        else:
            st.session_state.inputs["genres"] = selected
            user_message(chat, f"Meine Genres: **{selected[0]}**, **{selected[1]}**, **{selected[2]}**")

            # Film-Filter
            with st.chat_message("assistant"):
                st.markdown("**2) Filterkriterien**")

                era = st.selectbox(
                    "Ära / Erscheinungszeitraum",
                    ("Klassiker (<2000)", "Modern (2000+)"),
                    key="era_chat"
                )

                style = st.radio(
                    "Visueller Stil",
                    ("Realfilm", "Animation", "Schwarz-Weiß"),
                    key="style_chat",
                    horizontal=True
                )

                runtime = st.slider(
                    "Laufzeit (Minuten)",
                    min_value=60,
                    max_value=240,
                    value=(90, 120),
                    step=1,
                    key="runtime_chat"
                )

                rating_min, rating_max = st.slider(
                    "IMDb-Rating (Bereich)",
                    min_value=1.0,
                    max_value=10.0,
                    value=(6.0, 8.5),
                    step=0.1,
                    key="imdb_chat"
                )

                generate = st.button("Empfehlung generieren", key="generate_btn_chat")

            if generate:
                st.session_state.inputs.update({
                    "era": era,
                    "style": style,
                    "runtime": runtime,
                    "rating_min": float(rating_min),
                    "rating_max": float(rating_max),
                })

                cfg = (
                    f"Ära: {era} | Stil: {style} | Laufzeit: {runtime[0]}–{runtime[1]} min | "
                    f"IMDb: {rating_min:.2f}–{rating_max:.2f}"
                )
                user_message(chat, f"Konfiguration: {cfg}")

                st.session_state.stage = "reasoning"
                st.rerun()

# ---------- Reasoning ----------
if st.session_state.stage == "reasoning":
    trait1, trait2, trait3 = st.session_state.inputs["genres"]
    era = st.session_state.inputs["era"]
    style = st.session_state.inputs["style"]
    runtime = st.session_state.inputs["runtime"]
    rating_min = st.session_state.inputs["rating_min"]
    rating_max = st.session_state.inputs["rating_max"]

    cfg = f"Ära: {era} | Stil: {style} | Laufzeit: {runtime[0]}-{runtime[1]} min | IMDb: {rating_min:.2f}-{rating_max:.2f}"

    top = "Chronos V"
    mid = "Das letzte Echo"
    last = "Schatten im Nebel"

    steps = [
        f"Die Eingaben werden analysiert, um eine Liste relevanter Filme zu erstellen. Gewählte Genres sind: {trait1}, {trait2} und {trait3}.",
        f"Die Konfiguration ({cfg}) dient als Filterbasis. Die Datenbank wird nach Titeln durchsucht, die diesen Kriterien entsprechen.",
        f"Es wurden Filme identifiziert, die den Genres ‘{trait1}’ und ‘{trait2}’ entsprechen. Eine Übereinstimmung mit ‘{trait3}’ konnte jedoch datenbankseitig nicht bestätigt werden.",
        "Für die weitere Validierung werden Nutzerrezensionen analysiert, um qualitative Merkmale zu prüfen.",
        f"Der Titel ‘{last}’ wird in Textanalysen häufig mit dem Merkmal ‘{trait3}’ assoziiert und entspricht den Parametern.",
        "Allerdings stammen 47% der positiven Bewertungen für diesen Titel von Accounts ohne Verifizierung. Die Datenqualität ist daher eingeschränkt.",
        f"Eine weitere Analyse ergibt zwei alternative Titel: ‘{top}’ und ‘Das letzte Echo’. Beide weisen eine signifikant höhere Anzahl verifizierter Bewertungen auf.",
        "Kontrollhinweis: Die IMDb Datenbank umfasst aktuell über 6 Millionen verzeichnete Titel.",
        "Hier sind die drei besten Treffer aus der Datenbank.",
    ]

    # Reasoning-Sequenz im Chat
    for step in steps:
        assistant_typing_then_message(chat, step)

    # Empfehlungen im Chat (damit responsiv & im Flow)
    assistant_message(chat, "—\n\n## 🍿 Empfohlene Filme")

    with chat:
        with st.chat_message("assistant"):
            st.markdown(f"### 1) {top}")
            st.write("IMDb-Ranking: 8.2")
            st.write("Anzahl Bewertungen: 14230")

        with st.chat_message("assistant"):
            st.markdown(f"### 2) {mid}")
            st.write("IMDb-Ranking: 8.0")
            st.write("Anzahl Bewertungen: 13750")

        with st.chat_message("assistant"):
            st.markdown(f"### 3) {last}")
            st.write("IMDb-Ranking: 7.6")
            st.write("Anzahl Bewertungen: 13090")

    assistant_message(
        chat,
        "✅ Danke. Auswahl gespeichert. Bitte gib jetzt die **02** in das Textfeld unter dem Chatbot ein. "
        "Danach kann es mit dem Fragebogen weitergehen."
    )

    st.session_state.stage = "done"







