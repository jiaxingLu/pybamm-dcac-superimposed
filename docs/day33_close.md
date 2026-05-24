# Day 33 Closure — Plating-risk localization map

## 1. Purpose

Day 33 moved the PyBaMM-DCAC project from gain–margin classification toward plating-risk localization.

The goal was not to search for the fastest DC–AC protocol. The goal was to identify where and under which internal-state conditions the negative-electrode plating-margin risk becomes most severe.

The working question was:

> Under an admissible-fast-protocol framing, where does the minimum negative-electrode margin occur, and which state variables explain that risk?

---

## 2. Project framing

The DC–AC project no longer uses maximum raw timing gain as the primary design target.

The current framing is:

```text
Find an admissible DC–AC protocol under:
1. state-equivalent timing gain,
2. geometry–residual separation,
3. microstate response,
4. negative-electrode plating margin,
5. future thermal / aging admissibility.
```

Notebook 33 continues the Day30–Day32 mainline:

- Notebook 30: DC–AC creates equal-Q microstate differences, but raw timing gain is geometry-dominated.
- Notebook 31: Chen2020 / DFN shows an amplitude-dependent negative-electrode hard-margin boundary.
- Notebook 32: timing geometry dominance transfers across parameter sets, while plating-margin admissibility is parameter-set dependent.
- Notebook 33: localizes the state conditions that trigger the minimum negative-electrode margin.

---

## 3. Notebook and outputs

Notebook:

- `notebooks/33_plating_risk_localization_map.ipynb`

Main output files:

- `data/day33_metadata.json`
- `data/day33_variable_inventory.csv`
- `data/day33_prior_notebook_variable_lineage.csv`
- `data/day33_prior_plating_margin_file_inventory.csv`
- `data/day33_variable_registry.csv`
- `data/day33b_protocol_table.csv`
- `data/day33b_run_summary.csv`
- `data/day33b_state_extraction_audit.csv`
- `data/day33b_plating_risk_localization_summary.csv`
- `data/day33b_plating_risk_localization_summary_refined.csv`
- `data/day33b_compact_risk_trigger_map.csv`
- `data/day33c_frequency_sensitivity_protocol_table.csv`
- `data/day33c_run_summary.csv`
- `data/day33c_state_extraction_audit.csv`
- `data/day33c_frequency_sensitivity_risk_localization.csv`
- `data/day33_final_risk_localization_synthesis.csv`

Branch:

- `day33-plating-risk-localization`

Main Day33 commit:

- `00355dc audit: add Day33 plating-risk localization map`

---

## 4. Frequency and protocol basis

Day33 follows the Day30–Day32 set-rebased mainline.

Parameter set:

- `Chen2020`

Model:

- DFN

Thermal setting:

- isothermal

Main frequency mode:

```text
set_rebased
```

Frequency formula:

```text
f_set = 1 / (2π · tau_factor · τ_ref,set)
```

Chen2020 reference time constant:

```text
τ_ref,set = Day17 tau2_biexp = 36.316532 s
```

Main tau factor:

```text
tau_factor = 1.5
```

Main frequency:

```text
f_main ≈ 0.002922 Hz
```

MJ1 fixed-label frequencies were not used in the Day33 mainline.

---

## 5. Day33A — Variable lineage and registry freeze

Day33A established the variable lineage and froze the variable registry.

The logic was:

```text
previous notebook lineage
→ current notebook availability verification
→ Day33 variable registry
```

### 5.1 Prior notebook lineage

Notebook30 provided microstate-response variables:

- electrolyte concentration / gradient,
- negative particle surface stoichiometry,
- negative surface stoichiometry range,
- negative / positive reaction overpotential.

Notebook31 and Notebook32 provided plating-margin variables:

- `Negative electrode surface potential difference [V]`,
- `Negative electrode surface potential difference at separator interface [V]`,
- `X-averaged negative electrode surface potential difference [V]`.

### 5.2 Variable registry

Primary plating-margin proxy:

```text
Negative electrode surface potential difference [V]
```

Primary reduction:

```text
spatial minimum over the negative electrode
```

Auxiliary plating-margin variables:

- `Negative electrode surface potential difference at separator interface [V]`,
- `X-averaged negative electrode surface potential difference [V]`.

Explanatory variables:

- negative electrode reaction overpotential,
- electrolyte concentration / electrolyte concentration range,
- negative particle surface stoichiometry,
- negative surface stoichiometry range.

Explicit boundary:

```text
Negative electrode OCP is not a primary plating-margin proxy.
```

OCP is only an equilibrium reference. It excludes electrolyte potential and kinetic polarization under load.

