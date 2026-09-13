# ROUND2_PRODUCT_SPEC.md

Status: FROZEN
Owner: ChatGPT (Team Lead / Product Architect)

This document is the implementation source of truth for Round 2. Codex may not redesign the product or expand scope without an approved decision in `docs/DECISION_LOG.md`.

## 1. Product definition
bussinessmaxprovjp is a merchant-side B2A offer intelligence system. It receives a complex shopping request from a buyer AI, converts it into structured intent, matches the intent against the merchant catalogue, constructs the best feasible offer by balancing buyer fit with merchant economics, and produces a machine-readable transaction handoff when the buyer accepts.

The product is not a consumer shopping assistant. The merchant-side system is the product.

## 2. Core differentiation
Many solutions can stop at:

`intent -> product recommendation`

This product continues to:

`intent -> product candidate -> feasible merchant offer -> transaction handoff`

The Round 1 differentiator is preserved through deterministic offer optimisation across merchant-controlled levers such as price, shipping and warranty while respecting stock, buyer constraints and minimum merchant contribution/margin rules.

## 3. Target users
Primary human users:
- e-commerce/category managers who control product offers;
- merchant IT/integration teams.

Primary machine counterpart:
- autonomous buyer AI / shopping agent.

For the hackathon demo, the Streamlit UI is a transparent demonstration surface for judges and merchant users. The important interaction is the machine-readable buyer-agent-to-merchant-system flow.

## 4. Demo scenario
Category: fictional laptop catalogue.

Example buyer-agent request:
"I need a gaming laptop under AUD 1,300, strong GPU performance, delivery within 3 days, and at least 2 years of warranty. I care more about gaming performance than portability."

The system must:
1. decode this request into validated structured intent;
2. reject products that fail immutable product-level constraints;
3. score remaining products on semantic/soft preference fit;
4. generate bounded merchant-approved offer scenarios;
5. test each generated offer against buyer hard constraints and merchant economics;
6. select the best feasible offer;
7. return an explanation and machine-readable B2A offer response;
8. when the buyer accepts, create a synthetic machine-readable transaction handoff.

## 5. End-to-end flow
Buyer AI request
-> Intent Decoder
-> Structured Intent
-> Product-level Eligibility Filter
-> Semantic Catalogue Matcher
-> Candidate Products
-> Merchant Offer Scenario Generator
-> Offer-level Buyer + Merchant Feasibility Checks
-> Offer Scoring / Selection
-> B2A Offer JSON + concise explanation
-> Buyer accepts
-> Synthetic Checkout / Order Intent
-> `transaction_ready`

Optional stretch only after all core acceptance criteria pass:
-> one counter-offer / negotiation turn that updates buyer constraints and reruns the same deterministic pipeline.

Multi-round autonomous negotiation is out of scope.

## 6. Structured intent schema
Minimum schema:

```json
{
  "use_case": "gaming",
  "budget_max": 1300,
  "delivery_days_max": 3,
  "warranty_years_min": 2,
  "hard_requirements": ["gaming", "budget", "delivery", "warranty"],
  "preferences": {
    "performance": 0.9,
    "portability": 0.3,
    "battery": 0.4
  },
  "requested_attributes": [],
  "unresolved_requirements": [],
  "assumptions": []
}
```

Rules:
- preference weights use a documented range such as 0.0–1.0;
- if the buyer expresses a clear relative priority, the parser may map it to documented weights;
- if the buyer does not express relative priorities, use documented neutral defaults or record the assumption explicitly;
- the LLM must not silently invent highly specific priority weights;
- missing values are explicit null/unknown values, not invented facts;
- ambiguous or unsupported requirements go to `unresolved_requirements`.

## 7. Catalogue schema
The demo catalogue uses synthetic fictional data and must be labelled as such.

Minimum fields:
- `product_id`
- `name`
- `description`
- `base_price`
- `unit_cost`
- `stock`
- `delivery_days`
- `merchant_shipping_cost`
- `buyer_shipping_fee`
- `base_warranty_years`
- `extended_warranty_years`
- `extended_warranty_cost`
- `performance_score`
- `portability_score`
- `battery_score`
- `tags`
- `evidence_notes`

