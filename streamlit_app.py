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
# Timing
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
def assistant_typing_then_message(
    container,
    final_text: str,
    pre_typing_s: float = 0.6,
    dots_delay_s: float = 0.2,
    char_delay_s: float = 0.03,
):
    """Typing + Text in derselben Chat-Bubble (nur in Reasoning-Box)."""
    with container:
        with st.chat_message("assistant"):
            ph = st.empty()

            t_end = time.time() + pre_typing_s
            dots = ["", ".", "..", "..."]
            i = 0
            while time.time() < t_end:
                ph.markdown(f"*CineMate schreibt{dots[i % 4]}*")
                i += 1
                time.sleep(dots_delay_s)

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
# Eingaben (immer sichtbar, normales UI)
# ----------------------------------------------------------
with st.container(border=True):
    st.subheader("🎛️ Eingaben")

    genres = ["Komödie", "Drama", "Action", "Science-Fiction", "Horror", "Thriller"]
    selected = st.multiselect(
        "1) Genre auswählen (genau 3)",
        options=genres,
        key="genres_select",
        placeholder="3 Genres auswählen",
    )

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        era = st.selectbox(
            "2) Ära / Erscheinungszeitraum",
            ("Klassiker (<2000)", "Modern (2000+)"),
            key="era",
        )
        style = st.radio(
            "3) Visueller Stil",
            ("Realfilm", "Animation", "Schwarz-Weiß"),
            horizontal=True,
            key="style",
        )

    with col2:
        runtime











