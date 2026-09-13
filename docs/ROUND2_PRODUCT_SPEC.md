# ROUND2_PRODUCT_SPEC.md

Status: DRAFT FOR REVIEW
Owner: ChatGPT (Team Lead / Product Architect)

## 1. Product definition
bussinessmaxprovjp is a merchant-side B2A offer intelligence system. It receives a complex shopping request from a buyer AI, converts it into structured intent, matches the intent against the merchant catalogue, and constructs the best feasible offer by balancing buyer fit with merchant economics.

The product is not a consumer shopping assistant. The merchant-side system is the product.

## 2. Core differentiation
Many solutions can stop at: intent -> product recommendation.

This product continues to: intent -> product candidate -> feasible merchant offer.

The Round 1 differentiator is preserved through deterministic offer optimisation across merchant-controlled levers such as price, shipping subsidy and warranty, while respecting stock and minimum contribution constraints.

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
1. decode this request into structured intent;
2. reject products that violate hard constraints;
3. score remaining products on semantic/soft preference fit;
4. generate merchant-approved offer scenarios;
5. reject scenarios that violate merchant economics or stock rules;
6. select the best feasible offer;
7. return an explanation and machine-readable JSON response.

## 5. End-to-end flow
Buyer AI request
-> Intent Decoder
-> Structured Intent
-> Hard Eligibility Filter
-> Semantic Catalogue Matcher
-> Candidate Products
-> Merchant Offer Scenario Generator
-> Feasibility + Economics Checks
-> Offer Scoring / Selection
-> B2A Response JSON + concise explanation

