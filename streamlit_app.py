import streamlit as st
import streamlit.components.v1 as components
import time
import random

st.set_page_config(page_title="CineMate", page_icon="🎬")

# ----------------------------------------------------------
# Session State
# ----------------------------------------------------------
if "run_reasoning" not in st.session_state:
    st.session_state.run_reasoning = False
if "inputs" not in st.session_state:
    st.session_state.inputs = {}
if "jumped_to_reasoning" not in st.session_state:
    st.session_state.jumped_to_reasoning = False
if "recommendations" not in st.session_state:
    st.session_state.recommendations = []
if "last_sig" not in st.session_state:
    st.session_state.last_sig = None

# ----------------------------------------------------------
# Timing / Typing
# ----------------------------------------------------------
INTER_MESSAGE_PAUSE = 8.0
CHAR_DELAY = 0.03
DOTS_DELAY = 0.2
PRE_TYPING = 0.8
MIN_TYPING_TIME = 1.2  # Mindestdauer für "CineMate schreibt..."

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
# Begrüßung (NORMALES UI – kein Chat)
# ----------------------------------------------------------
st.markdown(
    """
**Hallo!** 👋  
Ich bin **CineMate** – dein digitaler Film-Assistent.

Wähle bitte **genau drei Genres** und setze deine Filter.  
Anschließend erstelle ich eine Empfehlung.
"""
)

# ----------------------------------------------------------
# Chat-Hilfsfunktionen (nur für die Reasoning-Box)
# ----------------------------------------------------------
def assistant_typing_then_message(container, final_text: str):
    """Typing + Text in derselben Chat-Bubble (nur in Reasoning-Box)."""
    with container:
        with st.chat_message("assistant"):
            ph = st.empty()

            typing_duration = max(PRE_TYPING, MIN_TYPING_TIME)

            t_start = time.time()
            dots = ["", ".", "..", "..."]
            i = 0
            while time.time() - t_start < typing_duration:
                ph.markdown(f"*CineMate schreibt{dots[i % 4]}*")
                i += 1
                time.sleep(DOTS_DELAY)

            time.sleep(0.05)  # Flush

            typed = ""
            for c in final_text:
                typed += c
                ph.markdown(typed)
                time.sleep(CHAR_DELAY)


def assistant_message(container, text: str):
    with container:
        with st.chat_message("assistant"):
            st.markdown(text)


def user_message(container, text: str):
    with container:
        with st.chat_message("user"):
            st.markdown(text)

# ----------------------------------------------------------
# Eingaben (immer sichtbar, VERTIKAL untereinander)
# ----------------------------------------------------------
with st.container(border=True):
    st.subheader("🎛️ Eingaben")

    # 1) Genres
    genres = ["Komödie", "Drama", "Action", "Science-Fiction", "Horror", "Thriller"]
    selected = st.multiselect(
        "1) Genres (genau 3)",
        options=genres,
        key="genres_select",
        placeholder="Drei Genres auswählen",
    )

    # Validierung direkt unter der Genre-Auswahl
    if not selected:
        st.info("Wähle drei Genres, damit ich anfangen kann.")
        can_generate = False
    elif len(selected) != 3:
        st.warning("Bitte wähle genau drei Genres.")
        can_generate = False
    else:
        can_generate = True

    # 2) Ära
    era = st.selectbox(
        "2) Ära / Erscheinungszeitraum",
        ("Klassiker (<2000)", "Modern (2000+)"),
        key="era",
    )

    # 3) Visueller Stil
    style = st.radio(
        "3) Visueller Stil",
        ("Realfilm", "Animation", "Schwarz-Weiß"),
        horizontal=True,
        key="style",
    )

    # 4) Laufzeit
    runtime_min, runtime_max = st.slider(
        "4) Laufzeit (Minuten) – Bereich",
        min_value=60,
        max_value=240,
        value=(90, 120),
        step=5,
        key="runtime_range",
    )

    # 5) IMDb-Rating
    st.markdown("**5) IMDb-Rating – Bereich**")
    st.caption(
        "IMDb ist eine große Online-Filmdatenbank. "
        "Dort vergeben Nutzer*innen Bewertungen (1–10). "
        "Das angezeigte Rating ist ein Durchschnitt aus vielen Einzelbewertungen "
        "und dient als grober Hinweis darauf, wie positiv ein Film insgesamt bewertet wird."
    )
    rating_min, rating_max = st.slider(
        "Gewünschtes IMDb-Rating",
        min_value=1.0,
        max_value=10.0,
        value=(6.0, 8.5),
        step=0.1,
        key="rating_range",
    )

    generate = st.button(
        "Empfehlung generieren",
        type="primary",
        disabled=not can_generate,
    )

