# Round 2 Submission Status

Status: **CORE MVP VERIFIED / FINAL PACKAGING REMAINS**

## Verified product state

Latest user-machine verification:
- Python 3.14.5
- `py -m pytest -q` -> **15 passed in 0.48s**
- Streamlit launches at `http://localhost:8501`
- no external LLM API key required for reliable demo path
- success flow reaches `offer_available`
- hard gaming capability filtering works
- explicit acceptance reaches synthetic `transaction_ready`
- impossible request reaches explicit `no_feasible_offer`
- changing the request clears stale accepted transaction state

Detailed evidence: `docs/RUNTIME_VERIFICATION.md`.

## Submission-ready repository assets

Ready:
- source code (`app.py`, `src/`, `data/`, `tests/`)
- `requirements.txt`
- `README.md`
- frozen product spec and decision log
- requirements trace
- QA/review log
- runtime verification evidence
- Round 2 submission checklist
- English pitch content source in `pitch/PITCH_CONTENT.md`

Still required before final submission:
1. create/export the **final Pitch Deck file** from the approved pitch content;
2. visually confirm the GitHub `main` branch and README render correctly;
3. decide whether a public Streamlit URL is required/useful by the submission form, otherwise retain documented local live-demo instructions;
4. rehearse the 90-second primary demo once without code changes;
5. complete the official submission form before the deadline and save confirmation evidence.

## Frozen live demo path

1. Use `Controlled mapping`.
2. Keep the default gaming request.
3. Click **Run merchant pipeline**.
4. Show decoded intent and execution mode.
5. Show explicit gaming-capable catalogue candidates.
6. Show bounded scenarios and the selected feasible offer.
7. Show the machine-readable B2A JSON.
8. Click **Accept recommended offer**.
9. Show `transaction_ready` and explain that it is a synthetic integration handoff, not a real payment.

Backup failure request:

`I need a gaming laptop under AUD 500, delivery within 1 day, and at least 3 years of warranty.`

Expected result: explicit `no_feasible_offer`, no crash.

## No-more-feature rule

Do not add product features before submission unless a genuinely blocking defect is discovered. Remaining work is packaging, pitch, rehearsal and submission only.