Optional stretch only after core acceptance criteria pass:
-> one counter-offer / negotiation turn that updates buyer constraints and reruns the same deterministic pipeline.

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
  "unresolved_requirements": []
}
```

Rules:
- weights are normalised to a documented range;
- missing values are explicit null/unknown values, not invented defaults unless the demo preset defines them;
- ambiguous or unsupported requirements go to `unresolved_requirements`.

## 7. Catalogue schema
The demo catalogue uses synthetic fictional data and must be labelled as such.

Minimum fields:
- `product_id`
- `name`
- `description`
- `price`
- `unit_cost`
- `stock`
- `delivery_days`
- `shipping_cost`
- `warranty_years`
- `warranty_incremental_cost`
- `performance_score`
- `portability_score`
- `battery_score`
- `tags`
- `evidence_notes`

The catalogue should contain about 8-12 products, enough to demonstrate real trade-offs without creating unnecessary data work.

## 8. Intent decoding
Preferred path:
- an LLM converts the natural-language request to the validated structured intent schema.

Fallback path:
- predefined demo requests or a structured input form must allow the full app to run when the external LLM API is unavailable.

The LLM must not receive merchant unit cost, margin threshold or other private merchant economics unless explicitly approved later.

## 9. Hard eligibility logic
Hard constraints are deterministic.

A product is ineligible when any mandatory condition fails, for example:
- stock <= 0;
- the product cannot be configured into an offer at or below a hard buyer budget;
- delivery requirement cannot be met;
- minimum warranty cannot be met;
- an explicitly mandatory verified attribute is known to be false.

Unknown evidence is not treated as verified truth.

## 10. Semantic matching logic
Semantic matching must go beyond direct keyword equality but remain explainable.

For the MVP:
- LLM or a controlled mapping converts nuanced language such as "gaming", "portable", "long battery life", "beginner-friendly" into catalogue dimensions/tags;
- deterministic Python converts the resulting structured preferences into numeric component scores;
- the final fit score is a declared weighted combination of relevant dimensions.

Example:
`buyer_fit = w_perf*performance_fit + w_port*portability_fit + w_batt*battery_fit + requirement_bonus`

No claim is made that this reproduces proprietary platform ranking behaviour.

The UI should expose component scores/reasons so the judge can see why one candidate ranks above another.

## 11. Merchant offer optimisation
The optimiser searches only a small set of merchant-controlled scenarios for top candidate products.

Minimum levers:
- current price;
- small approved discount levels;
- current shipping vs merchant-subsidised shipping;
- current warranty vs an approved extended-warranty option when available.

Example price scenarios may be current price, -3%, and -5%, bounded by merchant rules.

Do not create arbitrary discounts outside declared scenario rules.

## 12. Merchant economics
All arithmetic is deterministic Python.

Definitions:

`contribution = offer_price - unit_cost - shipping_subsidy - warranty_incremental_cost`

`contribution_margin_rate = contribution / offer_price` when offer_price > 0.

A scenario is infeasible if:
- stock <= 0;
- contribution < 0;
- contribution margin rate is below the configured merchant minimum;
- it fails a buyer hard constraint.

The demo must clearly label financial values as synthetic / illustrative.

## 13. Offer selection
For every feasible scenario, compute:
- buyer-fit score;
- economic score based on contribution or contribution margin;
- optional fulfilment confidence from delivery/stock facts.

Use normalised metrics before combining unlike units.

Recommended MVP objective:
`offer_score = alpha * normalised_buyer_fit + beta * normalised_economic_score`

Default demo can use a balanced objective with declared alpha/beta values. The values must be visible or documented, not hidden as mysterious AI logic.

The final offer must always satisfy all hard constraints first. A high soft score can never override an infeasible hard constraint.

## 14. Machine-readable B2A response
Minimum response shape:

```json
{
  "status": "offer_available",
  "decoded_intent": {},
  "recommended_offer": {
    "product_id": "LAP-001",
    "product_name": "Example Laptop",
    "offer_price": 1299,
    "delivery_days": 2,
    "warranty_years": 2,
    "shipping_subsidy": 20
  },
  "buyer_match": {
    "score": 0.87,
    "reasons": [
      "within budget",
      "strong performance fit",
      "delivery requirement satisfied"
    ]
  },
  "merchant_constraints": {
    "stock": "satisfied",
    "minimum_margin": "satisfied"
  },
  "evidence": [],
  "unresolved_requirements": []
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

## 15. Evidence / hallucination safeguards
For requirements whose support is absent from the catalogue:
- mark them `unverified` or include them in `unresolved_requirements`;
- do not state that the merchant satisfies them;
- do not let an LLM invent sustainability, ethical sourcing, compatibility, stock, delivery or warranty facts.

LLM explanations may only verbalise structured facts produced by the pipeline.

## 16. Minimal architecture
- `app.py`: Streamlit demo / orchestration.
- `data/catalog.csv`: synthetic catalogue.
- `src/intent.py`: LLM parsing + validation + fallback, only if separating modules improves clarity.
- `src/matcher.py`: hard eligibility + semantic fit.
- `src/optimizer.py`: scenario generation, economics, offer selection.
- `tests/test_core.py`: critical deterministic tests.

If module separation would slow implementation materially, the same logical boundaries may live in `app.py`; behaviour matters more than file count.

## 17. Required UI surfaces
The Streamlit demo should visibly show:
1. Buyer Agent Request.
2. Decoded Intent.
3. Candidate products and why they matched/failed.
4. Recommended Merchant Offer.
5. Buyer-fit and merchant-constraint explanation.
6. Machine-readable JSON response.

Do not spend material time on decorative dashboard polish before the full flow works.

## 18. Failure behaviour
Required cases:
- LLM API unavailable -> fallback input/demo still works;
- invalid LLM JSON -> validation/fallback instead of crash;
- no product eligible -> explicit no-match state;
- candidates exist but no economically feasible offer -> explicit no-feasible-offer state;
- stock zero -> reject;
- missing evidence -> unverified, not fabricated;
- divide-by-zero / missing numeric fields -> safe validation/error handling.

## 19. MVP scope
Must have:
- one product category;
- synthetic 8-12 product catalogue;
- complex natural-language request or preset fallback;
- structured intent;
- hard eligibility;
- semantic/soft preference matching;
- merchant economics;
- bounded offer scenario optimisation;
- explanation;
- machine-readable B2A response;
- Streamlit demo;
- core tests;
- README/run instructions.

## 20. Explicit out-of-scope
For Round 2 implementation unless separately approved:
- real payment processing;
- production checkout;
- authentication;
- database;
- web scraping;
- multi-merchant marketplace;
- multi-category catalogue;
- model training;
- proprietary ranking reconstruction;
- real sales-uplift claims;
- large analytics dashboard;
- production FPT integration.

## 21. Acceptance criteria
The core MVP is accepted only if all are true:
1. App launches with a documented command.
2. A buyer request produces validated structured intent.
3. Hard buyer constraints are enforced deterministically.
4. Semantic preference scoring affects product ranking.
5. Stock-zero products cannot be recommended.
6. The optimiser evaluates more than one merchant offer scenario.
7. Minimum merchant economics are enforced.
8. The final offer is feasible for both buyer hard constraints and merchant constraints.
9. The UI explains why the offer was selected.
10. A machine-readable JSON response is produced.
11. No-match and no-feasible-offer cases do not crash.
12. Missing evidence is not hallucinated.
13. Core deterministic tests pass.
14. Synthetic/demo data and simulated outputs are clearly labelled.

## 22. Round 3 readiness
Because core product features cannot be redesigned after Round 2 submission, the submitted MVP should already contain the complete core story:

complex buyer intent -> semantic understanding -> catalogue match -> merchant-aware offer optimisation -> explainable B2A response.

Round 3 work should focus on presentation, explanation, demo reliability, evidence, deployment roadmap and defence rather than replacing this core flow.

## 23. Review gate
This document is currently DRAFT.

Next step:
1. Gemini performs an independent Red Team review and writes `docs/REVIEW_LOG.md`.
2. ChatGPT assesses each P0/P1/P2 item.
3. Core changes, if any, are returned to the user for approval.
4. After approval, this document is marked FROZEN and Codex may begin implementation planning.
