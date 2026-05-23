# Day 30 Closure — Microstate observability under DC–AC excitation

## 1. Purpose

Day 30 examined whether low-frequency DC–AC excitation produces persistent equal-Q microstate differences beyond prescribed-current geometry.

The notebook separates:

- `Δt_raw(Q)`: model-observed state-equivalent first-passage time gain;
- `Δt_geom(Q)`: prescribed-current geometry contribution;
- `Δt_resid(Q)`: residual timing beyond current geometry;
- equal-Q microstate differences;
- model-hierarchy-dependent transport and surface-state responses.

The goal was not to prove that DC–AC charging is intrinsically faster. The goal was to determine whether DC–AC acts as a non-geometric acceleration mechanism or as a dynamic excitation probe for internal battery states.

## 2. Notebook and outputs

Notebook:

- `notebooks/30_microstate_dfn_spme_spm_dcac_audit.ipynb`

Primary output tables:

- `data/day30_notebook30_final_synthesis_table.csv`
- `data/day30_hierarchy_mechanism_with_geom_resid.csv`
- `data/day30_hierarchy_geom_resid_summary.csv`
- `data/day30_fine_scan_candidate_window_selection.csv`
- `data/day30_fine_scan_integrated_frequency_response_verdict.csv`
- `data/day30_hierarchy_mechanism_localization_summary.csv`
- `data/day30_hierarchy_feature_support_table.csv`

Branch:

- `day30-microstate-observability-audit`

Main Day30 commit:

- `0bf5a0e audit: close Day30 microstate observability hierarchy`

## 3. Model and protocol design

Parameter set:

- `Chen2020`

Model hierarchy:

- DFN
- SPMe
- SPM

The relaxation reference used for frequency rebasing was taken from the previous Day 17 HPPC-style relaxation audit:

```text
tau_ref,set = tau2_biexp = 36.316532 s
```

Current protocol:

- DC baseline: `0.3C`
- DC–AC: `0.3C DC + 0.7C AC`

Current convention:

```text
PyBaMM: +I = discharge, −I = charge
I_py(t) = −I_DC − I_AC sin(2π f t)
```

This corresponds to the charge-positive experimental waveform:

```text
I_charge(t) = I_DC + I_AC sin(2π f t)
```

## 4. Frequency design

Two frequency modes were separated.

### 4.1 Fixed-MJ1-label frequency

The first audit used MJ1-derived labels:

- `0.1τ_MJ1`
- `1τ_MJ1`
- `5τ_MJ1`
- `10τ_MJ1`
- `f = 0.000412 Hz`

A key finding was that MJ1-label frequencies do not retain the same normalized meaning in Chen2020. For example:

```text
MJ1-label 10τ applied to Chen2020 ≈ 3.06τ_set
f = 0.000412 Hz applied to Chen2020 ≈ 10.64τ_set
```

Therefore, fixed experimental-frequency transfer and set-rebased frequency matching must not be mixed in interpretation.

### 4.2 Set-rebased normalized frequency

The second audit recalculated frequency using Chen2020's own relaxation descriptor:

```text
f = 1 / (2π · tau_factor_set · tau_ref,set)
```

The fine scan used:

- `0.5τ_set`
- `1.0τ_set`
- `1.5τ_set`
- `2.0τ_set`
- `3.0τ_set`
- `4.0τ_set`
- `5.0τ_set`

## 5. Microstate registry

A controlled microstate registry was built instead of interpreting arbitrary PyBaMM variables.

Key variables included:

- negative particle average stoichiometry;
- negative particle surface stoichiometry;
- negative surface stoichiometry range;
- positive particle surface stoichiometry;
- electrolyte concentration mean;
- electrolyte concentration range;
- negative reaction overpotential;
- positive reaction overpotential;
- interfacial current density;
- cell temperature;
- total heating.

Main interpretation variables:

| Feature | Interpretation |
|---|---|
| `elyte_c_range` | electrolyte concentration-gradient response |
| `neg_avg_surface_sto` | average negative surface state |
| `neg_surface_sto_range` | DFN-level negative surface spatial heterogeneity |
| `eta_n_mean` | negative reaction overpotential |
| `pos_avg_surface_sto` | positive surface-state response |

## 6. Normalized frequency-window result

The Chen2020 / DFN fine scan identified a normalized microstate-response window.

Candidate window:

```text
tau_factor_set = 1.0 to 3.0
```

Most balanced region:

```text
approximately 1.5–2.0τ_set
```

Interpretation:

