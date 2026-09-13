from decimal import Decimal
from pathlib import Path

import pytest

from src.intent import controlled_mapping, decode_intent, decode_preset, validate_intent
from src.matcher import evaluate_products, load_catalog, product_level_eligibility
from src.optimizer import assess_offer, assess_scenarios, build_b2a_response, build_transaction_handoff, generate_scenarios, safe_minmax, select_best_offer

CATALOG = Path(__file__).resolve().parents[1] / "data" / "catalog.csv"


def _products():
    return load_catalog(CATALOG)


def _intent():
    return decode_preset("Gaming under AUD 1,300")[0]


def _llm_shape(**overrides):
    value = {
        "use_case": "gaming",
        "budget_max": 1300.0,
        "delivery_days_max": 3,
        "warranty_years_min": 2,
        "hard_requirements": ["gaming", "budget", "delivery", "warranty"],
        "preferences": {"performance": 0.9, "portability": 0.3, "battery": 0.4},
        "requested_attributes": [],
        "unresolved_requirements": [],
        "assumptions": [],
    }
    value.update(overrides)
    return value


def test_catalogue_and_stock_guard():
    data = _products()
    assert len(data) == 8
    zero = next(p for p in data if p["product_id"] == "LAP-007")
    ok, reasons = product_level_eligibility(zero, _intent())
    assert not ok and "out_of_stock" in reasons


def test_hard_gaming_requires_explicit_gaming_or_gpu_evidence():
    products = _products()
    creator = next(p for p in products if p["product_id"] == "LAP-003")
    ok, reasons = product_level_eligibility(creator, _intent())
    assert not ok
    assert "gaming_capability_not_verified" in reasons

    eligible, _ = evaluate_products(products, _intent())
    assert all(p["product_id"] != "LAP-003" for p in eligible)


def test_paraphrase_semantics():
    a = controlled_mapping("strong GPU for modern games under AUD 1300")
    b = controlled_mapping("gaming performance matters most, budget up to AUD 1300")
    assert a["use_case"] == b["use_case"] == "gaming"
    assert a["budget_max"] == b["budget_max"] == 1300
    assert a["preferences"]["performance"] == b["preferences"]["performance"] == 0.9


def test_llm_failure_falls_back_without_relaxing_budget():
    def bad_decoder(text, key):
        return {"bad": "shape"}

    intent, mode, reason = decode_intent("gaming laptop under AUD 1300", prefer_llm=True, api_key="demo", llm_decoder=bad_decoder)
    assert mode == "controlled_mapping" and reason
    assert intent["budget_max"] == 1300


def test_llm_unsupported_hard_requirement_is_forced_unresolved():
    def decoder(text, key):
        return _llm_shape(hard_requirements=["budget", "ethical sourcing"])

    intent, mode, reason = decode_intent("Only ethical options under AUD 1300", prefer_llm=True, api_key="demo", llm_decoder=decoder)
    assert mode == "llm" and reason is None
    assert "ethical sourcing" in intent["unresolved_requirements"]
    eligible, rejected = evaluate_products(_products(), intent)
    assert not eligible
    assert rejected
    assert all(any(r.startswith("unverified_hard_requirement") for r in item["reasons"]) for item in rejected)


def test_llm_missing_preference_dimensions_get_neutral_defaults_and_assumption():
    def decoder(text, key):
        return _llm_shape(preferences={"performance": 0.9})

    intent, mode, _ = decode_intent("Gaming laptop", prefer_llm=True, api_key="demo", llm_decoder=decoder)
    assert mode == "llm"
    assert intent["preferences"]["portability"] == 0.5
    assert intent["preferences"]["battery"] == 0.5
    assert any("defaulted to neutral 0.5" in item for item in intent["assumptions"])


def test_nonfinite_numeric_intent_is_rejected():
    bad = _llm_shape(budget_max=float("nan"))
    with pytest.raises(ValueError):
        validate_intent(bad)


def test_product_over_base_budget_survives_pre_optimizer():
    p = next(p for p in _products() if p["product_id"] == "LAP-001")
    assert p["base_price"] > 1300
    ok, reasons = product_level_eligibility(p, _intent())
    assert ok, reasons


