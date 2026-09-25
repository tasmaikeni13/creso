# Phase 04 — Data, model and comparison protocol

**State: not started.** Requires Phases 01–03. Freeze choices before confirmation.

## Work

1. Specify the **125M-parameter** decoder model: layer count, widths, heads,
   vocabulary, positional encoding, context, activations, normalization, tying
   and dropout. Report the exact trainable parameter count and explain the 125M
   convention; do not silently substitute a different model size. Use identical
   architecture, initialization, loss and parameter groups for all optimizers.
2. Pin the [FineWeb-Edu dataset](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu)
   revision, selected files and hashes, tokenizer/version, shuffle, packing and
   masking. Split by document before packing; check train/validation/test overlap.
   Reserve validation for tuning and a locked test set for confirmation analysis.
3. Define a training token as a nonpadding target token contributing to the loss.
   Each optimizer/seed consumes exactly **2,500,000,000** such tokens, using an
   identical final partial-batch mask if necessary. Log input tokens, loss tokens
   and duplicate documents separately. Reusing two halves of one batch must not
   double the counted data. Mask and normalize replica means correctly.
4. Fix global batch, sequence length, schedule expressed in tokens, evaluation
   frequency, loss aggregation, decay treatment, clipping and mixed precision.
   Any permitted method-specific setting must be recorded and tuned fairly.
5. Preregister quality and cost endpoints: held-out token-weighted NLL (nats/token),
   perplexity, elapsed time including collectives, steady-state tokens/s, peak
   memory, compile/setup cost and numerical failures. Define a common validation
   loss target for time-to-quality without using test outcomes.
6. Fix equal HPO opportunity, development seeds distinct from 42/43/44, practical
   noninferiority/superiority margins, multiplicity rules and uncertainty methods.
   Keep matched-token quality and matched-time efficiency as separate questions.

## Gates and outputs

- Hashable model/data/protocol manifests and deterministic replay are validated.
- All baselines receive the same information and declared tuning budget.
- The complete registry, ablations and token/compute budget are enumerated.
- The three-seed power limitation is acknowledged before observing results.

Changes to data, architecture, metrics, selection or margins invalidate the
confirmation protocol and downstream results; retain the earlier version.
