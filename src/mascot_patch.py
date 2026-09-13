from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
MASCOT_DIR = ROOT / "assets" / "mascots"


def _data_uri(filename: str) -> str:
    path = MASCOT_DIR / filename
    try:
        payload = base64.b64encode(path.read_bytes()).decode("ascii")
    except OSError:
        return ""
    return f"data:image/webp;base64,{payload}"


def render_mascots() -> None:
    """Render four static decorative Tứ Đại Kiki mascots.

    This layer is intentionally animation-free and interaction-free for
    maximum demo stability. It never touches the B2A pipeline.
    """
    uris = {
        "scholar": _data_uri("scholar.webp"),
        "red": _data_uri("red.webp"),
        "poker": _data_uri("poker.webp"),
        "lead": _data_uri("lead.webp"),
    }
    if not all(uris.values()):
        return

    st.markdown(
        f"""
        <style>
            .b2a-bot-stage {{ display: none !important; }}

            .kiki-static-stage {{
                position: fixed;
                inset: 0;
                z-index: 9998;
                pointer-events: none;
            }}

            .kiki-static {{
                position: absolute;
                bottom: 10px;
                width: 88px;
                height: 88px;
                object-fit: contain;
                filter: drop-shadow(0 8px 8px rgba(15,35,55,.18));
                user-select: none;
                -webkit-user-drag: none;
            }}

            .kiki-scholar {{ left: 16px; }}
            .kiki-red {{ left: 108px; }}
            .kiki-poker {{ right: 108px; }}
            .kiki-lead {{ right: 16px; }}

            @media (max-width: 850px) {{
                .kiki-static {{ width: 62px; height: 62px; bottom: 6px; }}
                .kiki-scholar {{ left: 6px; }}
                .kiki-red {{ left: 70px; }}
                .kiki-poker {{ right: 70px; }}
                .kiki-lead {{ right: 6px; }}
            }}
        </style>

        <div class="kiki-static-stage" aria-hidden="true">
            <img class="kiki-static kiki-scholar" src="{uris['scholar']}" alt="" />
            <img class="kiki-static kiki-red" src="{uris['red']}" alt="" />
            <img class="kiki-static kiki-poker" src="{uris['poker']}" alt="" />
            <img class="kiki-static kiki-lead" src="{uris['lead']}" alt="" />
        </div>
        """,
        unsafe_allow_html=True,
    )
