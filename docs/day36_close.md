# Day 36 Closure — Double-layer surface-form sensitivity audit

## 1. Purpose

Day 36 tested whether the previous PyBaMM-DCAC conclusions were sensitive to the omission of dynamic double-layer surface formulation.

The motivating question was:

> Could the absence of non-geometric acceleration in earlier notebooks be caused by not enabling double-layer capacitance dynamics through `surface form = differential`?

---

## 2. Notebook and outputs

Notebook:

- `notebooks/36_double_layer_surface_form_sensitivity.ipynb`

Primary outputs:

- `data/day36_metadata.json`
- `data/day36_double_layer_parameter_audit.csv`
- `data/day36_double_layer_parameter_keyword_inventory.csv`
- `data/day36_surface_form_model_variant_audit.csv`
- `data/day36_surface_form_variable_audit.csv`
- `data/day36_refined_capacitive_interfacial_variable_inventory.csv`
- `data/day36_protocol_table.csv`
- `data/day36_current_waveform_summary.csv`
- `data/day36_surface_form_run_summary.csv`
- `data/day36_state_extraction_audit.csv`
- `data/day36_protocol_margin_state_summary.csv`
- `data/day36_equalQ_timing_geom_resid_curves.csv`
- `data/day36_equalQ_timing_geom_resid_summary.csv`
- `data/day36_surface_form_sensitivity_ledger.csv`
- `data/day36_surface_form_delta_vs_false.csv`
- `data/day36_equal_terminalQ_state_progression_diff_false_vs_differential.csv`
- `data/day36_equal_terminalQ_state_progression_summary_false_vs_differential.csv`
- `data/day36b_high_frequency_protocol_table.csv`
- `data/day36b_high_frequency_run_summary.csv`
- `data/day36b_high_frequency_state_extraction_audit.csv`
- `data/day36b_high_frequency_equalQ_timing_curves.csv`
- `data/day36b_high_frequency_timing_summary.csv`
- `data/day36b_high_frequency_delta_false_vs_differential.csv`
- `data/day36_option_synthesis.csv`
- `data/day36_mainline_surface_form_synthesis.csv`
- `data/day36_high_frequency_surface_form_synthesis.csv`
- `data/day36_final_conclusion_table.csv`

---

## 3. Model variants

Day36 compared:

| Variant | Surface form | Role |
|---|---|---|
| `surface_form_false` | `false` | prior baseline / quasi-steady surface form |
| `surface_form_differential` | `differential` | dynamic double-layer branch |
| `surface_form_algebraic` | `algebraic` | algebraic surface-form diagnostic |

All three variants built and ran successfully.

---

## 4. Double-layer parameter audit

Chen2020 contains the required double-layer capacity parameters:

```text
Negative electrode double-layer capacity [F.m-2] = 0.2
Positive electrode double-layer capacity [F.m-2] = 0.2
```

Interpretation:

> The previous notebooks did not lack the C_dl parameters. Rather, they did not explicitly enable the differential surface-form dynamics.

---

## 5. Variable audit

All surface-form variants retained the required plating-margin proxy:

```text
Negative electrode surface potential difference [V]
```

This allowed direct comparison of U_NE margin across surface-form variants.

No direct PyBaMM output variable matching a clear capacitive-current name was identified in the variable audit. Therefore, Day36B reconstructed a diagnostic proxy:

```text
j_dl_proxy ≈ C_dl · d(U_NE_xavg)/dt
```

This proxy is interpretive and should not be treated as a direct PyBaMM capacitive-current output.

---

## 6. Day36A protocol set

Day36A tested the mainline frequency:

```text
1.5τ_set
```

Protocols:

- DC `0.3C`
- fixed `0.3C + 0.38C`
- fixed `0.3C + 0.7C`
- scheduled `sched_v2_conservative`

`sched_v2_conservative` was selected because Day35 identified it as the primary first-generation rule-based candidate.

---

## 7. Day36A main result

At `1.5τ_set`, enabling `surface form = differential` did not materially change the main outputs.

### 7.1 Timing

All non-DC protocols remained:

```text
geometry_dominated
```

The changes in mean raw timing and mean residual timing relative to `surface_form_false` were very small.

Representative differential-minus-false changes:

