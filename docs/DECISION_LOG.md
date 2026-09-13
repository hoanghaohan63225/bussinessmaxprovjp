# Decision Log

## D-001 — Core product flow
Status: APPROVED / FROZEN

Decision: Buyer Intent -> Semantic Match -> Merchant Optimisation -> B2A Offer.

Reason: This aligns the Round 2 merchant-side interaction with the strongest Round 1 differentiator: offer optimisation under merchant constraints.

## D-002 — AI responsibility boundary
Status: APPROVED / FROZEN

Decision:
- LLM: natural-language intent decoding, semantic interpretation, concise explanation from approved facts.
- Deterministic Python: eligibility, stock, price/cost/margin calculations, shipping and warranty economics, scenario search, constraints, final offer selection.

Reason: Keep arithmetic and business rules testable and explainable.

## D-003 — Implementation stack
Status: APPROVED / FROZEN

Use: Python, Streamlit, Pandas, pytest, optional Gemini API.

Do not add unless separately approved: React, Next.js, FastAPI, database, authentication, Docker, microservices, production payment integration.

## D-004 — Shared project source of truth
Status: APPROVED / FROZEN

Decision: GitHub stores the project specification, decision log, task log, review log, source code, tests and submission documentation.

File ownership:
- ChatGPT: governance, product spec, task and submission documents.
- Gemini: independent review log.
- Codex: implementation code, data, tests and requirements.
- Codex may draft README; ChatGPT approves the final README.

## Next decision gate
After Gemini reviews `docs/ROUND2_PRODUCT_SPEC.md`, ChatGPT will assess each issue and bring any core-change proposal back to the user for approval.
