# bussinessmaxprovjp — Pitch Content

Purpose: English content source for the required Round 3 / Gala pitch deck.
Target delivery: approximately 10 minutes plus Q&A.

## Slide 1 — Title

**bussinessmaxprovjp**

**Merchant-side offer intelligence for the B2A era**

From complex buyer-agent intent to a feasible, machine-readable merchant offer.

UAVS Hackathon 2026 · FPT Australasia

Speaker point:
AI shopping agents are becoming a new customer interface. Retailers need more than product visibility; they need a system that can understand machine-mediated buyer intent and construct an offer the merchant can actually afford and fulfil.

---

## Slide 2 — The B2A problem

### Commerce was designed for humans

Traditional e-commerce optimises:
- visual persuasion;
- human navigation;
- emotional copy;
- conventional SEO;
- human checkout flows.

AI shopping agents instead need:
- structured facts;
- machine-readable constraints;
- semantic intent understanding;
- deterministic price / policy data;
- transaction-ready outputs.

### Merchant problem

A buyer agent may ask:

> “I need a gaming laptop under AUD 1,300, strong GPU performance, delivery within 3 days, and at least 2 years of warranty. Gaming performance matters more than portability.”

A normal catalogue can filter products. It does not answer the harder merchant question:

**What is the best feasible offer we should construct for this intent?**

---

## Slide 3 — Our solution

### Merchant-side B2A Offer Intelligence

Core flow:

`Buyer AI request`
→ `Intent Decoder`
→ `Product-level Eligibility`
→ `Semantic Catalogue Match`
→ `Merchant Offer Scenario Generator`
→ `Buyer + Merchant Feasibility`
→ `Offer Selection`
→ `Machine-readable B2A Offer`
→ `Buyer Accept`
→ `Synthetic Transaction Handoff`

### Key idea

**Buyer fit × Merchant economics**

We do not stop at “which product matches?”

We continue to “which truthful, fulfilable and economically feasible offer should the merchant present?”

---

## Slide 4 — What makes it different

### Not just semantic search
Semantic matching identifies which products fit the buyer’s use case and preferences.

### Not just price optimisation
The optimiser considers buyer constraints and multiple merchant-controlled levers, not price in isolation.

### Not just AI-shopping visibility
The system constructs an actionable merchant offer rather than reporting whether the brand appeared in an AI answer.

### Our differentiator

A product can be a strong semantic match but still be rejected if the resulting offer violates:
- buyer total budget;
- delivery requirement;
- warranty requirement;
- stock availability;
- merchant minimum economics.

Conversely, a product slightly above the current list-price budget can remain a candidate when an approved discount or shipping scenario can make the final offer feasible.

---

## Slide 5 — Live demo

### Example input

“I need a gaming laptop under AUD 1,300, strong GPU performance, delivery within 3 days, and at least 2 years of warranty. I care more about gaming performance than portability.”

### Demo sequence

1. Natural-language request becomes validated structured intent.
2. UI shows execution mode: LLM, controlled mapping, or fallback preset.
3. Immutable failures are rejected first.
4. Remaining products receive explainable semantic component scores.
5. System generates bounded price / shipping / warranty scenarios.
6. Every scenario is checked against buyer and merchant constraints.
7. Best feasible offer is returned as machine-readable JSON.
8. Buyer accepts the offer.
9. System emits a synthetic `transaction_ready` order-intent object.

Demo statement:
The transaction handoff is intentionally synthetic. We are demonstrating the machine contract, not pretending that a real payment occurred.

---

## Slide 6 — Technical architecture and safeguards

### Architecture

**Streamlit demo surface**
→ `src/intent.py`
→ `src/matcher.py`
→ `src/optimizer.py`
→ synthetic catalogue / B2A JSON

### AI responsibility boundary

LLM / semantic layer:
- interpret natural language;
- map nuanced language into structured intent.

Deterministic Python:
- stock and eligibility;
- buyer budget;
- shipping economics;
- warranty options;
- contribution and margin;
- scenario search;
- final offer selection;
- transaction handoff.

### Hallucination safeguards

- Unsupported hard requirements fail closed as unresolved.
- Missing evidence is never treated as verified.
- LLM never receives private merchant economics in the approved design.
- App remains demoable without an API key.
- No real customer data is required for the MVP.

---

## Slide 7 — Economics logic

Buyer budget is evaluated on the buyer’s actual demo total:

