# Day20B — Full-protocol PyBaMM batch verdict

Status: batch audit closed

## Scope

This document summarizes the full CC+CV PyBaMM simulations for:

```text
Chen2020
OKane2022
ORegan2022
```

Protocol logic:

```text
DC reference:
  CC at -0.2C until Vmax
  CV at Vmax until |I| <= normalized cutoff

DCAC:
  charge-first DC+AC during CC
  AC off at Vmax
  pure DC-CV at Vmax until |I| <= normalized cutoff
```

The cutoff current is normalized:

```text
I_cutoff = (0.05 / 3.4) · Q_nom
```

## Full-protocol result

| param_set | evidence status | total Δt [min] | Q_to_Vmax shift [Ah] | Segment A median [min] | Segment B median [min] | Segment D median [min] |
|---|---|---:|---:|---:|---:|---:|
| Chen2020 | valid | 37.439 | 0.857446 | 21.103 | 29.202 | 37.665 |
| OKane2022 | valid | 31.820 | 0.806319 | 21.882 | 24.730 | 32.691 |
| ORegan2022 | valid_with_CV_current_transient_warning | 82.269 | 1.513654 | 23.969 | 58.673 | 82.406 |

## Anchor points

| param_set | Q80 common [min] | Q90 common [min] | Q80 nominal [min] | Q90 nominal [min] | Q80/Q90 in Segment B |
|---|---:|---:|---:|---:|---|
| Chen2020 | 18.139 | 35.179 | 22.134 | 37.562 | True |
| OKane2022 | 13.161 | 29.990 | 18.250 | 32.846 | True |
| ORegan2022 | 53.224 | 71.586 | 60.023 | 77.180 | True |

## Current C-rate audit

| param_set | CC charge peak [C] | CC discharge peak [C] | CC ok | CV charge peak [C] | CV transient warning |
|---|---:|---:|---|---:|---|
| Chen2020 | 0.700 | 0.300 | True | 0.675 | False |
| OKane2022 | 0.700 | 0.300 | True | 0.644 | False |
| ORegan2022 | 0.700 | 0.300 | True | 1.387 | True |

## Interpretation

All three full-protocol simulations show positive raw Δt(Q) and positive total full-protocol time gain.

For all three parameter sets, Q80/Q90 anchors lie in Segment B:

```text
DCAC is already voltage-limited / CV-controlled
DC remains in CC
```

Therefore, the batch supports a voltage-boundary / control-state split explanation. It does not support a claim of non-geometric Segment-A acceleration.

ORegan2022 shows a CV current transient above 1C. This is not a CC waveform phase error; the CC drive-cycle audit remains correct. ORegan2022 should be treated as valid with a CV-current-transient warning.

## Final Day20B verdict

```text
Full-protocol raw gain: supported across Chen2020, OKane2022, ORegan2022.
Segment-A non-geometric acceleration: not supported.
Dominant mechanism class: voltage-boundary / control-state split, with late-CV preservation of earlier advantage.
```
