# Codex Task T5 — Build the Round 2 MVP

You are the Implementation Engineer for `bussinessmaxprovjp`.

## Mandatory reading before changing code
Read completely, in this order:
1. `AGENTS.md`
2. `docs/ROUND2_PRODUCT_SPEC.md`
3. `docs/ROUND2_REQUIREMENTS_TRACE.md`
4. `docs/DECISION_LOG.md`
5. `docs/CODEX_IMPLEMENTATION_PLAN.md`
6. `docs/CODEX_IMPLEMENTATION_APPROVAL.md`
7. `docs/TASKS.md`

Decisions D-001 through D-010 are FROZEN.
The Product Spec is FROZEN.
The implementation plan is approved by D-010.
Do not redesign the product and do not expand accepted gaps.

## Task
Execute T5.1 through T5.11 from the approved implementation plan and produce a working Round 2 MVP.

You do NOT need separate approval between each T5 subtask.
Proceed sequentially and keep the repository in a runnable state.

STOP and report to Team Lead only if:
- you encounter a P0 blocker;
- implementation would conflict with the frozen Product Spec or Decisions;
- solving the issue requires changing product scope;
- a required dependency or API cannot be used without changing the approved design.

## Binding execution rules
1. Make `controlled_mapping` / fallback work end-to-end before optional Gemini API integration can become a dependency.
2. External Gemini API is optional. The full demo must work without an API key.
3. LLM handles language interpretation only. Deterministic Python handles constraints, economics and final selection.
4. Do not add negotiation, dynamic bundling, real checkout/payment, database, auth, FastAPI, React, Docker, scraping, multi-category support or other accepted-gap features.
5. Do not commit secrets. Use environment variables or Streamlit secrets only.
6. Prefer readable Python that a beginner can explain.
7. Working end-to-end demo and correctness outrank decorative UI polish.
8. Deterministic `pytest` business-logic tests are mandatory.
9. Manual Streamlit fresh-start smoke tests for one success flow and one failure flow are mandatory.
10. Automated Streamlit UI tests are optional only if fast and stable. Do not lose time fighting UI-test tooling.

## Required core flow
Buyer AI Request
-> Intent Decoder
-> Structured Intent
-> Product-level Eligibility
-> Semantic Catalogue Matching
-> Merchant Offer Scenario Generation
-> Offer-level Buyer + Merchant Feasibility
-> Offer Scoring / Selection
-> Machine-readable B2A Offer
-> Buyer Accept
-> Synthetic Transaction Handoff (`transaction_ready`)

## Approved demo configuration
Use the values approved in D-010 unless the frozen spec already states a stricter rule:
- discounts: 0%, 3%, 5%;
- buyer shipping scenario: catalogue fee or free-to-buyer while merchant shipping cost remains;
- warranty: base or explicitly declared extension only;
- synthetic `min_margin_rate = 0.10`;
- `alpha = 0.5`, `beta = 0.5`;
- preference range 0..1 with documented neutral/default assumptions;
- equal-value min-max normalisation returns 0.5;
- deterministic tie-break: offer score descending, buyer total price ascending, then product_id and offer_id;
- AUD monetary arithmetic uses Decimal and deterministic cent rounding.

## Implementation order
Follow the approved T5 order:
- T5.1 project skeleton + requirements + `.gitignore`
- T5.2 synthetic catalogue + validation
- T5.3 intent decoder + controlled mapping/fallback
- T5.4 product-level eligibility + semantic matcher
- T5.5 bounded offer scenario generator
- T5.6 offer-level feasibility + economics
- T5.7 scoring + selection
- T5.8 B2A response JSON
- T5.9 acceptance + synthetic transaction handoff
- T5.10 Streamlit end-to-end UI
- T5.11 tests, failure handling and smoke verification

## Required files
Expected:
- `app.py`
- `requirements.txt`
- `.gitignore`
- `data/catalog.csv`
- `src/intent.py`
- `src/matcher.py`
- `src/optimizer.py`
- `tests/test_core.py`

Do not create extra architecture layers unless absolutely necessary for a correctness issue, and if doing so would materially change the approved structure, stop for Team Lead review.

## Test and verification requirements
Run relevant tests after major implementation stages, then run the full suite at the end.
At minimum before declaring T5 complete:
- run `python -m pytest -q`;
- verify no-key/offline fallback works;
- verify paraphrase semantic test;
- verify base price above budget can become feasible through an approved discount scenario;
- verify buyer shipping fee can make an otherwise cheap product exceed budget;
- verify merchant shipping cost remains under free-to-buyer shipping;
- verify warranty extension uses declared options only;
- verify stock-zero product is rejected;
- verify no eligible / no feasible paths do not crash;
- verify missing evidence is not fabricated;
- verify equal-value normalisation is safe;
- verify transaction handoff only occurs after explicit acceptance of the current feasible offer;
- manually smoke-test Streamlit from a fresh start through one success flow to `transaction_ready` and one failure flow;
- inspect tracked files and confirm no API secret or credential is committed.

Never claim a test passed unless you actually ran it.

## Git / handoff
Commit implementation work to the repository. Keep commits understandable; do not rewrite frozen governance documents.

When T5 is complete, create or update `docs/CODEX_BUILD_REPORT.md` with:
- status: COMPLETE or BLOCKED;
- changed files;
- architecture actually implemented;
- commands actually run;
- exact test results;
- manual smoke-test results;
- success-flow summary;
- failure-flow summary;
- execution mode(s) implemented;
- known limitations;
- any deviations from the approved plan, with justification;
- explicit confirmation that no secret/API credential is tracked.

Then commit `docs/CODEX_BUILD_REPORT.md` and stop. Do not start T6, T7 or T8 unless separately instructed.

Communicate explanations in Vietnamese. Keep code identifiers and filenames in English.