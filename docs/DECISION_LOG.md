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

## D-009 — Requirements trace for implementation agents
Status: APPROVED / FROZEN

Decision:
- Maintain `docs/ROUND2_REQUIREMENTS_TRACE.md` as the compact bridge from the official FPT Round 2 requirements and Rulebook outputs to the frozen product response, implementation modules and demo evidence.
- Codex must read this trace before producing the implementation plan or changing product code.
- The trace may expose deliberate gaps/partial coverage, but Codex must not expand scope to close them without a new Team Lead decision.
- Original source PDFs remain outside the current public repository under D-004.

Reason: Give Codex enough challenge context to understand why each module exists without polluting implementation context with historical/source documents or creating conflicting requirements.

## D-010 — Approve Codex implementation plan
Status: APPROVED / FROZEN

Decision:
- Approve `docs/CODEX_IMPLEMENTATION_PLAN.md` as the execution plan for T5.
- Codex may implement T5.1 through T5.11 sequentially without requesting approval between every subtask.
- Codex must stop and return to the Team Lead only if it encounters a P0 blocker, a conflict with the frozen Product Spec/Decisions, or a need to change product scope.
- Controlled mapping and fallback must work end-to-end before optional external Gemini API integration is allowed to become a dependency.
- Deterministic `pytest` business-logic coverage and manual end-to-end Streamlit smoke tests are mandatory. Automated Streamlit UI tests are optional if they are fast and stable.
- Working end-to-end demo and correctness take priority over UI-test sophistication or decorative polish.

Approved demo configuration from the Codex plan:
- discount rates: 0%, 3%, 5%;
- shipping scenarios: catalogue buyer fee or free-to-buyer while merchant shipping cost remains;
- warranty: base or explicitly declared extension only;
- synthetic `min_margin_rate = 0.10`;
- balanced selection objective `alpha = 0.5`, `beta = 0.5`;
- preference range 0..1 with documented neutral/default assumptions;
- equal-value min-max normalisation returns 0.5;
- deterministic tie-break: offer score descending, buyer total price ascending, then product/offer IDs;
- AUD monetary arithmetic uses Decimal and deterministic cent rounding as proposed.

Reason: The plan implements the frozen B2A core with bounded scope, explicit economics, offline reliability and sufficient testability while avoiding unnecessary architecture under the Round 2 deadline.

## Low-cost implementation clarifications accepted from review
These do not change the frozen product concept:
- Warranty scenarios must use declared options such as base warranty and explicit extended-warranty years/cost.
- Normalisation must be safe when all candidate values are equal.
- API credentials must be loaded from environment variables / Streamlit secrets and never committed.
- Missing evidence remains `unverified`; explanations may only verbalise structured facts.

## Current gate
Decisions D-001 through D-010 and `docs/ROUND2_PRODUCT_SPEC.md` are FROZEN. T4 is approved. Codex is authorised to execute T5.1–T5.11 under `docs/PROMPT_CODEX_BUILD.md`. Any P0 blocker, frozen-spec conflict or scope change must stop implementation and return to ChatGPT Team Lead.