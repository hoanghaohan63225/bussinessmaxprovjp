# REVIEW_LOG.md

Reviewer: ChatGPT acting in separate Red Team / QA pass
Source priority: FPT Round 2 Problem Statement > frozen Product Spec / Decisions > implementation plan

## Product-spec review — RESOLVED

The original pre-build review identified three P0 design risks:
1. budget could be checked before the optimiser and wrongly eliminate discount-rescuable products;
2. buyer shipping fee and merchant shipping cost were not clearly separated;
3. the flow stopped before a transaction handoff.

These were resolved and frozen through D-005, D-006 and D-007. Low-cost semantic, warranty, normalisation, execution-mode and secrets clarifications were resolved through D-008 and the frozen Product Spec.

## T6 code review — COMPLETE

Status: DONE. All currently identified P0/P1 findings are fixed and latest-build runtime evidence passed.

Reviewed files:
- `app.py`
- `src/intent.py`
- `src/matcher.py`
- `src/optimizer.py`
- `data/catalog.csv`
- `tests/test_core.py`
- `requirements.txt`
- `README.md`

### T6-P0-01 — Unsupported LLM hard requirement could be silently treated as satisfied

**Fix:** `validate_intent()` fails closed. Unsupported hard requirements are added to `unresolved_requirements`; hard budget/delivery/warranty/gaming constraints with missing backing values are also forced unresolved. Product-level eligibility blocks unverified hard requirements.

**Regression test:** added.

Status: FIXED / VERIFIED.

### T6-P1-01 — Missing LLM preference dimensions could silently receive neutral defaults

**Fix:** missing preference dimensions default to 0.5 with an explicit assumption describing the defaulted dimensions.

**Regression test:** added.

Status: FIXED / VERIFIED.

### T6-P1-02 — Non-finite intent numerics not rejected explicitly

**Fix:** numeric constraints and preference weights must be finite and in range before downstream economics logic runs.

**Regression test:** added.

Status: FIXED / VERIFIED.

### T6-P1-03 — Failed rerun could leave a stale previous pipeline visible

**Fix:** `app.py` clears current pipeline and transaction state before each explicit run. Input-signature changes also clear stale state.

**Interactive evidence:** user changed the request after an accepted transaction; the new impossible-request result showed `no_feasible_offer` and the prior transaction was no longer presented as current.

Status: FIXED / INTERACTIVE PASS.

### T6-P1-04 — Streamlit secrets path was ignored by app-level key lookup

**Fix:** app checks environment variables first, then Streamlit secrets, and still works without any key.

Status: FIXED.

### T6-P1-05 — Earlier emergency report overstated repository test evidence

**Fix:** runtime records distinguish earlier working-copy results from exact repository evidence.

Final valid latest-build result:

```text
15 passed in 0.73s
```

Status: FIXED / DOCUMENTATION CORRECTED.

### T6-P1-06 — Generic performance tag could satisfy a hard gaming requirement

**Problem:** initial success-flow screenshots showed `CreatorPro 15` as an eligible candidate for a hard gaming request because the product-level rule treated generic `performance` as sufficient gaming-capability evidence.

**Fix:** hard `gaming` now requires an explicit `gaming` or `gpu` catalogue tag. Generic `performance` can still affect soft semantic fit but cannot satisfy the immutable gaming requirement.

**Regression test:** added.

**Interactive evidence:** latest catalogue matching contained only `NovaForge G15`, `TitanEdge 16` and `ValueStrike 15`; `CreatorPro 15` was absent.

Status: FIXED / INTERACTIVE PASS.

## Final latest-build verification

Confirmed on the user's machine:

1. Python 3.14.5.
2. Dependencies install successfully.
3. Latest exact suite: `py -m pytest -q` -> **15 passed in 0.73s**.
4. Streamlit launches successfully at `localhost:8501` without an API key.
5. Default gaming request runs in `Controlled mapping` mode.
6. Catalogue matching respects the hard gaming-capability fix.
7. A feasible B2A offer is produced.
8. Explicit buyer acceptance produces `transaction_ready` with synthetic `order_intent` and `payment_status = not_processed_demo`.
9. An impossible request returns explicit `no_feasible_offer` without crashing.
10. Changing the request after acceptance clears stale accepted state.

## Non-blocking limitations retained intentionally

- Optional Gemini mode is not required for the reliable demo path.
- No dynamic bundles, live LLM-to-LLM pair, real payment, production checkout backend, database, auth, scraping, multi-category or multi-round negotiation.
- Buyer-fit/economic scores are illustrative deterministic demo metrics, not measured purchase probability or sales uplift.
- Streamlit currently emits a non-blocking deprecation warning for `use_container_width`; this does not affect the demonstrated flow.

## Reviewer recommendation

T5/T6/T7 are complete. Do not add new product features. Move entirely to submission documentation, pitch/demo rehearsal, repository hygiene and final submission.