def test_offer_scenarios_are_bounded_and_keep_merchant_shipping_cost():
    eligible, _ = evaluate_products(_products(), _intent())
    scenarios = generate_scenarios(eligible[0])
    assert 1 < len(scenarios) <= 12
    free = next(s for s in scenarios if s["buyer_shipping_fee"] == 0)
    assert free["merchant_shipping_cost"] > 0


def test_budget_is_on_buyer_total_and_discount_can_rescue():
    eligible, _ = evaluate_products(_products(), _intent())
    candidate = next(c for c in eligible if c["product_id"] == "LAP-001")
    scenarios = generate_scenarios(candidate)
    base = next(s for s in scenarios if s["discount_rate"] == Decimal("0.00") and s["buyer_shipping_fee"] > 0 and s["warranty_years"] == 2)
    assessed = assess_offer(base, _intent())
    assert assessed["buyer_total_price"] > Decimal("1300.00")
    assert "buyer_budget_exceeded" in assessed["feasibility_reasons"]
    feasible, _ = assess_scenarios(scenarios, _intent())
    assert any(o["buyer_total_price"] <= Decimal("1300.00") and o["offer_price"] < Decimal("1349.00") for o in feasible)


def test_economics_formula_and_margin_guard():
    scenario = {"offer_id":"x","product_id":"x","product_name":"x","offer_price":Decimal("1200.00"),"buyer_shipping_fee":Decimal("20.00"),"merchant_shipping_cost":Decimal("30.00"),"warranty_incremental_cost":Decimal("40.00"),"unit_cost":Decimal("900.00"),"delivery_days":2,"warranty_years":2,"stock":1,"buyer_fit":0.8,"match":{"components":{}}}
    assessed = assess_offer(scenario, _intent())
    assert assessed["buyer_total_price"] == Decimal("1220.00")
    assert assessed["contribution"] == Decimal("250.00")


def test_unverified_hard_requirement_blocks_offer():
    intent = controlled_mapping("I only want ethical gaming laptops under AUD 1300")
    scenario = {"offer_id":"x","product_id":"x","product_name":"x","offer_price":Decimal("1000.00"),"buyer_shipping_fee":Decimal("0.00"),"merchant_shipping_cost":Decimal("20.00"),"warranty_incremental_cost":Decimal("0.00"),"unit_cost":Decimal("700.00"),"delivery_days":2,"warranty_years":2,"stock":1,"buyer_fit":0.9,"match":{"components":{}}}
    assessed = assess_offer(scenario, intent)
    assert not assessed["feasible"]
    assert any(r.startswith("unverified_hard_requirement") for r in assessed["feasibility_reasons"])


def test_safe_normalization_and_deterministic_selection():
    assert safe_minmax([2.0, 2.0]) == [0.5, 0.5]
    eligible, _ = evaluate_products(_products(), _intent())
    feasible, _ = assess_scenarios([s for c in eligible for s in generate_scenarios(c)], _intent())
    a = select_best_offer(feasible)
    b = select_best_offer(list(reversed(feasible)))
    assert a["offer_id"] == b["offer_id"]


def test_no_feasible_offer_returns_explicit_failure_state():
    intent = _intent()
    intent["budget_max"] = 500.0
    eligible, _ = evaluate_products(_products(), intent)
    feasible, _ = assess_scenarios([s for c in eligible for s in generate_scenarios(c)], intent)
    assert not feasible
    response = build_b2a_response(intent, None, intent_mode="fallback_preset", no_eligible=not eligible)
    assert response["status"] == "no_feasible_offer"
    assert response["reason"]


def test_end_to_end_response_and_transaction_handoff():
    request = "I need a gaming laptop under AUD 1,300, strong GPU performance, delivery within 3 days, and at least 2 years of warranty. I care more about gaming performance than portability."
    intent, mode, _ = decode_intent(request)
    eligible, _ = evaluate_products(_products(), intent)
    feasible, _ = assess_scenarios([s for c in eligible for s in generate_scenarios(c)], intent)
    selected = select_best_offer(feasible)
    response = build_b2a_response(intent, selected, intent_mode=mode)
    assert response["status"] == "offer_available"
    assert response["recommended_offer"]["buyer_total_price"] <= 1300
    assert build_transaction_handoff(selected, None) is None
    handoff = build_transaction_handoff(selected, selected["offer_id"])
    assert handoff["status"] == "transaction_ready"
    assert handoff["payment_status"] == "not_processed_demo"
