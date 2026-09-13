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
- ChatGPT Red Team / QA: independent review log when Gemini cannot write to GitHub.
- Codex: implementation code, data, tests and requirements.
- Codex may draft README; ChatGPT approves the final README.

Source documents such as the FPT brief, Round 1 proposal, supporting materials and rulebook are not committed to the current public repository unless separately approved.

## D-005 — Two-stage hard-constraint evaluation
Status: APPROVED / FROZEN

Decision:
- Product-level eligibility runs before offer optimisation and only rejects immutable failures such as zero stock, impossible delivery/capability constraints, or verified mandatory attributes known to be false.
- Offer-level feasibility runs after scenario generation and checks buyer total price, merchant margin, shipping, warranty and other configurable constraints.
- A product must not be rejected merely because its current listed price exceeds budget if an approved merchant scenario could make the final offer feasible.

Reason: Preserve the core merchant-adaptation differentiator and avoid eliminating products before the optimiser can legally reconfigure the offer.

## D-006 — Explicit shipping economics and landed buyer budget
Status: APPROVED / FROZEN

Decision:
- Separate `merchant_shipping_cost` from `buyer_shipping_fee`.
- Define `buyer_total_price = offer_price + buyer_shipping_fee`.
- Buyer budget applies to `buyer_total_price` in the demo.
- Define contribution as `offer_price + buyer_shipping_fee - unit_cost - merchant_shipping_cost - warranty_incremental_cost`.
- A free-shipping scenario sets `buyer_shipping_fee = 0`; the merchant still bears `merchant_shipping_cost`.

Reason: Prevent inconsistent budget and margin calculations and make the buyer-fit × merchant-economics claim mathematically defensible.

## D-007 — Minimal transaction handoff is core
Status: APPROVED / FROZEN

Decision:
- After a buyer accepts the recommended offer, the system creates a synthetic machine-readable `checkout_request` / `order_intent` object.
- The demo returns `transaction_ready` (or equivalent demo status), an offer ID and a synthetic order ID.
- No real payment provider, production checkout backend or payment credentials are added.

Reason: Close the B2A interaction loop without expanding into a real payment system, improving Round 3 readiness while keeping implementation bounded.

## D-008 — Semantic credibility and execution-mode transparency
Status: APPROVED / FROZEN

Decision:
- Semantic matching must include explicit `use_case_fit` or equivalent tag compatibility in addition to numeric preference dimensions.
- At least one test must show paraphrased buyer requests producing materially equivalent structured intent/priority meaning.
- The UI must display whether intent decoding used `LLM mode`, `controlled mapping`, or `fallback preset`.
- Missing buyer preference weights use documented neutral defaults or are marked as assumptions; the LLM must not silently invent precise priorities.

Reason: Demonstrate that the solution goes beyond literal keyword matching without overstating AI capability.

## Low-cost implementation clarifications accepted from review
These do not change the frozen product concept:
- Warranty scenarios must use declared options such as base warranty and explicit extended-warranty years/cost.
- Normalisation must be safe when all candidate values are equal.
- API credentials must be loaded from environment variables / Streamlit secrets and never committed.
- Missing evidence remains `unverified`; explanations may only verbalise structured facts.

## Current gate
`docs/ROUND2_PRODUCT_SPEC.md` may now be marked FROZEN. Codex may proceed only with an implementation plan first. Product code must not be written until the plan has been reviewed by ChatGPT Team Lead.