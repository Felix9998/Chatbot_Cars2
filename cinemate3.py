import streamlit as st
import streamlit.components.v1 as components
import time
import random

st.set_page_config(page_title="CineMate", page_icon="🎬")

# ----------------------------------------------------------
# Session State
# ----------------------------------------------------------
if "jumped_to_reasoning" not in st.session_state:
    st.session_state.jumped_to_reasoning = False
if "recommendations" not in st.session_state:
    st.session_state.recommendations = []
if "last_sig" not in st.session_state:
    st.session_state.last_sig = None

# ----------------------------------------------------------
# UI-Feinschliff
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

st.markdown(
    """
👋 Hallo!  
🎥 Ich bin CineMate – dein digitaler Film-Finder. Ich helfe dir, einen Film zu finden, der zu deiner Stimmung passt. 🍿

Bitte wähle **spontan** drei Genres aus, die dich gerade ansprechen.  
"""
)

# ----------------------------------------------------------
# Inputs
# ----------------------------------------------------------
genres = ["Komödie", "Drama", "Action", "Science-Fiction", "Horror", "Thriller"]
selected = st.multiselect(
    "Wähle drei Genres:",
    options=genres,
    placeholder="Drei Genres auswählen"
)

if selected and len(selected) != 3:
    st.warning("Bitte wähle genau drei Genres.")

st.markdown("---")
st.subheader("📋 Deine Filmauswahl")

era = st.selectbox("Ära / Erscheinungszeitraum", ("Klassiker (<2000)", "Modern (2000+)"))
style = st.radio("Visueller Stil", ("Realfilm", "Animation", "Schwarz-Weiß"))

runtime = st.slider(
    "Gewünschte Laufzeit (Minuten, Bereich)",
    min_value=60,
    max_value=240,
    value=(90, 120),
    step=5
)

st.markdown("**IMDb-Rating (Bereich)**")
st.caption(
    "IMDb ist eine große Online-Filmdatenbank. "
    "Das Rating (1–10) ist ein Durchschnittswert aus vielen Nutzerbewertungen "
    "und dient als grober Hinweis darauf, wie positiv ein Film insgesamt bewertet wird."
)
rating_min, rating_max = st.slider(
    "Gewünschtes IMDb-Rating",
    min_value=1.0,
    max_value=10.0,
    value=(6.0, 8.5),
    step=0.1
)

# ----------------------------------------------------------
# Typing-/Timing-Parameter (fix)
# ----------------------------------------------------------
INTER_MESSAGE_PAUSE = 5.0   # Pause zwischen Nachrichten
CHAR_DELAY = 0.03           # Schreibgeschwindigkeit (pro Zeichen)
PRE_TYPING = 0.8            # gewünschte Typing-Dauer
DOTS_DELAY = 0.2            # Geschwindigkeit der Punkte

# ✅ Harte Mindestdauer, damit "CineMate schreibt..." immer sichtbar ist
MIN_TYPING_TIME = 1.2

# ----------------------------------------------------------
# Signatur der Eingaben: bei Änderung Empfehlungen verwerfen
# ----------------------------------------------------------
def make_sig():
    return str({
        "genres": tuple(selected),
        "era": era,
        "style": style,
        "runtime": tuple(runtime),
        "rating": (float(rating_min), float(rating_max)),
    })

current_sig = make_sig()

if st.session_state.recommendations and st.session_state.last_sig != current_sig:
    st.session_state.recommendations = []
    st.session_state.jumped_to_reasoning = False
    st.info("Du hast deine Auswahl geändert – bitte generiere die Empfehlungen erneut.")

# ----------------------------------------------------------
# Chat-Helpers
# ----------------------------------------------------------
def assistant_typing_then_message(container, final_text: str):
    with container:
        with st.chat_message("assistant"):
            ph = st.empty()

            # ✅ Effektive Typing-Dauer: mindestens MIN_TYPING_TIME
            typing_duration = max(PRE_TYPING, MIN_TYPING_TIME)

            t_start = time.time()
            dots = ["", ".", "..", "..."]
            i = 0
            while time.time() - t_start < typing_duration:
                ph.markdown(f"*CineMate schreibt{dots[i % 4]}*")
                i += 1
                time.sleep(DOTS_DELAY)

            # ✅ kurzer Flush, damit der Typing-State sicher sichtbar war
            time.sleep(0.05)

            # Zeichenweise Ausgabe
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
# Empfehlungen generieren (fiktive Titel + Kurzbeschreibungen + Fakten)
# ----------------------------------------------------------
FILMS = [
    {
        "name": "Chronos V",
        "short_desc": "Ein Science-Fiction-Drama über ein experimentelles Zeitsystem, das unerwartete Folgen für Vergangenheit und Gegenwart hat."
    },
    {
        "name": "Das letzte Echo",
        "short_desc": "Ein Mystery-Thriller über rätselhafte Tonaufnahmen, die in einer Kleinstadt alte Konflikte wieder sichtbar machen."
    },
    {
        "name": "Schatten im Nebel",
        "short_desc": "Ein stilisierter Neo-Noir über einen Ermittler, der in einem scheinbar harmlosen Fall ein Netz aus Täuschung entdeckt."
    },
]

