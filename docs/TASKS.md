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
Original P0/P1 design findings were resolved through D-005 to D-008 plus frozen implementation clarifications.

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
Owner: ChatGPT temporary implementation takeover after Codex quota/network interruption
Status: CORE CODE COMMITTED / FRESH LOCAL RUNTIME GATE PENDING
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

The earlier emergency working-copy `28 passed` result is not treated as proof for the current committed suite. A fresh run of the exact repository is required.

Before marking T5 DONE, run on the user's machine:
1. `pip install -r requirements.txt`
2. `python -m pytest -q`
3. `python -m streamlit run app.py`
4. verify primary success flow reaches `transaction_ready`;
5. verify one impossible/failure request returns an explicit no-feasible state;
6. change the request after acceptance and confirm stale transaction state is cleared.

## T6 — Code and Logic Review
Owner: ChatGPT Red Team / QA
Status: STATIC PASS 1 DONE / RUNTIME CLOSURE PENDING
Output: `docs/REVIEW_LOG.md`

Static review fixes already applied:
- unsupported LLM hard requirements fail closed as unresolved;
- neutral defaults for missing LLM preference dimensions are explicitly recorded as assumptions;
- non-finite numeric intent values are rejected;
- reruns clear stale pipeline/transaction state before execution;
- optional API key can come from environment variables or Streamlit secrets;
- regression tests cover the new safety behaviour and explicit no-feasible state;
- emergency build verification evidence was corrected.

T6 closes only after fresh local pytest and Streamlit smoke-test results are observed.

## T7 — Fix Approved Issues
Owner: ChatGPT implementation pass after QA findings
Status: STATIC FIXES APPLIED / RUNTIME FIXES IF NEEDED
Current static P0/P1 fixes restore compliance with frozen scope and do not add features. Any runtime-discovered P0/P1 will be fixed next and retested.

## T8 — Submission Documentation
Owner: ChatGPT
Status: IN PROGRESS
`README.md` exists. Remaining required outputs:
- `docs/SUBMISSION_CHECKLIST.md`
- `pitch/PITCH_CONTENT.md`

Final docs must cover architecture, technologies/APIs, setup/run instructions, synthetic-data disclosure, limitations, deployment/scalability, market strategy, adaptation to FPT full brief and secrets handling.

## T9 — Final Verification
Owner: User + ChatGPT checklist support
Status: TODO
Run the app from a fresh start, verify the primary demo and at least one failure scenario, confirm repository completeness/secrets safety and submit through the official channel.