- fixed AC0.38: Δ raw ≈ +0.04 s, Δ residual ≈ +0.005 s
- fixed AC0.7: Δ raw ≈ +0.06 s, Δ residual ≈ +0.004 s
- sched v2: Δ raw ≈ +0.03 s, Δ residual ≈ +0.006 s

### 7.2 Plating margin

The min U_NE changes were sub-mV scale:

- fixed AC0.38: approximately +0.07 mV
- fixed AC0.7: approximately +0.04 mV
- sched v2: approximately +0.02 mV

Margin classes did not change.

### 7.3 State progression

Equal-terminal-Q state-progression differences between `false` and `differential` were very small:

- negative average stoichiometry differences were on the order of 10⁻⁵ to 10⁻⁴;
- U_NE differences were sub-mV;
- eta_n differences were very small.

Interpretation:

> At the mainline 1.5τ_set frequency, double-layer differential surface dynamics do not explain the absence of non-geometric acceleration.

---

## 8. Day36B high-frequency sensitivity

Day36B tested faster forcing for fixed `0.3C + 0.38C`:

- `0.5τ_set`
- `0.1τ_set`

Surface forms:

- `false`
- `differential`

### 8.1 Double-layer proxy

The reconstructed diagnostic proxy:

```text
C_dl · d(U_NE_xavg)/dt
```

was visibly larger in the `differential` branch than in the `false` branch.

Interpretation:

> Enabling `surface form = differential` does introduce a detectable capacitive dynamic response proxy.

### 8.2 Timing

At `0.5τ_set`:

- both `false` and `differential` remained geometry-dominated;
- differential-minus-false residual change was small.

At `0.1τ_set`:

- residual effects became more visible;
- the differential branch showed a more negative residual shift;
- this did not represent positive non-geometric acceleration.

Representative result:

```text
0.1τ_set:
false residual mean ≈ −0.24 s
differential residual mean ≈ −0.72 s
```

### 8.3 Plating margin

The min U_NE differences remained tiny:

- 0.5τ_set: differential minus false ≈ +0.04 mV
- 0.1τ_set: differential minus false ≈ +0.01 mV

No margin class changed.

---

## 9. Main Day36 conclusion

Day36 supports the following conclusion:

> In Chen2020 / DFN under the tested 0.1–1.5τ_set DC–AC forcing range, enabling `surface form = differential` introduces visible double-layer proxy dynamics but does not materially change timing, geometry–residual classification, plating-margin verdicts, or equal-terminal-Q state progression.

Therefore:

> The previous absence of non-geometric acceleration is not explained by omission of differential double-layer surface dynamics under the tested conditions.

---

## 10. What Day36 verified

Day36 verified that:

1. Chen2020 includes double-layer capacity parameters.
2. `surface form = differential` builds and runs in PyBaMM.
3. The U_NE plating-margin proxy remains available under all surface-form variants.
4. Differential surface form introduces visible reconstructed C_dl proxy dynamics.
5. The mainline 1.5τ_set timing result remains geometry-dominated.
6. High-frequency 0.5τ_set remains geometry-dominated.
7. High-frequency 0.1τ_set shows a stronger residual shift, but not positive non-geometric acceleration.
8. Plating-margin classification does not change across surface-form variants.

---

## 11. What Day36 did not prove

Day36 did not prove that:

1. double-layer effects are universally irrelevant;
2. higher frequencies beyond the tested range would show no effect;
3. larger C_dl sensitivity would show no effect;
4. other parameter sets would behave the same;
5. thermal or aging coupling would not interact with double-layer dynamics;
6. experimental measurement-chain dynamics are irrelevant;
7. non-geometric acceleration is impossible in all model classes.

---

## 12. Interpretation boundary

Day36 applies to:

- Chen2020,
- DFN,
- isothermal setting,
- default Chen2020 C_dl values,
- tested forcing range 0.1–1.5τ_set,
- protocols DC03, fixed AC0.38, fixed AC0.7, and sched_v2.

The reconstructed double-layer proxy is not a direct PyBaMM capacitive-current output.

---

## 13. Next discussion point

The next step should not be another blind parameter scan.

The project should now explicitly discuss the claim-level question:

> Is non-geometric acceleration physically absent under the current model class, or is it not identifiable under the current terminal-Q / geometry-residual decomposition?

This is a methodology and interpretation issue, not merely a missing-parameter issue.
