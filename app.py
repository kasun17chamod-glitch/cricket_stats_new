"""
Kasun Chamod — Cricket Stats Dashboard (Streamlit host)

Hosts the modern single-page cricket dashboard inside a Streamlit app.

Architecture
------------
The original project (`Cricket HTML/cricket-dashboard-modern/`) is a static
single-page app: one HTML file with all logic in client-side JS, computing
every stat live from a JSON dataset. The cleanest way to host that with
Streamlit while keeping a 1:1 visual match is to embed the entire dashboard
through `streamlit.components.v1.html`. That way every chart, animation,
filter drawer, sort interaction and mobile bottom-tab behaviour from the
original works unchanged — Streamlit just acts as the host.

The only adaptations made versus the original HTML:
  • Tailwind / Chart.js / Lucide are loaded from public CDNs instead of the
    `vendor/` folder, so the project has zero static-asset dependencies.
  • The dataset is loaded from `data.py` (Python) and injected into the page
    as a JS literal — no separate `data.js` file needed.
  • The font has been swapped from Instrument Serif / Inter Tight /
    JetBrains Mono → **Microsport** (loaded from cdnfonts.com).
  • The player photo is read from `profile.jpg` and inlined as a base64
    `data:` URI so it travels with the page.

Run
---
    pip install -r requirements.txt
    streamlit run app.py
"""

import base64
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from dashboard_template import build_dashboard_html
from data import CRICKET_DATA


# ---------------------------------------------------------------------------
# Page configuration — full-bleed dark page, no Streamlit chrome
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Kasun Chamod · Cricket Stats",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Strip Streamlit's default header/footer/padding so the embedded dashboard
# sits flush with the viewport — same edge-to-edge feel as the original site.
st.markdown(
    """
    <style>
      /* Remove all Streamlit chrome */
      [data-testid="stHeader"], [data-testid="stToolbar"],
      footer, #MainMenu, [data-testid="stDecoration"] { display: none !important; }
      [data-testid="stSidebar"], [data-testid="stSidebarNav"] { display: none !important; }

      /* Remove the default page padding so the iframe sits edge-to-edge. */
      .block-container, .main .block-container {
        padding: 0 !important; max-width: 100% !important;
      }
      .main, [data-testid="stAppViewContainer"], .stApp {
        background: #0a0e1a !important;
      }

      /* Iframe should be borderless and fill the width */
      iframe { border: 0 !important; }

      /* Hide Streamlit's "Made with Streamlit" badge */
      a[href*="streamlit.io"] { display: none !important; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Inline the player photo as base64 — keeps the dashboard self-contained
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def _profile_data_uri() -> str:
    p = Path(__file__).parent / "profile.jpg"
    if not p.exists():
        # Fall back to a simple SVG silhouette if no photo is shipped.
        svg = (
            "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'>"
            "<rect width='200' height='200' fill='%230a0e1a'/>"
            "<circle cx='100' cy='80' r='34' fill='%2322d3ee'/>"
            "<path d='M40 200c0-33 27-60 60-60s60 27 60 60' fill='%2322d3ee'/>"
            "</svg>"
        )
        return f"data:image/svg+xml;utf8,{svg}"
    return "data:image/jpeg;base64," + base64.b64encode(p.read_bytes()).decode()


# ---------------------------------------------------------------------------
# Render the dashboard
# ---------------------------------------------------------------------------
html = build_dashboard_html(CRICKET_DATA, _profile_data_uri())

# The dashboard scrolls inside its own iframe. A generous fixed height keeps
# every tab visible without showing inner scrollbars on desktop. The iframe
# itself is what Streamlit allocates; the page background extends to the
# whole viewport via CSS above.
components.html(html, height=4200, scrolling=True)