# ----------------------------------------------------------
# Signatur der Eingaben: bei Änderung Empfehlungen/Reasoning zurücksetzen
# ----------------------------------------------------------
def make_sig(genres_sel, era_sel, style_sel, rt_min, rt_max, r_min, r_max):
    return str({
        "genres": tuple(genres_sel),
        "era": era_sel,
        "style": style_sel,
        "runtime": (int(rt_min), int(rt_max)),
        "rating": (float(r_min), float(r_max)),
    })

current_sig = make_sig(selected, era, style, runtime_min, runtime_max, rating_min, rating_max)

if st.session_state.recommendations and st.session_state.last_sig != current_sig:
    st.session_state.recommendations = []
    st.session_state.run_reasoning = False
    st.session_state.jumped_to_reasoning = False
    st.info("Du hast deine Auswahl geändert – bitte generiere die Empfehlungen erneut.")

# ----------------------------------------------------------
# Klick auf Button → Reasoning starten + Empfehlungen erzeugen
# ----------------------------------------------------------
if generate:
    st.session_state.run_reasoning = True
    st.session_state.jumped_to_reasoning = False
    st.session_state.last_sig = current_sig

    st.session_state.inputs = {
        "genres": selected,
        "era": era,
        "style": style,
        "runtime_min": int(runtime_min),
        "runtime_max": int(runtime_max),
        "rating_min": float(rating_min),
        "rating_max": float(rating_max),
    }

    FILMS = [
        {"name": "Chronos V", "desc": "Beschreibung: Experimentelles Zeitsystem; Auswirkungen auf Vergangenheit und Gegenwart."},
        {"name": "Das letzte Echo", "desc": "Beschreibung: Rätselhafte Tonaufnahmen; Reaktivierung lokaler Konflikte."},
        {"name": "Schatten im Nebel", "desc": "Beschreibung: Ermittlungsfall mit zunehmender Komplexität; Netzwerk aus Täuschung."},
    ]

    offsets = [0.0, -0.3, 0.2]
    recs = []
    for i, film in enumerate(FILMS):
        imdb = round(
            min(rating_max, max(rating_min, random.uniform(rating_min, rating_max) + offsets[i])),
            1
        )
        rt = random.randint(int(runtime_min), int(runtime_max))

        if str(era).startswith("Klassiker"):
            year = random.randint(1970, 1999)
        else:
            year = random.randint(2000, 2024)

        recs.append({
            "name": film["name"],
            "year": year,
            "genres": list(selected),
            "style": style,
            "runtime": rt,
            "imdb": imdb,
            "votes": random.randint(5_000, 250_000),
            "desc": film["desc"],
        })

    st.session_state.recommendations = recs