The catalogue should contain about 8–12 products, enough to demonstrate real trade-offs without creating unnecessary data work.

Warranty extension may only be offered when explicit extended-warranty fields are present and feasible.

## 8. Intent decoding
Preferred path:
- an LLM converts the natural-language request to the validated structured intent schema.

Fallback paths:
- controlled semantic mapping; and/or
- predefined demo requests / structured input form.

The full app must remain demoable when the external LLM API is unavailable.

The UI must clearly display one of:
- `LLM mode`
- `controlled mapping`
- `fallback preset`

The LLM must not receive merchant unit cost, minimum margin threshold or other private merchant economics unless separately approved later.

API credentials must be loaded from environment variables or Streamlit secrets and never committed to GitHub.

## 9. Two-stage hard constraints
Hard constraints are deterministic and evaluated in two stages.

### 9.1 Product-level eligibility before optimisation
Reject only immutable or currently impossible product conditions, for example:
- stock <= 0;
- immutable capability does not satisfy a mandatory requirement;
- required delivery is impossible for that product under the declared demo fulfilment facts;
- a mandatory verified attribute is known to be false.

Do NOT reject a product merely because its current `base_price` exceeds the buyer budget if an approved offer scenario could reduce the final buyer total into budget.

Unknown evidence is not treated as verified truth.

### 9.2 Offer-level feasibility after scenario generation
Every generated offer must then satisfy:
- buyer budget using `buyer_total_price`;
- required warranty;
- delivery constraint;
- stock availability;
- minimum merchant contribution / margin rules;
- all other applicable hard buyer requirements.

A high soft fit score can never override an infeasible hard constraint.

## 10. Semantic matching logic
Semantic matching must go beyond direct keyword equality but remain explainable.

For the MVP:
- LLM or controlled semantic mapping converts nuanced phrases such as "gaming performance matters most", "strong GPU for modern games", "portable", "long battery life" into the same documented intent dimensions/tags where appropriate;
- deterministic Python converts structured preferences into component scores;
- `use_case_fit` or equivalent tag compatibility is scored explicitly;
- final buyer fit is a declared weighted combination of relevant components.

Example:

`buyer_fit = w_use*use_case_fit + w_perf*performance_fit + w_port*portability_fit + w_batt*battery_fit`

Weights must be documented and derived from explicit buyer priorities or documented neutral defaults.

No claim is made that this reproduces proprietary platform ranking or real purchase probability.

The UI should expose component scores/reasons so judges can see why one candidate ranks above another.

At least one deterministic or parser-level test must show two paraphrased requests with equivalent meaning producing materially equivalent structured intent / priority meaning.

## 11. Merchant offer optimisation
The optimiser searches only a small bounded set of merchant-controlled scenarios for top candidate products.

Minimum levers:
- base/current price;
- small approved discount levels such as 0%, 3% and 5%;
- current buyer shipping fee vs free/subsidised buyer shipping;
- base warranty vs declared extended-warranty option when available.

Do not create arbitrary discounts or warranty options outside declared scenario rules.

The optimiser must evaluate more than one scenario for at least one candidate in the demo.

## 12. Shipping and merchant economics
All arithmetic is deterministic Python.

Definitions:

`buyer_total_price = offer_price + buyer_shipping_fee`

`contribution = offer_price + buyer_shipping_fee - unit_cost - merchant_shipping_cost - warranty_incremental_cost`

`contribution_margin_rate = contribution / buyer_total_price` when `buyer_total_price > 0`.

For a free-shipping scenario:
- `buyer_shipping_fee = 0`
- merchant still bears `merchant_shipping_cost`.

A scenario is infeasible if:
- stock <= 0;
- buyer total price exceeds a hard budget;
- contribution < 0;
- contribution margin rate is below the configured merchant minimum;
- warranty or delivery hard requirements fail;
- any other hard requirement fails.

