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
Approved by D-010.

## T5 — MVP Build
Owner: ChatGPT Team Lead temporary emergency takeover after Codex quota/network interruption
Status: CORE CODE COMMITTED — USER-MACHINE STREAMLIT SMOKE TEST REQUIRED
Evidence: `docs/EMERGENCY_BUILD_REPORT.md`

Committed implementation:
- `app.py`
- `requirements.txt`
- `.gitignore`
- `data/catalog.csv`
- `src/intent.py`
- `src/matcher.py`
- `src/optimizer.py`
- `tests/test_core.py`
- `README.md`

Core verification in Team Lead working environment:
- equivalent core suite: `python -m pytest -q` -> 28 passed;
- `python -m py_compile app.py src/intent.py src/matcher.py src/optimizer.py` -> passed;
- real Streamlit launch not run because the Team Lead environment cannot download missing packages due outbound network restrictions.

Before marking T5 DONE, run on the user's machine:
1. `pip install -r requirements.txt`
2. `python -m pytest -q`
3. `python -m streamlit run app.py`
4. verify primary success flow reaches `transaction_ready`;
5. verify one impossible/failure request returns an explicit no-feasible state.

## T6 — Code and Logic Review
Owner: ChatGPT Red Team / QA
Status: READY AFTER USER-MACHINE SMOKE TEST
Input: frozen spec + committed code/tests + `docs/EMERGENCY_BUILD_REPORT.md`.
Output: update `docs/REVIEW_LOG.md` with P0/P1/P2 findings focused on crashes, logic errors, edge cases, misleading outputs and spec mismatches.

## T7 — Fix Approved Issues
Owners: ChatGPT then implementation agent
Status: TODO
ChatGPT selects grounded P0/P1 fixes. Only approved items are changed and relevant tests are rerun.

## T8 — Submission Documentation
Owners: ChatGPT final review
Status: IN PROGRESS
`README.md` already exists. Remaining outputs: `docs/SUBMISSION_CHECKLIST.md`, `pitch/PITCH_CONTENT.md`.

## T9 — Final Verification
Owner: User
Status: TODO
Run the app from a fresh start, verify the primary demo and at least one failure scenario, confirm repository completeness and submit through the official channel.
