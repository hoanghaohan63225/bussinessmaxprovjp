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
Status: EXACT LOCAL TESTS PASS / STREAMLIT INTERACTIVE SMOKE PENDING
Evidence: `docs/EMERGENCY_BUILD_REPORT.md`, `docs/RUNTIME_VERIFICATION.md`

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

Fresh user-machine verification on the downloaded repository:
- Python 3.14.5 detected;
- dependencies installed successfully with `py -m pip install -r requirements.txt`;
- exact committed suite: `py -m pytest -q` -> **14 passed in 10.51s**;
- `py -m streamlit run app.py` started Streamlit and reached the first-run onboarding prompt.

Before marking T5 DONE, complete the interactive Streamlit checks:
1. leave Streamlit onboarding email blank and press Enter;
2. open the Local URL / browser page;
3. verify primary success flow reaches `transaction_ready`;
4. verify one impossible/failure request returns an explicit no-feasible state;
5. change the request after acceptance and confirm stale transaction state is cleared;
6. verify controlled mapping/fallback works without an API key.

## T6 — Code and Logic Review
Owner: ChatGPT Red Team / QA
Status: STATIC PASS 1 DONE / EXACT PYTEST PASS / INTERACTIVE CLOSURE PENDING
Output: `docs/REVIEW_LOG.md`

Static review fixes already applied:
- unsupported LLM hard requirements fail closed as unresolved;
- neutral defaults for missing LLM preference dimensions are explicitly recorded as assumptions;
- non-finite numeric intent values are rejected;
- reruns clear stale pipeline/transaction state before execution;
- optional API key can come from environment variables or Streamlit secrets;
- regression tests cover the new safety behaviour and explicit no-feasible state;
- emergency build verification evidence was corrected.

T6 closes after the interactive Streamlit smoke-test results are observed.

## T7 — Fix Approved Issues
Owner: ChatGPT implementation pass after QA findings
Status: STATIC FIXES APPLIED / RUNTIME FIXES IF NEEDED
Current static P0/P1 fixes restore compliance with frozen scope and do not add features. Any runtime-discovered P0/P1 will be fixed next and retested.

## T8 — Submission Documentation
Owner: ChatGPT
Status: IN PROGRESS
Existing outputs:
- `README.md`
- `docs/SUBMISSION_CHECKLIST.md`
- `pitch/PITCH_CONTENT.md`

Final docs must cover architecture, technologies/APIs, setup/run instructions, synthetic-data disclosure, limitations, deployment/scalability, market strategy, adaptation to FPT full brief and secrets handling.

## T9 — Final Verification
Owner: User + ChatGPT checklist support
Status: TODO
Run the app from a fresh start, verify the primary demo and at least one failure scenario, confirm repository completeness/secrets safety and submit through the official channel.