| Range | Interpretation |
|---|---|
| `< 1τ_set` | filtered or weak cycle-mean response |
| `1–1.5τ_set` | onset of microstate response |
| `1.5–3τ_set` | main candidate response window |
| `> 3τ_set` | stronger gradients but increasingly nonlocal / boundary-sensitive |
| `~5τ_set` | still responsive, but Q-locality and cycle-count quality degrade |

The result does not prove an optimal fast-charging frequency. It identifies the cleanest frequency region for observing cycle-averaged microstate response in Chen2020 / DFN.

## 7. Model-hierarchy result

The hierarchy audit compared Chen2020 DFN, SPMe, and SPM at representative normalized frequencies:

- `0.5τ_set`: fast-side filtered control
- `1.5τ_set`: balanced candidate
- `3.0τ_set`: upper candidate / strong response
- `5.0τ_set`: slow-side boundary

### 7.1 Raw timing layer

Raw `Δt(Q)` was similar across DFN, SPMe, and SPM.

This indicates that raw timing gain is not a DFN-specific microstate transport effect.

### 7.2 Electrolyte-gradient layer

`elyte_c_range` was visible in DFN and SPMe, but not represented in SPM.

Interpretation:

```text
DFN / SPMe >> SPM
```

This indicates that electrolyte concentration-gradient response depends on electrolyte transport modeling.

### 7.3 Negative surface spatial heterogeneity layer

`neg_surface_sto_range` was visible in DFN, but absent or degenerate in SPMe and SPM.

Interpretation:

```text
DFN >> SPMe ≈ SPM
```

This indicates that negative surface spatial heterogeneity is a DFN-level porous-electrode spatial effect.

### 7.4 Average surface-state layer

Average surface stoichiometry responses appeared in DFN, SPMe, and SPM.

Interpretation:

```text
DFN ≈ SPMe ≈ SPM
```

This layer can be represented by lower-order particle models and is not sufficient by itself to diagnose spatial transport risk.

## 8. Geometry-residual result

The hierarchy audit decomposed:

```text
Δt_raw(Q) = Δt_geom(Q) + Δt_resid(Q)
```

Across DFN, SPMe, and SPM:

```text
Δt_raw_mean_s ≈ Δt_geom_mean_s
Δt_resid_mean_s ≈ 0
```

All tested model/frequency combinations were classified as:

```text
geometry-dominated raw timing gain
```

This is the central Day30 result.

## 9. Final interpretation

DC–AC excitation produces real equal-Q microstate differences in Chen2020, especially in electrolyte concentration gradients and negative surface states.

However, these microstate differences do not translate into measurable positive `Δt_resid(Q)` in the tested Chen2020 hierarchy.

Therefore, the correct interpretation is:

```text
DC–AC is currently supported as a dynamic excitation / microstate observability probe,
not as a proven non-geometric fast-charging acceleration mechanism.
```

## 10. What Day30 verified

Day30 verified that:

1. Chen2020 / DFN has a normalized microstate-response window.
2. The candidate window is approximately `1–3τ_set`.
3. The most balanced region is approximately `1.5–2τ_set`.
4. DC–AC changes equal-Q electrolyte gradients and negative surface states.
5. Electrolyte-gradient response appears in DFN/SPMe but not SPM.
6. Negative-surface spatial heterogeneity is mainly DFN-level.
7. Raw `Δt(Q)` is geometry-dominated across DFN/SPMe/SPM.
8. No significant positive `Δt_resid(Q)` was found in the tested Chen2020 hierarchy.

## 11. What Day30 did not prove

Day30 did not prove that:

1. DC–AC creates non-geometric state-layer acceleration.
2. DC–AC improves lithium intercalation kinetics.
3. DC–AC improves electrolyte transport coefficients.
4. The observed microstate gradients are beneficial.
5. `1.5–2τ_set` is an optimal fast-charging frequency.
6. The result transfers to other parameter sets, chemistries, temperatures, or aging states.

## 12. Boundary conditions

Current boundaries:

- Parameter set: Chen2020 only
- Models: DFN / SPMe / SPM
- Thermal setting: isothermal
- Protocol: prescribed-current DC–AC, `0.3C + 0.7C`
- Current convention: charge-first
- Comparison: equal-Q first-passage
- Aging: not included
- Plating onset: not explicitly audited
- Temperature dependence: not audited
- Cross-parameter-set transfer: not yet audited

## 13. Next step

The next step is a transferability audit on:

- Ecker2015
- ORegan2022

using set-rebased frequencies near:

- `0.5τ_set`
- `1.5τ_set`
- `3.0τ_set`
- `5.0τ_set`

The transferability audit should test whether the Day30 separation holds across parameter sets:

```text
geometry-dominated timing
+
model-dependent microstate restructuring
```
