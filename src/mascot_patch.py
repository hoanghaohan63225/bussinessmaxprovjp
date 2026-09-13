from __future__ import annotations

import base64
import json
from pathlib import Path

import streamlit.components.v1 as components

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

    The layer is visual-only: it lives above the Streamlit UI with
    pointer-events disabled, so it cannot change the B2A pipeline or block
    any controls. Special pairs only mock-fight when they physically meet.
    """
    uris = {
        "poker": _data_uri("poker.webp"),
        "lead": _data_uri("lead.webp"),
        "red": _data_uri("red.webp"),
        "scholar": _data_uri("scholar.webp"),
    }
    if not all(uris.values()):
        return

    characters = [
        {
            "id": "poker",
            "label": "Poker Kiki",
            "src": uris["poker"],
            "size": 110,
            "x": 0.10,
            "y": 0.68,
            "vx": 68,
            "vy": -31,
        },
        {
            "id": "lead",
            "label": "Lead Kiki",
            "src": uris["lead"],
            "size": 112,
            "x": 0.80,
            "y": 0.63,
            "vx": -63,
            "vy": -27,
        },
        {
            "id": "red",
            "label": "Red Kiki",
            "src": uris["red"],
            "size": 106,
            "x": 0.78,
            "y": 0.20,
            "vx": -54,
            "vy": 39,
        },
        {
            "id": "scholar",
            "label": "Scholar Kiki",
            "src": uris["scholar"],
            "size": 104,
            "x": 0.13,
            "y": 0.16,
            "vx": 49,
            "vy": 43,
        },
    ]

    config = json.dumps(characters, ensure_ascii=False)
    html = r"""