The demo must clearly label financial values as synthetic / illustrative.

## 13. Offer selection
For every feasible scenario, compute:
- buyer-fit score;
- economic score based on contribution or contribution margin;
- optional fulfilment confidence from delivery/stock facts.

Use normalised metrics before combining unlike units.

Recommended MVP objective:

`offer_score = alpha * normalised_buyer_fit + beta * normalised_economic_score`

Default demo may use a balanced objective with declared alpha/beta values.

Safe normalisation is required. If all candidate values are equal, normalisation must return a documented neutral/equal value rather than divide by zero.

The final offer must satisfy all hard constraints before any soft-score comparison.

## 14. Machine-readable B2A offer response
Minimum response shape:

```json
{
  "status": "offer_available",
  "decoded_intent": {},
  "recommended_offer": {
    "offer_id": "OFFER-001",
    "product_id": "LAP-001",
    "product_name": "Example Laptop",
    "offer_price": 1250,
    "buyer_shipping_fee": 0,
    "buyer_total_price": 1250,
    "delivery_days": 2,
    "warranty_years": 2
  },
  "buyer_match": {
    "score": 0.87,
    "reasons": [
      "buyer total price is within budget",
      "strong gaming use-case and performance fit",
      "delivery requirement satisfied"
    ]
  },
  "merchant_constraints": {
    "stock": "satisfied",
    "minimum_margin": "satisfied"
  },
  "evidence": [],
  "unresolved_requirements": [],
  "intent_mode": "llm"
}
```

If there is no feasible offer:

```json
{
  "status": "no_feasible_offer",
  "reason": "No catalogue offer satisfies all hard buyer and merchant constraints."
}
```

The system must never fabricate a product claim merely to produce an offer.

## 15. Minimal transaction handoff
This is core Round 2 functionality, but it is a synthetic demo contract rather than real payment processing.

When the buyer accepts the recommended offer, create a machine-readable object such as:

```json
{
  "status": "transaction_ready",
  "order_intent": {
    "order_id": "DEMO-ORDER-001",
    "offer_id": "OFFER-001",
    "product_id": "LAP-001",
    "quantity": 1,
    "buyer_total_price": 1250,
    "currency": "AUD"
  },
  "payment_status": "not_processed_demo"
}
```

Requirements:
- synthetic/demo labels must be visible;
- do not integrate Stripe or real payment credentials;
- do not claim that a production checkout transaction occurred;
- the handoff should be generated deterministically from the accepted offer.

## 16. Evidence / hallucination safeguards
For requirements whose support is absent from the catalogue:
- mark them `unverified` or include them in `unresolved_requirements`;
- do not state that the merchant satisfies them;
- do not let an LLM invent sustainability, ethical sourcing, compatibility, stock, delivery or warranty facts.

LLM explanations may only verbalise structured facts produced by the pipeline.

## 17. Minimal architecture
- `app.py`: Streamlit demo / orchestration.
- `data/catalog.csv`: synthetic catalogue.
- `src/intent.py`: LLM parsing + validation + controlled mapping/fallback.
- `src/matcher.py`: product-level eligibility + semantic fit.
- `src/optimizer.py`: scenario generation, offer-level feasibility, economics and offer selection.
- `tests/test_core.py`: critical deterministic tests.

If module separation would materially slow implementation, the same logical boundaries may live in fewer files, but behaviour and testability matter more than file count.

No FastAPI/backend service is required for the transaction handoff; the machine-readable JSON contract is sufficient for the MVP.

## 18. Required UI surfaces
The Streamlit demo should visibly show:
1. Buyer Agent Request.
2. Intent execution mode (`LLM mode`, `controlled mapping`, or `fallback preset`).
3. Decoded Intent.
4. Candidate products and why they matched/failed.
5. Recommended Merchant Offer.
6. Buyer-fit and merchant-constraint explanation.
7. Machine-readable offer JSON.
8. Buyer accept action.
9. Synthetic `transaction_ready` / order-intent JSON.

