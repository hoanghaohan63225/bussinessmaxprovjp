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
Status: INTERACTIVE RUNTIME PASS / FINAL LATEST-BUILD PYTEST PENDING
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

Runtime evidence already confirmed on the user machine:
- Python 3.14.5;
- dependencies installed successfully;
- Streamlit launches at `localhost:8501` without an API key;
- latest-build default gaming flow returns a feasible B2A offer;
- explicit buyer acceptance returns synthetic `transaction_ready`;
- latest-build catalogue matching excludes `CreatorPro 15` from a hard gaming request after the gaming-capability fix;
- impossible request returns explicit `no_feasible_offer` without crashing;
- changing request after an accepted transaction clears stale accepted state.

One closure action remains:
- run `py -m pytest -q` on the latest downloaded ZIP after the gaming-capability regression fix.

## T6 — Code and Logic Review
Owner: ChatGPT Red Team / QA
Status: STATIC + INTERACTIVE PASS / FINAL LATEST-BUILD PYTEST PENDING
Output: `docs/REVIEW_LOG.md`

Review/fixes already applied:
- unsupported LLM hard requirements fail closed as unresolved;
- neutral defaults for missing LLM preference dimensions are recorded as assumptions;
- non-finite numeric intent values are rejected;
- reruns clear stale pipeline/transaction state;
- optional API key can come from environment variables or Streamlit secrets;
- hard gaming capability now requires explicit `gaming` or `gpu` catalogue evidence;
- regression tests cover safety behaviour and explicit no-feasible state;
- runtime screenshots confirm success, transaction, failure and stale-state flows.

T6 closes after the latest-build pytest command passes once locally.

## T7 — Fix Approved Issues
Owner: ChatGPT implementation pass after QA findings
Status: DONE FOR CURRENT P0/P1 FINDINGS
All currently identified P0/P1 implementation findings have been fixed without expanding frozen product scope. Re-open only if the final latest-build pytest or submission rehearsal exposes a new blocking issue.

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
Run the final latest-build pytest, rehearse the primary demo once, confirm repository completeness/secrets safety and submit through the official channel.