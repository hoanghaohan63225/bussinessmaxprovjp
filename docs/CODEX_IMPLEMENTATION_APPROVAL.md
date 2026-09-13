# Codex Implementation Plan Approval

Status: APPROVED
Decision: D-010
Approved plan: `docs/CODEX_IMPLEMENTATION_PLAN.md`

The Codex T4 implementation plan is approved for T5 execution with these binding execution rules:

1. Controlled mapping/fallback must work end-to-end before optional Gemini API integration is allowed to become a dependency.
2. Codex may execute T5.1 through T5.11 sequentially without requesting approval between every subtask. Stop and return to the Team Lead only for a P0 blocker, a conflict with frozen Product Spec/Decisions, or a required scope change.
3. Deterministic pytest business-logic coverage and manual Streamlit end-to-end smoke tests are mandatory. Automated Streamlit UI tests are optional if fast and stable. Working demo and correctness take priority over UI-test sophistication or decorative polish.

The demo configuration proposed in the plan is approved under D-010: discount rates 0/3/5%, synthetic minimum margin rate 10%, balanced alpha/beta 0.5/0.5, documented preference defaults, safe equal-value normalisation at 0.5, deterministic tie-breaks, and Decimal-based AUD arithmetic.

This approval note overrides the older `PROPOSED` status line inside the original T4 plan if that line remains visible. Governance authority is `docs/DECISION_LOG.md`.