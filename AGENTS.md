# AGENTS.md

## Project
bussinessmaxprovjp — UAVS Hackathon 2026, FPT Australasia case study.

## Source priority
1. FPT Round 2 problem statement
2. Hackathon Rulebook
3. `docs/ROUND2_PRODUCT_SPEC.md`
4. `docs/ROUND2_REQUIREMENTS_TRACE.md`
5. `docs/DECISION_LOG.md`
6. `docs/CODEX_IMPLEMENTATION_PLAN.md` when implementing T5
7. `docs/TASKS.md`
8. Round 1 proposal and supporting materials as historical context only

If any lower-priority source conflicts with a higher-priority source, follow the higher-priority source.

## Team roles
- Product Owner / Final Approver: user
- Team Lead / Product Architect: ChatGPT
- Red Team / QA: ChatGPT acting in a separate review pass
- Implementation Engineer: Codex when available; ChatGPT may execute approved implementation work when Codex is unavailable

## Frozen decisions
- D-001: Core product flow is Buyer Intent -> Semantic Match -> Merchant Optimisation -> B2A Offer.
- D-002: LLM handles language/semantic interpretation and explanation; deterministic Python handles economics, constraints and optimisation.
- D-003: Stack is Python + Streamlit + Pandas + pytest + optional Gemini API. No unnecessary framework expansion.
- D-004: GitHub is the shared source of truth for derived project artifacts and source code. Source PDFs are not uploaded while the repository is public.
- D-005: Product-level eligibility and offer-level feasibility are separate; budget is not used to prematurely reject products before approved offer scenarios.
- D-006: `merchant_shipping_cost` and `buyer_shipping_fee` are separate; buyer budget applies to `buyer_total_price`.
- D-007: Minimal synthetic transaction handoff is core; no real payment/checkout backend.
- D-008: Semantic matching must show use-case fit, paraphrase credibility and execution-mode transparency.
- D-009: `docs/ROUND2_REQUIREMENTS_TRACE.md` is the compact case-study-to-implementation trace; accepted gaps must not be silently expanded.
- D-010: `docs/CODEX_IMPLEMENTATION_PLAN.md` is approved for T5, with reliable fallback first, no per-subtask approval unless P0/scope conflict, and mandatory deterministic tests + manual Streamlit smoke testing.

## Engineering rules
1. Communicate explanations to the user in Vietnamese.
2. Use English for code identifiers, function names, filenames and technical schema keys.
3. Read the Product Spec, Requirements Trace, Decision Log and Task Board before implementation work.
4. The Product Spec is authoritative once marked FROZEN.
5. Do not silently expand scope.
6. Do not add React, Next.js, FastAPI, databases, authentication, Docker or microservices unless a new approved decision explicitly allows it.
7. Do not rewrite unrelated modules when a small fix is sufficient.
8. Before meaningful changes, identify the plan and files to be changed.
9. After changes, run relevant tests when the environment supports them and report actual results.
10. Never claim a test passed unless that exact committed code/test set was actually run.
11. Prioritise in this order: working end-to-end flow, reliability, testability, readability, UI polish, feature count.
12. Simulated metrics must never be presented as real-world sales, ranking or platform performance.
13. Do not claim access to proprietary AI-shopping ranking logic.
14. If data/evidence is missing, return an explicit unknown/unverified state instead of inventing a claim.
15. Keep private merchant economics out of hosted LLM prompts unless explicitly required and approved.
16. Any code or external library/API used must be declared in README documentation.
17. Accepted gaps in `docs/ROUND2_REQUIREMENTS_TRACE.md` are deliberate; do not close them without a new approved decision.

## AI responsibility boundary
### LLM may
- Parse natural-language buyer requests into validated structured intent.
- Map nuanced language to catalogue concepts/attributes.
- Produce concise explanation text from deterministic facts.

### Deterministic Python must
- Apply product-level and offer-level hard constraints.
- Check stock.
- Calculate price, buyer total, cost, contribution/margin, shipping and warranty cost.
- Generate bounded offer scenarios.
- Enforce merchant constraints.
- Rank/select feasible offers using declared scoring logic.
- Create the synthetic transaction handoff from an explicitly accepted feasible offer.

## Change control
Large product decisions follow:
PROPOSED -> USER APPROVED -> FROZEN.

Implementation bug fixes that only restore compliance with the frozen spec may be applied without redefining the product. Any core-scope change must return to the decision log and user approval.

## File ownership
- ChatGPT: `AGENTS.md`, `docs/ROUND2_PRODUCT_SPEC.md`, `docs/ROUND2_REQUIREMENTS_TRACE.md`, `docs/DECISION_LOG.md`, `docs/TASKS.md`, `docs/REVIEW_LOG.md`, `docs/SUBMISSION_CHECKLIST.md`, `pitch/PITCH_CONTENT.md`
- Codex or ChatGPT acting as approved implementation engineer: `app.py`, `src/**`, `data/**`, `tests/**`, `requirements.txt`, `.gitignore`
- README may be drafted by implementation work; ChatGPT gives final approval.

## Stop conditions
Stop and report instead of guessing when:
- the Product Spec is ambiguous on a core behaviour;
- implementation would require a new framework or major architecture change;
- business logic conflicts with a frozen decision;
- a test exposes an unresolved P0 issue;
- an API dependency prevents the core demo from running and no fallback exists;
- fixing an issue would require changing an accepted gap or adding a new core feature.
