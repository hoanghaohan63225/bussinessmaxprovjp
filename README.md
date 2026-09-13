# bussinessmaxprovjp

Merchant-side B2A offer intelligence MVP for UAVS Hackathon 2026 / FPT Australasia.

## What it demonstrates

`Buyer AI request -> structured intent -> product-level eligibility -> semantic matching -> bounded merchant offer scenarios -> buyer + merchant feasibility -> offer scoring -> machine-readable B2A offer -> buyer acceptance -> synthetic transaction handoff`

The demo uses a fictional laptop catalogue and synthetic merchant economics. It does not claim real-world purchase probability, sales uplift, access to proprietary shopping-agent ranking logic, or a completed payment.

## Stack

- Python
- Streamlit
- Pandas
- pytest
- Optional Gemini intent decoding through `google-genai`

All pricing, stock, shipping, warranty, contribution and selection calculations are deterministic Python. The optional LLM is only used to interpret natural language into the validated intent schema.

## Run

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
python -m streamlit run app.py
```

The app works without an API key using `controlled mapping` or `fallback preset` mode.

Optional Gemini mode:

```bash
# Windows PowerShell
$env:GEMINI_API_KEY="your-key"
# macOS/Linux
# export GEMINI_API_KEY="your-key"
```

Never commit the key. `.env` and `.streamlit/secrets.toml` are ignored.

## Tests

```bash
python -m pytest -q
```

Core tests cover paraphrased intent mapping, two-stage constraints, stock, buyer-total budget, shipping economics, discount rescue, margin guardrails, unresolved hard evidence, safe normalisation, deterministic selection and transaction handoff.

## Demo data

`data/catalog.csv` contains 8 fictional laptops. Important fields include:

- `base_price`, `unit_cost`
- `stock`, `delivery_days`
- `merchant_shipping_cost`, `buyer_shipping_fee`
- base and optional extended warranty fields
- performance, portability and battery scores
- machine-readable tags and evidence notes

## Business rules

Buyer budget is evaluated on:

`buyer_total_price = offer_price + buyer_shipping_fee`

Merchant contribution is:

`contribution = offer_price + buyer_shipping_fee - unit_cost - merchant_shipping_cost - warranty_incremental_cost`

Free shipping sets the buyer fee to zero but does not remove merchant shipping cost. Hard constraints are evaluated before soft scoring can select an offer.

Approved offer scenarios are bounded to 0%, 3% and 5% discount; catalogue shipping fee or free-to-buyer; and base or explicitly declared extended warranty.

## Limits / accepted gaps

- One fictional laptop category only.
- No database, authentication, scraping or multi-merchant marketplace.
- No real checkout/payment processing.
- No dynamic multi-product bundles in the core MVP.
- No multi-round autonomous negotiation.
- The transaction handoff is a synthetic JSON contract (`transaction_ready`).
- Gemini is optional; offline fallback remains the reliable demo path.

See `docs/ROUND2_PRODUCT_SPEC.md`, `docs/ROUND2_REQUIREMENTS_TRACE.md`, and `docs/DECISION_LOG.md` for the frozen implementation scope.