Do not spend material time on decorative dashboard polish before the full flow works.

## 19. Failure behaviour
Required cases:
- LLM API unavailable -> controlled mapping/fallback still works;
- invalid LLM JSON -> validation/fallback instead of crash;
- no product eligible -> explicit no-match state;
- candidates exist but no economically feasible offer -> explicit no-feasible-offer state;
- stock zero -> reject;
- missing evidence -> unverified, not fabricated;
- divide-by-zero / missing numeric fields -> safe validation/error handling;
- identical values during normalisation -> safe equal handling;
- transaction handoff is unavailable unless a feasible offer has been accepted.

## 20. MVP scope
Must have:
- one product category;
- synthetic 8–12 product catalogue;
- complex natural-language buyer request or fallback path;
- validated structured intent;
- two-stage hard constraints;
- semantic/soft preference matching with explicit use-case fit;
- merchant economics;
- bounded offer scenario optimisation;
- explanation grounded in structured facts;
- machine-readable B2A offer response;
- buyer acceptance action;
- synthetic machine-readable transaction handoff;
- Streamlit demo;
- core tests;
- README/run instructions.

## 21. Explicit out-of-scope
For Round 2 implementation unless separately approved:
- real payment processing;
- production checkout backend;
- authentication;
- database;
- web scraping;
- multi-merchant marketplace;
- multi-category catalogue;
- model training;
- proprietary ranking reconstruction;
- real sales-uplift claims;
- large analytics dashboard;
- production FPT integration;
- multi-round autonomous negotiation;
- dynamic multi-product bundles unless all core work is already complete and a later decision explicitly approves them.

## 22. Acceptance criteria
The core MVP is accepted only if all are true:
1. App launches with a documented command.
2. A buyer request produces validated structured intent.
3. UI identifies whether intent used LLM, controlled mapping or fallback preset.
4. Product-level hard constraints are enforced deterministically.
5. A product above current budget is not prematurely rejected when an approved offer scenario could make it feasible.
6. Semantic preference scoring, including use-case fit, affects ranking.
7. At least one paraphrase test demonstrates materially equivalent intent meaning.
8. Stock-zero products cannot be recommended.
9. The optimiser evaluates more than one merchant offer scenario.
10. Buyer budget is checked against `buyer_total_price`.
11. Merchant shipping cost and buyer shipping fee are modelled separately.
12. Minimum merchant economics are enforced.
13. Warranty choices use only declared options.
14. Final offer is feasible for both buyer hard constraints and merchant constraints.
15. UI explains why the offer was selected.
16. A machine-readable B2A offer JSON is produced.
17. Buyer acceptance generates a synthetic `transaction_ready` / order-intent JSON.
18. No-match and no-feasible-offer cases do not crash.
19. Missing evidence is not hallucinated.
20. Safe normalisation handles equal values without divide-by-zero.
21. Core deterministic tests pass.
22. Synthetic/demo data and simulated outputs are clearly labelled.
23. No secret/API credential is committed to the repository.

## 23. Round 3 readiness
Because core product features cannot be redesigned after Round 2 submission, the submitted MVP must already contain the complete core story:

complex buyer intent -> semantic understanding -> catalogue match -> merchant-aware offer optimisation -> explainable B2A offer -> synthetic transaction handoff.

Round 3 work should focus on presentation, explanation, demo reliability, evidence, deployment roadmap and defence rather than replacing this core flow.

## 24. Freeze gate
This specification is FROZEN following user approval of D-001 through D-008.

Next step:
1. Codex reads `AGENTS.md`, this Product Spec, `docs/DECISION_LOG.md` and `docs/TASKS.md`.
2. Codex proposes a minimal implementation plan only; no product code yet.
3. ChatGPT Team Lead reviews the plan.
4. After Team Lead approval, Codex implements the MVP in bounded tasks and runs relevant tests after each major step.
5. Any proposed core-scope change must return to the decision log and user approval before implementation.