from __future__ import annotations

import hashlib
import os
from pathlib import Path

import pandas as pd
import streamlit as st

from src.intent import PRESETS, decode_intent, decode_preset
from src.matcher import evaluate_products, load_catalog
from src.optimizer import (
    assess_scenarios,
    build_b2a_response,
    build_transaction_handoff,
    generate_scenarios,
    json_ready,
    select_best_offer,
)

CATALOG_PATH = Path(__file__).parent / "data" / "catalog.csv"
DEFAULT_REQUEST = (
    "I need a gaming laptop under AUD 1,300, strong GPU performance, delivery within 3 days, "
    "and at least 2 years of warranty. I care more about gaming performance than portability."
)


def _get_api_key() -> str | None:
    key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if key:
        return key
    try:
        return st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
    except Exception:
        return None


def _step_header(number: int, title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="step-header">
            <div class="step-number">{number:02d}</div>
            <div>
                <div class="step-title">{title}</div>
                <div class="step-subtitle">{subtitle}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.set_page_config(
    page_title="bussinessmaxprovjp · B2A Offer Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        :root {
            --ink: #10243e;
            --muted: #617087;
            --navy: #0b1f36;
            --navy-2: #123a5a;
            --teal: #14b8a6;
            --sky: #38bdf8;
            --surface: #ffffff;
            --line: #dce6ef;
            --soft: #f5f8fb;
            --success: #0f8f78;
        }

        .stApp {
            background:
                radial-gradient(circle at 85% 5%, rgba(56, 189, 248, 0.08), transparent 24rem),
                linear-gradient(180deg, #f8fbfd 0%, #ffffff 30%);
        }

        .block-container {
            max-width: 1280px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        #MainMenu, footer {
            visibility: hidden;
        }

        div[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0b1f36 0%, #102c48 100%);
            border-right: 1px solid rgba(255,255,255,0.08);
        }

        div[data-testid="stSidebar"] * {
            color: #edf6fb;
        }

        div[data-testid="stSidebar"] label,
        div[data-testid="stSidebar"] p {
            color: #dcecf5 !important;
        }

        .sidebar-brand {
            padding: 0.25rem 0 1.1rem 0;
            border-bottom: 1px solid rgba(255,255,255,0.12);
            margin-bottom: 1.15rem;
        }

        .sidebar-brand .eyebrow {
            font-size: 0.72rem;
            letter-spacing: 0.16em;
            font-weight: 700;
            color: #7dd3fc;
            text-transform: uppercase;
        }

        .sidebar-brand .brand {
            margin-top: 0.35rem;
            font-size: 1.18rem;
            font-weight: 800;
            color: #ffffff;
        }

        .sidebar-brand .copy {
            margin-top: 0.25rem;
            color: #b9ccda;
            font-size: 0.82rem;
            line-height: 1.45;
        }

        .hero {
            padding: 2.15rem 2.35rem;
            border-radius: 24px;
            background:
                radial-gradient(circle at 84% 12%, rgba(56,189,248,0.28), transparent 16rem),
                linear-gradient(135deg, #081a2d 0%, #0c2b48 58%, #0f4a61 100%);
            box-shadow: 0 20px 50px rgba(13, 35, 55, 0.15);
            border: 1px solid rgba(255,255,255,0.08);
            margin-bottom: 1.25rem;
        }

        .hero-badge {
            display: inline-block;
            padding: 0.34rem 0.72rem;
            border-radius: 999px;
            background: rgba(20,184,166,0.14);
            border: 1px solid rgba(94,234,212,0.38);
            color: #99f6e4;
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.11em;
            text-transform: uppercase;
        }

        .hero-title {
            margin-top: 0.95rem;
            color: #ffffff;
            font-size: clamp(2rem, 4vw, 3.35rem);
            font-weight: 850;
            letter-spacing: -0.035em;
            line-height: 1.02;
        }

        .hero-copy {
            margin-top: 0.78rem;
            max-width: 850px;
            color: #d7e8f2;
            font-size: 1.04rem;
            line-height: 1.62;
        }

        .hero-flow {
            margin-top: 1.35rem;
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
            align-items: center;
        }

        .flow-chip {
            padding: 0.45rem 0.72rem;
            border-radius: 10px;
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.12);
            color: #f8fdff;
            font-size: 0.82rem;
            font-weight: 650;
        }

        .flow-arrow {
            color: #67e8f9;
            font-weight: 800;
        }

        .trust-strip {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.8rem;
            margin: 0.85rem 0 1.4rem 0;
        }

        .trust-card {
            background: rgba(255,255,255,0.92);
            border: 1px solid var(--line);
            border-radius: 16px;
            padding: 0.95rem 1rem;
            box-shadow: 0 8px 22px rgba(15, 35, 55, 0.05);
        }

        .trust-label {
            color: var(--muted);
            font-size: 0.72rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .trust-value {
            color: var(--ink);
            font-size: 0.95rem;
            font-weight: 750;
            margin-top: 0.2rem;
        }

        .input-shell {
            background: rgba(255,255,255,0.94);
            border: 1px solid var(--line);
            border-radius: 20px;
            padding: 1.25rem 1.35rem 0.35rem 1.35rem;
            box-shadow: 0 10px 28px rgba(15,35,55,0.05);
            margin-bottom: 1.4rem;
        }

        .section-kicker {
            color: #0e7490;
            font-size: 0.72rem;
            font-weight: 850;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            margin-bottom: 0.2rem;
        }

        .section-heading {
            color: var(--ink);
            font-size: 1.2rem;
            font-weight: 800;
            margin-bottom: 0.12rem;
        }

        .section-copy {
            color: var(--muted);
            font-size: 0.88rem;
            margin-bottom: 0.75rem;
        }

        .step-header {
            display: flex;
            align-items: center;
            gap: 0.9rem;
            padding: 1rem 1.1rem;
            margin-top: 1.2rem;
            margin-bottom: 0.85rem;
            border-radius: 16px;
            border: 1px solid var(--line);
            background: linear-gradient(90deg, #ffffff 0%, #f7fbfd 100%);
        }

        .step-number {
            width: 2.45rem;
            height: 2.45rem;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 12px;
            color: #ffffff;
            background: linear-gradient(135deg, #0f766e 0%, #0891b2 100%);
            font-weight: 850;
            font-size: 0.82rem;
            box-shadow: 0 8px 18px rgba(8,145,178,0.18);
        }

        .step-title {
            color: var(--ink);
            font-size: 1.06rem;
            font-weight: 820;
        }

        .step-subtitle {
            color: var(--muted);
            font-size: 0.82rem;
            margin-top: 0.08rem;
        }

        div[data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid var(--line);
            border-radius: 16px;
            padding: 0.85rem 1rem;
            box-shadow: 0 8px 20px rgba(15,35,55,0.04);
        }

        div[data-testid="stMetricLabel"] {
            color: #64748b;
        }

        div[data-testid="stMetricValue"] {
            color: #0b2a42;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid var(--line);
            border-radius: 14px;
            overflow: hidden;
        }

        div.stButton > button {
            border-radius: 12px;
            min-height: 2.8rem;
            font-weight: 750;
            border: 0;
            box-shadow: 0 8px 18px rgba(8,145,178,0.15);
        }

        div.stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #0f766e 0%, #0891b2 100%);
        }

        .selected-banner {
            margin: 0.9rem 0 0.75rem 0;
            padding: 0.8rem 0.95rem;
            border-radius: 13px;
            background: #ecfdf8;
            border: 1px solid #b7eadf;
            color: #0d5f52;
            font-size: 0.88rem;
            font-weight: 700;
        }

        .micro-note {
            color: #738196;
            font-size: 0.78rem;
            line-height: 1.45;
        }

        @media (max-width: 850px) {
            .trust-strip {
                grid-template-columns: 1fr;
            }

            .hero {
                padding: 1.6rem 1.35rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    """
    <div class="sidebar-brand">
        <div class="eyebrow">Round 2 MVP</div>
        <div class="brand">bussinessmaxprovjp</div>
        <div class="copy">Merchant-side B2A offer intelligence. Configure the intent engine, then run one auditable offer pipeline.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

mode_label = st.sidebar.selectbox(
    "Intent execution mode",
    ["Controlled mapping", "Fallback preset", "LLM mode (optional Gemini)"],
    help="Controlled mapping is the reliable no-API-key demo path. Gemini is optional.",
)
preset_name = st.sidebar.selectbox("Demo preset", list(PRESETS)) if mode_label == "Fallback preset" else None
api_key = _get_api_key()

st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">Merchant-side B2A · Working MVP</div>
        <div class="hero-title">Construct the right offer<br/>for an AI-mediated buyer.</div>
        <div class="hero-copy">
            Decode complex buyer intent, filter the catalogue, optimise bounded merchant scenarios,
            and return a feasible machine-readable offer without handing pricing or margin logic to an LLM.
        </div>
        <div class="hero-flow">
            <span class="flow-chip">Buyer AI Request</span>
            <span class="flow-arrow">→</span>
            <span class="flow-chip">Intent</span>
            <span class="flow-arrow">→</span>
            <span class="flow-chip">Catalogue Match</span>
            <span class="flow-arrow">→</span>
            <span class="flow-chip">Offer Optimisation</span>
            <span class="flow-arrow">→</span>
            <span class="flow-chip">B2A JSON</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="trust-strip">
        <div class="trust-card">
            <div class="trust-label">Decision principle</div>
            <div class="trust-value">Buyer fit × Merchant economics</div>
        </div>
        <div class="trust-card">
            <div class="trust-label">AI responsibility</div>
            <div class="trust-value">Language understanding, not margin math</div>
        </div>
        <div class="trust-card">
            <div class="trust-label">Demo boundary</div>
            <div class="trust-value">Synthetic catalogue · No real payment</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="input-shell">
        <div class="section-kicker">01 · Buyer request</div>
        <div class="section-heading">Describe what the buyer agent needs</div>
        <div class="section-copy">Use natural language. Hard constraints stay hard; softer preferences influence ranking only.</div>
    """,
    unsafe_allow_html=True,
)

request_text = st.text_area(
    "Buyer Agent Request",
    value=DEFAULT_REQUEST,
    height=125,
    label_visibility="collapsed",
)

run_clicked = st.button("Run merchant pipeline", type="primary", width="stretch")
st.markdown("</div>", unsafe_allow_html=True)

st.info(
    "Synthetic hackathon demo. No real payment is processed and no real-world purchase probability is claimed.",
    icon="ℹ️",
)

signature = hashlib.sha1(f"{mode_label}|{preset_name}|{request_text}".encode()).hexdigest()
if st.session_state.get("input_signature") not in (None, signature):
    for key in ("pipeline", "transaction"):
        st.session_state.pop(key, None)
st.session_state["input_signature"] = signature

if run_clicked:
    # Never leave a stale offer visible if this run fails validation or an API call errors.
    st.session_state.pop("pipeline", None)
    st.session_state.pop("transaction", None)
    try:
        products = load_catalog(CATALOG_PATH)
        if mode_label == "Fallback preset":
            intent, intent_mode, fallback_reason = decode_preset(preset_name)
        else:
            intent, intent_mode, fallback_reason = decode_intent(
                request_text,
                prefer_llm=mode_label.startswith("LLM"),
                api_key=api_key,
            )
        eligible, rejected_products = evaluate_products(products, intent)
        scenarios = [s for candidate in eligible for s in generate_scenarios(candidate)]
        feasible, rejected_scenarios = assess_scenarios(scenarios, intent)
        selected = select_best_offer(feasible)
        response = build_b2a_response(
            intent,
            selected,
            intent_mode=intent_mode,
            no_eligible=not eligible,
        )
        st.session_state["pipeline"] = {
            "intent": intent,
            "intent_mode": intent_mode,
            "fallback_reason": fallback_reason,
            "eligible": eligible,
            "rejected_products": rejected_products,
            "scenario_count": len(scenarios),
            "feasible_count": len(feasible),
            "rejected_scenarios": rejected_scenarios,
            "selected": selected,
            "response": response,
        }
    except Exception as exc:
        st.error(f"Pipeline validation error: {exc}")

pipeline = st.session_state.get("pipeline")
if pipeline:
    mode_display = {
        "llm": "LLM mode",
        "controlled_mapping": "Controlled mapping",
        "fallback_preset": "Fallback preset",
    }[pipeline["intent_mode"]]

    decision_label = "Offer available" if pipeline["selected"] else "No feasible offer"
    summary_1, summary_2, summary_3, summary_4 = st.columns(4)
    summary_1.metric("Execution mode", mode_display)
    summary_2.metric("Eligible products", len(pipeline["eligible"]))
    summary_3.metric("Feasible scenarios", pipeline["feasible_count"])
    summary_4.metric("Decision", decision_label)

    _step_header(
        2,
        "Decoded intent",
        "Natural-language intent becomes a structured, auditable merchant input.",
    )
    if pipeline.get("fallback_reason"):
        st.warning(pipeline["fallback_reason"])
    st.json(pipeline["intent"])

    _step_header(
        3,
        "Catalogue matching",
        "Immutable constraints filter first; semantic fit ranks only products that remain eligible.",
    )
    rows = [
        {
            "product_id": p["product_id"],
            "name": p["name"],
            "buyer_fit": round(p["match"]["buyer_fit"], 3),
            "use_case_fit": round(p["match"]["components"]["use_case_fit"], 3),
            "performance_fit": round(p["match"]["components"]["performance_fit"], 3),
            "portability_fit": round(p["match"]["components"]["portability_fit"], 3),
            "battery_fit": round(p["match"]["components"]["battery_fit"], 3),
        }
        for p in pipeline["eligible"]
    ]
    if rows:
        st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
    else:
        st.warning("No product passed immutable product-level constraints.")
    with st.expander("Rejected products · show reasons"):
        st.json(pipeline["rejected_products"])

    _step_header(
        4,
        "Merchant offer optimisation",
        "Generate bounded price, shipping and warranty scenarios, then keep only economically feasible offers.",
    )
    st.caption(
        f"Generated {pipeline['scenario_count']} bounded scenarios · "
        f"{pipeline['feasible_count']} passed all offer-level constraints."
    )

    selected = pipeline["selected"]
    if selected:
        st.markdown(
            f"""
            <div class="selected-banner">
                Recommended offer · {selected["product_name"]} · feasible for the buyer and acceptable for merchant economics
            </div>
            """,
            unsafe_allow_html=True,
        )
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Product", selected["product_name"])
        c2.metric("Offer price", f"AUD {selected['offer_price']:.2f}")
        c3.metric("Buyer total", f"AUD {selected['buyer_total_price']:.2f}")
        c4.metric("Warranty", f"{selected['warranty_years']} years")

        c5, c6, c7 = st.columns(3)
        c5.metric("Buyer fit", f"{selected['buyer_fit']:.3f}")
        c6.metric("Contribution margin", f"{float(selected['contribution_margin_rate']):.1%}")
        c7.metric("Combined offer score", f"{selected['offer_score']:.3f}")

        st.markdown(
            '<div class="micro-note">Economics are synthetic/illustrative merchant-side values. '
            "Hard constraints are checked before soft scoring.</div>",
            unsafe_allow_html=True,
        )
    else:
        st.error(pipeline["response"]["reason"])

    _step_header(
        5,
        "Machine-readable B2A offer",
        "The selected decision is exposed as a structured object for the next machine step.",
    )
    st.json(json_ready(pipeline["response"]))

    _step_header(
        6,
        "Buyer acceptance → transaction handoff",
        "A synthetic transaction object appears only after explicit acceptance of the current feasible offer.",
    )
    if selected:
        if st.button("Accept recommended offer", type="primary", width="stretch"):
            st.session_state["transaction"] = build_transaction_handoff(selected, selected["offer_id"])
        if st.session_state.get("transaction"):
            st.success("transaction_ready · synthetic demo handoff", icon="✅")
            st.json(json_ready(st.session_state["transaction"]))
        else:
            st.caption(
                "No transaction object yet. Acceptance is explicit; the system does not silently auto-close the offer."
            )
    else:
        st.caption("Accept is unavailable because there is no feasible current offer.")
