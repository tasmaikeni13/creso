# Phase 09 — Paper and repository release

**State: not started.** Requires the completed, audited record from Phases 01–08.
A publication-quality account can report a negative result; performance claims
must match Phase 08's evidence.

## Work

1. Expand `theory.md` into a journal-level paper with abstract, problem statement,
   related work, precise contribution, method, assumptions, proofs, numerical
   analysis, experimental protocol, complete results, limitations and conclusion.
   Cite mathematical antecedents and the strongest relevant optimizers. Clearly
   separate the original proposal from the final validated revision.
2. Include exact hardware, model parameter count, dataset/tokenizer hashes,
   tuning budgets, all three seeds, failure outcomes, effect sizes, uncertainty,
   compute costs and practical limits. Do not claim universal superiority.
3. Make every figure/table reproducible from archived data. Link theorem numbers
   to Lean declarations. Run the kernel proof and axiom audit again. Ensure any
   theorem used for approximate kernels was actually proved under its stated
   assumptions and matches the implementation.
4. Organize source, references, configs, tests, scripts and documentation. Add
   concise comments explaining non-obvious mathematics, layouts and collectives.
   Apply PEP8, an explicitly pinned formatter and linting to Python. Remove dead
   code and transient files while preserving rejected methods and raw evidence
   in the research archive.
5. Rewrite the README for people: motivation, honest results, install/setup,
   minimal examples, reproduction commands, cost expectations and limitations.
   Check it against a fresh checkout with submodules. Include dependency and
   upstream-license attribution, dataset terms and a suitable project license.
6. Verify links and artifact hashes, run relevant tests, review the final diff,
   tag the audited revision, and push the release artifacts to the user's GitHub
   within the publication task's authorized scope. Never commit credentials,
   large training data or private logs.

## Final gate

The paper, repository, Lean statements, implementation, configs and raw evidence
describe the same method and experiment. No placeholders, fabricated results,
unsupported novelty claims, missing eligible competitors or stale dependencies
are hidden by prose. Provide the release commit, reproduction commands and
remaining limitations. If the original “match every peer” objective remains
unmet, say so explicitly in the paper and handoff.
