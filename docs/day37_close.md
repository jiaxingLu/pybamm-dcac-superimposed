# Day 37 Closure — Mechanism and parameterization sensitivity matrix

## 1. Purpose

Day 37 was designed as the final evidence-gathering notebook before writing a formal non-geometric-acceleration claim review.

The central question was:

> After adding one missing-physics or parameterization branch at a time, does any branch create stable, positive, engineering-significant non-geometric terminal-Q acceleration?

This notebook was not a blind scan and not an optimizer. It was a structured sensitivity matrix.

---

## 2. Background

Day30–Day36 established that:

- raw DC–AC timing gain is largely prescribed-current geometry;
- `Δt_resid(Q)` remains near zero in the tested model branches;
- DC–AC creates measurable microstate and negative-electrode margin effects;
- state-aware scheduling improves hard U_NE margin;
- differential double-layer surface form does not explain the lack of non-geometric acceleration.

Day37 added two missing audit directions:

1. electrolyte transport parameterization sensitivity;
2. OCP / hysteresis / path-dependence capability audit.

---

## 3. Notebook and outputs

Notebook:

- `notebooks/37_mechanism_parameterization_sensitivity_matrix.ipynb`

Primary outputs:

- `data/day37_metadata.json`
- `data/day37_parameter_function_audit.csv`
- `data/day37_parameter_keyword_inventory.csv`
- `data/day37_option_capability_audit.csv`
- `data/day37_option_variable_inventory.csv`
- `data/day37_transport_branch_registry.csv`
- `data/day37_mechanism_branch_registry.csv`
- `data/day37_protocol_table_preview.csv`
- `data/day37_transport_function_implementation_audit.csv`
- `data/day37_branch_registry_final.csv`
- `data/day37_branch_build_audit.csv`
- `data/day37_protocol_table.csv`
- `data/day37_current_waveform_summary.csv`
- `data/day37_run_summary.csv`
- `data/day37_state_extraction_audit.csv`
- `data/day37_protocol_margin_microstate_summary.csv`
- `data/day37_equalQ_timing_geom_resid_curves.csv`
- `data/day37_equalQ_timing_geom_resid_summary.csv`
- `data/day37_matrix_ledger.csv`
- `data/day37_branch_delta_vs_baseline.csv`
- `data/day37_non_geometric_candidate_screen.csv`
- `data/day37_non_geometric_candidate_counts.csv`
- `data/day37_branch_sensitivity_synthesis.csv`
- `data/day37_final_claim_synthesis.csv`

---

## 4. Audited branches

Runnable Day37B branches:

| Branch | Type | Surface form | Transport |
|---|---|---|---|
| `baseline_default` | baseline | false | default |
| `double_layer_differential` | double-layer | differential | default |
| `transport_flattened` | transport diagnostic | false | flattened |
| `transport_nonlinearity_amplified` | transport diagnostic | false | amplified |
| `combined_sensitivity` | combined diagnostic | differential | amplified |

Deferred / excluded branches:

| Branch | Status | Reason |
|---|---|---|
| `ocp_hysteresis_dynamic` | deferred | no supported PyBaMM / Chen2020 DFN option identified |
| `sei_solvent_diffusion_limited` | excluded from clean matrix | side-reaction / degradation branch confounds reversible terminal-Q acceleration |
| particle mechanics branches | failed capability audit | missing Chen2020 parameters |
| reversible lithium plating | failed capability audit | missing stripping exchange-current parameter |

---

## 5. Protocol set

Every runnable branch used the same mandatory protocol set:

| Protocol | Role |
|---|---|
| `DC03` | DC reference |
| `fixed_AC0p38` | near-boundary baseline |
| `fixed_AC0p7` | high-amplitude stress control |
| `sched_v2_conservative` | Day35 primary scheduled candidate |

`fixed_AC0p7` was retained deliberately because it is the high-amplitude stress control needed to test whether a branch amplifies residual or risk behavior.

---

## 6. Parameterization audit

Chen2020 electrolyte transport parameters are callable functions:

- `Electrolyte diffusivity [m2.s-1]`
- `Electrolyte conductivity [S.m-1]`

The OCP functions are also callable:

- `Negative electrode OCP [V]`
- `Positive electrode OCP [V]`

However, no supported dynamic-OCP / hysteresis branch was identified for the current Chen2020 DFN setup.

Transport diagnostics implemented:

1. `transport_flattened`
   - replaces electrolyte diffusivity and conductivity with reference constants;
   - diagnostic branch only.

2. `transport_nonlinearity_amplified`
   - amplifies concentration dependence around a reference electrolyte concentration;
   - diagnostic stress test only.

These are not physical truth models.

---

## 7. Timing result

The timing result was decisive.

Across all runnable branches and all non-DC protocols:

```text
Δt_raw_mean ≈ Δt_geom_mean
Δt_resid_mean ≈ 0
```

All non-DC cases were classified as:

```text
geometry_dominated
```

The non-geometric candidate screen found:

```text
5 DC reference cases
15 non-DC cases with no_material_residual_acceleration
0 positive non-geometric acceleration candidates
```

Therefore:

