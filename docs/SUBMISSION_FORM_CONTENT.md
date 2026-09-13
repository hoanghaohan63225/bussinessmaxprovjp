# Round 2 Submission Form Content

Purpose: copy-ready English text for the official UAVS Hackathon 2026 Round 2 submission form.

> Keep this file as the source of truth when filling the form. Do not invent new claims at submission time.

## Project name

**bussinessmaxprovjp**

## Short tagline

**Merchant-side B2A Offer Intelligence**

## One-sentence description

`bussinessmaxprovjp` is a merchant-side B2A offer intelligence system that converts complex buyer-agent intent into a feasible, machine-readable merchant offer while enforcing buyer constraints, fulfilment rules and merchant economics.

## Short description (approximately 80–100 words)

`bussinessmaxprovjp` helps retailers adapt to AI-mediated commerce by turning complex buyer-agent requests into truthful, feasible merchant offers. The system decodes natural-language intent, applies immutable catalogue constraints, ranks candidates using explainable semantic fit, generates bounded price/shipping/warranty scenarios, and selects only offers that satisfy both buyer hard constraints and merchant economics. The final result is returned as machine-readable B2A JSON, with a synthetic transaction handoff after explicit acceptance. The MVP uses a fictional laptop catalogue and synthetic economics; it does not claim real payment, measured purchase probability or proprietary shopping-agent ranking logic.

## Problem statement

Traditional e-commerce is designed primarily for human browsing, persuasion and checkout. AI shopping agents instead require structured facts, semantic intent understanding, explicit constraints and machine-readable transaction outputs. Retailers therefore need a merchant-side decision layer that can determine not only which product matches a request, but which offer can truthfully be presented while remaining fulfilable and economically acceptable.

## Solution summary

Core flow:

`Buyer AI request -> structured intent -> product-level eligibility -> semantic catalogue matching -> bounded merchant offer scenarios -> offer-level buyer + merchant feasibility -> offer selection -> machine-readable B2A offer -> explicit buyer acceptance -> synthetic transaction handoff`

Key principle:

**Buyer fit × Merchant economics**

The system does not allow soft semantic fit to override hard constraints such as stock, delivery, warranty, buyer budget or minimum merchant economics.

## Key differentiators

1. **Beyond semantic search** — semantic relevance is only the first step; the system continues into merchant offer construction and feasibility.
2. **Beyond AI visibility monitoring** — it produces an actionable machine-readable offer rather than only reporting whether a brand appears.
3. **Beyond price optimisation** — the optimiser considers buyer intent plus price, shipping, warranty and merchant contribution together.
4. **Deterministic merchant controls** — stock, budget, shipping, warranty, contribution and final feasibility are calculated in Python rather than delegated to an LLM.
5. **Fail-closed safety** — unsupported hard requirements or missing evidence are not invented; impossible requests return an explicit `no_feasible_offer` state.

## Target users / customer segment

Primary users:
- merchant e-commerce managers;
- category managers;
- retail transformation / commerce technology teams.

Initial customer profile:
- retailer or product company with structured catalogue data;
- control over offer levers such as price, shipping and warranty;
- increasing exposure to AI-mediated shopping journeys.

Initial beachhead:

**One retailer -> one category -> one merchant decision owner.**

## Market / go-to-market approach

Pilot path:

`Shadow mode -> controlled intervention -> measured business validation -> category / integration expansion`

The first pilot should compare the system's recommended offers against current merchant decision-making without automatically changing production commerce. After data rights, economics and safety are validated, bounded interventions can be tested before broader rollout.

## Technical architecture

- **Streamlit** — transparent hackathon demo surface.
- **`src/intent.py`** — natural-language intent interpretation, controlled mapping/fallback and validation.
- **`src/matcher.py`** — catalogue validation, immutable eligibility and semantic component scoring.
- **`src/optimizer.py`** — bounded price/shipping/warranty scenarios, buyer/merchant feasibility, deterministic economics, final offer selection and synthetic transaction handoff.
- **`data/catalog.csv`** — fictional laptop catalogue with synthetic merchant economics.

