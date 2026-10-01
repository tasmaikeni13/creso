# CRESO

**Certified Replica Spectral Optimization** is an experimental matrix optimizer
that uses replica noise to propose directions and fresh data to certify and select
feasible spectral updates. Its finite decision needs ten scalar quadratic solves.

Phases **01 and 02** provide literature research, Lean proofs and controlled
numerical/statistical analysis. No language-model or TPU training has run.
The method has breakthrough potential as a research question; extreme novelty
and a breakthrough are **not established** by the current evidence.

## Start here

- [Theory and assumptions](theory.md)
- [Lean proofs and exact claim map](formal/README.md)
- [Executed study and reproduction](research/c001/README.md)
- [Results, ties and failures](research/c001/results.md)
- [Primary literature and novelty boundary](research/c001/literature.md)
- [Nine research phases](phases/README.md)
- [Working instructions](AGENTS.md)

The study uses 49,152 final matrix contexts across 12 laws. Prespecified local
contrasts include **Muon**, with ideal polar and finite NS5 distinguished.
Covariance shrinkage controls, adverse regimes and all statistical costs remain
visible. Local matrix results do not establish a training win against every peer.

## Verify the mathematics

```bash
git clone --recurse-submodules https://github.com/tasmaikeni13/creso.git
cd creso/formal
lake exe cache get
lake build
lake env lean Audit.lean
```

Lean and mathlib are pinned; every public theorem is audited. The executable
numerical reference is float64 CPU code. It is not a source-parity bf16 Muon or
an implemented JAX/Pallas training optimizer.

## Future confirmation contract

One identical **125M model**, **2.5B FineWeb-Edu training tokens per optimizer
per seed**, seeds **42, 43, 44**, on **TPU v4-32 (16 chips)**. These seeds have
not selected the method. The 54-variant peer inventory includes Muon, MONA and
MARS-M; complete ports and matched tuning are required before confirmation.
Report quality, time, memory and reliability separately. Phases 03–09 await
start instructions.

## Layout

```text
theory.md          Mathematical decision and confidence contract
formal/            Standalone Lean geometry, optimization and statistics
research/c001/     Literature, frozen study, raw manifests and handoffs
phases/            Nine execution instructions and live state
skills/            Pinned research skills submodule
AGENTS.md          Concrete repository rules
```
