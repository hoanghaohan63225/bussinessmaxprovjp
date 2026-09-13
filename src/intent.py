"""Intent decoding for the B2A demo.

Language interpretation can use an optional Gemini call, but all outputs are
validated and the deterministic controlled mapping is always available.
"""
from __future__ import annotations

import json
import os
import re
from copy import deepcopy
from typing import Any, Callable

NEUTRAL_PREFERENCES = {"performance": 0.5, "portability": 0.5, "battery": 0.5}

PRESETS: dict[str, dict[str, Any]] = {
    "Gaming under AUD 1,300": {
        "use_case": "gaming",
        "budget_max": 1300.0,
        "delivery_days_max": 3,
        "warranty_years_min": 2,
        "hard_requirements": ["gaming", "budget", "delivery", "warranty"],
        "preferences": {"performance": 0.9, "portability": 0.3, "battery": 0.4},
        "requested_attributes": ["strong GPU performance"],
        "unresolved_requirements": [],
        "assumptions": ["Preset values are synthetic demo inputs."],
    },
    "Travel creator": {
        "use_case": "creative",
        "budget_max": 1400.0,
        "delivery_days_max": 4,
        "warranty_years_min": 2,
        "hard_requirements": ["budget", "delivery", "warranty"],
        "preferences": {"performance": 0.7, "portability": 0.9, "battery": 0.9},
        "requested_attributes": ["video editing", "frequent travel"],
        "unresolved_requirements": [],
        "assumptions": ["Preset values are synthetic demo inputs."],
    },
}


def _extract_number(patterns: list[str], text: str) -> float | None:
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            try:
                return float(match.group(1).replace(",", ""))
            except (TypeError, ValueError):
                return None
    return None


def controlled_mapping(request_text: str) -> dict[str, Any]:
    text = (request_text or "").strip()
    lower = text.lower()
    preferences = deepcopy(NEUTRAL_PREFERENCES)
    assumptions: list[str] = []
    requested: list[str] = []
    unresolved: list[str] = []
    hard: list[str] = []

    use_case: str | None = None
    if any(k in lower for k in ["gaming", "modern games", "game performance", "strong gpu", "gpu"]):
        use_case = "gaming"
        preferences["performance"] = 0.9
        requested.append("gaming performance")
        if any(k in lower for k in ["gaming laptop", "must game", "for modern games", "strong gpu"]):
            hard.append("gaming")
    elif any(k in lower for k in ["video edit", "video editing", "creator", "creative work"]):
        use_case = "creative"
        preferences["performance"] = 0.8
        requested.append("creative performance")
    elif any(k in lower for k in ["travel", "cafés", "cafes", "on the road", "frequent flyer"]):
        use_case = "travel_work"

    if any(k in lower for k in ["portable", "lightweight", "travel", "cafés", "cafes"]):
        preferences["portability"] = max(preferences["portability"], 0.9)
        requested.append("portability")
    if any(k in lower for k in ["battery", "long battery", "all day"]):
        preferences["battery"] = 0.9
        requested.append("battery life")
    elif any(k in lower for k in ["travel", "cafés", "cafes"]):
        preferences["battery"] = max(preferences["battery"], 0.8)

    if "more" in lower and "performance" in lower:
        preferences["performance"] = 0.9
    if re.search(r"performance\s+(?:matters|is)\s+(?:the\s+)?most", lower):
        preferences["performance"] = 0.9
    if "more" in lower and "portability" in lower and "performance" in lower:
        if lower.find("performance") < lower.find("portability"):
            preferences["portability"] = min(preferences["portability"], 0.3)
    if any(k in lower for k in ["don't care about portability", "do not care about portability"]):
        preferences["portability"] = 0.2

    budget = _extract_number(
        [
            r"(?:under|below|max(?:imum)?|budget(?:\s+of)?|up to)\s*(?:aud\s*)?\$?\s*([0-9][0-9,]*(?:\.\d+)?)",
            r"(?:aud\s*|\$)\s*([0-9][0-9,]*(?:\.\d+)?)\s*(?:or less|maximum|max)?",
        ],
        text,
    )
    if budget is not None:
        hard.append("budget")

    delivery = _extract_number(
        [r"(?:within|in|delivery(?:\s+within)?|deliver(?:ed)?\s+within)\s*([0-9]+)\s*days?"],
        text,
    )
    if delivery is not None:
        hard.append("delivery")

    warranty = _extract_number(
        [
            r"(?:at least|min(?:imum)?(?:\s+of)?)\s*([0-9]+)\s*years?(?:\s+of)?\s+warranty",
            r"([0-9]+)[-\s]*year\s+warranty",
        ],
        text,
    )
    if warranty is not None:
        hard.append("warranty")

    if any(k in lower for k in ["ethical", "ethically sourced"]):
        requested.append("ethical sourcing")
        unresolved.append("ethical sourcing")
        if any(k in lower for k in ["only ethical", "only want ethical", "must be ethical", "ethical only"]):
            hard.append("ethical sourcing")
    if any(k in lower for k in ["sustainable", "sustainability"]):
        requested.append("sustainability")
        unresolved.append("sustainability")
        if any(k in lower for k in ["only sustainable", "must be sustainable"]):
            hard.append("sustainability")

    if preferences == NEUTRAL_PREFERENCES:
        assumptions.append("No relative preference priority detected; neutral 0.5 weights used.")
    if not text:
        unresolved.append("buyer request is empty")

    return {
        "use_case": use_case,
        "budget_max": budget,
        "delivery_days_max": int(delivery) if delivery is not None else None,
        "warranty_years_min": int(warranty) if warranty is not None else None,
        "hard_requirements": sorted(set(hard)),
        "preferences": preferences,
        "requested_attributes": sorted(set(requested)),
        "unresolved_requirements": sorted(set(unresolved)),
        "assumptions": assumptions,
    }


