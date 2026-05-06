# Day20A — PyBaMM pre-CV / voltage-boundary segmented audit

Status: interim audit closed

## Scope

Day20A audits the existing Day18 v4 charge-first PyBaMM trajectory cache:

```text
data/day18_step1_phase_audit_trajectories_v4_charge_first.npz
```

The cache contains `t`, `V`, `I`, and `Q_net` for DC and DCAC arms, but it terminates at the maximum-voltage event. It does not contain an AC-off transition or a CV feedback tail.

Therefore Day20A covers:

- Segment A: AC-on prescribed-current shared-Q window
- Segment B: voltage-boundary event separation

Day20A does not cover:

- Segment C: AC-off transition
- Segment D: pure DC-CV feedback to cutoff

## Segment A finding

Segment A is geometry-dominated for all audited parameter sets.

| param_set | median Δt_model [s] | median Δt_geom [s] | median Δt_resid [s] | p95 |Δt_resid| [s] | max |Δt_resid| [s] |
|---|---:|---:|---:|---:|---:|
| Chen2020 | 1302.893 | 1302.894 | -0.001338 | 0.007722 | 0.014259 |
| OKane2022 | 1345.949 | 1345.949 | -0.000882 | 0.003514 | 0.005144 |
| ORegan2022 | 1378.561 | 1378.560 | 0.000279 | 0.005973 | 0.014275 |

Interpretation:

```text
Segment A raw Δt(Q) is explained by current geometry. Non-geometric residual is numerical-null.
```

## Segment B finding

Segment B shows large voltage-boundary separation. DCAC reaches the voltage boundary at substantially lower Q and earlier time than DC.

| param_set | Q shift [Ah] | Q shift [% nominal] | time shift [s] | state gain at DCAC boundary [s] | DC remaining time [s] | DC voltage headroom [V] | class |
|---|---:|---:|---:|---:|---:|---:|---|
| Chen2020 | 0.856056 | 17.121 | 3852.061 | 770.260 | 3081.801 | 0.113419 | large_boundary_shift |
| OKane2022 | 0.807622 | 16.152 | 3497.993 | 590.554 | 2907.440 | 0.106144 | large_boundary_shift |
| ORegan2022 | 1.513671 | 30.273 | 7081.008 | 1631.792 | 5449.216 | 0.454153 | very_large_boundary_shift |

The event timing shift decomposes as:

```text
t_DC,Vmax − t_DCAC,Vmax
=
[t_DC(Q_DCAC,Vmax) − t_DCAC,Vmax]
+
[t_DC,Vmax − t_DC(Q_DCAC,Vmax)]
```

The second term dominates: at the Q where DCAC reaches the voltage boundary, the DC arm is still below Vmax and still requires substantial additional charging time.

## Cutoff normalization rule for future full-protocol simulations

The MJ1 experimental cutoff current of 50 mA must not be transferred as an absolute current to all PyBaMM parameter sets.

It must be normalized as:

```text
C_cutoff = 0.05 / 3.4 ≈ 0.0147059 C
I_cutoff = C_cutoff · Q_nom
```

## Day20A conclusion

```text
The existing charge-first PyBaMM v4 trajectory cache supports a pre-CV audit only.
Segment A is current-geometry dominated with numerical-null residual.
Segment B shows large voltage-boundary separation.
The current cache does not contain AC-off transition or CV feedback.
A new full CC+CV PyBaMM protocol is required for Segment C/D.
```
