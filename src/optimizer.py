"""Deterministic merchant scenario generation, economics, selection and handoff."""
from __future__ import annotations

import hashlib
import json
from decimal import Decimal, ROUND_HALF_UP
from typing import Any

CENT = Decimal("0.01")
DISCOUNT_RATES = (Decimal("0.00"), Decimal("0.03"), Decimal("0.05"))
DEFAULT_MIN_MARGIN_RATE = Decimal("0.10")
DEFAULT_ALPHA = 0.5
DEFAULT_BETA = 0.5


def money(value: Any) -> Decimal:
    return Decimal(str(value)).quantize(CENT, rounding=ROUND_HALF_UP)


def _scenario_id(product_id: str, discount: Decimal, shipping_fee: Decimal, warranty_years: int) -> str:
    discount_bp = int(discount * 10000)
    ship_cents = int(shipping_fee * 100)
    return f"{product_id}-D{discount_bp:04d}-S{ship_cents:06d}-W{warranty_years}"


def generate_scenarios(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    base_price = money(candidate["base_price"])
    base_shipping = money(candidate["buyer_shipping_fee"])
    merchant_shipping = money(candidate["merchant_shipping_cost"])
    warranty_options = [(int(candidate["base_warranty_years"]), Decimal("0.00"), "base")]
    if candidate.get("extended_warranty_years") is not None:
        warranty_options.append((int(candidate["extended_warranty_years"]), money(candidate["extended_warranty_cost"]), "extended"))

    scenarios: dict[str, dict[str, Any]] = {}
    for discount in DISCOUNT_RATES:
        offer_price = (base_price * (Decimal("1.00") - discount)).quantize(CENT, rounding=ROUND_HALF_UP)
        for shipping_fee in (base_shipping, Decimal("0.00")):
            for warranty_years, warranty_cost, warranty_type in warranty_options:
                offer_id = _scenario_id(candidate["product_id"], discount, shipping_fee, warranty_years)
                scenarios[offer_id] = {
                    "offer_id": offer_id,
                    "product_id": candidate["product_id"],
                    "product_name": candidate["name"],
                    "offer_price": offer_price,
                    "discount_rate": discount,
                    "buyer_shipping_fee": shipping_fee,
                    "merchant_shipping_cost": merchant_shipping,
                    "delivery_days": int(candidate["delivery_days"]),
                    "warranty_years": warranty_years,
                    "warranty_type": warranty_type,
                    "warranty_incremental_cost": warranty_cost,
                    "unit_cost": money(candidate["unit_cost"]),
                    "stock": int(candidate["stock"]),
                    "buyer_fit": float(candidate["match"]["buyer_fit"]),
                    "match": candidate["match"],
                    "evidence_notes": candidate.get("evidence_notes", ""),
                }
    return [scenarios[k] for k in sorted(scenarios)]


def assess_offer(scenario: dict[str, Any], intent: dict[str, Any], *, min_margin_rate: Decimal = DEFAULT_MIN_MARGIN_RATE) -> dict[str, Any]:
    assessed = dict(scenario)
    buyer_total = money(scenario["offer_price"] + scenario["buyer_shipping_fee"])
    contribution = money(buyer_total - scenario["unit_cost"] - scenario["merchant_shipping_cost"] - scenario["warranty_incremental_cost"])
    margin = contribution / buyer_total if buyer_total > 0 else Decimal("-1")
    reasons: list[str] = []

    budget = intent.get("budget_max")
    if budget is not None and buyer_total > money(budget):
        reasons.append("buyer_budget_exceeded")
    delivery_max = intent.get("delivery_days_max")
    if delivery_max is not None and int(scenario["delivery_days"]) > int(delivery_max):
        reasons.append("delivery_requirement_failed")
    warranty_min = intent.get("warranty_years_min")
    if warranty_min is not None and int(scenario["warranty_years"]) < int(warranty_min):
        reasons.append("warranty_requirement_failed")
    if int(scenario["stock"]) <= 0:
        reasons.append("out_of_stock")

    hard = set(intent.get("hard_requirements", []))
    unresolved = set(intent.get("unresolved_requirements", []))
    for requirement in sorted(hard.intersection(unresolved)):
        reasons.append(f"unverified_hard_requirement:{requirement}")

    if buyer_total <= 0:
        reasons.append("non_positive_buyer_total")
    if contribution < 0:
        reasons.append("negative_contribution")
    if buyer_total > 0 and margin < min_margin_rate:
        reasons.append("minimum_margin_failed")

    assessed.update({
        "buyer_total_price": buyer_total,
        "contribution": contribution,
        "contribution_margin_rate": margin,
        "feasible": not reasons,
        "feasibility_reasons": reasons,
    })
    return assessed


def assess_scenarios(scenarios: list[dict[str, Any]], intent: dict[str, Any], *, min_margin_rate: Decimal = DEFAULT_MIN_MARGIN_RATE) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    feasible, rejected = [], []
    for scenario in scenarios:
        assessed = assess_offer(scenario, intent, min_margin_rate=min_margin_rate)
        (feasible if assessed["feasible"] else rejected).append(assessed)
    return feasible, rejected


def safe_minmax(values: list[float]) -> list[float]:
    if not values:
        return []
    lo, hi = min(values), max(values)
    if hi == lo:
        return [0.5 for _ in values]
    span = hi - lo
    return [(v - lo) / span for v in values]


def select_best_offer(feasible: list[dict[str, Any]], *, alpha: float = DEFAULT_ALPHA, beta: float = DEFAULT_BETA) -> dict[str, Any] | None:
    if not feasible:
        return None
    buyer_scores = [float(o["buyer_fit"]) for o in feasible]
    econ_scores = [float(o["contribution_margin_rate"]) for o in feasible]
    buyer_norm = safe_minmax(buyer_scores)
    econ_norm = safe_minmax(econ_scores)
    ranked: list[dict[str, Any]] = []
    for offer, bn, en in zip(feasible, buyer_norm, econ_norm):
        item = dict(offer)
        item["normalized_buyer_fit"] = round(bn, 6)
        item["normalized_economic_score"] = round(en, 6)
        item["offer_score"] = round(alpha * bn + beta * en, 6)
        ranked.append(item)
    ranked.sort(key=lambda o: (-o["offer_score"], o["buyer_total_price"], o["product_id"], o["offer_id"]))
    return ranked[0]


def _json_number(value: Any) -> Any:
    if isinstance(value, Decimal):
        return float(value)
    return value


def build_b2a_response(intent: dict[str, Any], selected: dict[str, Any] | None, *, intent_mode: str, no_eligible: bool = False) -> dict[str, Any]:
    if selected is None:
        reason = "No catalogue product passes immutable product-level constraints." if no_eligible else "No catalogue offer satisfies all hard buyer and merchant constraints."
        return {
            "status": "no_feasible_offer",
            "reason": reason,
            "decoded_intent": intent,
            "unresolved_requirements": intent.get("unresolved_requirements", []),
            "intent_mode": intent_mode,
        }

    match = selected["match"]
    reasons = [
        "buyer total price is within budget" if intent.get("budget_max") is not None else "no hard budget supplied",
        f"semantic buyer-fit score {selected['buyer_fit']:.2f}",
        "delivery requirement satisfied" if intent.get("delivery_days_max") is not None else "delivery fact available",
        "warranty requirement satisfied" if intent.get("warranty_years_min") is not None else "warranty fact available",
    ]
    evidence = [{"state": "synthetic_demo_fact", "note": selected["evidence_notes"]}] if selected.get("evidence_notes") else [{"state": "unverified", "note": "No evidence note supplied."}]

    return {
        "status": "offer_available",
        "decoded_intent": intent,
        "recommended_offer": {
            "offer_id": selected["offer_id"],
            "product_id": selected["product_id"],
            "product_name": selected["product_name"],
            "offer_price": _json_number(selected["offer_price"]),
            "buyer_shipping_fee": _json_number(selected["buyer_shipping_fee"]),
            "buyer_total_price": _json_number(selected["buyer_total_price"]),
            "delivery_days": selected["delivery_days"],
            "warranty_years": selected["warranty_years"],
        },
        "buyer_match": {
            "score": round(float(selected["buyer_fit"]), 4),
            "component_scores": {k: round(float(v), 4) for k, v in match["components"].items()},
            "reasons": reasons,
        },
        "merchant_constraints": {"stock": "satisfied", "minimum_margin": "satisfied"},
        "evidence": evidence,
        "unresolved_requirements": intent.get("unresolved_requirements", []),
        "intent_mode": intent_mode,
    }


def build_transaction_handoff(selected: dict[str, Any] | None, accepted_offer_id: str | None) -> dict[str, Any] | None:
    if selected is None or not accepted_offer_id or selected.get("offer_id") != accepted_offer_id or not selected.get("feasible"):
        return None
    digest = hashlib.sha1(accepted_offer_id.encode("utf-8")).hexdigest()[:10].upper()
    return {
        "status": "transaction_ready",
        "order_intent": {
            "order_id": f"DEMO-ORDER-{digest}",
            "offer_id": selected["offer_id"],
            "product_id": selected["product_id"],
            "quantity": 1,
            "buyer_total_price": _json_number(selected["buyer_total_price"]),
            "currency": "AUD",
        },
        "payment_status": "not_processed_demo",
        "demo_notice": "Synthetic handoff only; no payment or production checkout occurred.",
    }


def json_ready(value: Any) -> Any:
    return json.loads(json.dumps(value, default=lambda x: float(x) if isinstance(x, Decimal) else str(x)))
