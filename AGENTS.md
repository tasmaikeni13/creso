# Working on CRESO

CRESO means Certified Replica Spectral Optimization. Read `theory.md` for the
active algorithm, `phases/README.md` for scope and gates, and
`research/c001/README.md` for executed evidence. The project is standalone.

## Scope and research decisions

- The authorized work is mechanism research, theory, Lean verification and
  Phases 01–02. Phases 03–09 await their start instruction. Do not call a plan
  an executed training study.
- Apply relevant repository skills under `skills/`: literature-frontier,
  mechanism-transfer, theory-research, ml-research and experimental-research.
  Load the references needed by the active task. Preserve the submodule pin
  and its independent history.
- Seek a contribution that survives strong alternatives and comparison with
  primary prior art. A new name, a familiar component or a toy win cannot
  establish extreme novelty or a breakthrough. Use exact, scoped claims.
- Separate definitions, proved claims, measured results and hypotheses. Search
  operationally equivalent updates; stop bounded literature checks once the
  closest sources and their differences are resolved.
- Fix ordinary reversible errors autonomously within the requested scope.
  Follow the dependency and failure process in `phases/README.md`.

## Method and evidence rules

- Freeze proposal directions before post-proposal data. Calibrate both projected
  and residual noise; never assume a learned subspace contains all future noise.
- Reusing calibration pair sums in validation requires the unconditional union
  argument in the theory. Reusing proposal data breaks the stated certificate.
- The current proof needs iid unbiased same-weight replicas, a justified fourth
  moment bound and an explicit loss upper model for descent. Do not transfer it
  to momentum, shared noise, drift, heavy tails or bf16 without new evidence.
- Preserve raw measurements, failed gates, exact configurations and source
  hashes. Freeze code and selections before final draws; changes require a new
  revision and fresh confirmation. Do not weaken a gate to get a positive result.
- Muon is mandatory: ideal polar, finite NS5 diagnostics and source-faithful bf16
  implementations must be distinguished. Include covariance/deflation controls,
  MONA, MARS-M and every eligible peer in the current 54-variant inventory.
  An omitted eligible peer prevents an all-peer claim.
- Give baselines the same data and tuning opportunity. Charge calibration,
  candidate construction, communication, memory and gradient work. Local
  initial-state maps do not establish complete optimizer trajectory superiority.

## Verification and implementation

From `formal/`: `lake build` and `lake env lean Audit.lean`.
On a fresh checkout: `git submodule update --init --recursive`, then
`cd formal` and `lake exe cache get`. Preserve Lean and mathlib pins.

- No `sorry`, `admit`, custom `axiom`, unsafe proof shortcuts or `native_decide`.
  Audit every public theorem and update the claim map.
- Prove feasibility and existence for the actual rectangular matrix operator
  ball. A scalar optimizer cannot replace a matrix geometry theorem. Identify
  numerical/SVD and continuous-probability claims that are not mechanized.
- Reference verification: `.venv/bin/python -m pytest -q research/c001/test_*.py`;
  lint/format: `.venv/bin/python -m ruff check research/c001` and
  `.venv/bin/python -m ruff format --check research/c001`.
- Python follows PEP8, meaningful numerical checks and focused comments. Keep
  credentials, caches, raw NPZ data and checkpoints out of Git. Large evidence
  belongs in durable storage with downloadable manifests and checksums.
- Planned hardware is TPU v4-32 (16 chips), with JAX/Pallas. CPU/CUDA times are
  not TPU times. No training launch command is implemented yet.

## Confirmation contract and done

Use the same 125M model and 2.5B FineWeb-Edu training tokens for each optimizer
and each seed. Reserve seeds 42, 43 and 44 for confirmation; none may select the
method. Match baseline fidelity and tuning budgets before freezing the protocol.

A phase is complete when its reproducible artifacts exist, stated gates pass,
claims and failure ledger agree, and a short handoff states remaining limits.
Report the exact state. A controlled mechanism result does not establish an
all-peer training result or a breakthrough.
