# Round 2 Submission Checklist

Owner: ChatGPT Team Lead + User final verification
Status: ACTIVE

## Hard deadline

Official Round 2 submission deadline: **17:00 AEST, 13 September 2026**.
For Vietnam time (UTC+7), use **14:00 on 13 September 2026** as the hard cutoff.
Internal target: **13:40 Vietnam time** to preserve a submission buffer.

Do not spend the final buffer on new features.

## Required Round 2 outputs

- [ ] Working product / AI solution demo that can be demonstrated live.
- [ ] `README.md` with architecture, technologies/APIs, installation and run instructions.
- [ ] GitHub repository containing the full source code.
- [ ] Pitch Deck for Round 3 / Gala use.

## Runtime gate — must complete before final submission

From a fresh terminal in the repository root:

```bash
pip install -r requirements.txt
python -m pytest -q
python -m streamlit run app.py
```

Record the exact pytest result. Never reuse an earlier count from a different working copy.

Manual success flow:
- [ ] App launches without an API key.
- [ ] Default gaming buyer request decodes into structured intent.
- [ ] Execution mode is visibly shown.
- [ ] Candidate products / rejection reasons are visible.
- [ ] More than one merchant offer scenario is evaluated.
- [ ] Final selected offer is within buyer hard constraints.
- [ ] Merchant margin rule is satisfied.
- [ ] B2A JSON is displayed.
- [ ] Clicking Accept creates a synthetic `transaction_ready` handoff.

Manual failure / safety flow:
- [ ] Impossible budget or constraints return an explicit no-feasible state without crashing.
- [ ] Stock-zero product is never recommended.
- [ ] Missing hard evidence is unresolved/unverified, not invented.
- [ ] Editing the buyer request after acceptance clears the previous transaction state.
- [ ] LLM mode without a valid key visibly falls back to controlled mapping if selected.

## Repository hygiene

- [ ] No API key, token, password or credential is tracked.
- [ ] `.env` is ignored.
- [ ] `.streamlit/secrets.toml` is ignored.
- [ ] Source competition PDFs are not committed to the public repository.
- [ ] Synthetic catalogue and economics are clearly labelled synthetic/illustrative.
- [ ] No claim of real purchase probability, ranking accuracy, sales uplift or proprietary shopping-agent logic.
- [ ] No accidental large cache, virtualenv or generated secret file is committed.

## Product-scope integrity

Core submitted story must remain:

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
- [ ] Target human users are clearly identified as merchant e-commerce/category managers and IT/integration teams.
- [ ] Machine counterpart is clearly identified as buyer AI / shopping agent.
- [ ] Demo flow is understandable in one screen without decorative complexity.
- [ ] Success and failure states are visible and consistent.

### 2. Technical Quality — 25%
- [ ] Working end-to-end MVP.
- [ ] One-command documented Streamlit launch.
- [ ] Deterministic economics and constraints are separated from LLM interpretation.
- [ ] Tests run on the exact submitted code.
- [ ] Architecture and file responsibilities are documented.
- [ ] Secrets / data-safety approach is stated.

### 3. Deployability & Scalability — 20%
- [ ] Explain that demo uses local CSV but production can replace it with authorised merchant catalogue/inventory APIs.
- [ ] Explain that deterministic matching/optimisation can run as a stateless service behind an API.
- [ ] Explain scaling path: catalogue indexing / retrieval first, bounded optimisation only on candidate set, horizontally scalable stateless workers.
- [ ] State that production requires authentication, audit, tenant isolation, observability, privacy/residency and load testing; these are roadmap items, not demo claims.

### 4. Market Strategy — 25%
- [ ] Primary customer segment: retailers/product companies selling through AI-mediated commerce.
- [ ] Initial beachhead: one retailer, one category, merchant team with authority over price/shipping/warranty levers.
- [ ] Value proposition: improve agent-fit while respecting merchant economics rather than merely increasing visibility.
- [ ] Competitive distinction: not just semantic search, visibility monitoring or price optimisation; connects semantic buyer intent to feasible merchant offer construction.
- [ ] GTM: retailer pilot -> shadow mode -> controlled intervention -> integration/service expansion.
- [ ] FPT relevance: potential integration layer across commerce, AI/data and retailer transformation services; no unverified partnership/API claim.

### 5. Adaptation & Upgrade — 10%
- [ ] Full FPT case-study input is visibly incorporated: complex intent, semantic matching, machine-readable offer and transaction closure.
- [ ] Round 1 merchant economics differentiator is preserved.
- [ ] Requirements trace explains deliberate partial/gap coverage without pretending those gaps are solved.

## Pitch / demo rehearsal

Primary 90-second live demo path:
1. Show complex buyer request.
2. Run pipeline.
3. Point to decoded intent and execution mode.
4. Show why products passed/failed.
5. Show multiple merchant scenarios and selected offer.
6. Explain buyer-fit × merchant economics.
7. Show machine-readable B2A JSON.
8. Click Accept.
9. Show `transaction_ready` JSON and state explicitly that it is synthetic, not a real payment.

Failure demo backup:
- use an impossible budget or hard requirement;
- show explicit no-feasible/unverified state rather than hallucinated recommendation.

## Final submission actions — User

- [ ] Open the official submission channel before the last 20 minutes.
- [ ] Confirm repository link opens correctly to the intended branch.
- [ ] Confirm README renders correctly on GitHub.
- [ ] Confirm required deck file/link is ready.
- [ ] Confirm live demo command one final time.
- [ ] Submit before the hard deadline.
- [ ] Save submission confirmation / screenshot.
