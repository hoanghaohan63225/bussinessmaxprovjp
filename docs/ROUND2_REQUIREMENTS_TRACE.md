# Round 2 Requirements Trace

Status: APPROVED / FROZEN under D-009
Owner: ChatGPT Team Lead
Purpose: give implementation agents a compact trace from official Round 2 requirements to the frozen product design, implementation modules, demo evidence, and known gaps. This file paraphrases the source documents; it does not replace them.

## Source priority
1. FPT Problem Statement Final — official Round 2 case study.
2. Hackathon Rulebook 2026 Final Updated — official Round 2 outputs and judging criteria.
3. `docs/ROUND2_PRODUCT_SPEC.md` — frozen implementation source of truth.
4. `docs/DECISION_LOG.md` — frozen team decisions.
5. Round 1 proposal — retained differentiators and historical rationale only.

## Requirement-to-implementation trace

| ID | Source requirement / priority | Frozen product response | Planned implementation / evidence | Coverage |
|---|---|---|---|---|
| R2-01 | The solution must be merchant-side: the business adapts to the buyer's agent, not a consumer-facing shopping assistant. | `bussinessmaxprovjp` is the merchant-side system; Streamlit is only a transparent demo surface. | `app.py` shows Buyer AI request entering the merchant system and a machine-readable response leaving it. | FULL |
| R2-02 | Decode complex, multi-constraint buyer-agent intentions. | Intent Decoder converts natural language into validated structured intent with hard requirements, preferences, assumptions and unresolved requirements. | `src/intent.py`; UI displays decoded intent and execution mode. | FULL |
| R2-03 | Intention accuracy / semantic matching should go beyond basic keyword or specification matching. | LLM semantic interpretation when available; controlled semantic mapping fallback; deterministic weighted fit including `use_case_fit`. | `src/intent.py`, `src/matcher.py`, paraphrase test in `tests/test_core.py`. | FULL for MVP demonstration; not a claim of real-world purchase prediction. |
| R2-04 | Dynamically analyse the merchant catalogue against decoded intent. | Two-stage flow: product-level eligibility, then semantic scoring/ranking. | `data/catalog.csv`, `src/matcher.py`; UI exposes candidates, rejected products and reasons. | FULL |
| R2-05 | Return a tailored proposal with logical justification, not merely a SKU list. | Merchant Offer Optimizer generates bounded price/shipping/warranty scenarios and selects the best feasible offer using buyer fit × merchant economics. | `src/optimizer.py`; UI shows recommended offer, component reasoning and merchant constraints. | FULL |
| R2-06 | Machine-readable data structuring is in scope; AI agents rely on deterministic facts, structured data, APIs and machine-readable pricing. | Structured intent, structured catalogue, B2A response JSON and deterministic merchant calculations. | JSON panel in `app.py`; deterministic calculations in Python. | FULL |
| R2-07 | The system should avoid mismatched or hallucinated product claims. | Missing evidence is `unverified`; unknown facts cannot be converted into positive claims; LLM explanations may only verbalise pipeline facts. | Catalogue evidence fields + validation/failure paths; tests for missing evidence. | FULL |
| R2-08 | API-based checkout / closing the loop is in scope and appears in the desired winning-demo flow. | Minimal synthetic transaction handoff after buyer acceptance. No real payment system. | `offer_available` -> accept -> `checkout_request` / `order_intent` -> `transaction_ready`, synthetic offer/order IDs. | PARTIAL by design: demonstrates contract/handoff, not production checkout. |
| R2-09 | Dynamic B2A negotiation is an illustrative direction and AI-to-AI negotiation is in scope. | Core MVP does not require multi-round negotiation. A single counter-offer remains stretch-only after core acceptance criteria pass. | Re-run the same deterministic pipeline with updated constraints only if time remains. | PARTIAL / STRETCH; not required for core build. |
| R2-10 | Dynamic product bundling is in scope and appears under the Technical Architecture evaluation priority. | Frozen MVP uses one laptop product per recommended offer and does not implement bundles. | Architecture should keep matcher/optimizer separable so bundle candidates could be added later without replacing the core pipeline. | GAP ACCEPTED under frozen MVP scope. Do not add bundling without Team Lead approval. |
| R2-11 | Technical Architecture prioritises viable/scalable design, APIs and machine-to-machine logic; human-dashboard polish is lower priority. | Small modular Python architecture, machine-readable contracts, deterministic core, optional external LLM. | `app.py`, optional `src/intent.py`, `src/matcher.py`, `src/optimizer.py`; JSON response and transaction handoff are primary demo evidence. | FULL for hackathon architecture; live LLM-to-LLM agent pair is not implemented. |
| R2-12 | Business Value & Conversion: help a traditional product company win the sale by proving fit to the buyer agent. | Selection balances buyer fit with merchant economics and rejects economically unsafe offers. | Optimizer enforces stock, landed buyer budget, contribution and minimum contribution margin. | FULL as a decision/offer demonstration; no real conversion uplift claim. |
| R2-13 | Round 2 requires a working live demo/MVP. | One-command Streamlit demo with fallback that does not depend on an external API key. | `streamlit run app.py`; primary scenario plus failure scenario. | REQUIRED OUTPUT |
| R2-14 | Round 2 requires technical documentation describing architecture, technologies/APIs and installation/running instructions. | README is a required submission artifact. | `README.md` drafted by Codex and final-reviewed by ChatGPT. | REQUIRED OUTPUT |
| R2-15 | Round 2 requires repository/full source code and a Pitch Deck. | GitHub is the project source of truth; pitch content is a tracked output. | repository source + `pitch/PITCH_CONTENT.md` / final deck. | REQUIRED OUTPUT |
| R2-16 | Technical quality includes reproducibility, appropriate AI integration, information security and data privacy. | Deterministic tests, fallback mode, secrets excluded from repo, no personal customer data needed for MVP. | `tests/test_core.py`, environment/Streamlit secrets instructions, no committed credentials. | FULL for MVP scope. |
| R2-17 | Adaptation & upgrade rewards incorporation of the full case study / Problem Setter input. | Round 1 merchant-economics optimizer is retained but repositioned behind direct buyer-agent intent decoding and B2A response. | Core flow visibly combines Round 2 semantic interaction with Round 1 merchant offer optimisation. | FULL |

## Round 1 differentiators intentionally preserved

The Round 1 proposal defined a merchant-side decision layer around truthful offer changes, especially price, delivery/shipping and warranty, evaluated against merchant contribution, inventory and uncertainty. Round 2 keeps the defensible part of that idea as the `Merchant Offer Optimizer`, but moves it into the direct B2A interaction required by the full case study.

Implementation consequence:
- do not reduce the MVP to semantic product search only;
- do not let a high semantic score override merchant feasibility;
- do not claim access to proprietary shopping-agent ranking logic;
- label demo catalogue, financial figures and transaction outputs as synthetic/illustrative.

## Known deliberate limitations

These are visible limitations, not hidden omissions:
- fictional laptop catalogue only;
- no real retailer/FPT integration;
- no real payment or production checkout;
- no multi-product dynamic bundling in the frozen MVP;
- no multi-round autonomous negotiation in the core MVP;
- no claim that `buyer_fit` predicts real AI-agent purchase probability;
- no sales-uplift or ranking-accuracy claim;
- external LLM is optional and the app must remain demoable without it.

Codex must not close these gaps by expanding scope unless the Team Lead records a new approved decision.