# Task Board

## T0 — Governance
Owner: ChatGPT
Status: DONE
Outputs: `AGENTS.md`, `docs/DECISION_LOG.md`, `docs/TASKS.md`

## T1 — Round 2 Product Spec
Owner: ChatGPT
Status: DONE / FROZEN
Output: `docs/ROUND2_PRODUCT_SPEC.md`
Decisions D-001 through D-008 are approved and reflected in the frozen spec.

## T2 — Product Spec Red Team Review
Owner: ChatGPT acting in separate Red Team / QA role
Status: DONE
Output: `docs/REVIEW_LOG.md`
Review findings resolved through approved decisions D-005 to D-008 plus low-cost implementation clarifications.

## T3 — Resolve Review and Freeze Spec
Owner: ChatGPT
Status: DONE
Outputs: frozen `docs/ROUND2_PRODUCT_SPEC.md` and updated `docs/DECISION_LOG.md`.

## T4 — Implementation Plan
Owner: Codex
Status: READY — NEXT
Input: `AGENTS.md`, frozen `docs/ROUND2_PRODUCT_SPEC.md`, `docs/DECISION_LOG.md`, `docs/TASKS.md`.
Output: minimal implementation plan only; no product code yet.

Codex must state for each step:
- files to create/change;
- input and output;
- test/verification;
- dependency on earlier steps;
- estimated implementation risk.

Priority order:
1. end-to-end working flow;
2. deterministic business correctness;
3. demo reliability/fallback;
4. tests;
5. readability;
6. visual polish.

## T5 — MVP Build
Owner: Codex
Status: BLOCKED UNTIL T4 PLAN APPROVED
Required implementation order unless Team Lead approves a change:
1. project skeleton + requirements;
2. synthetic laptop catalogue;
3. intent decoder + controlled fallback;
4. product-level eligibility + semantic matcher;
5. bounded offer scenario generator;
6. offer-level buyer/merchant feasibility + economics;
7. offer scoring/selection;
8. machine-readable B2A offer response;
9. buyer acceptance + synthetic transaction handoff;
10. Streamlit end-to-end UI;
11. core tests and failure cases.

Expected files: `app.py`, `data/catalog.csv`, `tests/test_core.py`, `requirements.txt`, optional `src/intent.py`, `src/matcher.py`, `src/optimizer.py`.

## T6 — Code and Logic Review
Owner: ChatGPT Red Team / QA
Status: TODO
Input: frozen spec + completed repository code/tests.
Output: update `docs/REVIEW_LOG.md` with new P0/P1/P2 findings focused on crashes, logic errors, edge cases, misleading outputs and spec mismatches.

## T7 — Fix Approved Issues
Owners: ChatGPT then Codex
Status: TODO
ChatGPT selects grounded P0/P1 fixes. Codex changes only approved items and reruns relevant tests.

## T8 — Submission Documentation
Owners: Codex draft, ChatGPT final review
Status: TODO
Outputs: `README.md`, `docs/SUBMISSION_CHECKLIST.md`, `pitch/PITCH_CONTENT.md`.

README must include architecture, technology/API list, setup/run instructions, demo-data disclosure, limitations, external resources and secrets instructions.

## T9 — Final Verification
Owner: User
Status: TODO
Run the app from a fresh start, verify the primary demo and at least one failure scenario, confirm repository completeness and submit through the official channel.