> Day37 does not support stable, positive, engineering-significant non-geometric terminal-Q acceleration.

---

## 8. Branch-level residual synthesis

All branch-level residual verdicts were:

```text
no_positive_non_geometric_acceleration
```

This applies to:

- baseline default;
- double-layer differential;
- flattened electrolyte transport;
- amplified electrolyte transport nonlinearity;
- combined differential + amplified transport branch.

The result strengthens the Day30–Day36 conclusion: raw DC–AC timing gain is not converted into non-geometric terminal-Q acceleration by the audited missing-physics / parameterization branches.

---

## 9. Plating-margin and microstate effects

Day37 did not show that the branches are irrelevant.

Transport perturbations had a clear effect on plating-margin and microstate stress.

### 9.1 fixed AC0.38

| Branch | min U_NE | Margin class |
|---|---:|---|
| baseline | +0.57 mV | near-boundary |
| transport flattened | −1.15 mV | risk_flag |
| transport nonlinearity amplified | −4.10 mV | risk_flag |
| combined sensitivity | −4.09 mV | risk_flag |

### 9.2 fixed AC0.7

| Branch | min U_NE | Margin class |
|---|---:|---|
| baseline | −25.31 mV | risk_flag |
| transport flattened | −28.48 mV | risk_flag |
| transport nonlinearity amplified | −34.20 mV | risk_flag |
| combined sensitivity | −34.15 mV | risk_flag |

### 9.3 sched_v2_conservative

| Branch | min U_NE | Margin class |
|---|---:|---|
| baseline | +24.16 mV | near-boundary |
| transport flattened | +21.28 mV | near-boundary |
| transport nonlinearity amplified | +16.74 mV | near-boundary |
| combined sensitivity | +16.76 mV | near-boundary |

Interpretation:

> Transport parameterization affects admissibility and stress severity, not non-geometric terminal-Q acceleration.

---

## 10. Role of fixed AC0.7

The fixed `AC0.7` stress protocol was essential.

It showed that:

- high raw gain does not imply admissibility;
- high-amplitude fixed DC–AC remains hard-margin inadmissible across all branches;
- transport perturbations make the high-amplitude stress case more severe.

This supports the project direction away from “fastest protocol” and toward “admissible fast protocol.”

---

## 11. Role of sched_v2_conservative

`sched_v2_conservative` remains the preferred first-generation scheduled candidate within this matrix.

It remains above the 0 mV hard-margin proxy across all runnable branches, but its margin decreases under transport perturbation.

Interpretation:

> sched_v2 is more robust than fixed AC0.38 and fixed AC0.7, but it remains near-boundary and is not yet thermally or aging validated.

---

## 12. OCP / hysteresis status

Dynamic OCP / hysteresis remains deferred.

Day37 found callable OCP functions, but did not identify a supported PyBaMM / Chen2020 DFN model branch for dynamic OCP or hysteresis.

Therefore:

> The OCP / hysteresis hypothesis is not disproven. It is deferred due to lack of a supported model branch in the current audit.

This point must remain explicit in the claim review.

---

## 13. Main Day37 conclusion

Day37 supports the following conclusion:

> The audited missing-physics / parameterization branches do not create stable, positive, engineering-significant non-geometric terminal-Q acceleration. Double-layer dynamics, flattened transport, amplified transport nonlinearity, and the combined branch all remain geometry-dominated. These branches can substantially affect plating-margin and microstate-stress severity, especially under fixed high-amplitude DC–AC, but they do not turn raw timing gain into non-geometric terminal-Q acceleration.

---

## 14. What Day37 verified

Day37 verified that:

1. electrolyte diffusivity and conductivity are callable Chen2020 functions;
2. flattened and amplified transport diagnostic branches can be built and run;
3. double-layer differential branch can be included in the sensitivity matrix;
4. all runnable branches complete the mandatory four-protocol matrix;
5. no branch produces a positive non-geometric residual candidate;
6. transport branches materially affect U_NE margin and electrolyte-gradient stress;
7. fixed AC0.7 remains a necessary and informative stress control;
8. sched_v2 remains the preferred first-generation scheduled candidate, but with reduced margin under transport stress.

---

## 15. What Day37 did not prove

Day37 did not prove that:

1. non-geometric acceleration is impossible in all real cells;
2. dynamic OCP / hysteresis is irrelevant;
3. thermal coupling is irrelevant;
4. aging / degradation pathways are irrelevant;
5. the diagnostic transport branches are physical truth models;
6. sched_v2 is globally optimal;
7. any policy is experimentally plating-free.

---

## 16. Claim-review implication

Day37 provides enough evidence to write a formal claim review.

The claim review should state:

- supported: raw timing gain exists but is geometry-dominated;
- supported: DC–AC modifies microstate and plating-margin behavior;
- supported: state-aware scheduling improves hard-margin admissibility;
- unsupported: stable, positive, engineering-significant non-geometric terminal-Q acceleration in the current model class;
- deferred: dynamic OCP / hysteresis, thermal coupling, aging coupling, and experimental validation.

The next document should be:

```text
docs/non_geometric_acceleration_claim_review_after_day37.md
```
