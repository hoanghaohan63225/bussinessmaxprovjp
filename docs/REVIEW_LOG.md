# REVIEW_LOG.md

Reviewer: ChatGPT acting in separate Red Team / QA pass
Source priority: FPT Round 2 Problem Statement > frozen Product Spec / Decisions > implementation plan

## Product-spec review — RESOLVED

The original pre-build review identified three P0 design risks:
1. budget could be checked before the optimiser and wrongly eliminate discount-rescuable products;
2. buyer shipping fee and merchant shipping cost were not clearly separated;
3. the flow stopped before a transaction handoff.

These were resolved and frozen through D-005, D-006 and D-007. Low-cost semantic, warranty, normalisation, execution-mode and secrets clarifications were resolved through D-008 and the frozen Product Spec.

## T6 static code review — PASS 1

Status: STATIC REVIEW COMPLETE; runtime closure still blocked on fresh local pytest + Streamlit smoke test.

Reviewed files:
- `app.py`
- `src/intent.py`
- `src/matcher.py`
- `src/optimizer.py`
- `data/catalog.csv`
- `tests/test_core.py`
- `requirements.txt`
- `README.md`

### Finding T6-P0-01 — LLM could return an unsupported hard requirement without marking it unresolved

**Risk:** If optional LLM mode returned a hard requirement such as ethical sourcing but omitted it from `unresolved_requirements`, deterministic feasibility logic could treat the request as if no unsupported hard requirement existed. That violates the frozen rule that missing evidence must not be treated as satisfied.

**Fix applied:** `validate_intent()` now fails closed. Unsupported hard requirements are automatically added to `unresolved_requirements`; hard budget/delivery/warranty/gaming constraints with missing backing values are also forced unresolved. Product-level eligibility then blocks unverified hard requirements.

**Regression test added:** unsupported LLM hard requirement is forced unresolved and prevents recommendation.

Status: FIXED — requires local pytest confirmation.

### Finding T6-P1-01 — Missing LLM preference dimensions could silently receive 0.5 defaults

**Risk:** D-008 requires neutral defaults to be documented or explicitly recorded as assumptions.

**Fix applied:** missing preference dimensions are still safely defaulted to 0.5, but an explicit assumption is appended listing the defaulted dimensions.

**Regression test added.**

Status: FIXED — requires local pytest confirmation.

### Finding T6-P1-02 — Non-finite intent numeric values were not rejected explicitly

**Risk:** Non-standard LLM JSON or malformed inputs could pass a NaN-like numeric through initial validation and later break Decimal/economics logic.

**Fix applied:** numeric constraints and preference weights must be finite as well as in range.

**Regression test added.**

Status: FIXED — requires local pytest confirmation.

### Finding T6-P1-03 — A failed rerun could leave a previous pipeline visible

**Risk:** If a rerun with the same input failed validation/API execution, stale offer state could remain visible and potentially confuse the demo.

**Fix applied:** `app.py` clears current pipeline and transaction state before every explicit pipeline run. Input-signature changes already clear stale state as well.

Status: FIXED — requires Streamlit smoke confirmation.

### Finding T6-P1-04 — Streamlit secrets path was ignored by app-level key lookup

**Risk:** The spec permits environment variables or Streamlit secrets. Supporting only environment variables is not fatal, but makes hosted/demo configuration less flexible.

**Fix applied:** app now checks environment variables first, then Streamlit secrets, and still works without any key.

Status: FIXED — static review only.

### Finding T6-P1-05 — Earlier emergency report overstated repository test evidence

**Problem:** An earlier working copy produced a `28 passed` result, but the exact extended test set was not identical to the final committed `tests/test_core.py`.

**Fix applied:** `docs/EMERGENCY_BUILD_REPORT.md` now explicitly states that the old 28-pass count is not proof for the current repository. The committed suite must be rerun locally before T5/T6 can be closed.

Status: FIXED / DOCUMENTATION CORRECTED.

## Remaining runtime gate

Before T6 can be marked DONE, run the exact committed repository locally:

```bash
pip install -r requirements.txt
python -m pytest -q
python -m streamlit run app.py
```

Required manual observations:
1. default gaming request returns `offer_available`;
2. accepted current offer produces `transaction_ready`;
3. an impossible budget/request returns explicit `no_feasible_offer` without crashing;
4. editing the request after acceptance clears the stale transaction;
5. controlled mapping/fallback works with no API key;
6. no secret is committed or displayed.

## Non-blocking limitations retained intentionally

- Optional Gemini mode is not required for the demo and has not been runtime-validated in this environment.
- No dynamic bundles, live LLM-to-LLM pair, real payment, production checkout backend, database, auth, scraping, multi-category or multi-round negotiation.
- Buyer-fit/economic scores are illustrative deterministic demo metrics, not measured purchase probability or sales uplift.

## Current reviewer recommendation

Do not add new features. Complete the local runtime gate, then close T5/T6 and move immediately to submission documentation and pitch readiness.
