"""Catalogue validation, product-level eligibility, and semantic fit scoring."""
from __future__ import annotations

from math import isfinite
from pathlib import Path
from typing import Any

import pandas as pd

REQUIRED_COLUMNS = [
    "product_id","name","description","base_price","unit_cost","stock","delivery_days",
    "merchant_shipping_cost","buyer_shipping_fee","base_warranty_years","extended_warranty_years",
    "extended_warranty_cost","performance_score","portability_score","battery_score","tags","evidence_notes",
]
NUMERIC_REQUIRED = [
    "base_price","unit_cost","stock","delivery_days","merchant_shipping_cost","buyer_shipping_fee",
    "base_warranty_years","performance_score","portability_score","battery_score",
]


def _clean_optional_number(value: Any) -> float | None:
    if pd.isna(value) or value == "":
        return None
    number = float(value)
    if not isfinite(number):
        raise ValueError("Optional numeric value must be finite")
    return number


def load_catalog(path: str | Path) -> list[dict[str, Any]]:
    df = pd.read_csv(path, dtype={"product_id": str})
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Catalogue missing columns: {missing}")
    if df["product_id"].isna().any() or df["product_id"].duplicated().any():
        raise ValueError("product_id must be present and unique")

    products: list[dict[str, Any]] = []
    for _, row in df.iterrows():
        product = row.to_dict()
        for field in NUMERIC_REQUIRED:
            if pd.isna(product[field]):
                raise ValueError(f"Missing numeric field {field} for {product['product_id']}")
            number = float(product[field])
            if not isfinite(number):
                raise ValueError(f"Non-finite numeric field {field} for {product['product_id']}")
            product[field] = number

        product["extended_warranty_years"] = _clean_optional_number(product["extended_warranty_years"])
        product["extended_warranty_cost"] = _clean_optional_number(product["extended_warranty_cost"])
        if (product["extended_warranty_years"] is None) != (product["extended_warranty_cost"] is None):
            raise ValueError(f"Incomplete extended warranty option for {product['product_id']}")

        for field in ("base_price", "unit_cost", "merchant_shipping_cost", "buyer_shipping_fee"):
            if product[field] < 0:
                raise ValueError(f"Negative {field} for {product['product_id']}")
        if product["stock"] < 0 or product["delivery_days"] < 0 or product["base_warranty_years"] < 0:
            raise ValueError(f"Negative operational value for {product['product_id']}")
        for field in ("performance_score", "portability_score", "battery_score"):
            if not 0 <= product[field] <= 100:
                raise ValueError(f"{field} outside 0..100 for {product['product_id']}")

        product["stock"] = int(product["stock"])
        product["delivery_days"] = int(product["delivery_days"])
        product["base_warranty_years"] = int(product["base_warranty_years"])
        if product["extended_warranty_years"] is not None:
            product["extended_warranty_years"] = int(product["extended_warranty_years"])
        product["tags"] = [t.strip().lower() for t in str(product.get("tags", "")).split(";") if t.strip()]
        note = "" if pd.isna(product.get("evidence_notes")) else str(product.get("evidence_notes", "")).strip()
        product["evidence_notes"] = note
        products.append(product)
    return products


def _use_case_fit(use_case: str | None, tags: list[str]) -> float:
    if not use_case:
        return 0.5
    mapping = {
        "gaming": {"gaming", "gpu", "performance"},
        "creative": {"creative", "video", "performance"},
        "travel_work": {"travel", "portable", "work", "battery"},
        "work": {"work", "general"},
    }
    expected = mapping.get(use_case, {use_case})
    hits = len(expected.intersection(set(tags)))
    if hits >= 2:
        return 1.0
    if hits == 1:
        return 0.75
    if "general" in tags:
        return 0.4
    return 0.2


def product_level_eligibility(product: dict[str, Any], intent: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if int(product["stock"]) <= 0:
        reasons.append("out_of_stock")
    max_delivery = intent.get("delivery_days_max")
    if max_delivery is not None and int(product["delivery_days"]) > int(max_delivery):
        reasons.append("delivery_impossible")

    min_warranty = intent.get("warranty_years_min")
    if min_warranty is not None:
        max_warranty = product["base_warranty_years"]
        if product.get("extended_warranty_years") is not None:
            max_warranty = max(max_warranty, product["extended_warranty_years"])
        if max_warranty < min_warranty:
            reasons.append("warranty_impossible")

    hard = set(intent.get("hard_requirements", []))
    tags = set(product["tags"])
    # A hard gaming capability must be backed by an explicit gaming/GPU tag.
    # Generic performance evidence may influence soft fit but is not enough to
    # satisfy an immutable gaming capability requirement.
    if "gaming" in hard and not ({"gaming", "gpu"} & tags):
        reasons.append("gaming_capability_not_verified")

    unresolved = set(intent.get("unresolved_requirements", []))
    for requirement in hard.intersection(unresolved):
        reasons.append(f"unverified_hard_requirement:{requirement}")
    return not reasons, reasons


def semantic_score(product: dict[str, Any], intent: dict[str, Any]) -> dict[str, Any]:
    prefs = intent["preferences"]
    components = {
        "use_case_fit": _use_case_fit(intent.get("use_case"), product["tags"]),
        "performance_fit": float(product["performance_score"]) / 100.0,
        "portability_fit": float(product["portability_score"]) / 100.0,
        "battery_fit": float(product["battery_score"]) / 100.0,
    }
    weights = {
        "use_case_fit": 1.0 if intent.get("use_case") else 0.5,
        "performance_fit": float(prefs.get("performance", 0.5)),
        "portability_fit": float(prefs.get("portability", 0.5)),
        "battery_fit": float(prefs.get("battery", 0.5)),
    }
    total_weight = sum(weights.values()) or 1.0
    buyer_fit = sum(components[k] * weights[k] for k in components) / total_weight
    evidence_state = "verified_demo_fact" if product.get("evidence_notes") else "unverified"
    return {
        "buyer_fit": round(buyer_fit, 6),
        "components": components,
        "weights": weights,
        "reasons": [
            f"use-case fit {components['use_case_fit']:.2f}",
            f"performance fit {components['performance_fit']:.2f}",
            f"portability fit {components['portability_fit']:.2f}",
            f"battery fit {components['battery_fit']:.2f}",
        ],
        "evidence_state": evidence_state,
    }


def evaluate_products(products: list[dict[str, Any]], intent: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    eligible: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for product in products:
        ok, reasons = product_level_eligibility(product, intent)
        if not ok:
            rejected.append({"product_id": product["product_id"], "name": product["name"], "reasons": reasons})
            continue
        scored = dict(product)
        scored["match"] = semantic_score(product, intent)
        eligible.append(scored)
    eligible.sort(key=lambda p: (-p["match"]["buyer_fit"], p["product_id"]))
    return eligible, rejected