AI responsibility boundary:
- optional LLM/semantic layer interprets natural language and maps intent;
- deterministic Python validates hard constraints and calculates all merchant-economic decisions.

## Technologies / APIs

- Python 3
- Streamlit
- Pandas
- pytest
- Optional Google Gemini intent decoding through `google-genai`

The reliable demo path does **not** require an external API key.

## Runtime / testing evidence

Latest verified local build:

- `py -m pytest -q` -> **15 passed in 0.48s**;
- Streamlit launched successfully at `localhost:8501`;
- default gaming flow produced a feasible B2A offer;
- non-gaming `CreatorPro 15` was excluded from a hard gaming request;
- explicit acceptance produced synthetic `transaction_ready`;
- impossible request produced explicit `no_feasible_offer` without crashing;
- changing the request after acceptance cleared stale transaction state.

## Repository

**GitHub:** `https://github.com/hoanghaohan63225/bussinessmaxprovjp`

## Local run instructions

```bash
pip install -r requirements.txt
python -m pytest -q
python -m streamlit run app.py
```

On Windows, if `python`/`pip` aliases are unavailable:

```powershell
py -m pip install -r requirements.txt
py -m pytest -q
py -m streamlit run app.py
```

## Deployment / scalability path

The hackathon MVP intentionally uses Streamlit and CSV for reliability. A production path would:

1. replace the synthetic CSV with authorised merchant catalogue, inventory, cost and policy APIs;
2. expose the same structured intent / offer contracts through a stateless merchant-side service;
3. retrieve/index a bounded candidate set before deterministic offer optimisation on large catalogues;
4. scale stateless workers horizontally for buyer-agent traffic;
5. add authentication, tenant isolation, audit logs, observability, privacy/data-residency controls, rate limits and load testing.

## Adaptation from Round 1

Round 1 focused on merchant decision intelligence across price, shipping, warranty, product strategy and merchant economics.

After receiving the full FPT case study for Round 2, the concept was adapted into a direct B2A flow:

`complex buyer intent -> semantic understanding -> catalogue match -> merchant offer optimisation -> machine-readable proposal -> synthetic transaction handoff`

This preserves the Round 1 merchant-economics differentiator while incorporating the full-case emphasis on intention decoding, machine-to-machine interaction and transaction closure.

## Limitations / honest disclosure

- one fictional laptop category;
- synthetic catalogue and economics;
- no real payment or production checkout;
- no database or authentication in the MVP;
- no dynamic multi-product bundling;
- no multi-round autonomous negotiation;
- no live two-agent LLM-to-LLM pair required for the reliable demo;
- no production FPT API integration is claimed;
- buyer-fit/economic scores are illustrative deterministic metrics, not measured purchase probability or sales uplift.

## Demo path (90 seconds)

1. Show the default complex gaming buyer request.
2. Click **Run merchant pipeline**.
3. Show decoded intent and visible execution mode.
4. Show eligible/rejected catalogue candidates.
5. Show bounded merchant offer scenarios and the selected feasible offer.
6. Explain **buyer fit × merchant economics**.
7. Show machine-readable B2A JSON.
8. Click **Accept recommended offer**.
9. Show `transaction_ready` and explicitly state that it is a synthetic handoff, not real payment.

## Important submission wording

Use:
- **working MVP / prototype**
- **synthetic catalogue / economics**
- **machine-readable B2A offer**
- **synthetic transaction handoff**
- **optional Gemini intent decoding**
- **deterministic merchant economics**

Avoid claiming:
- production-ready checkout;
- real-world sales uplift;
- real purchase probability;
- proprietary AI-shopping ranking knowledge;
- confirmed FPT integration or partnership;
- real payment processing.