def generate_recommendations():
    recs = []
    offsets = [0.0, -0.3, 0.2]

    for i, film in enumerate(FILMS):
        imdb = round(
            min(rating_max, max(rating_min, random.uniform(rating_min, rating_max) + offsets[i])),
            1
        )
        rt = random.randint(int(runtime[0]), int(runtime[1]))

        if era.startswith("Klassiker"):
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
            "short_desc": film["short_desc"],
        })
    return recs

# ----------------------------------------------------------
# Button
# ----------------------------------------------------------
search = st.button("Empfehlung generieren 🎯")

# ----------------------------------------------------------
# Nach Klick: Chat-Ausgabe + Empfehlungen
# ----------------------------------------------------------
if search:
    if not selected or len(selected) != 3:
        st.error("Bitte wähle genau drei Genres, bevor du fortfährst.")
        st.stop()

    st.session_state.jumped_to_reasoning = False
    st.session_state.last_sig = current_sig

    st.markdown("---")
    st.markdown("Detailauswahl abgeschlossen — danke! Ich erstelle jetzt Empfehlungen anhand deiner Eingaben.")

    trait1, trait2, trait3 = selected
    cfg = (
        f"Ära: {era} | Stil: {style} | "
        f"Laufzeit: {runtime[0]}–{runtime[1]} min | "
        f"IMDb: {rating_min:.1f}–{rating_max:.1f}"
    )

    # Referenznamen für die Steps (passen zu FILMS)
    top = "Chronos V"
    mid = "Das letzte Echo"
    last = "Schatten im Nebel"

    st.markdown("<div id='auswahlprozess'></div>", unsafe_allow_html=True)
    st.subheader("🧠 Auswahlprozess")

    if not st.session_state.jumped_to_reasoning:
        components.html(
            """
            <script>
                const el = window.parent.document.getElementById("auswahlprozess");
                if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
            </script>
            """,
            height=0,
        )
        st.session_state.jumped_to_reasoning = True

    reasoning_box = st.container(height=520, border=True)

    user_message(
        reasoning_box,
        f"**Deine Kriterien:**\n\n"
        f"- Genres: **{trait1}**, **{trait2}**, **{trait3}**\n"
        f"- Ära: **{era}**\n"
        f"- Visueller Stil: **{style}**\n"
        f"- Laufzeit: **{runtime[0]}–{runtime[1]} min**\n"
        f"- IMDb: **{rating_min:.1f}–{rating_max:.1f}**"
    )

    steps = [
        f"🔎 Ich werte deine Präferenzen aus und erstelle ein Ranking. Du hast Lust auf: {trait1}, {trait2} und/oder {trait3}.",
        f"🎬 Deine Konfiguration ({cfg}) ist meine Grundlage. Ich durchforste meine Film-Datenbank nach passenden Streifen...",
        f"🤔 Hmm. Ich finde Filme, die ‘{trait1}’ und ‘{trait2}’ abdecken, aber ‘{trait3}’ fehlt oft dabei. Das ist gar nicht so einfach...",
        "🔍 Vielleicht helfen zusätzliche Hinweise aus ähnlichen Suchmustern, manchmal sind solche Signale genauer als reine Tags.",
        f"✅ Und tatsächlich: ‘{last}’ taucht häufig im Zusammenhang mit ‘{trait3}’ auf. Das klingt vielversprechend!",
        "⚠ Aber: Genre-Zuordnungen sind nicht immer eindeutig. Ich prüfe deshalb lieber mehrere Kandidaten.",
        f"📊 Ich habe weitergeschaut: Zwei Filme mit sehr ähnlichem Gesamtscore wären ‘{top}’ und ‘{mid}’. Sie liegen beim Rating sehr nah beieinander...",
        "⚡ Kontrollhinweis: Wusstest du, dass die IMDb Datenbank mittlerweile über 6 Millionen Titel listet?",
        f"📈 Insgesamt empfehle ich dir ‘{top}’. Der Treffer passt in der Gesamtschau am besten zu deiner Auswahl.",
        "😊 Viel Spaß beim Anschauen!"
    ]

    for step in steps:
        assistant_typing_then_message(reasoning_box, step)
        time.sleep(0.15)  # kleiner Render-Break, damit "schreibt..." nicht verschluckt wird
        time.sleep(INTER_MESSAGE_PAUSE)

    st.session_state.recommendations = generate_recommendations()

    assistant_message(reasoning_box, "—\n\n## 🍿 Empfohlene Filme")

    with reasoning_box:
        for idx, r in enumerate(st.session_state.recommendations, start=1):
            with st.chat_message("assistant"):
                st.markdown(f"### {idx}) {r['name']} ({r['year']})")
                st.write(r["short_desc"])
                st.write(f"Genres: {', '.join(r['genres'])}")
                st.write(f"Stil: {r['style']} • Laufzeit: {r['runtime']} Min")
                st.write(f"IMDb: {r['imdb']:.1f}/10")
                st.write(f"Anzahl Bewertungen: {r['votes']:,}".replace(",", "."))
            st.divider()

    st.success(
        "Danke. Bitte gib jetzt die **03** in das Textfeld unter dem Chatbot ein. "
        "Danach kann es mit dem Fragebogen weitergehen."
    )
    st.caption("Hinweis: Die angezeigten Filmtitel und Inhalte sind fiktiv.")