def validate_intent(intent: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(intent, dict):
        raise ValueError("Intent must be an object.")
    out = deepcopy(intent)
    required = ["use_case", "budget_max", "delivery_days_max", "warranty_years_min", "hard_requirements", "preferences", "requested_attributes", "unresolved_requirements", "assumptions"]
    for key in required:
        if key not in out:
            raise ValueError(f"Missing intent field: {key}")

    for key in ("budget_max", "delivery_days_max", "warranty_years_min"):
        value = out[key]
        if value is not None:
            if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
                raise ValueError(f"Invalid {key}")

    prefs = out["preferences"]
    if not isinstance(prefs, dict):
        raise ValueError("preferences must be an object")
    for key in NEUTRAL_PREFERENCES:
        if key not in prefs:
            prefs[key] = 0.5
        value = prefs[key]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= float(value) <= 1:
            raise ValueError(f"Invalid preference: {key}")
        prefs[key] = float(value)

    for list_key in ("hard_requirements", "requested_attributes", "unresolved_requirements", "assumptions"):
        if not isinstance(out[list_key], list) or not all(isinstance(x, str) for x in out[list_key]):
            raise ValueError(f"{list_key} must be a list of strings")

    if out["use_case"] is not None and not isinstance(out["use_case"], str):
        raise ValueError("use_case must be string or null")
    return out


def _extract_json_object(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < start:
        raise ValueError("No JSON object in LLM response")
    return json.loads(text[start : end + 1])


def try_gemini_decode(request_text: str, api_key: str) -> dict[str, Any]:
    try:
        from google import genai  # type: ignore
    except Exception as exc:
        raise RuntimeError("google-genai is unavailable") from exc

    client = genai.Client(api_key=api_key)
    schema_example = {
        "use_case": "gaming or null",
        "budget_max": 1300,
        "delivery_days_max": 3,
        "warranty_years_min": 2,
        "hard_requirements": ["budget"],
        "preferences": {"performance": 0.9, "portability": 0.3, "battery": 0.5},
        "requested_attributes": [],
        "unresolved_requirements": [],
        "assumptions": [],
    }
    prompt = (
        "Convert the buyer request into ONLY one JSON object matching this schema. "
        "Use null for missing numeric constraints. Preferences are importance weights from 0 to 1; "
        "use neutral 0.5 when no relative priority is expressed and record that in assumptions. "
        "Never invent product facts or merchant economics. Put unsupported requirements in unresolved_requirements.\n"
        f"Schema example: {json.dumps(schema_example)}\nBuyer request: {request_text}"
    )
    response = client.models.generate_content(model="gemini-2.5-flash-lite", contents=prompt)
    response_text = getattr(response, "text", "") or ""
    return _extract_json_object(response_text)


def decode_intent(request_text: str, *, prefer_llm: bool = False, api_key: str | None = None, llm_decoder: Callable[[str, str], dict[str, Any]] | None = None) -> tuple[dict[str, Any], str, str | None]:
    if prefer_llm and api_key:
        decoder = llm_decoder or try_gemini_decode
        try:
            return validate_intent(decoder(request_text, api_key)), "llm", None
        except Exception as exc:
            mapped = validate_intent(controlled_mapping(request_text))
            return mapped, "controlled_mapping", f"LLM unavailable/invalid; controlled mapping used ({type(exc).__name__})."
    mapped = validate_intent(controlled_mapping(request_text))
    reason = None if not prefer_llm else "No API key available; controlled mapping used."
    return mapped, "controlled_mapping", reason


def decode_preset(name: str) -> tuple[dict[str, Any], str, None]:
    if name not in PRESETS:
        raise ValueError(f"Unknown preset: {name}")
    return validate_intent(deepcopy(PRESETS[name])), "fallback_preset", None


def get_gemini_api_key() -> str | None:
    return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
