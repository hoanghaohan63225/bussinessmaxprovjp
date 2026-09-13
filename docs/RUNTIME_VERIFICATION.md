# Runtime Verification

Owner: User machine + ChatGPT Team Lead
Status: PARTIAL PASS — exact committed pytest suite passed on the downloaded build; success-flow Streamlit smoke passed. One logic issue exposed by screenshots was fixed on GitHub and requires a fresh local rerun before final closure.

## Environment

- OS: Windows
- Python: 3.14.5
- Repository: `hoanghaohan63225/bussinessmaxprovjp`

## Dependency installation

Command:

```powershell
py -m pip install -r requirements.txt
```

Result: PASS. Streamlit, Pandas, pytest, google-genai and transitive dependencies installed successfully.

## Exact downloaded-build test suite

Command:

```powershell
py -m pytest -q
```

Observed result on user machine before the latest gaming-capability regression fix:

```text
.............. [100%]
14 passed in 10.51s
```

This was valid evidence for that downloaded repository state. A fresh test run is required after the latest GitHub fix because the current repository now has an additional regression test.

## Streamlit launch

Command:

```powershell
py -m streamlit run app.py
```

Result: PASS. Browser app loaded successfully at `localhost:8501` with no API key required.

## Success-flow smoke test

Observed on user machine:

- execution mode displayed `controlled mapping`;
- default gaming request decoded to budget 1300, delivery 3 days, warranty 2 years, gaming hard requirement and performance-first preference;
- catalogue matching rendered successfully;
- bounded merchant optimisation generated multiple scenarios and returned a feasible offer;
- selected offer: `NovaForge G15`, offer price / buyer total AUD 1281.55, 2-year warranty;
- merchant contribution margin displayed 14.8%;
- B2A JSON returned `offer_available`;
- explicit buyer acceptance produced `transaction_ready` with synthetic `order_intent` and `payment_status = not_processed_demo`.

Result: SUCCESS FLOW PASS.

## Runtime-discovered logic issue and fix

The success-flow screenshots exposed that `CreatorPro 15` was still listed as eligible for a hard gaming request because the old product-level rule treated a generic `performance` tag as sufficient gaming capability evidence.

This is too permissive for a hard capability constraint.

Fix applied on GitHub:
- a hard `gaming` requirement now requires an explicit `gaming` or `gpu` catalogue tag;
- generic `performance` may still influence soft semantic fit but cannot satisfy the immutable gaming capability requirement;
- regression test added to ensure `CreatorPro 15` is rejected for the hard gaming request.

Because the user downloaded the ZIP before this fix, final runtime closure requires downloading the latest repository state and rerunning tests + smoke checks.

## Remaining interactive smoke checks on latest GitHub state

1. Fresh `py -m pytest -q` passes with the new regression test.
2. Default gaming success flow still returns `offer_available` and `transaction_ready`.
3. `CreatorPro 15` no longer appears as eligible for the hard gaming request.
4. An impossible request returns explicit `no_feasible_offer` without crashing.
5. Editing the request after acceptance clears the previous transaction.
6. Controlled mapping/fallback works with no API key.

T5/T6 close only after these latest-build checks are confirmed.