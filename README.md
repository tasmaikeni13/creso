# RASP

**Replica-Aware Spectral Proximal optimization** is an experimental matrix
optimizer proposal. It uses disagreement between two halves of a gradient batch
to penalize unreliable update directions while enforcing a spectral-norm bound.

This repository contains a short theory, machine-checked exact mathematics,
and a research plan. It does not yet contain a training implementation or
benchmark results.

## Start here

- [Theory](theory.md): update rule, assumptions, guarantees and limits.
- [Lean proofs and claim map](formal/README.md): what has been checked.
- [Nine research phases](phases/README.md): execution gates and revision rules.
- [Research record](phases/research-record.md): literature, mechanism transfer,
  alternatives and novelty boundaries.
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

All nine phases are **not started**. The initial literature review and Lean
proofs are preparation for them. To begin, ask the agent to execute a phase, for
example: “Execute Phase 01.” The agent repairs failed work and its dependents
within the requested scope, retaining failures and updating the theory. Training
does not start until its phase is requested.

The research goal is to match or exceed every eligible peer under a declared
protocol. A negative or inconclusive result remains a valid result; changing
the model, optimizer or protocol creates a new research revision.

## Layout

```text
theory.md           Short mathematical proposal
formal/             Lean source, pinned dependencies and audit
phases/             Nine phase instructions and preparation record
skills/             Pinned research skills submodule
AGENTS.md           Repository working instructions
```

Preparation date: 2026-09-25. See the research record for primary sources and
which source claims have not been independently reproduced.
