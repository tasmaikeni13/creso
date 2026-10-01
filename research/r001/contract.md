# Revision r001 research contract

Started 2026-10-01 at preparation commit `318c9ea`. Authorized work is Phase 01
and Phase 02; phases 03–09 remain unstarted. This revision retains the exact
split-gradient objective in `theory.md` unless a mathematical or novelty failure
requires an explicitly archived replacement revision.

## Objective and evidence

Investigate a distinct, useful matrix optimizer whose uncertainty observation
changes a spectrally feasible direction. The ultimate comparison objective is
the fixed 125M FineWeb-Edu / TPU v4-32 protocol in `phases/README.md`. These two
phases can establish exact mathematics, a dated operational novelty comparison,
and controlled statistical mechanism evidence. They cannot establish LLM
superiority, TPU efficiency, or absolute absence of prior art.

Evidence labels: definition, Lean proved, source reported, numerical verification,
measured simulation, hypothesis, and unresolved. Existing clipping, mean–variance
penalties and low-rank proximal solvers cannot be claimed as new primitives.
An equivalent instantiated split-gradient constrained quadratic kills the
algorithmic novelty claim and triggers a replacement search.

## Phase 01 work and stopping rule

Refresh primary papers and official code through 2026-10-01. Include the required
families and their strongest discrete variants, preserve snapshots and hashes,
write exact update facets and assumptions, audit all matrix boundary cases, and
extend the exact-projection stopping theorem to an approximate projection / VI
certificate. Pass only after the Lean build and full axiom audit pass, closest
work is read, and claims have precise domains or falsification tests.

## Phase 02 first discriminating checks

Verify independent constrained and VI evaluators against analytic positive and
negative matrix cases before selecting any method. Freeze distribution laws,
trial counts, development seeds, matched tuning budgets, effect thresholds and
stopping criteria before the final simulation. Use seeds other than 42–44.
Compare coupled disagreement against zero penalty, scalar damping, scrambled
disagreement and projection after an unconstrained solve. Use independent
evaluation noise to separate realized suppression from population risk and true
quadratic progress. Preserve unfavorable regimes and all failed runs.

Kill or redesign if reliable disagreement cannot help in its intended controlled
regime, adaptive bias reverses that regime, or projection work precludes a
credible implementation path. Passing mechanism simulations grants no training
or hardware performance claim.
