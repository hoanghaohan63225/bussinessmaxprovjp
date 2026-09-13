# Task Board

## T0 — Governance
Owner: ChatGPT
Status: DONE
Outputs: `AGENTS.md`, `docs/DECISION_LOG.md`, `docs/TASKS.md`

## T1 — Round 2 Product Spec
Owner: ChatGPT
Status: REVIEW
Output: `docs/ROUND2_PRODUCT_SPEC.md`
Must define: product, target users, demo flow, input/output schemas, semantic matching, merchant optimisation, architecture, MVP scope, out-of-scope, acceptance criteria.

Current note: first draft is complete and ready for Gemini Red Team review.

## T2 — Product Spec Review
Owner: Gemini
Status: TODO
Output: `docs/REVIEW_LOG.md`
Classify findings as P0/P1/P2. Do not implement code or redesign the whole product unless a fatal P0 is found.

## T3 — Resolve Review and Freeze Spec
Owner: ChatGPT
Status: TODO
Output: final `docs/ROUND2_PRODUCT_SPEC.md` and updated `docs/DECISION_LOG.md`.
Any core change requires user approval.

## T4 — Implementation Plan
Owner: Codex
Status: TODO
Input: `AGENTS.md`, frozen Product Spec, Decision Log, Task Board.
Output: minimal implementation plan before coding.

## T5 — MVP Build
Owner: Codex
Status: TODO
Order: project skeleton -> catalogue -> intent decoder -> semantic matcher -> offer optimiser -> B2A response -> Streamlit flow -> tests.
Expected files: `app.py`, `data/catalog.csv`, `tests/test_core.py`, `requirements.txt`, optional `src/**`.

## T6 — Code and Logic Review
Owner: Gemini
Status: TODO
Output: update `docs/REVIEW_LOG.md` with P0/P1/P2 findings focused on crashes, logic errors, edge cases, misleading outputs and spec mismatches.

## T7 — Fix Approved Issues
Owners: ChatGPT then Codex
Status: TODO
ChatGPT selects grounded P0/P1 fixes. Codex changes only approved items and reruns relevant tests.

## T8 — Submission Documentation
Owners: Codex draft, ChatGPT final review
Status: TODO
Outputs: `README.md`, `docs/SUBMISSION_CHECKLIST.md`, `pitch/PITCH_CONTENT.md`.

## T9 — Final Verification
Owner: User
Status: TODO
Run the app from a fresh start, verify the demo scenario and confirm the repository contains all required outputs before submission.
