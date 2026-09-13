# Task Board

## T0 — Governance
Owner: ChatGPT
Status: DONE
Outputs: `AGENTS.md`, `docs/DECISION_LOG.md`, `docs/TASKS.md`

## T1 — Round 2 Product Spec
Owner: ChatGPT
Status: DONE / FROZEN
Output: `docs/ROUND2_PRODUCT_SPEC.md`
Decisions D-001 through D-010 are approved and frozen.

## T2 — Product Spec Red Team Review
Owner: ChatGPT acting in separate Red Team / QA role
Status: DONE
Output: `docs/REVIEW_LOG.md`
Review findings resolved through approved decisions D-005 to D-008 plus low-cost implementation clarifications.

## T3 — Resolve Review and Freeze Spec
Owner: ChatGPT
Status: DONE
Outputs: frozen `docs/ROUND2_PRODUCT_SPEC.md`, updated `docs/DECISION_LOG.md`, and `docs/ROUND2_REQUIREMENTS_TRACE.md`.

## T4 — Implementation Plan
Owner: Codex
Status: DONE / APPROVED
Output: `docs/CODEX_IMPLEMENTATION_PLAN.md`
Approved by D-010 with three execution rules:
1. controlled mapping/fallback must work end-to-end before optional Gemini API can become a dependency;
2. Codex may proceed through T5.1–T5.11 without per-step approval, but must stop on a P0 blocker, frozen-spec conflict, or required scope change;
3. deterministic pytest coverage and manual Streamlit smoke tests are mandatory; automated UI tests are optional if fast/stable.

## T5 — MVP Build
Owner: Codex
Status: READY — NEXT
Execution prompt: `docs/PROMPT_CODEX_BUILD.md`
Implementation authority: `docs/CODEX_IMPLEMENTATION_PLAN.md` + frozen Product Spec + Decisions D-001 through D-010.

Required implementation order:
1. T5.1 project skeleton + requirements + `.gitignore`;
2. T5.2 synthetic laptop catalogue + validation;
3. T5.3 intent decoder + controlled mapping/fallback;
4. T5.4 product-level eligibility + semantic matcher;
5. T5.5 bounded offer scenario generator;
6. T5.6 offer-level buyer/merchant feasibility + economics;
7. T5.7 offer scoring/selection;
8. T5.8 machine-readable B2A offer response;
9. T5.9 buyer acceptance + synthetic transaction handoff;
10. T5.10 Streamlit end-to-end UI;
11. T5.11 core tests + failure handling + final smoke test.

Expected implementation files:
- `app.py`
- `requirements.txt`
- `.gitignore`
- `data/catalog.csv`
- `src/intent.py`
- `src/matcher.py`
- `src/optimizer.py`
- `tests/test_core.py`

T5 completion evidence Codex must commit/report:
- actual test command(s) and results;
- manual fresh-start Streamlit smoke-test result;
- primary success-flow result through `transaction_ready`;
- at least one failure/no-feasible scenario;
- list of changed files;
- any known limitations;
- explicit confirmation that no secret/API credential is tracked.

## T6 — Code and Logic Review
Owner: ChatGPT Red Team / QA
Status: BLOCKED UNTIL T5 COMPLETE
Input: frozen spec + completed repository code/tests + Codex build report.
Output: update `docs/REVIEW_LOG.md` with P0/P1/P2 findings focused on crashes, logic errors, edge cases, misleading outputs and spec mismatches.

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