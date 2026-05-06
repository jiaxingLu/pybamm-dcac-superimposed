# Day20B — Chen2020 full-protocol CC+CV smoke test

Status: smoke test passed

## Scope

This document summarizes the first full CC+CV PyBaMM smoke simulation after Day20A.

Parameter set:

```text
Chen2020
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

Normalized cutoff:

```text
C_cutoff = 0.05 / 3.4 = 0.014705882 C
I_cutoff = C_cutoff · Q_nom
```

For Chen2020, `Q_nom = 5 Ah`, so `I_cutoff = 73.529 mA`.

## Smoke result

| metric | value |
|---|---:|
| DC end time [s] | 19352.284 |
| DCAC end time [s] | 17105.918 |
| total Δt [s] | 2246.367 |
| total Δt [min] | 37.439 |
| DC final Q [Ah] | 4.872815 |
| DCAC final Q [Ah] | 4.872588 |
| DC cutoff reached | True |
| DCAC cutoff reached | True |
| DC CV tail | True |
| DCAC CV tail | True |

## Voltage-boundary result

| metric | value |
|---|---:|
| Q_to_Vmax DC [Ah] | 4.627667 |
| Q_to_Vmax DCAC [Ah] | 3.770222 |
| Q_to_Vmax shift [Ah] | 0.857446 |
| t_to_Vmax shift [s] | 3860.316 |

## Segment summary

| segment | Q range [Ah] | median Δt [min] | min Δt [min] | max Δt [min] | interpretation |
|---|---:|---:|---:|---:|---|
| A | 0.244–3.745 | 21.103 | 7.777 | 32.538 | geometry-dominated |
| B | 3.783–4.600 | 29.202 | 13.451 | 38.331 | boundary / control-state split |
| D | 4.639–4.873 | 37.665 | 37.256 | 38.131 | late CV feedback region |

## Anchor points

| anchor | segment | Δt [min] | DC stage | DCAC stage |
|---|---|---:|---|---|
| Q80_common | B_between_DCAC_Vmax_and_DC_Vmax | 18.139 | CC_until_Vmax | CV_after_Vmax |
| Q90_common | B_between_DCAC_Vmax_and_DC_Vmax | 35.179 | CC_until_Vmax | CV_after_Vmax |
| Q80_nominal_5Ah | B_between_DCAC_Vmax_and_DC_Vmax | 22.134 | CC_until_Vmax | CV_after_Vmax |
| Q90_nominal_5Ah | B_between_DCAC_Vmax_and_DC_Vmax | 37.562 | CC_until_Vmax | CV_after_Vmax |

## Interpretation

The Chen2020 full CC+CV smoke simulation successfully implements the intended MJ1-like control logic at the PyBaMM protocol level.

The full-protocol raw gain is positive:

```text
Δt_total = 37.439 min
```

The gain also survives into the late CV region:

```text
Segment D median Δt = 37.665 min
```

However, Q80/Q90 gains occur in Segment B, where the DCAC branch is already voltage-limited while the DC reference remains in CC. This supports a voltage-boundary / control-state explanation rather than non-geometric Segment-A acceleration.

## Verdict

```text
Full-protocol raw gain: supported for Chen2020 smoke test.
Non-geometric Segment-A acceleration: not supported by this smoke test.
Dominant interpretation: boundary/control-state split, with CV preserving earlier advantage.
```

## Next step

Run the same full-protocol workflow for:

```text
OKane2022
ORegan2022
```

Then compare whether the Segment B / late-CV pattern is consistent across the charge-first full-protocol batch.
