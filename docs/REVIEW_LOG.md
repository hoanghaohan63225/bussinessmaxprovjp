# REVIEW_LOG.md

Reviewer: ChatGPT acting in Red Team / QA role
Review target: `docs/ROUND2_PRODUCT_SPEC.md`
Source priority: FPT Round 2 Problem Statement > frozen team decisions > Round 1 differentiators
Status: REVIEW COMPLETE — awaiting Team Lead resolution

## Executive assessment

The product direction is strongly aligned with the Round 2 brief: it is merchant-side, starts from a complex buyer-agent intent, performs structured intent decoding and catalogue matching, and preserves the Round 1 merchant-economics differentiator through offer optimisation.

The current draft should NOT be frozen yet. Three issues can materially weaken correctness or the Round 3 story if implemented literally.

## P0 — must resolve before coding

### P0-01 — Budget eligibility is ordered incorrectly relative to offer optimisation

**Problem**
Section 9 says a product can be rejected when it cannot be configured at or below the buyer budget, but the pipeline places hard eligibility before merchant offer scenario generation. If implementation interprets this as `current_price > budget => reject`, a product priced at 1,349 could be rejected even though an approved -5% scenario would make it feasible under a 1,300 budget.

**Risk**
This breaks the core differentiator: the optimiser is supposed to adapt merchant-controlled offer levers.

**Required correction**
Split hard checks into two stages:
1. product-level eligibility before optimisation: stock, immutable capability constraints, impossible delivery, verified/known attributes;
2. offer-level feasibility after scenario generation: buyer total price, margin, shipping, warranty and other configurable constraints.

Budget should be checked against the generated offer, not blindly against current catalogue price.

### P0-02 — Shipping economics and buyer budget are ambiguous

**Problem**
The current schema has `shipping_cost` and the optimiser refers to merchant-subsidised shipping, but it does not distinguish:
- what the buyer pays for shipping;
- what fulfilment costs the merchant;
- what amount the merchant subsidises.

The contribution formula can therefore become misleading, and it is unclear whether buyer budget means product price only or landed checkout cost.

**Risk**
The core `buyer fit x merchant economics` claim becomes mathematically inconsistent.

**Required correction**
Use explicit fields/variables:
- `merchant_shipping_cost`
- `buyer_shipping_fee`

Define:
`buyer_total_price = offer_price + buyer_shipping_fee`

`contribution = offer_price + buyer_shipping_fee - unit_cost - merchant_shipping_cost - warranty_incremental_cost`

Buyer budget must apply to `buyer_total_price` for the demo.

A free-shipping scenario sets `buyer_shipping_fee = 0`; the merchant still bears `merchant_shipping_cost`.

### P0-03 — The core story does not yet close the transaction loop

**Problem**
The FPT full brief describes a strong demonstration as returning a tailored proposal and closing the loop through an API-driven transaction. The current MVP stops at a machine-readable offer and explicitly excludes production checkout.

**Risk**
The app can still pass Round 2, but because core features cannot be changed after Round 2, this leaves a visible gap for a Round 3 Gala demo.

**Required correction**
Do NOT add real payments or a backend service. Add a minimal deterministic transaction handoff to the core:
- buyer accepts recommended offer;
- system produces a machine-readable `checkout_request` / `order_intent` object;
- demo returns `transaction_ready` or `order_created_demo` status with offer ID and synthetic order ID.

This is a demo contract, not a real payment system. It should be clearly labelled synthetic/demo.

## P1 — important, fix in spec if low cost

### P1-01 — Semantic matching needs a concrete credibility test
The spec says matching goes beyond keyword equality, but implementation could still degenerate into hand-written keyword rules.

Add at least one acceptance test where two paraphrased buyer requests map to materially equivalent structured intent, for example `strong GPU for modern games` and `gaming performance matters most`.

If an LLM API is unavailable, label the fallback as controlled semantic mapping rather than pretending it has the same capability as an LLM.

### P1-02 — `use_case` should contribute explicitly to fit
The sample formula scores performance, portability and battery but does not explicitly score use-case/category fit. Add a documented `use_case_fit` / tag compatibility component or treat it as an explicit requirement bonus.

### P1-03 — Warranty scenario data is under-specified
The catalogue has `warranty_years` and `warranty_incremental_cost`, but the optimiser needs to know what extended option is actually available.

Prefer explicit demo fields such as:
- `base_warranty_years`
- `extended_warranty_years`
- `extended_warranty_cost`

The optimiser may only choose declared options.

### P1-04 — Preference weights must not be silently invented
If the buyer does not express relative priorities, the system should either use documented neutral defaults or mark confidence/assumption explicitly. Do not let an LLM invent highly specific weights without explanation.

### P1-05 — Normalisation needs a safe definition
`normalised_economic_score` must define behaviour when all feasible scenarios have the same value. Use a safe normaliser that cannot divide by zero. Keep the formula simple and documented.

### P1-06 — LLM failure mode should be visible in the demo
The UI should display whether intent came from `LLM mode`, `fallback preset`, or `controlled mapping`. This prevents the demo from overstating AI capability.

### P1-07 — Secrets must stay out of GitHub
If an external LLM API is used, load the key from environment variables / Streamlit secrets and never commit credentials. The app must remain demoable without the key.

## P2 — roadmap / do not spend core build time now

- Multi-product dynamic bundles.
- Multi-round autonomous negotiation beyond one counter-offer.
- Real checkout/payment provider.
- Database/authentication.
- Multi-category catalogues.
- Production deployment and FPT integration.
- Real-world ranking calibration or sales-uplift claims.
- Large merchant analytics dashboard.

## Judge-pressure questions to prepare later

1. How is this different from ordinary semantic product search?
2. Why is merchant economics necessary rather than simply ranking the best product?
3. What happens when the best semantic match is not economically feasible?
4. How do you stop the LLM from inventing product claims?
5. Does your `buyer_fit` model actually predict agent purchase behaviour?
6. What parts are synthetic and what parts are validated in the real world?
7. How would a real buyer agent call this merchant system?
8. How would this scale from 10 demo products to a retail catalogue?
9. How would a merchant set safe discount/margin boundaries?
10. What data is sent to the LLM, and what remains private?

## Reviewer recommendation

Proceed after resolving P0-01, P0-02 and P0-03. Incorporate the low-cost P1 clarifications into the frozen spec. Do not add P2 features before a stable end-to-end MVP exists.