---

## 6. Day33B — Fixed-frequency risk localization

Day33B localized the plating-margin risk at the Day30–Day32 mainline frequency:

```text
1.5τ_set
```

Protocol set:

- DC `0.3C`,
- DC–AC `0.3C + 0.7C`: stress case,
- DC–AC `0.3C + 0.38C`: near hard-margin boundary,
- DC–AC `0.3C + 0.3C`: intermediate reference.

### 6.1 Main result

The minimum negative-electrode potential does not occur uniformly over the charge trajectory.

For all tested cases, the minimum U_NE localizes in the high-Q / high-SOC and voltage-boundary-adjacent region.

For DC–AC cases, the minimum U_NE is also phase-locked to the charge-current peak.

### 6.2 DC reference

DC 0.3C:

```text
min_U_NE ≈ +37.3 mV
margin_class = near_boundary
Q_frac_of_DC_end_at_min_U_NE = 1.0
```

Interpretation:

> The DC reference remains above 0 mV but enters the conservative 50 mV buffer at the end of charge.

### 6.3 DC–AC stress case

DC–AC 0.3C + 0.7C:

```text
min_U_NE ≈ −25.3 mV
margin_class = risk_flag
phase_norm_at_min_U_NE ≈ 0.276
I_charge_at_min_U_NE ≈ 4.95 A
```

Interpretation:

> The stress case crosses the hard 0 mV proxy. The minimum U_NE occurs near the AC charge-current peak, high Q/SOC, and voltage-boundary-adjacent operation.

### 6.4 Near-boundary case

DC–AC 0.3C + 0.38C:

```text
min_U_NE ≈ +0.58 mV
margin_class = near_boundary
phase_norm_at_min_U_NE ≈ 0.223
I_charge_at_min_U_NE ≈ 3.37 A
```

Interpretation:

> The case remains narrowly above the hard 0 mV proxy but is very close to the boundary.

### 6.5 Intermediate case

DC–AC 0.3C + 0.3C:

```text
min_U_NE ≈ +6.66 mV
margin_class = near_boundary
phase_norm_at_min_U_NE ≈ 0.228
I_charge_at_min_U_NE ≈ 2.99 A
```

Interpretation:

> The case preserves the 0 mV hard-margin proxy but remains near-boundary.

---

## 7. Day33B risk-trigger structure

The dominant trigger structure for DC–AC cases is:

```text
current peak
+ charge peak phase
+ high Q/SOC
+ voltage-boundary coupling
```

Electrolyte-gradient and surface-state variables provide explanatory context.

Compared with DC, the DC–AC cases show amplified electrolyte concentration gradients at the minimum-U_NE point:

- AC0.7 stress: c_e range ≈ 2.71× DC,
- AC0.38 boundary: c_e range ≈ 1.76× DC,
- AC0.3 intermediate: c_e range ≈ 1.61× DC.

Surface heterogeneity is also amplified, but less strongly than electrolyte-gradient response.

Correct interpretation:

> Electrolyte-gradient and surface-heterogeneity variables are important background states, but the immediate risk minimum is best described as peak-current + high-Q/SOC + voltage-boundary coupled.

---

## 8. Day33C — Frequency sensitivity of risk localization

Day33C tested whether the Day33B risk-trigger structure is stable across representative normalized frequencies.

Fixed amplitude:

```text
DC = 0.3C
AC = 0.38C
```

Frequency points:

```text
0.5τ_set
1.5τ_set
3.0τ_set
5.0τ_set
```

### 8.1 Margin result

| tau factor | min U_NE | margin class |
|---:|---:|---|
| 0.5τ_set | +3.54 mV | near_boundary |
| 1.5τ_set | +0.58 mV | near_boundary |
| 3.0τ_set | −1.22 mV | risk_flag |
| 5.0τ_set | +1.73 mV | near_boundary |

All cases operate very close to the 0 mV hard-margin proxy. The `3.0τ_set` case crosses the proxy in this run.

### 8.2 Trigger stability

Across all frequency points, the minimum U_NE remains:

```text
current-peak coupled
charge-peak-phase coupled
high-Q/SOC coupled
voltage-boundary coupled
```

The phase of minimum U_NE remains close to the theoretical charge-current peak phase:

```text
phase_norm ≈ 0.25
```

### 8.3 Frequency-dependent state location

The Q location of the minimum U_NE shifts with frequency:

| tau factor | Q fraction of DC end at min U_NE |
|---:|---:|
| 0.5τ_set | 0.884 |
| 1.5τ_set | 0.869 |
| 3.0τ_set | 0.853 |
| 5.0τ_set | 0.792 |

