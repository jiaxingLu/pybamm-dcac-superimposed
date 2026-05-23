# Day 31 Closure — Negative-electrode plating-margin audit under DC–AC excitation

## 1. Purpose

Day 31 added an admissibility layer to the DC–AC analysis.

Notebook 30 showed that DC–AC excitation can create equal-Q microstate differences, but the state-equivalent timing gain in the Chen2020 model hierarchy remained geometry-dominated. Day 31 therefore asked a different question:

> Do DC–AC protocols that produce raw state-equivalent or event-level timing gains preserve negative-electrode plating margin?

The goal was not to prove lithium plating occurrence or absence. The goal was to audit a thermodynamic negative-electrode potential proxy using PyBaMM as a virtual three-electrode model.

---

## 2. Notebook and outputs

Notebook:

- `notebooks/31_negative_electrode_plating_margin_audit.ipynb`

Primary output tables:

- `data/day31_protocol_table_smoke.csv`
- `data/day31_run_summary_smoke.csv`
- `data/day31_variable_availability_plating_margin_smoke.csv`
- `data/day31_plating_margin_candidate_keys_smoke.csv`
- `data/day31_plating_margin_extraction_audit_smoke.csv`
- `data/day31_protocol_plating_margin_summary_smoke.csv`
- `data/day31_equalQ_plating_margin_summary_smoke.csv`
- `data/day31_gain_margin_admissibility_ledger_smoke.csv`
- `data/day31_phase_risk_audit_smoke.csv`
- `data/day31_amplitude_admissibility_ledger_1p5tau.csv`
- `data/day31_fine_amplitude_admissibility_ledger_1p5tau.csv`
- `data/day31_fine_amplitude_hard_margin_boundary_estimate_1p5tau.csv`
- `data/day31_amplitude_boundary_synthesis_1p5tau.csv`

Branch:

- `day31-negative-electrode-plating-margin-audit`

Main Day31 commit:

- `ebee695 audit: add Day31 negative-electrode plating-margin audit`

---

## 3. Model and protocol design

Parameter set:

- `Chen2020`

Model:

- DFN

Thermal setting:

- isothermal

Current protocol family:

- DC baseline: `0.3C`
- DC–AC: `0.3C DC + AC`

Current convention:

```text
PyBaMM: +I = discharge, −I = charge
I_py(t) = −I_DC − I_AC sin(2π f t)
```

This corresponds to the charge-positive experimental waveform:

```text
I_charge(t) = I_DC + I_AC sin(2π f t)
```

Frequency reference:

- Chen2020 `tau_ref,set = tau2_biexp = 36.316532 s`

Initial frequency points for smoke audit:

- `0.5τ_set`
- `1.5τ_set`
- `3.0τ_set`
- `5.0τ_set`

Amplitude scan at fixed `1.5τ_set`:

- `AC = 0.1C`
- `AC = 0.2C`
- `AC = 0.3C`
- `AC = 0.4C`
- `AC = 0.5C`
- `AC = 0.7C`

Fine amplitude scan at fixed `1.5τ_set`:

- `AC = 0.30C`
- `AC = 0.32C`
- `AC = 0.34C`
- `AC = 0.36C`
- `AC = 0.38C`
- `AC = 0.40C`

---

## 4. Plating-margin proxy

The intended plating-margin proxy was the negative-electrode surface potential difference vs Li/Li+:

```text
U_NE_vs_Li ≈ φ_s,n − φ_e,n
```

The primary extracted variable was:

- `Negative electrode surface potential difference [V]`

This variable has spatial resolution over the negative electrode. The notebook used the spatial minimum as the primary plating-margin proxy:

```text
min_U_NE_vs_Li = min_x(negative electrode surface potential difference)
```

Auxiliary variables:

- `Negative electrode surface potential difference at separator interface [V]`
- `X-averaged negative electrode surface potential difference [V]`

Margin classes:

