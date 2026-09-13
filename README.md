# bussinessmaxprovjp

Merchant-side B2A offer intelligence MVP for UAVS Hackathon 2026 / FPT Australasia.

## Product in one sentence

`bussinessmaxprovjp` receives a complex buyer-agent request, decodes it into structured intent, matches it against a merchant catalogue, constructs the best feasible merchant offer under buyer and merchant constraints, and produces a machine-readable transaction handoff after explicit buyer acceptance.

The product is **merchant-side**. It is not a consumer shopping assistant.

## What the demo demonstrates

`Buyer AI request -> structured intent -> product-level eligibility -> semantic matching -> bounded merchant offer scenarios -> buyer + merchant feasibility -> offer scoring -> machine-readable B2A offer -> buyer acceptance -> synthetic transaction handoff`

The demo uses a fictional laptop catalogue and synthetic merchant economics. It does not claim real-world purchase probability, sales uplift, access to proprietary shopping-agent ranking logic, or a completed payment.

## Architecture

```text
Streamlit demo surface (app.py)
        |
        v
Intent Decoder (src/intent.py)
  - optional Gemini interpretation
  - controlled mapping / preset fallback
  - intent validation / unresolved requirements
        |
        v
Catalogue Matcher (src/matcher.py)
  - catalogue validation
  - product-level immutable eligibility
  - semantic component scoring / use-case fit
        |
        v
Offer Optimiser (src/optimizer.py)
  - bounded price / shipping / warranty scenarios
  - offer-level buyer + merchant feasibility
  - deterministic economics and selection
  - B2A response JSON
  - synthetic transaction handoff
        |
        v
Synthetic catalogue (data/catalog.csv)
```

The Streamlit layer is only a transparent demonstration surface. The core logic is kept in normal Python modules so it can be tested independently and later exposed behind merchant APIs.

## Stack / APIs

- Python 3
- Streamlit
- Pandas
- pytest
- Optional Gemini intent decoding through `google-genai`

All pricing, stock, shipping, warranty, contribution and final selection calculations are deterministic Python. The optional LLM is only used to interpret natural language into the validated intent schema.

The full demo remains functional without an external LLM key.

## AI responsibility boundary

### LLM / semantic layer may
- interpret natural-language buyer requests;
- map nuanced phrases to structured intent dimensions.

### Deterministic Python must
- validate hard constraints;
- check stock and delivery;
- calculate price, buyer total, cost, contribution and margin;
- apply shipping and warranty economics;
- generate bounded scenarios;
- select the final feasible offer;
- generate the accepted-offer transaction handoff.

Unsupported hard requirements are marked unresolved and fail closed rather than being invented.