Longer-period excitation shifts the minimum-U_NE point toward earlier Q.

At `5.0τ_set`, the minimum occurs farther from the 4.2 V boundary and with stronger electrolyte-gradient involvement. This is consistent with the Day30 observation that longer-period excitation becomes increasingly nonlocal / boundary-sensitive.

---

## 9. Microstate-context boundary

Notebook33 does not repeat the full equal-Q microstate-response audit from Notebook30.

Instead, it uses selected microstate variables as explanatory context at the localized minimum-U_NE point.

Extracted microstate context includes:

- electrolyte concentration range,
- negative-surface stoichiometry range,
- negative-electrode reaction overpotential.

These variables help interpret whether the risk point is accompanied by:

- transport-gradient amplification,
- surface-state heterogeneity,
- stronger kinetic polarization.

In the current Chen2020 / DFN localization map, the dominant trigger structure is:

```text
peak-current + high-Q/SOC + voltage-boundary coupling
```

Electrolyte-gradient and surface-heterogeneity variables are important background states, especially under DC–AC, but they are not used as standalone admissibility criteria.

The hard admissibility criterion remains:

```text
negative-electrode potential proxy U_NE vs Li/Li+
```

---

## 10. Main Day33 conclusion

Notebook33 shows that plating-margin risk is localized, not trajectory-uniform.

In the tested Chen2020 / DFN setting:

1. The minimum U_NE occurs near high-Q / high-SOC operation.
2. The minimum U_NE is strongly coupled to the voltage-boundary-adjacent region.
3. Under DC–AC, the minimum U_NE is phase-locked to the charge-current peak.
4. Electrolyte concentration gradients and negative-surface heterogeneity are amplified under DC–AC and provide explanatory background states.
5. Frequency changes the severity and Q-location of the minimum U_NE, but it does not change the dominant trigger structure across the tested representative frequencies.

The practical interpretation is:

> The main plating-margin risk trigger is peak-current forcing applied near high-Q / voltage-boundary-adjacent operation.

---

## 11. What Day33 verified

Day33 verified that:

1. The Day30–Day32 variable lineage is coherent.
2. `Negative electrode surface potential difference [V]` remains the correct primary U_NE proxy for Day33.
3. Negative-electrode OCP must not be used as a primary plating-margin metric.
4. The minimum U_NE under DC–AC localizes near the AC charge-current peak.
5. The minimum U_NE occurs at high Q / high SOC.
6. Voltage-boundary proximity is part of the risk trigger.
7. The risk-trigger structure remains stable across representative frequencies at AC0.38C.
8. Longer-period forcing shifts the risk location toward earlier Q and increases electrolyte-gradient relevance.

---

## 12. What Day33 did not prove

Day33 did not prove that:

1. Lithium plating experimentally occurs.
2. DC–AC is plating-free.
3. The 50 mV buffer is a universal safety threshold.
4. A specific waveform is globally optimal.
5. Thermal admissibility is satisfied.
6. Aging admissibility is satisfied.
7. DC–AC produces non-geometric electrochemical acceleration.

---

## 13. Implication for Day34

Day34 should not optimize a fixed sinusoidal waveform.

It should use the Day33 risk-trigger map to design state-aware waveform scheduling.

Immediate design implications:

| Day33 finding | Day34 strategy |
|---|---|
| min U_NE occurs near high Q/SOC | high-SOC AC derating or AC shutdown |
| min U_NE is charge-peak-phase coupled | peak-current clipping |
| risk is voltage-boundary adjacent | AC-off before boundary or voltage-boundary-aware control |
| longer periods shift risk earlier | Q-window restriction for long-period forcing |
| electrolyte gradients are amplified | include transport-state-aware amplitude/frequency limits |

Candidate Day34 control concepts:

- SOC-dependent AC amplitude,
- U_NE-margin-aware peak-current clipping,
- high-SOC AC shutdown,
- frequency rebasing by τ_ref(SOC,T,SOH),
- future thermal admissibility constraints.

---

## 14. Final conclusion wording

Correct conclusion wording:

> In Chen2020 / DFN, DC–AC plating-margin risk localizes near high-Q / voltage-boundary-adjacent operation and is phase-locked to the AC charge-current peak. Frequency changes the severity and state location of the risk minimum, but the dominant trigger structure remains peak-current / high-Q / boundary-coupled across the tested representative frequencies. This supports moving from fixed sinusoidal DC–AC protocols toward state-aware waveform scheduling.

Short version:

```text
DC–AC risk is localized and state-dependent.
The next design target is state-aware admissible waveform scheduling, not maximum raw timing gain.
```