| Class | Criterion |
|---|---|
| `safe_margin` | min U_NE_vs_Li > 50 mV |
| `near_boundary` | 0 mV < min U_NE_vs_Li <= 50 mV |
| `risk_flag` | min U_NE_vs_Li <= 0 mV |

The 50 mV threshold is an audit buffer, not a universal physical constant. A `risk_flag` indicates that the thermodynamic proxy crosses the selected 0 mV threshold. It is not equivalent to experimentally confirmed lithium plating.

---

## 5. Variable availability result

The PyBaMM Chen2020 / DFN model exposes the required virtual three-electrode variables:

- `Negative electrode surface potential difference [V]`
- `Negative electrode surface potential difference at separator interface [V]`
- `X-averaged negative electrode surface potential difference [V]`

It also exposes lithium-plating-related variables, but Day 31 did not interpret those as confirmed plating because no plating submodel audit was performed in this notebook.

---

## 6. Smoke audit result: 0.3C + 0.7C across frequency

The first smoke audit tested:

- DC reference: `0.3C`
- DC–AC: `0.3C + 0.7C`
- frequencies: `0.5τ_set`, `1.5τ_set`, `3.0τ_set`, `5.0τ_set`

### 6.1 DC reference

The DC reference stayed above 0 mV but entered the conservative 50 mV buffer:

```text
DC 0.3C:
min_U_NE_vs_Li ≈ 37.3 mV
margin_class = near_boundary
```

Therefore, the DC reference should not be called `safe_margin`; it is better described as:

```text
above 0 mV but inside the 50 mV audit buffer
```

### 6.2 High-amplitude DC–AC

All tested `0.3C + 0.7C` DC–AC protocols crossed the 0 mV negative-electrode potential proxy:

```text
0.5τ_set: risk_flag
1.5τ_set: risk_flag
3.0τ_set: risk_flag
5.0τ_set: risk_flag
```

The minimum U_NE values were approximately in the range of −18 to −25 mV.

### 6.3 Phase-risk result

The worst U_NE values occurred near the AC charge-current peak.

This supports the interpretation that the hard-margin violation is driven by the high instantaneous charge-current half-cycle rather than by average current alone.

---

## 7. Equal-Q margin result

The equal-Q audit showed that the high-amplitude DC–AC protocols also reduce negative-electrode margin at the same Q_net.

For `0.3C + 0.7C`, the equal-Q window was classified as `risk_flag`.

This means that the margin issue is not only a terminal event artifact. It also appears within the shared-Q comparison window for high-amplitude DC–AC.

---

## 8. Amplitude-reduction audit at 1.5τ_set

Because all `0.3C + 0.7C` cases triggered risk flags, Day 31 shifted from frequency search to amplitude admissibility.

The amplitude scan fixed:

```text
DC = 0.3C
frequency = 1.5τ_set
```

and scanned:

```text
AC = 0.1C, 0.2C, 0.3C, 0.4C, 0.5C, 0.7C
```

### 8.1 Coarse amplitude scan result

The coarse scan showed:

- `AC = 0.1C`, `0.2C`, `0.3C`: above 0 mV, but near-boundary
- `AC = 0.4C`, `0.5C`, `0.7C`: full-protocol risk_flag

This established that amplitude controls the hard-margin admissibility of the DC–AC protocol.

---

## 9. Fine amplitude-boundary scan

A finer scan was performed around the hard-margin boundary:

```text
AC = 0.30C, 0.32C, 0.34C, 0.36C, 0.38C, 0.40C
```

at fixed:

```text
DC = 0.3C
frequency = 1.5τ_set
```

### 9.1 Full-protocol margin

Fine scan result:

| AC amplitude | peak C | min U_NE vs Li | classification |
|---:|---:|---:|---|
| 0.30C | 0.60C | +6.66 mV | near_boundary |
| 0.32C | 0.62C | +5.31 mV | near_boundary |
| 0.34C | 0.64C | +3.15 mV | near_boundary |
| 0.36C | 0.66C | +1.43 mV | near_boundary |
| 0.38C | 0.68C | +0.58 mV | near_boundary, almost at boundary |
| 0.40C | 0.70C | −1.33 mV | risk_flag |