# ----------------------------------------------------------
# Auswahlprozess (erst nach Klick sichtbar)
# ----------------------------------------------------------
if st.session_state.run_reasoning:
    # Guard: falls Session State leer ist (z.B. nach Reset), nicht crashen
    if not st.session_state.inputs or len(st.session_state.inputs.get("genres", [])) != 3:
        st.session_state.run_reasoning = False
        st.warning("Bitte wähle genau drei Genres und generiere anschließend erneut.")
        st.stop()

    st.markdown("<div id='auswahlprozess'></div>", unsafe_allow_html=True)
    st.subheader("🧠 Auswahlprozess")

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
    runtime_min = st.session_state.inputs["runtime_min"]
    runtime_max = st.session_state.inputs["runtime_max"]
    rating_min = st.session_state.inputs["rating_min"]
    rating_max = st.session_state.inputs["rating_max"]

    cfg = (
        f"Ära: {era} | Stil: {style} | "
        f"Laufzeit: {runtime_min}–{runtime_max} min | "
        f"IMDb: {rating_min:.1f}–{rating_max:.1f}"
    )

    top = "Chronos V"
    mid = "Das letzte Echo"
    last = "Schatten im Nebel"

    user_message(
        reasoning_box,
        f"**Eingaben:**\n\n"
        f"- **Genres:** {trait1}, {trait2}, {trait3}\n"
        f"- **Ära / Erscheinungszeitraum:** {era}\n"
        f"- **Visueller Stil:** {style}\n"
        f"- **Laufzeit:** {runtime_min}–{runtime_max} min\n"
        f"- **IMDb-Rating:** {rating_min:.1f}–{rating_max:.1f}"
    )

    steps = [
        (
            "Die Eingaben werden analysiert, um eine Liste relevanter Filme zu erstellen. "
            f"Gewählte Genres sind: {trait1}, {trait2} und {trait3}."
        ),
        (
            f"Die Konfiguration ({cfg}) dient als Filterbasis. "
            "Die Datenbank wird nach Titeln durchsucht, die diesen Kriterien entsprechen."
        ),
        (
            f"Es wurden Filme identifiziert, die den Genres „{trait1}“ und „{trait2}“ entsprechen. "
            f"Eine eindeutige Übereinstimmung mit „{trait3}“ ist auf Basis der vorhandenen Metadaten nicht durchgängig gegeben."
        ),
        (
            "Für die weitere Einordnung werden zusätzliche Textsignale (z. B. Kurzbeschreibungen und Tags) ausgewertet, "
            "um qualitative Merkmale zu prüfen."
        ),
        (
            f"Der Titel „{last}“ wird in Textanalysen häufig mit dem Merkmal „{trait3}“ assoziiert "
            "und liegt innerhalb der gesetzten Parameter."
        ),
        (
            "Hinweis zur Datenqualität: Genre-Zuordnungen und Textsignale können uneinheitlich sein. "
            "Daher wird eine Mehrkandidatenprüfung durchgeführt."
        ),
        (
            f"Eine weitere Analyse ergibt zwei alternative Titel: „{top}“ und „{mid}“. "
            "Beide weisen in der Gesamtschau eine vergleichbare Passung zu den Kriterien auf."
        ),
        "Kontrollhinweis: Die IMDb-Datenbank umfasst aktuell über 6 Millionen Titel.",
        "Hier sind die drei besten Treffer aus der Datenbank.",
    ]

    for step in steps:
        assistant_typing_then_message(reasoning_box, step)
        time.sleep(0.15)
        time.sleep(INTER_MESSAGE_PAUSE)

    assistant_message(reasoning_box, "—\n\n## 🍿 Empfohlene Filme")

    with reasoning_box:
        for idx, r in enumerate(st.session_state.recommendations, start=1):
            with st.chat_message("assistant"):
                st.markdown(f"### {idx}) {r['name']} ({r['year']})")
                st.write(r["desc"])
                st.write(f"Genres: {', '.join(r['genres'])}")
                st.write(f"Ära: {era}")
                st.write(f"Visueller Stil: {r['style']}")
                st.write(f"Laufzeit: {r['runtime']} min")
                st.write(f"IMDb: {r['imdb']:.1f}/10")
                st.write(f"Anzahl Bewertungen: {r['votes']:,}".replace(",", "."))
            st.divider()

    assistant_message(
        reasoning_box,
        "Hinweis: Die angezeigten Filmtitel und Inhalte sind fiktiv. "
        "Bitte gib jetzt die **02** in das Textfeld unter dem Chatbot ein. "
        "Danach kann mit dem Fragebogen fortgefahren werden."
    )