## Install and run

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```

Install and launch:

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

The app works without an API key using `controlled mapping` or `fallback preset` mode.

### Optional Gemini mode

Windows PowerShell:

```powershell
$env:GEMINI_API_KEY="your-key"
```

macOS / Linux:

```bash
export GEMINI_API_KEY="your-key"
```

Streamlit secrets are also supported. Never commit the key. `.env` and `.streamlit/secrets.toml` are ignored.

If Gemini is unavailable or returns invalid structured output, the app falls back to controlled mapping instead of making merchant-economic decisions through the LLM.

## Tests

Run the exact submitted test suite:

```bash
python -m pytest -q
```

Core tests cover:
- paraphrased intent mapping;
- optional-LLM failure fallback;
- unsupported hard-requirement fail-closed behaviour;
- explicit neutral preference defaults;
- non-finite numeric rejection;
- product-level stock / eligibility;
- base-price-over-budget survival before optimisation;
- bounded offer scenarios;
- buyer-total budget and discount rescue;
- shipping economics and contribution;
- unresolved hard evidence;
- safe normalisation and deterministic selection;
- explicit no-feasible state;
- end-to-end B2A response and transaction handoff.

Do not rely on test counts from another working copy; record the fresh result produced by the submitted repository.

## Demo data

`data/catalog.csv` contains 8 fictional laptops. Important fields include:

- `base_price`, `unit_cost`
- `stock`, `delivery_days`
- `merchant_shipping_cost`, `buyer_shipping_fee`
- base and optional extended warranty fields
- performance, portability and battery scores
- machine-readable tags and evidence notes

All catalogue facts and financial values are synthetic / illustrative.

## Two-stage constraints

### Product-level eligibility

Before offer optimisation, reject only immutable/currently impossible conditions such as:
- zero stock;
- impossible declared delivery;
- unavailable declared warranty capacity;
- required capability known not to match;
- unresolved hard evidence requirements.

A product is **not** rejected merely because its current base price exceeds the buyer budget if an approved offer scenario could reduce the final buyer total into budget.

### Offer-level feasibility

After scenario generation, every offer must satisfy buyer hard constraints and merchant economics before it may be ranked.

## Business rules

Buyer budget is evaluated on:

`buyer_total_price = offer_price + buyer_shipping_fee`

Merchant contribution is:

`contribution = offer_price + buyer_shipping_fee - unit_cost - merchant_shipping_cost - warranty_incremental_cost`

Free shipping sets the buyer fee to zero but does not remove merchant shipping cost.

Approved offer scenarios are bounded to:
- 0%, 3% and 5% discount;
- catalogue buyer shipping fee or free-to-buyer shipping;
- base warranty or explicitly declared extended warranty only.

The demo minimum contribution-margin threshold is synthetic and configured for demonstration. Soft scoring never overrides a failed hard constraint.

## Machine-readable transaction handoff

After explicit acceptance of the current feasible recommended offer, the app creates a deterministic object with:
- `transaction_ready` status;
- synthetic order ID;
- accepted offer ID / product ID;
- quantity;
- buyer total price;
- AUD currency;
- `not_processed_demo` payment status.

This is a **synthetic integration contract**, not a claim that payment or production checkout occurred.

## Deployment / scalability path

The MVP intentionally uses CSV + Streamlit to maximise hackathon reliability. A production path would:

1. replace the CSV with authorised merchant catalogue, inventory, cost and policy interfaces;
2. expose structured intent / offer contracts through a stateless merchant-side service;
3. retrieve/index a bounded candidate set from large catalogues before deterministic scenario optimisation;
4. scale stateless workers horizontally for agent requests;
5. add production controls such as authentication, tenant isolation, audit logs, observability, privacy/data-residency controls, rate limits and load testing.

These are deployment requirements / roadmap items, not features claimed by the current demo.

## Market / positioning

Initial target: retailers or product companies with structured catalogue data and control over offer levers such as price, shipping fee and warranty.

Initial beachhead: one retailer, one category and one merchant decision owner.

Differentiation:
- semantic search stops at relevance;
- visibility tools report whether a brand appears;
- price optimisers focus mainly on pricing;
- this MVP connects **semantic buyer intent -> feasible merchant offer -> buyer fit × merchant economics -> machine-readable handoff**.

A sensible pilot path is shadow mode first, then validated controlled interventions before any causal sales-uplift claim.

## Limits / accepted gaps

- One fictional laptop category only.
- No database, authentication, scraping or multi-merchant marketplace.
- No real checkout/payment processing.
- No dynamic multi-product bundles in the core MVP.
- No multi-round autonomous negotiation.
- No live two-agent LLM-to-LLM pair in the core MVP.
- No production FPT integration is claimed.
- Buyer-fit/economic scores are illustrative deterministic demo metrics, not measured purchase probability.
- The transaction handoff is a synthetic JSON contract (`transaction_ready`).
- Gemini is optional; offline fallback remains the reliable demo path.

## Project governance / traceability

- `docs/ROUND2_PRODUCT_SPEC.md` — frozen implementation source of truth.
- `docs/ROUND2_REQUIREMENTS_TRACE.md` — FPT requirement -> product response -> implementation/demo evidence.
- `docs/DECISION_LOG.md` — approved/frozen decisions.
- `docs/CODEX_IMPLEMENTATION_PLAN.md` — approved T5 implementation plan.
- `docs/REVIEW_LOG.md` — Red Team / QA findings.
- `docs/SUBMISSION_CHECKLIST.md` — final Round 2 submission gate.
- `pitch/PITCH_CONTENT.md` — source content for the required pitch deck.