Linear interpolation gives:

```text
full-protocol hard-margin boundary:
AC ≈ 0.386C
peak current ≈ 0.686C
```

### 9.2 Equal-Q margin

The common equal-Q window did not cross 0 mV within `AC = 0.30–0.40C`.

At `AC = 0.40C`, the equal-Q minimum U_NE remained slightly above 0 mV:

```text
equal-Q min U_NE ≈ +0.39 mV
```

This indicates that the full-protocol risk appears later than the shared-Q comparison window, likely near higher-Q / voltage-boundary-adjacent operation.

---

## 10. Day31 main conclusion

Day 31 establishes that DC–AC timing gain must be filtered through a negative-electrode admissibility constraint.

At fixed `1.5τ_set`, increasing AC amplitude increases raw timing gain, but decreases negative-electrode plating margin.

The high-amplitude protocol:

```text
0.3C + 0.7C
```

is not admissible under the Chen2020 / DFN virtual three-electrode hard-margin criterion.

A lower-amplitude region:

```text
0.3C + 0.30–0.38C
```

preserves the 0 mV hard-margin proxy but remains within the conservative 50 mV buffer. These cases should be interpreted as:

```text
hard-margin admissible but near-boundary
```

not as fully safe-margin protocols.

---

## 11. What Day31 verified

Day 31 verified that:

1. PyBaMM Chen2020 / DFN can be used as a virtual three-electrode model for negative-electrode potential audit.
2. `Negative electrode surface potential difference [V]` can be extracted and spatially minimized.
3. The DC 0.3C reference remains above 0 mV but enters the conservative 50 mV buffer.
4. `0.3C + 0.7C` DC–AC protocols produce raw timing gains but violate the hard 0 mV negative-electrode margin proxy.
5. At fixed `1.5τ_set`, reducing AC amplitude recovers hard-margin admissibility.
6. The full-protocol hard-margin boundary is approximately `AC ≈ 0.386C`.
7. Equal-Q margin remains above 0 mV for `AC = 0.30–0.40C`, meaning the first hard-margin violation emerges later in the full-protocol window.
8. The correct objective is not fastest protocol, but admissible fast protocol.

---

## 12. What Day31 did not prove

Day 31 did not prove that:

1. Lithium plating actually occurs experimentally.
2. Lithium plating is absent when the proxy remains above 0 mV.
3. The 50 mV buffer is a universal safety threshold.
4. The Chen2020 admissibility boundary transfers to MJ1, Ecker2015, ORegan2022, other chemistries, lower temperatures, or aged cells.
5. DC–AC is safe under all thermal conditions.
6. DC–AC produces non-geometric electrochemical acceleration.

---

## 13. Current interpretation boundary

Current boundaries:

- Parameter set: Chen2020
- Model: DFN
- Thermal condition: isothermal
- Protocol: prescribed-current DC–AC
- DC component: 0.3C
- Frequency: primarily `1.5τ_set`
- Safety metric: negative-electrode potential proxy only
- No explicit plating submodel interpretation
- No non-isothermal heat generation / temperature-rise audit
- No cross-parameter-set transfer yet

---

## 14. Next step

The next step is to combine the Day30 and Day31 logic into a multi-constraint DC–AC protocol framework.

Future DC–AC protocols should be judged by at least four dimensions:

1. Timing / state-equivalent progression
2. Geometry–residual separation
3. Microstate response
4. Admissibility constraints:
   - negative-electrode plating margin
   - thermal admissibility
   - future aging risk

The immediate next technical step is either:

1. create a `docs/day31_close.md` closure and commit the Day31 branch;
2. start a transferability audit for Ecker2015 / ORegan2022 using the same gain–margin logic;
3. later add non-isothermal / thermal admissibility to evaluate `T_cell`, `ΔT`, heat generation, and thermal-aging risk.
