# CRESO executed research — c001

Phases **01 and 02 passed** on 1 October 2026. These are literature, formal and
controlled numerical/statistical studies. No language-model or TPU training runs
have executed. Phases 03–09 are not started and are for the user to run personally.

## Evidence

- [Theory](../../theory.md), [formal claim map](../../formal/README.md), 47 audited theorems.
- [Results and failures](results.md), 49,152 final contexts, 12 laws, 15 numerical tests.
- [Primary literature](literature.md), [54 eligible peers](competitors.json), Muon mandatory.
- [Frozen protocol](protocol.md), [machine protocol](protocol.json), [development selection](run-v1/selection.json).
- [Raw replay and bootstrap](reproduction-checks.json), [assumption attacks and CPU profiles](diagnostics.json).
- [Assumptions](assumptions.md), [cost](complexity.md), [failure ledger](failures.jsonl).
- [Phase 01 handoff](phase01-handoff.md), [Phase 02 handoff](phase02-handoff.md).

Primary local comparisons beat ideal Muon, feasible float64 NS5 and hard spectral
projection in three active orthogonal-noise shapes. TONGA ties and adverse-law
losses remain. Novelty is a bounded inference about the complete composition;
generic filtering, calibration and aggregation are prior mechanisms. A breakthrough
and all-peer training superiority remain unestablished.

## Reproduce

Create a Python environment and install `requirements.txt`. Run the commands in
`commands.txt`. Independent development and final draws use fixed seeds 20261021
and 20261022; seeds 42–44 are reserved. The manifest records the pre-final numerical
source revision and hashes. Every peer may average the complete method data.

Lossless raw NPZ replicas, directions and assessments are excluded from Git
and retained locally. There is no public raw-data download. `raw-storage.json`
records local archive paths and SHA-256 checksums. With access to those archives,
verify the checksums and extract the three tar files at the repository root.
Then run `analyze.py`; it verifies all 192 final files, replays every tuned method
and checks independent readouts. The supplemental `source-muon-raw.npz` is also
retained locally. A fresh source checkout alone cannot replay the raw study.

Source primary documents are cached outside Git with hashes in source-manifest.json.
Complete optimizer ports, numerical certification and TPU comparisons remain open.
