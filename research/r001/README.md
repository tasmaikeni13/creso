# Executed revision r001

Phases **01 and 02 passed** on 2026-10-01. Later phases have not started.

- [Findings and negative evidence](results.md)
- [Phase 01 handoff](phase01-handoff.md)
- [Phase 02 handoff](phase02-handoff.md)
- [Frozen competitor definitions](peer-updates.md) and [registry](competitors.json)
- [Claims](evidence.md), [assumptions](assumptions.md), [failures](failures.md)
- [Protocol](phase02/protocol.md), [environment](environment.json),
  [raw evidence audit](raw-audit.json)

## Reproduce

From the repository root, Python 3.10:

```bash
git submodule update --init --recursive
python3 -m venv .venv
.venv/bin/pip install -r research/r001/requirements.txt
.venv/bin/ruff check research/r001
.venv/bin/ruff format --check research/r001
.venv/bin/pytest -q research/r001
```

Formatter/linter: Ruff 0.16.9. Numerical tests: pytest 9.1.1. Lean commands:

```bash
cd formal
lake exe cache get
lake build
lake env lean Audit.lean
```

From the repository root, restore source snapshots without altering manifests:

```bash
.venv/bin/python research/r001/fetch_sources.py --restore
```

Raw simulation data are excluded from Git. On a fresh clone, the frozen study
regenerates the raw files next to the saved summaries; it writes new development
outputs separately. These commands refuse to overwrite an existing `reproduction`
run. The evaluation source commit and timestamp will differ; numeric raw hashes
should match in the recorded numerical environment.

An independent complete replay reproduced all 108 development selections, all
12 raw NPZ hashes and all final statistics exactly; see `reproduction-checks.json`.

The original archive is attached to [draft release `r001-phase01-02`](https://github.com/tasmaikeni13/rasp/releases/tag/untagged-0d2cee371caba99ed583); the
owner can download it with authenticated GitHub CLI. Verify its SHA256 against
`raw-storage.json` before extracting at the repository root:

```bash
gh release download r001-phase01-02 --repo tasmaikeni13/rasp --pattern r001-raw-evidence.tar --dir .source-cache
sha256sum .source-cache/r001-raw-evidence.tar
tar -xf .source-cache/r001-raw-evidence.tar
```

```bash
.venv/bin/python research/r001/phase02/study.py develop --output research/r001/phase02/reproduction
```

Compare `reproduction/selection.json` with `run-v1/selection.json` before
evaluating. Neither uses confirmation seeds. Then:

```bash
.venv/bin/python research/r001/phase02/study.py evaluate --output research/r001/phase02/reproduction
```

The originally executed development/final command logs and manifests are
preserved under `phase02/`. `diagnostics.py` and `solver_attack.py` deliberately
refuse to overwrite their evidence files; tests rerun their independent checks.
`analyze_phase02.py` verifies the original local raw files and reproduces the
standalone PNG/SVG and CSV; on a clone point it at the reproduced raw directory.

No training commands or TPU benchmarks exist yet.
