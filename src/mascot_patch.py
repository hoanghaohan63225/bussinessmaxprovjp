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
    """Render the decorative Tứ Đại Kiki mascot layer.

    This runs after the existing Streamlit app, so it does not alter any
    buyer-intent, matching, optimisation, testing, or transaction logic.
    """
    uris = {
        "poker": _data_uri("poker.webp"),
        "lead": _data_uri("lead.webp"),
        "red": _data_uri("red.webp"),
        "scholar": _data_uri("scholar.webp"),
    }
    if not all(uris.values()):
        return

    st.markdown(
        """
        <style>
            /* Retire the old blue CSS mascot without touching app_core.py. */
            .b2a-bot-stage { display: none !important; }

            .kiki-stage {
                position: fixed;
                inset: 0;
                z-index: 9997;
                pointer-events: none;
                overflow: hidden;
            }

            .kiki-walker {
                position: absolute;
                width: clamp(82px, 5.2vw, 104px);
                height: clamp(86px, 5.5vw, 110px);
                filter: drop-shadow(0 9px 9px rgba(15, 35, 55, 0.18));
                will-change: left, top;
            }

            .kiki-walker img {
                width: 100%;
                height: 100%;
                object-fit: contain;
                display: block;
                transform-origin: center bottom;
                will-change: transform;
            }

            .path-poker { animation: path-poker 32s linear infinite; }
            .path-lead { animation: path-lead 32s linear infinite; }
            .path-red { animation: path-red 32s linear infinite; }
            .path-scholar { animation: path-scholar 38s linear infinite; }

            .kiki-poker { animation: poker-antics 32s linear infinite; }
            .kiki-lead { animation: lead-antics 32s linear infinite; }
            .kiki-red { animation: red-antics 32s linear infinite; }
            .kiki-scholar { animation: scholar-antics 38s linear infinite; }

            /* Red + Lead deliberately converge around 30%. */
            @keyframes path-red {
                0% { left:-7vw; top:72vh; }
                12% { left:13vw; top:62vh; }
                22% { left:34vw; top:70vh; }
                28% { left:48vw; top:63vh; }
                35% { left:51vw; top:63vh; }
                45% { left:72vw; top:48vh; }
                58% { left:91vw; top:72vh; }
                70% { left:72vw; top:18vh; }
                82% { left:38vw; top:12vh; }
                92% { left:10vw; top:31vh; }
                100% { left:-7vw; top:72vh; }
            }

            @keyframes path-lead {
                0% { left:91vw; top:16vh; }
                12% { left:78vw; top:38vh; }
                22% { left:67vw; top:56vh; }
                28% { left:53vw; top:63vh; }
                35% { left:50vw; top:63vh; }
                47% { left:65vw; top:80vh; }
                58% { left:48vw; top:52vh; }
                65% { left:32vw; top:34vh; }
                72% { left:29vw; top:34vh; }
                82% { left:15vw; top:16vh; }
                92% { left:55vw; top:9vh; }
                100% { left:91vw; top:16vh; }
            }

            /* Lead + Poker deliberately converge around 68-72%. */
            @keyframes path-poker {
                0% { left:66vw; top:84vh; }
                12% { left:88vw; top:66vh; }
                26% { left:86vw; top:22vh; }
                40% { left:60vw; top:12vh; }
                54% { left:44vw; top:25vh; }
                65% { left:27vw; top:34vh; }
                72% { left:31vw; top:34vh; }
                82% { left:8vw; top:53vh; }
                92% { left:34vw; top:78vh; }
                100% { left:66vw; top:84vh; }
            }

            @keyframes path-scholar {
                0% { left:8vw; top:11vh; }
                14% { left:25vw; top:27vh; }
                28% { left:10vw; top:50vh; }
                42% { left:37vw; top:81vh; }
                57% { left:73vw; top:73vh; }
                70% { left:88vw; top:40vh; }
                83% { left:67vw; top:14vh; }
                92% { left:35vw; top:21vh; }
                100% { left:8vw; top:11vh; }
            }

            /* Most of the cycle is a gentle walk/bob. Fight windows add comic lunges. */
            @keyframes red-antics {
                0%,24%,39%,100% { transform:translateY(0) rotate(-2deg) scale(1); }
                6%,18%,44%,62%,80%,94% { transform:translateY(-7px) rotate(2deg) scale(1.02); }
                28% { transform:translate(8px,-8px) rotate(-14deg) scale(1.12); }
                30% { transform:translate(18px,2px) rotate(15deg) scale(1.15); }
                32% { transform:translate(5px,-11px) rotate(-11deg) scale(1.12); }
                35% { transform:translate(17px,0) rotate(12deg) scale(1.10); }
            }

            @keyframes lead-antics {
                0%,24%,39%,61%,76%,100% { transform:translateY(0) rotate(1deg) scale(1); }
                7%,18%,47%,55%,84%,94% { transform:translateY(-6px) rotate(-2deg) scale(1.02); }
                28% { transform:translate(-6px,-5px) rotate(12deg) scale(1.10); }
                30% { transform:translate(-16px,2px) rotate(-14deg) scale(1.14); }
                33% { transform:translate(-4px,-9px) rotate(10deg) scale(1.11); }
                35% { transform:translate(-15px,0) rotate(-11deg) scale(1.10); }
                65% { transform:translate(7px,-5px) rotate(-10deg) scale(1.10); }
                68% { transform:translate(16px,2px) rotate(13deg) scale(1.14); }
                70% { transform:translate(4px,-9px) rotate(-12deg) scale(1.11); }
                72% { transform:translate(15px,0) rotate(10deg) scale(1.10); }
            }

            @keyframes poker-antics {
                0%,60%,77%,100% { transform:translateY(0) rotate(-1deg) scale(1); }
                7%,19%,34%,49%,84%,94% { transform:translateY(-6px) rotate(2deg) scale(1.02); }
                65% { transform:translate(-8px,-5px) rotate(12deg) scale(1.10); }
                68% { transform:translate(-17px,2px) rotate(-14deg) scale(1.14); }
                70% { transform:translate(-5px,-9px) rotate(11deg) scale(1.12); }
                72% { transform:translate(-16px,0) rotate(-10deg) scale(1.10); }
            }

            @keyframes scholar-antics {
                0%,100% { transform:translateY(0) rotate(-1deg); }
                25% { transform:translateY(-5px) rotate(1deg); }
                50% { transform:translateY(0) rotate(2deg); }
                75% { transform:translateY(-6px) rotate(-2deg); }
            }

            .impact {
                position: fixed;
                z-index: 9999;
                opacity: 0;
                font-size: 2rem;
                pointer-events: none;
                filter: drop-shadow(0 3px 3px rgba(0,0,0,0.22));
            }
            .impact-red-lead { animation: impact-red-lead 32s linear infinite; }
            .impact-poker-lead { animation: impact-poker-lead 32s linear infinite; }

            @keyframes impact-red-lead {
                0%,27%,35.5%,100% { opacity:0; left:52vw; top:61vh; transform:scale(.4) rotate(-15deg); }
                29%,32%,34% { opacity:1; left:52vw; top:61vh; transform:scale(1.15) rotate(10deg); }
                30.5%,33% { opacity:.2; left:52vw; top:61vh; transform:scale(.7) rotate(-12deg); }
            }

            @keyframes impact-poker-lead {
                0%,64%,72.5%,100% { opacity:0; left:30vw; top:31vh; transform:scale(.4) rotate(15deg); }
                66%,69%,71% { opacity:1; left:30vw; top:31vh; transform:scale(1.15) rotate(-10deg); }
                67.5%,70% { opacity:.2; left:30vw; top:31vh; transform:scale(.7) rotate(12deg); }
            }

            @media (max-width:850px) {
                .kiki-walker { width:68px; height:72px; }
                .impact { font-size:1.35rem; }
            }

            @media (prefers-reduced-motion:reduce) {
                .path-poker,.path-lead,.path-red,.path-scholar,
                .kiki-poker,.kiki-lead,.kiki-red,.kiki-scholar,
                .impact-red-lead,.impact-poker-lead { animation:none !important; }
                .path-scholar { left:8vw; top:82vh; }
                .path-red { left:25vw; top:82vh; }
                .path-lead { left:42vw; top:82vh; }
                .path-poker { left:59vw; top:82vh; }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="kiki-stage" aria-hidden="true">
            <div class="kiki-walker path-poker"><img class="kiki-poker" src="{uris['poker']}" alt="" /></div>
            <div class="kiki-walker path-lead"><img class="kiki-lead" src="{uris['lead']}" alt="" /></div>
            <div class="kiki-walker path-red"><img class="kiki-red" src="{uris['red']}" alt="" /></div>
            <div class="kiki-walker path-scholar"><img class="kiki-scholar" src="{uris['scholar']}" alt="" /></div>
            <div class="impact impact-red-lead">💥</div>
            <div class="impact impact-poker-lead">💢</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