`buyer_total_price = offer_price + buyer_shipping_fee`

Merchant contribution is:

`contribution = offer_price + buyer_shipping_fee - unit_cost - merchant_shipping_cost - warranty_incremental_cost`

Important distinction:

**Free shipping for the buyer does not make shipping free for the merchant.**

The system first enforces all hard constraints, then combines normalised buyer-fit and economic scores for feasible offers only.

This avoids the failure mode where the “best recommendation” wins despite being impossible or unprofitable to fulfil.

---

## Slide 8 — Deployment and scalability

### MVP today

- one fictional laptop category;
- synthetic catalogue and economics;
- local Streamlit interface;
- optional external LLM for intent decoding;
- deterministic business logic.

### Production path

1. Replace CSV with authorised merchant catalogue, inventory and policy APIs.
2. Expose the same structured intent / offer contracts through a stateless merchant service.
3. Use catalogue indexing or retrieval to narrow large catalogues before bounded optimisation.
4. Scale stateless workers horizontally for buyer-agent traffic.
5. Add production controls: authentication, tenant isolation, audit logs, observability, privacy / residency controls and load testing.

These are deployment steps, not claims that the hackathon MVP already provides production infrastructure.

---

## Slide 9 — Customer and go-to-market

### Initial customer

Retailers or product companies that:
- have structured catalogue / cost data;
- control offer levers such as price, delivery charge or warranty;
- expect increasing AI-mediated shopping traffic.

### Beachhead

Start with:
- one retailer;
- one category;
- one merchant decision owner;
- bounded offer levers.

### Pilot path

**Shadow mode**
→ compare recommendations with current merchant decisions
→ validate data rights and economics
→ controlled intervention
→ expand categories / integrations after evidence.

### Value

For buyer agents:
- better fit;
- clearer machine-readable justification;
- fewer mismatched offers.

For merchants:
- controlled adaptation to agentic commerce;
- auditable economics;
- explicit trade-offs instead of blind discounting.

---

## Slide 10 — Why FPT / adaptation from Round 1

### Round 1 concept preserved

Our original differentiator was merchant decision intelligence across price, shipping, warranty and economics.

### Round 2 adaptation

The full case study required a more direct B2A flow, so we upgraded the concept to:

`complex buyer intent`
→ `semantic understanding`
→ `catalogue match`
→ `merchant-aware offer optimisation`
→ `machine-readable proposal`
→ `transaction handoff`

### Potential FPT fit

The system can conceptually sit between:
- digital commerce infrastructure;
- AI / data services;
- retailer transformation workflows.

We do **not** assume any specific FPT production API or partnership that has not been confirmed.

Closing line:

**The B2A shift is not only about helping an AI find a product. It is about helping the merchant construct the right offer for a machine-mediated buyer, without losing control of truth, fulfilment or economics.**

---

# Live demo script — 90 seconds

1. “This is a merchant-side system, not a consumer shopping assistant.”
2. Paste / show the default complex gaming request.
3. Click **Run merchant pipeline**.
4. “The request becomes structured intent. The mode is visible so we do not overstate what AI is doing.”
5. Point to candidate/rejected products and semantic component scores.
6. “Now the merchant layer creates bounded price, shipping and warranty scenarios.”
7. Point to scenario count and final offer.
8. “The winner must satisfy buyer hard constraints and merchant economics before soft scoring matters.”
9. Show B2A JSON.
10. Click **Accept recommended offer**.
11. Show `transaction_ready` JSON.
12. “This is a synthetic machine-to-machine transaction handoff, not a fake claim that payment happened.”

# Q&A defence anchors

**How is this different from normal semantic search?**
Semantic search ends at relevance. We continue into merchant-controlled offer construction, feasibility and economics.

**Does buyer_fit predict real purchases?**
No. It is an explainable MVP scoring function, not a measured purchase-probability model. Real calibration requires merchant traffic and controlled validation.

**Why not let the LLM choose the offer?**
Because stock, cost, margin, shipping and warranty constraints must be deterministic, auditable and testable.

**What happens when information is missing?**
Unsupported hard requirements are unresolved and fail closed rather than being invented.

**Where is the real checkout?**
The MVP demonstrates the machine-readable handoff contract. Production checkout/payment integration is intentionally outside hackathon scope.

**How does this scale?**
Retrieve a bounded candidate set from the large catalogue, then run deterministic offer optimisation on those candidates. The business logic can be exposed as stateless API workers.
