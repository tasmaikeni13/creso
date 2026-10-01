# RASP

**Replica-Aware Spectral Proximal optimization** is an experimental matrix
optimizer proposal. It uses disagreement between two halves of a gradient batch
to penalize unreliable update directions while enforcing a spectral-norm bound.

This repository contains a short theory, machine-checked mathematics and
executed controlled simulations. Phases **01 and 02 passed on 2026-10-01**.
Training implementations and language-model/TPU benchmarks remain future work.

## Start here

- [Theory](theory.md): update rule, assumptions, guarantees and limits.
- [Lean proofs and claim map](formal/README.md): what has been checked.
- [Nine research phases](phases/README.md): execution gates and revision rules.
- [Research record](phases/research-record.md): literature, mechanism transfer,
  alternatives and novelty boundaries.
- [Executed results and reproduction](research/r001/README.md): 12 noise laws,
  frozen protocol, independent evaluators, raw manifests and negative evidence.
- [Agent instructions](AGENTS.md): how to work in this repository.

The proposed update is more specific than ordinary variance scaling followed by
clipping. Whether that difference helps language-model training is unknown.
Several ingredients already occur in prior work, and the scalar solver is an
instance of established proximal calculus. We make no claim of absolute novelty
or superiority to existing optimizers.

## Verify the mathematics

Install [elan](https://github.com/leanprover/elan), then:

```bash
git clone --recurse-submodules https://github.com/tasmaikeni13/rasp.git
cd rasp/formal
lake exe cache get
lake build
lake env lean Audit.lean
```

The toolchain and dependency revisions are pinned. The first command in the
formal directory downloads mathlib build artifacts. The proofs use ordinary
Lean kernel checking, with no admitted proofs or project-specific axioms.
The formal step is a mathematical specification, not executable optimizer code.

## Planned experiment

The confirmation target is a **125M-parameter language model**, trained on
**2,500,000,000 FineWeb-Edu tokens per optimizer per seed**, with seeds
**42, 43 and 44**, on a **Google Cloud TPU v4-32 slice: 16 v4 chips**.
That is 7.5B training tokens per optimizer across the three seeds. Model count,
data hashes, tuning budgets and the complete competitor registry are frozen
before confirmation. Quality, elapsed time and memory are reported separately.

Phases **01–02 passed**; phases **03–09 are not started**. The initial September
review and proofs remain preparation records. The October execution adds 52
registered peer variants, 64 audited Lean theorems, 30 numerical tests and 98,304
final quadratic contexts. The intended law supports benefit beyond scalar damping;
adaptive bias, dependent-replica harm and expensive active solves are retained.
Later work starts only when requested.

The research goal is to match or exceed every eligible peer under a declared
protocol. A negative or inconclusive result remains a valid result; changing
the model, optimizer or protocol creates a new research revision.

## Layout

```text
theory.md           Short mathematical proposal
formal/             Lean source, pinned dependencies and audit
phases/             Nine phase instructions and preparation record
research/r001/      Executed frontier, simulations, evidence and handoffs
skills/             Pinned research skills submodule
AGENTS.md           Repository working instructions
```

Preparation date: 2026-09-25. See the research record for primary sources and
which source claims have not been independently reproduced.