<script>
(() => {
    const CHARACTERS = __CHARACTERS__;
    const parentWindow = window.parent;
    const doc = parentWindow.document;

    if (parentWindow.__kikiMascotRAF) {
        parentWindow.cancelAnimationFrame(parentWindow.__kikiMascotRAF);
        parentWindow.__kikiMascotRAF = null;
    }

    const oldRoot = doc.getElementById("kiki-mascot-root");
    if (oldRoot) oldRoot.remove();
    const oldStyle = doc.getElementById("kiki-mascot-style");
    if (oldStyle) oldStyle.remove();

    const style = doc.createElement("style");
    style.id = "kiki-mascot-style";
    style.textContent = `
        /* The old blue bot retires. Its four replacements have arrived. */
        .b2a-bot-stage { display: none !important; }

        #kiki-mascot-root {
            position: fixed;
            inset: 0;
            z-index: 9998;
            overflow: hidden;
            pointer-events: none;
            contain: layout style;
        }

        .kiki-char {
            position: absolute;
            left: 0;
            top: 0;
            width: 108px;
            height: 108px;
            will-change: transform;
            pointer-events: none;
        }

        .kiki-visual {
            width: 100%;
            height: 100%;
            transform-origin: center bottom;
            filter: drop-shadow(0 9px 10px rgba(15, 35, 55, .20));
            will-change: transform;
        }

        .kiki-visual img {
            width: 100%;
            height: 100%;
            display: block;
            object-fit: contain;
            animation: kiki-bob 1.05s ease-in-out infinite alternate;
            user-select: none;
            -webkit-user-drag: none;
        }

        .kiki-char[data-id="red"] .kiki-visual img {
            animation-duration: .82s;
        }

        .kiki-char[data-id="scholar"] .kiki-visual img {
            animation-duration: 1.28s;
        }

        .kiki-char.fighting .kiki-visual {
            animation: kiki-fight .16s ease-in-out infinite alternate;
        }

        .kiki-char.bumped .kiki-visual {
            animation: kiki-bump .28s ease-out;
        }

        .kiki-impact {
            position: fixed;
            z-index: 10000;
            pointer-events: none;
            font: 900 23px/1 system-ui, sans-serif;
            color: #fff;
            letter-spacing: .02em;
            text-shadow:
                -2px -2px 0 #10243e,
                 2px -2px 0 #10243e,
                -2px  2px 0 #10243e,
                 2px  2px 0 #10243e;
            animation: kiki-impact .78s cubic-bezier(.2,.9,.3,1) forwards;
        }

        @keyframes kiki-bob {
            from { transform: translateY(1px) rotate(-1.2deg); }
            to   { transform: translateY(-7px) rotate(1.2deg); }
        }

        @keyframes kiki-fight {
            from { transform: translate(-5px,-5px) rotate(-11deg) scale(1.12); }
            to   { transform: translate( 7px, 2px) rotate( 12deg) scale(1.16); }
        }

        @keyframes kiki-bump {
            0%   { transform: scale(1); }
            45%  { transform: scale(.88) rotate(-8deg); }
            100% { transform: scale(1); }
        }

        @keyframes kiki-impact {
            0%   { opacity: 0; transform: translate(-50%,-50%) scale(.35) rotate(-14deg); }
            18%  { opacity: 1; transform: translate(-50%,-60%) scale(1.18) rotate(8deg); }
            72%  { opacity: 1; transform: translate(-50%,-90%) scale(1) rotate(-4deg); }
            100% { opacity: 0; transform: translate(-50%,-145%) scale(1.25) rotate(6deg); }
        }

        @media (max-width: 850px) {
            .kiki-char { width: 76px !important; height: 76px !important; }
            .kiki-impact { font-size: 17px; }
        }

        @media (prefers-reduced-motion: reduce) {
            .kiki-visual img { animation-duration: 2.5s; }
        }
    `;
    doc.head.appendChild(style);

    const root = doc.createElement("div");
    root.id = "kiki-mascot-root";
    root.setAttribute("aria-hidden", "true");
    doc.body.appendChild(root);

    const mobile = () => parentWindow.innerWidth <= 850;
    const viewport = () => ({
        w: Math.max(320, parentWindow.innerWidth),
        h: Math.max(320, parentWindow.innerHeight),
    });

    const now = performance.now();
    const actors = CHARACTERS.map((c, index) => {
        const el = doc.createElement("div");
        el.className = "kiki-char";
        el.dataset.id = c.id;
        const size = mobile() ? 76 : c.size;
        el.style.width = `${size}px`;
        el.style.height = `${size}px`;

        const visual = doc.createElement("div");
        visual.className = "kiki-visual";
        const img = doc.createElement("img");
        img.src = c.src;
        img.alt = "";
        visual.appendChild(img);
        el.appendChild(visual);
        root.appendChild(el);

        const vp = viewport();
        return {
            ...c,
            el,
            visual,
            size,
            x: Math.min(vp.w - size - 4, Math.max(4, c.x * vp.w)),
            y: Math.min(vp.h - size - 4, Math.max(4, c.y * vp.h)),
            vx: c.vx,
            vy: c.vy,
            fightUntil: 0,
            bumpedUntil: 0,
            nextTurn: now + 2600 + index * 620,
        };
    });

    const pairKey = (a, b) => [a.id, b.id].sort().join("-");
    const specialPair = (a, b) => {
        const key = pairKey(a, b);
        return key === "lead-red" || key === "lead-poker";
    };

    const pairCooldown = new Map();
    const collisionCooldown = new Map();

    function center(c) {
        return { x: c.x + c.size / 2, y: c.y + c.size / 2 };
    }

    function makeImpact(text, x, y) {
        const impact = doc.createElement("div");
        impact.className = "kiki-impact";
        impact.textContent = text;
        impact.style.left = `${x}px`;
        impact.style.top = `${y}px`;
        root.appendChild(impact);
        setTimeout(() => impact.remove(), 850);
    }

    function fightWords(a, b) {
        const key = pairKey(a, b);
        if (key === "lead-red") return ["BỐP!", "MEOW!", "GÂU!", "💥"];
        if (key === "lead-poker") return ["CHÁT!", "ALL IN!", "MEOW!", "💢"];
        return ["ỤI!", "💫"];
    }

    function clampSpeed(c, minSpeed = 38, maxSpeed = 82) {
        const speed = Math.hypot(c.vx, c.vy) || 1;
        const target = Math.max(minSpeed, Math.min(maxSpeed, speed));
        c.vx = c.vx / speed * target;
        c.vy = c.vy / speed * target;
    }

    function separateAndBounce(a, b, dx, dy, dist, overlap) {
        const nx = dx / Math.max(dist, 0.001);
        const ny = dy / Math.max(dist, 0.001);
        const push = Math.max(2, overlap / 2 + 1);
        a.x -= nx * push;
        a.y -= ny * push;
        b.x += nx * push;
        b.y += ny * push;

        const av = a.vx * nx + a.vy * ny;
        const bv = b.vx * nx + b.vy * ny;
        const impulse = bv - av;
        a.vx += impulse * nx;
        a.vy += impulse * ny;
        b.vx -= impulse * nx;
        b.vy -= impulse * ny;

        a.vx += -nx * 13;
        a.vy += -ny * 13;
        b.vx += nx * 13;
        b.vy += ny * 13;
        clampSpeed(a);
        clampSpeed(b);
    }

    function startFight(a, b, t) {
        const key = pairKey(a, b);
        const lastFight = pairCooldown.get(key) || 0;
        if (t - lastFight < 5200) return false;
        pairCooldown.set(key, t);

        a.fightUntil = t + 950;
        b.fightUntil = t + 950;
        const ca = center(a);
        const cb = center(b);
        const words = fightWords(a, b);
        makeImpact(words[Math.floor(Math.random() * words.length)], (ca.x + cb.x) / 2, (ca.y + cb.y) / 2 - 18);

        setTimeout(() => {
            if (!root.isConnected) return;
            const ca2 = center(a);
            const cb2 = center(b);
            const words2 = fightWords(a, b);
            makeImpact(words2[Math.floor(Math.random() * words2.length)], (ca2.x + cb2.x) / 2, (ca2.y + cb2.y) / 2 - 12);
        }, 340);
        return true;
    }

    function wander(c, t) {
        if (t < c.nextTurn || t < c.fightUntil) return;
        c.nextTurn = t + 2400 + Math.random() * 3200;
        const angle = (Math.random() - .5) * .62;
        const cos = Math.cos(angle);
        const sin = Math.sin(angle);
        const vx = c.vx * cos - c.vy * sin;
        const vy = c.vx * sin + c.vy * cos;
        c.vx = vx;
        c.vy = vy;
        clampSpeed(c, 42, 76);
    }

    function mildAttraction(a, b, dt, t) {
        if (!specialPair(a, b)) return;
        const key = pairKey(a, b);
        if (t - (pairCooldown.get(key) || 0) < 5200) return;
        const ca = center(a);
        const cb = center(b);
        const dx = cb.x - ca.x;
        const dy = cb.y - ca.y;
        const dist = Math.hypot(dx, dy);
        if (dist < 170 || dist > 285) return;
        const strength = 5.2 * dt;
        a.vx += dx / dist * strength;
        a.vy += dy / dist * strength;
        b.vx -= dx / dist * strength;
        b.vy -= dy / dist * strength;
        clampSpeed(a, 38, 80);
        clampSpeed(b, 38, 80);
    }

    function handleCollisions(t) {
        for (let i = 0; i < actors.length; i++) {
            for (let j = i + 1; j < actors.length; j++) {
                const a = actors[i];
                const b = actors[j];
                const ca = center(a);
                const cb = center(b);
                const dx = cb.x - ca.x;
                const dy = cb.y - ca.y;
                const dist = Math.hypot(dx, dy) || 0.001;
                const minDist = (a.size + b.size) * 0.38;
                if (dist >= minDist) continue;

                const key = pairKey(a, b);
                const overlap = minDist - dist;
                separateAndBounce(a, b, dx, dy, dist, overlap);

                if (t - (collisionCooldown.get(key) || 0) < 520) continue;
                collisionCooldown.set(key, t);

                if (specialPair(a, b)) {
                    startFight(a, b, t);
                } else {
                    a.bumpedUntil = t + 300;
                    b.bumpedUntil = t + 300;
                    makeImpact("ỤI!", (ca.x + cb.x) / 2, (ca.y + cb.y) / 2 - 10);
                }
            }
        }
    }

    let last = performance.now();
    function frame(t) {
        if (!root.isConnected) return;
        const dt = Math.min(.034, Math.max(.001, (t - last) / 1000));
        last = t;
        const vp = viewport();

        for (let i = 0; i < actors.length; i++) {
            for (let j = i + 1; j < actors.length; j++) {
                mildAttraction(actors[i], actors[j], dt, t);
            }
        }

        actors.forEach(c => {
            const desiredSize = mobile() ? 76 : c.size;
            if (desiredSize !== c.size) {
                c.size = desiredSize;
                c.el.style.width = `${c.size}px`;
                c.el.style.height = `${c.size}px`;
            }

            wander(c, t);
            const fightSlow = t < c.fightUntil ? .42 : 1;
            c.x += c.vx * dt * fightSlow;
            c.y += c.vy * dt * fightSlow;

            const maxX = Math.max(4, vp.w - c.size - 4);
            const maxY = Math.max(4, vp.h - c.size - 4);
            if (c.x <= 4) { c.x = 4; c.vx = Math.abs(c.vx); }
            if (c.x >= maxX) { c.x = maxX; c.vx = -Math.abs(c.vx); }
            if (c.y <= 4) { c.y = 4; c.vy = Math.abs(c.vy); }
            if (c.y >= maxY) { c.y = maxY; c.vy = -Math.abs(c.vy); }
        });

        handleCollisions(t);

        actors.forEach(c => {
            c.el.classList.toggle("fighting", t < c.fightUntil);
            c.el.classList.toggle("bumped", t < c.bumpedUntil);
            c.el.style.transform = `translate3d(${c.x}px, ${c.y}px, 0)`;
            c.visual.style.transform = `scaleX(${c.vx < 0 ? -1 : 1})`;
        });

        parentWindow.__kikiMascotRAF = parentWindow.requestAnimationFrame(frame);
    }

    parentWindow.__kikiMascotRAF = parentWindow.requestAnimationFrame(frame);
})();
</script>
""".replace("__CHARACTERS__", config)

    components.html(html, height=0, width=0)
