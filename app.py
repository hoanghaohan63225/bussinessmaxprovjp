from __future__ import annotations

import hashlib
import os
from pathlib import Path

import pandas as pd
import streamlit as st

from src.intent import PRESETS, decode_intent, decode_preset
from src.matcher import evaluate_products, load_catalog
from src.optimizer import assess_scenarios, build_b2a_response, build_transaction_handoff, generate_scenarios, json_ready, select_best_offer

CATALOG_PATH = Path(__file__).parent / "data" / "catalog.csv"
DEFAULT_REQUEST = "I need a gaming laptop under AUD 1,300, strong GPU performance, delivery within 3 days, and at least 2 years of warranty. I care more about gaming performance than portability."

st.set_page_config(page_title="bussinessmaxprovjp", layout="wide")
st.title("bussinessmaxprovjp")
st.caption("Merchant-side B2A offer intelligence demo · synthetic catalogue and economics")
st.info("Synthetic hackathon demo. No real payment is processed and no real-world purchase probability is claimed.")

mode_label = st.sidebar.selectbox("Intent execution mode", ["Controlled mapping", "Fallback preset", "LLM mode (optional Gemini)"])
preset_name = st.sidebar.selectbox("Demo preset", list(PRESETS)) if mode_label == "Fallback preset" else None
request_text = st.text_area("Buyer Agent Request", value=DEFAULT_REQUEST, height=120)
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

signature = hashlib.sha1(f"{mode_label}|{preset_name}|{request_text}".encode()).hexdigest()
if st.session_state.get("input_signature") not in (None, signature):
    for key in ("pipeline", "transaction"):
        st.session_state.pop(key, None)
st.session_state["input_signature"] = signature

if st.button("Run merchant pipeline", type="primary"):
    try:
        products = load_catalog(CATALOG_PATH)
        if mode_label == "Fallback preset":
            intent, intent_mode, fallback_reason = decode_preset(preset_name)
        else:
            intent, intent_mode, fallback_reason = decode_intent(request_text, prefer_llm=mode_label.startswith("LLM"), api_key=api_key)
        eligible, rejected_products = evaluate_products(products, intent)
        scenarios = [s for candidate in eligible for s in generate_scenarios(candidate)]
        feasible, rejected_scenarios = assess_scenarios(scenarios, intent)
        selected = select_best_offer(feasible)
        response = build_b2a_response(intent, selected, intent_mode=intent_mode, no_eligible=not eligible)
        st.session_state["pipeline"] = {"intent": intent, "intent_mode": intent_mode, "fallback_reason": fallback_reason, "eligible": eligible, "rejected_products": rejected_products, "scenario_count": len(scenarios), "feasible_count": len(feasible), "rejected_scenarios": rejected_scenarios, "selected": selected, "response": response}
        st.session_state.pop("transaction", None)
    except Exception as exc:
        st.error(f"Pipeline validation error: {exc}")

pipeline = st.session_state.get("pipeline")
if pipeline:
    mode_display = {"llm": "LLM mode", "controlled_mapping": "controlled mapping", "fallback_preset": "fallback preset"}[pipeline["intent_mode"]]
    st.subheader("1. Decoded Intent")
    st.write(f"**Execution mode:** `{mode_display}`")
    if pipeline.get("fallback_reason"):
        st.warning(pipeline["fallback_reason"])
    st.json(pipeline["intent"])

    st.subheader("2. Catalogue Matching")
    rows = [{"product_id": p["product_id"], "name": p["name"], "buyer_fit": round(p["match"]["buyer_fit"], 3), "use_case_fit": round(p["match"]["components"]["use_case_fit"], 3), "performance_fit": round(p["match"]["components"]["performance_fit"], 3), "portability_fit": round(p["match"]["components"]["portability_fit"], 3), "battery_fit": round(p["match"]["components"]["battery_fit"], 3)} for p in pipeline["eligible"]]
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.warning("No product passed immutable product-level constraints.")
    with st.expander("Rejected products / reasons"):
        st.json(pipeline["rejected_products"])

    st.subheader("3. Merchant Offer Optimisation")
    st.write(f"Generated **{pipeline['scenario_count']}** bounded scenarios; **{pipeline['feasible_count']}** are feasible.")
    selected = pipeline["selected"]
    if selected:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Product", selected["product_name"])
        c2.metric("Offer price", f"AUD {selected['offer_price']:.2f}")
        c3.metric("Buyer total", f"AUD {selected['buyer_total_price']:.2f}")
        c4.metric("Warranty", f"{selected['warranty_years']} years")
        st.write(f"Buyer fit **{selected['buyer_fit']:.3f}** · merchant contribution margin **{float(selected['contribution_margin_rate']):.1%}** · combined offer score **{selected['offer_score']:.3f}**")
        st.caption("Economics shown are synthetic/illustrative merchant-side values.")
    else:
        st.error(pipeline["response"]["reason"])

    st.subheader("4. Machine-readable B2A Offer")
    st.json(json_ready(pipeline["response"]))

    st.subheader("5. Buyer Accept → Synthetic Transaction Handoff")
    if selected:
        if st.button("Accept recommended offer"):
            st.session_state["transaction"] = build_transaction_handoff(selected, selected["offer_id"])
        if st.session_state.get("transaction"):
            st.success("transaction_ready (synthetic demo handoff)")
            st.json(json_ready(st.session_state["transaction"]))
        else:
            st.caption("Transaction handoff appears only after explicit acceptance of the current feasible offer.")
    else:
        st.caption("Accept is unavailable because there is no feasible current offer.")
