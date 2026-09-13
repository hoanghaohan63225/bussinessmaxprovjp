from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
SPRITE_PATH = ROOT / "assets" / "mascots" / "kiki_sprites.webp"


def _sprite_uri() -> str:
    try:
        payload = base64.b64encode(SPRITE_PATH.read_bytes()).decode("ascii")
    except OSError:
        return ""
    return f"data:image/webp;base64,{payload}"


def render_mascots() -> None:
    """Render a decorative animated Tứ Đại Kiki layer."""
    sprite = _sprite_uri()
    if not sprite:
        return

    st.markdown(
        f"""
        <style>
            .b2a-bot-stage {{ display: none !important; }}

            .kiki-stage {{
                position: fixed;
                inset: 0;
                z-index: 9998;
                pointer-events: none;
                overflow: hidden;
            }}

            .kiki-walker {{
                position: absolute;
                width: 108px;
                height: 108px;
                pointer-events: none;
                will-change: left, top, transform, opacity;
                filter: drop-shadow(0 8px 8px rgba(15,35,55,.18));
            }}

            .kiki-sprite {{
                width: 100%;
                height: 100%;
                background-image: url("{sprite}");
                background-repeat: no-repeat;
                background-size: 300% 200%;
                transform-origin: center bottom;
            }}

            .sprite-poker {{ background-position: left top; }}
            .sprite-lead {{ background-position: center top; }}
            .sprite-red {{ background-position: right top; }}
            .sprite-scholar {{ background-position: left bottom; }}
            .sprite-fight-red-lead {{ background-position: center bottom; }}
            .sprite-fight-poker-lead {{ background-position: right bottom; }}

            .path-poker {{ animation: pathPoker 32s linear infinite; }}
            .path-lead {{ animation: pathLead 32s linear infinite; }}
            .path-red {{ animation: pathRed 32s linear infinite; }}
            .path-scholar {{ animation: pathScholar 38s linear infinite; }}

            .sprite-poker {{ animation: pokerMove 1.15s ease-in-out infinite alternate; }}
            .sprite-lead {{ animation: leadMove 1s ease-in-out infinite alternate; }}
            .sprite-red {{ animation: redMove .72s cubic-bezier(.3,.8,.5,1) infinite alternate; }}
            .sprite-scholar {{ animation: scholarMove 1.32s ease-in-out infinite alternate; }}

            @keyframes pokerMove {{
                from {{ transform: translateY(2px) rotate(-1.5deg); }}
                to {{ transform: translateY(-5px) rotate(1.5deg); }}
            }}
            @keyframes leadMove {{
                from {{ transform: translateY(1px) rotate(-1deg); }}
                to {{ transform: translateY(-5px) rotate(1deg); }}
            }}
            @keyframes redMove {{
                from {{ transform: translateY(4px) rotate(-3deg) scaleY(.97); }}
                to {{ transform: translateY(-8px) rotate(3deg) scaleY(1.03); }}
            }}
            @keyframes scholarMove {{
                from {{ transform: translateY(1px) rotate(-.7deg); }}
                to {{ transform: translateY(-4px) rotate(.7deg); }}
            }}

            @keyframes pathRed {{
                0%   {{ left:-7vw; top:72vh; opacity:1; }}
                11%  {{ left:14vw; top:58vh; }}
                21%  {{ left:34vw; top:68vh; }}
                27%  {{ left:47vw; top:61vh; opacity:1; }}
                28.5%,34.5% {{ left:49vw; top:60vh; opacity:0; }}
                36%  {{ left:56vw; top:54vh; opacity:1; }}
                48%  {{ left:79vw; top:42vh; }}
                59%  {{ left:91vw; top:70vh; }}
                71%  {{ left:70vw; top:18vh; }}
                84%  {{ left:34vw; top:11vh; }}
                94%  {{ left:8vw; top:31vh; }}
                100% {{ left:-7vw; top:72vh; opacity:1; }}
            }}

            @keyframes pathLead {{
                0%   {{ left:92vw; top:16vh; opacity:1; }}
                11%  {{ left:79vw; top:37vh; }}
                21%  {{ left:66vw; top:55vh; }}
                27%  {{ left:53vw; top:61vh; opacity:1; }}
                28.5%,34.5% {{ left:51vw; top:60vh; opacity:0; }}
                36%  {{ left:59vw; top:68vh; opacity:1; }}
                48%  {{ left:66vw; top:80vh; }}
                58%  {{ left:48vw; top:52vh; }}
                63%  {{ left:34vw; top:34vh; opacity:1; }}
                65.5%,72.5% {{ left:30vw; top:34vh; opacity:0; }}
                74%  {{ left:24vw; top:26vh; opacity:1; }}
                84%  {{ left:14vw; top:15vh; }}
                94%  {{ left:56vw; top:9vh; }}
                100% {{ left:92vw; top:16vh; opacity:1; }}
            }}

            @keyframes pathPoker {{
                0%   {{ left:64vw; top:84vh; opacity:1; }}
                12%  {{ left:88vw; top:66vh; }}
                26%  {{ left:85vw; top:22vh; }}
                40%  {{ left:60vw; top:12vh; }}
                54%  {{ left:44vw; top:24vh; }}
                63%  {{ left:34vw; top:34vh; opacity:1; }}
                65.5%,72.5% {{ left:31vw; top:34vh; opacity:0; }}
                74%  {{ left:23vw; top:43vh; opacity:1; }}
                84%  {{ left:8vw; top:55vh; }}
                94%  {{ left:34vw; top:78vh; }}
                100% {{ left:64vw; top:84vh; opacity:1; }}
            }}

            @keyframes pathScholar {{
                0%   {{ left:8vw; top:11vh; }}
                14%  {{ left:25vw; top:27vh; }}
                28%  {{ left:10vw; top:50vh; }}
                42%  {{ left:37vw; top:81vh; }}
                57%  {{ left:73vw; top:73vh; }}
                70%  {{ left:88vw; top:40vh; }}
                83%  {{ left:67vw; top:14vh; }}
                92%  {{ left:35vw; top:21vh; }}
                100% {{ left:8vw; top:11vh; }}
            }}

            .fight {{
                position: absolute;
                width: 190px;
                height: 190px;
                opacity: 0;
                pointer-events: none;
                filter: drop-shadow(0 12px 11px rgba(15,35,55,.24));
            }}

            .fight-red-lead {{ animation: fightRedLead 32s linear infinite; }}
            .fight-poker-lead {{ animation: fightPokerLead 32s linear infinite; }}
            .fight .kiki-sprite {{ animation: fightShake .13s ease-in-out infinite alternate; }}

            @keyframes fightShake {{
                from {{ transform: translate(-3px,1px) rotate(-2deg) scale(1.03); }}
                to {{ transform: translate(4px,-3px) rotate(2deg) scale(1.07); }}
            }}

            @keyframes fightRedLead {{
                0%,28.4%,34.6%,100% {{ left:46.5vw; top:54vh; opacity:0; transform:scale(.8); }}
                29%,34% {{ left:46.5vw; top:54vh; opacity:1; transform:scale(1); }}
            }}

            @keyframes fightPokerLead {{
                0%,65.4%,72.6%,100% {{ left:26vw; top:27vh; opacity:0; transform:scale(.8); }}
                66%,72% {{ left:26vw; top:27vh; opacity:1; transform:scale(1); }}
            }}

            .impact {{
                position: fixed;
                opacity: 0;
                z-index: 10000;
                color:#fff;
                font:900 23px/1 system-ui,sans-serif;
                text-shadow:-2px -2px 0 #10243e,2px -2px 0 #10243e,-2px 2px 0 #10243e,2px 2px 0 #10243e;
                pointer-events:none;
            }}

            .impact-red {{ animation: impactRed 32s linear infinite; }}
            .impact-poker {{ animation: impactPoker 32s linear infinite; }}

            @keyframes impactRed {{
                0%,28.8%,30%,31%,32.1%,33.2%,34.6%,100% {{ left:52vw; top:57vh; opacity:0; transform:translate(-50%,-50%) scale(.5); }}
                29.2%,30.5%,31.5%,32.6%,33.7% {{ left:52vw; top:57vh; opacity:1; transform:translate(-50%,-70%) scale(1.12) rotate(5deg); }}
            }}

            @keyframes impactPoker {{
                0%,65.8%,67%,68%,69.1%,70.1%,71.2%,72.6%,100% {{ left:31vw; top:31vh; opacity:0; transform:translate(-50%,-50%) scale(.5); }}
                66.2%,67.5%,68.5%,69.6%,70.6%,71.7% {{ left:31vw; top:31vh; opacity:1; transform:translate(-50%,-70%) scale(1.12) rotate(-5deg); }}
            }}

            @media (max-width:850px) {{
                .kiki-walker {{ width:76px; height:76px; }}
                .fight {{ width:135px; height:135px; }}
                .impact {{ font-size:17px; }}
            }}

            @media (prefers-reduced-motion: reduce) {{
                .path-poker,.path-lead,.path-red,.path-scholar,
                .sprite-poker,.sprite-lead,.sprite-red,.sprite-scholar,
                .fight-red-lead,.fight-poker-lead,.impact-red,.impact-poker {{
                    animation-duration:70s !important;
                }}
            }}
        </style>

        <div class="kiki-stage" aria-hidden="true">
            <div class="kiki-walker path-poker"><div class="kiki-sprite sprite-poker"></div></div>
            <div class="kiki-walker path-lead"><div class="kiki-sprite sprite-lead"></div></div>
            <div class="kiki-walker path-red"><div class="kiki-sprite sprite-red"></div></div>
            <div class="kiki-walker path-scholar"><div class="kiki-sprite sprite-scholar"></div></div>
            <div class="fight fight-red-lead"><div class="kiki-sprite sprite-fight-red-lead"></div></div>
            <div class="fight fight-poker-lead"><div class="kiki-sprite sprite-fight-poker-lead"></div></div>
            <div class="impact impact-red">BỐP! 💥</div>
            <div class="impact impact-poker">ALL IN! 💢</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
