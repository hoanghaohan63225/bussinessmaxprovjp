# Round 2 Submission Checklist

Owner: ChatGPT Team Lead + User final verification
Status: FINAL PRE-SUBMISSION PASS IN PROGRESS

## Hard deadline

Official Round 2 submission deadline: **17:00 AEST, 13 September 2026**.
For Vietnam time (UTC+7), use **14:00 on 13 September 2026** as the hard cutoff.
Internal target: **13:40 Vietnam time** to preserve a submission buffer.

Do not spend the final buffer on new features.

## Required Round 2 outputs

- [x] Working product / AI solution demo that can be demonstrated live locally.
- [x] `README.md` with architecture, technologies/APIs, installation and run instructions.
- [x] GitHub repository containing the full source code.
- [ ] Final Pitch Deck file/link ready for submission.

## Runtime gate — VERIFIED

Observed on the latest downloaded repository state:

```text
py -m pytest -q
15 passed in 0.48s
```

Streamlit also launched successfully at `http://localhost:8501`.

Manual success flow:
- [x] App launches without an API key.
- [x] Default gaming buyer request decodes into structured intent.
- [x] Execution mode is visibly shown.
- [x] Candidate products / rejection reasons are visible.
- [x] More than one merchant offer scenario is evaluated.
- [x] Final selected offer is within buyer hard constraints.
- [x] Merchant margin rule is satisfied.
- [x] B2A JSON is displayed.
- [x] Clicking Accept creates a synthetic `transaction_ready` handoff.

Manual failure / safety flow:
- [x] Impossible constraints return an explicit `no_feasible_offer` state without crashing.
- [x] Hard gaming capability excludes products without explicit gaming/GPU evidence.
- [x] Editing the buyer request after acceptance clears the previous transaction state.
- [x] Controlled mapping works without an API key.
- [x] Automated tests cover stock-zero rejection, unsupported hard evidence fail-closed behaviour and LLM failure fallback.

## Repository hygiene

- [x] No credential file is present at repository root.
- [x] `.env` is ignored.
- [x] `.streamlit/secrets.toml` is ignored.
- [x] Source competition PDFs are not present in the public repository.
- [x] Synthetic catalogue and economics are clearly labelled synthetic/illustrative.
- [x] No claim of real purchase probability, ranking accuracy, sales uplift or proprietary shopping-agent logic is made in the README/demo framing.
- [x] No virtualenv/cache directory is present in the repository root.

Before final submission, do one visual GitHub check for any accidental credential or upload made outside the tracked workflow.

## Product-scope integrity

Core submitted story is frozen as:

`complex buyer intent -> semantic understanding -> catalogue match -> merchant offer optimisation -> explainable B2A offer -> explicit accept -> synthetic transaction handoff`

Do not add before submission:
- real payment / production checkout;
- database or authentication;
- React / FastAPI / Docker / microservices;
- scraping;
- multi-category catalogue;
- dynamic multi-product bundles;
- multi-round autonomous negotiation;
- production FPT integration.

## Round 2 judging readiness

### 1. User Experience — 20%
- [x] Target human users identified as merchant e-commerce/category managers and IT/integration teams.
- [x] Machine counterpart identified as buyer AI / shopping agent.
- [x] Demo flow is understandable as one sequential pipeline.
- [x] Success and failure states are visible and consistent.

### 2. Technical Quality — 25%
- [x] Working end-to-end MVP.
- [x] Documented Streamlit launch.
- [x] Deterministic economics and constraints are separated from LLM interpretation.
- [x] Tests run on the latest submitted code: **15 passed in 0.48s** on the user machine.
- [x] Architecture and file responsibilities documented.
- [x] Secrets / data-safety approach stated.

### 3. Deployability & Scalability — 20%
- [x] README explains replacing local CSV with authorised merchant catalogue/inventory interfaces.
- [x] README explains stateless service/API production path.
- [x] README explains retrieval/indexing before bounded optimisation for large catalogues.
- [x] README states production controls such as authentication, audit, tenant isolation, observability, privacy/residency and load testing as roadmap requirements.

### 4. Market Strategy — 25%
- [x] Primary customer segment: retailers/product companies selling through AI-mediated commerce.
- [x] Initial beachhead: one retailer, one category, merchant team with authority over price/shipping/warranty levers.
- [x] Value proposition: improve agent-fit while respecting merchant economics rather than merely increasing visibility.
- [x] Competitive distinction: connects semantic buyer intent to feasible merchant offer construction.
- [x] GTM: retailer pilot -> shadow mode -> controlled intervention -> integration/service expansion.
- [x] FPT relevance framed as a potential integration layer without claiming an unverified production partnership/API.

### 5. Adaptation & Upgrade — 10%
- [x] Complex intent, semantic matching, machine-readable offer and transaction closure incorporated.
- [x] Round 1 merchant-economics differentiator preserved.
- [x] Requirements trace documents deliberate partial/gap coverage without pretending those gaps are solved.

## Pitch / demo rehearsal

Primary 90-second live demo path:
1. Show complex buyer request.
2. Run pipeline.
3. Point to decoded intent and execution mode.
4. Show why products passed/failed.
5. Show multiple merchant scenarios and selected offer.
6. Explain **buyer fit × merchant economics**.
7. Show machine-readable B2A JSON.
8. Click Accept.
9. Show `transaction_ready` JSON and state explicitly that it is synthetic, not a real payment.

Failure demo backup:
- use the tested impossible request;
- show explicit `no_feasible_offer` rather than a fabricated recommendation.

## Final submission actions — User

- [ ] Open the official submission channel before the last 20 minutes.
- [ ] Confirm repository link opens correctly on `main`.
- [ ] Confirm README renders correctly on GitHub.
- [ ] Confirm final Pitch Deck file/link is ready.
- [ ] Decide whether to submit a local-demo instruction only or also create a public Streamlit deployment link if time/rules require it.
- [ ] Rehearse the primary demo once without changing code.
- [ ] Submit before the hard deadline.
- [ ] Save submission confirmation / screenshot.
