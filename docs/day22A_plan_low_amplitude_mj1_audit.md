# Day22A Plan — Low-amplitude MJ1 full-protocol audit

## Objective

Apply the Day21A audit pipeline to a low-amplitude control group, prioritizing the 0.3C+0.4C DC–AC protocols.

The purpose is to test whether the boundary/control-state mediated first-passage gain observed in the 0.3C+0.7C group weakens or disappears when AC amplitude is reduced.

## Candidate group

- DC reference: 0.3C DC
- DC–AC protocols: 0.3C+0.4C at available frequency labels

## Reuse from Day21A

The following Day21A components should be reused without changing the audit contract unless explicitly justified:

- strict-net signed Q integration
- first-passage time definition
- nominal and common Q80/Q90 anchors
- Segment A/B/D segmentation
- Segment-A residual restricted to the shared prescribed-current region
- fitted-waveform diagnostic as explanatory, not threshold-redefining
- formal verdict separated from diagnostic interpretation

## Critical checks before execution

1. Confirm raw NGU201 files exist and are not tracked in Git.
2. Confirm matching DC reference.
3. Confirm protocol metadata: DC_C, AC_C, m_tau, frequency_Hz.
4. Confirm temperature summaries are available or explicitly marked as NaN.
5. Confirm the same 1C convention: 3.4 A.
6. Confirm phase convention remains charge-first.

## Expected scientific value

If Q80/Q90 anchors no longer fall in Segment B or the raw gains shrink substantially, the result supports the amplitude-boundary interpretation.

If boundary/control-state gain persists despite lower AC amplitude, the result requires reassessing the role of voltage-boundary timing versus current modulation amplitude.

## Non-goals

- Do not search for new mechanisms.
- Do not redefine Segment-A residual thresholds.
- Do not treat fitted-waveform residual as a formal replacement for the prescribed-geometry residual.
- Do not expand to all MJ1 groups at once.

