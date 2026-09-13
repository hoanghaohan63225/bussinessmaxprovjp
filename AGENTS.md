# AGENTS.md

## Project
bussinessmaxprovjp — UAVS Hackathon 2026, FPT Australasia case study.

## Source priority
1. FPT Round 2 problem statement
2. Hackathon Rulebook
3. `docs/ROUND2_PRODUCT_SPEC.md`
4. `docs/DECISION_LOG.md`
5. `docs/TASKS.md`
6. Round 1 proposal and supporting materials as historical context only

If any lower-priority source conflicts with a higher-priority source, follow the higher-priority source.

## Team roles
- Product Owner / Final Approver: user
- Team Lead / Product Architect: ChatGPT
- Independent Reviewer / Red Team: Gemini
- Implementation Engineer: Codex

## Frozen decisions
- D-001: Core product flow is Buyer Intent -> Semantic Match -> Merchant Optimisation -> B2A Offer.
- D-002: LLM handles language/semantic interpretation and explanation; deterministic Python handles economics, constraints and optimisation.
- D-003: Stack is Python + Streamlit + Pandas + pytest + optional Gemini API. No unnecessary framework expansion.
- D-004: GitHub is the shared source of truth for derived project artifacts and source code. Source PDFs are not uploaded while the repository is public.

## Engineering rules
1. Communicate explanations to the user in Vietnamese.
2. Use English for code identifiers, function names, filenames and technical schema keys.
3. Read `docs/ROUND2_PRODUCT_SPEC.md`, `docs/DECISION_LOG.md` and `docs/TASKS.md` before implementation work.
4. The Product Spec is authoritative once marked FROZEN.
5. Do not silently expand scope.
6. Do not add React, Next.js, FastAPI, databases, authentication, Docker or microservices unless a new approved decision explicitly allows it.
7. Do not rewrite unrelated modules when a small fix is sufficient.
8. Before meaningful changes, state the plan and files to be changed.
9. After changes, run relevant tests and report actual results.
10. Never claim a test passed unless it was actually run.
11. Prioritise in this order: working end-to-end flow, reliability, testability, readability, UI polish, feature count.
12. Simulated metrics must never be presented as real-world sales, ranking or platform performance.
13. Do not claim access to proprietary AI-shopping ranking logic.
14. If data/evidence is missing, return an explicit unknown/unverified state instead of inventing a claim.
15. Keep private merchant economics out of hosted LLM prompts unless explicitly required and approved.
16. Any code or external library/API used must be declared in README documentation.

## AI responsibility boundary
### LLM may
- Parse natural-language buyer requests into validated structured intent.
- Map nuanced language to catalogue concepts/attributes.
- Produce concise explanation text from deterministic facts.

### Deterministic Python must
- Apply hard eligibility constraints.
- Check stock.
- Calculate price, cost, margin, shipping subsidy and warranty cost.
- Generate offer scenarios.
- Enforce merchant constraints.
- Rank/select feasible offers using declared scoring logic.

## Change control
Large product decisions follow:
PROPOSED -> USER APPROVED -> FROZEN.

Codex must not alter a FROZEN product decision. Gemini may challenge a decision in `docs/REVIEW_LOG.md`, but only ChatGPT + user approval may change it.

## File ownership
- ChatGPT: `AGENTS.md`, `docs/ROUND2_PRODUCT_SPEC.md`, `docs/DECISION_LOG.md`, `docs/TASKS.md`, `docs/SUBMISSION_CHECKLIST.md`, `pitch/PITCH_CONTENT.md`
- Gemini: `docs/REVIEW_LOG.md`
- Codex: `app.py`, `src/**`, `data/**`, `tests/**`, `requirements.txt`
- Codex may draft `README.md`; ChatGPT gives final approval.

## Stop conditions
Stop and report instead of guessing when:
- the Product Spec is ambiguous on a core behaviour;
- implementation would require a new framework or major architecture change;
- business logic conflicts with a frozen decision;
- a test exposes an unresolved P0 issue;
- an API dependency prevents the core demo from running and no fallback exists.
