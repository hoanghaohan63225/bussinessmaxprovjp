# Runtime Verification

Owner: User machine + ChatGPT Team Lead
Status: INTERACTIVE SMOKE PASS — latest-build success/failure/transaction flows confirmed; one final latest-build pytest run still required for full closure.

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

## Earlier exact downloaded-build test suite

Command:

```powershell
py -m pytest -q
```

Observed result on the user machine before the latest gaming-capability regression fix:

```text
.............. [100%]
14 passed in 10.51s
```

This remains valid evidence for that earlier downloaded state only. The current GitHub repository contains an additional gaming-capability regression test, so one fresh pytest run on the latest ZIP is still required before final closure.

## Streamlit launch

Command:

```powershell
py -m streamlit run app.py
```

Result: PASS. Browser app loaded successfully at `localhost:8501` with no API key required.

## Latest-build success-flow smoke test

Observed on the user's newly downloaded latest build:

- execution mode displayed `Controlled mapping`;
- default gaming request ran without an API key;
- catalogue matching now contains only explicit gaming-capable products:
  - `LAP-001 NovaForge G15`
  - `LAP-006 TitanEdge 16`
  - `LAP-004 ValueStrike 15`
- `CreatorPro 15` is no longer treated as eligible for the hard gaming requirement;
- the merchant pipeline still produced a feasible recommended offer;
- explicit buyer acceptance produced `transaction_ready`;
- transaction payload contained a synthetic `order_intent`, AUD buyer total and `payment_status = not_processed_demo`.

Result: LATEST-BUILD SUCCESS FLOW PASS.

## Latest-build failure / stale-state smoke test

The user changed the buyer request after the successful accepted transaction to an impossible request:

`I need a gaming laptop under AUD 500, delivery within 1 day, and at least 3 years of warranty.`

Observed result:

- decoded intent reflected budget 500, delivery 1 day, warranty 3 years and hard gaming requirement;
- pipeline did not crash;
- no product passed immutable product-level constraints;
- machine-readable response returned `status = no_feasible_offer` with an explicit reason;
- the prior accepted transaction was no longer presented as the current result, demonstrating stale accepted state was cleared when the request changed.

Result: LATEST-BUILD FAILURE / STALE-STATE FLOW PASS.

## Runtime-discovered logic issue and fix

The earlier success-flow screenshots exposed that `CreatorPro 15` was listed as eligible for a hard gaming request because the old product-level rule treated a generic `performance` tag as sufficient gaming-capability evidence.

Fix applied on GitHub:
- a hard `gaming` requirement requires an explicit `gaming` or `gpu` catalogue tag;
- generic `performance` may influence soft semantic fit but cannot satisfy the immutable gaming capability requirement;
- regression test added to ensure `CreatorPro 15` is rejected for the hard gaming request.

The latest-build screenshots confirm this fix works interactively.

## Remaining final runtime gate

Run once on the latest downloaded ZIP:

```powershell
py -m pytest -q
```

If the latest suite passes, T5/T6 runtime closure can be marked DONE. No additional feature work is required before documentation/submission preparation.