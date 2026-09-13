# Codex Task T4 — Implementation Plan Only

You are the Implementation Engineer for `bussinessmaxprovjp`.

## Mandatory reading before doing anything
Read completely, in this order:
1. `AGENTS.md`
2. `docs/ROUND2_PRODUCT_SPEC.md`
3. `docs/DECISION_LOG.md`
4. `docs/TASKS.md`

`docs/ROUND2_PRODUCT_SPEC.md` is FROZEN.
Decisions D-001 through D-008 are FROZEN.
Do not redesign the product and do not add features outside the frozen scope.

## Your current task
Produce a minimal implementation plan for the Round 2 MVP.

DO NOT write product code yet.
DO NOT create implementation files yet.
DO NOT change the frozen spec or decision log.

For each proposed implementation step, state:
- task ID;
- exact files to create/change;
- purpose;
- inputs;
- outputs;
- implementation approach;
- tests/verification to run;
- dependency on previous steps;
- implementation risk: LOW / MEDIUM / HIGH.

## Required priorities
1. End-to-end working demo.
2. Correct deterministic buyer/merchant constraints and economics.
3. Reliable fallback when external LLM API is unavailable.
4. Core tests and failure handling.
5. Readable code a Python beginner can explain.
6. UI polish only after the core flow is stable.

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

## Architecture preference
Prefer the smallest reliable structure. Suggested files:
- `app.py`
- `requirements.txt`
- `data/catalog.csv`
- `src/intent.py`
- `src/matcher.py`
- `src/optimizer.py`
- `tests/test_core.py`

If fewer files are materially faster and remain testable, explain the simplification in the plan. Do not introduce React, FastAPI, databases, authentication, Docker, microservices, real payment processing, scraping or multi-category support.

## Important frozen business rules
- Budget is checked against generated offer `buyer_total_price`, not blindly against base catalogue price.
- `buyer_total_price = offer_price + buyer_shipping_fee`.
- `merchant_shipping_cost` and `buyer_shipping_fee` are separate.
- Free shipping to the buyer does not erase merchant shipping cost.
- Product-level and offer-level constraints are separate stages.
- LLM handles language/semantic interpretation only; deterministic Python handles economics, constraints and final offer selection.
- Warranty options must be declared in catalogue data.
- Missing evidence must be `unverified`; never fabricate claims.
- API keys must never be committed.
- App must work without an external LLM key using controlled mapping/fallback.
- UI must show whether intent decoding is `LLM mode`, `controlled mapping`, or `fallback preset`.
- At least one paraphrase test is required.
- Transaction handoff is synthetic only; no real payment integration.

## Output
Return the implementation plan only and stop for Team Lead approval.

Communicate explanations in Vietnamese. Keep code identifiers and filenames in English.