# Day21A Closure Note — MJ1 Experimental Full-Protocol Segmentation Audit

Generated: `2026-05-07T10:05:09.483722+00:00`  
Git HEAD: `bf7514db35b9f4e407fb5f6a2942e519a27b0953`  
Notebook: `25_day21A_MJ1_experimental_segment_audit.ipynb`

## 1. Scope

Day21A audited the experimental MJ1 full-protocol DC–AC charging data for the 0.3C reference group:

- `0.3C DC`
- `0.3C + 0.7C 0.1τ`
- `0.3C + 0.7C 1τ`
- `0.3C + 0.7C 10τ`

The audit followed the frozen pre-registered contract in:

`/Users/louislu/pybamm-dcac-superimposed/data/day21A_audit_contract_schema_thresholds.json`

The audit uses strict-net signed current integration:

- no rectification
- no cumulative maximum
- first-passage time at equal `Q_net`
- Segment-A residual only in the shared prescribed-current region

## 2. Core MJ1 formal verdict

MJ1 formal verdict rows remain conservative:

```text
              protocol_pair evidence_status                    mechanism_verdict                           interpretation_class                     Q80_common_segment                     Q90_common_segment  dt_Q80_common_raw_s  dt_Q90_common_raw_s segment_A_above_floor_status                                                                                                                                                                                             caveat
0.3C DC vs 0.3C+0.7C 0.1tau       ambiguous ambiguous_defer_mechanism_commitment                   spike_or_transition_artifact            A_shared_prescribed_current B_voltage_boundary_control_state_split             0.196020           351.715593 spike_or_transition_artifact                                                                                     asymmetric_final_Q;diagnostic_prescribed_spike_fit_unreliable_not_mechanism_evidence;diagnostic_fit_unreliable
 0.3C DC vs 0.3C+0.7C 10tau       ambiguous ambiguous_defer_mechanism_commitment segmentA_above_floor_without_inwindow_A_anchor B_voltage_boundary_control_state_split B_voltage_boundary_control_state_split           489.591991           908.727014                  above_floor asymmetric_final_Q;segment_A_above_floor_without_inwindow_A_anchor;diagnostic_waveform_geometry_mismatch_with_localized_first_passage_spike;diagnostic_localized_first_passage_spike_after_fitting
  0.3C DC vs 0.3C+0.7C 1tau       ambiguous ambiguous_defer_mechanism_commitment segmentA_above_floor_without_inwindow_A_anchor B_voltage_boundary_control_state_split B_voltage_boundary_control_state_split           139.916741           476.912802                  above_floor                    segment_A_above_floor_without_inwindow_A_anchor;diagnostic_waveform_geometry_mismatch_with_localized_first_passage_spike;diagnostic_localized_first_passage_spike_after_fitting
```

All MJ1 formal mechanism verdicts remain:

`ambiguous_defer_mechanism_commitment`

This is not a failure of the audit. It is the expected conservative outcome because the formal prescribed-geometry Segment-A residual audit flags either spike-like behavior or above-floor prescribed residuals.

## 3. Diagnostic interpretation

Diagnostic synthesis shows:

```text
              protocol_pair segment_A_above_floor_status                                     diagnostic_interpretation fit_quality_status  dt_resid_prescribed_p95_abs_s  dt_resid_fitted_p95_abs_s  dt_resid_prescribed_max_abs_s  dt_resid_fitted_max_abs_s
0.3C DC vs 0.3C+0.7C 0.1tau spike_or_transition_artifact        prescribed_spike_fit_unreliable_not_mechanism_evidence     fit_unreliable                       3.696359                   9.331629                      28.685838                  11.080290
 0.3C DC vs 0.3C+0.7C 10tau                  above_floor waveform_geometry_mismatch_with_localized_first_passage_spike         fit_usable                      10.835425                   0.794760                     426.430441                 406.283756
  0.3C DC vs 0.3C+0.7C 1tau                  above_floor waveform_geometry_mismatch_with_localized_first_passage_spike         fit_usable                      39.534453                   1.151761                      42.929877                  45.093658
```

Interpretation:

- `0.1τ`: prescribed residual behaves as spike/transition artifact; fitted waveform diagnostic is unreliable, so it is not mechanism evidence.
- `1τ` and `10τ`: prescribed Segment-A residual is above-floor, but fitted-waveform geometry collapses p95 residuals below the MJ1 floor. Remaining large extrema are localized first-passage spikes.

Therefore, the above-floor prescribed residuals in `1τ` and `10τ` should not be interpreted as distributed non-geometric Segment-A acceleration.

## 4. MJ1 anchor placement

The key MJ1 anchor placement is:

- `1τ`: Q80/Q90 common anchors lie in Segment B.
- `10τ`: Q80/Q90 common anchors lie in Segment B.
- `0.1τ`: Q80 common lies in Segment A, Q90 common lies in Segment B.

Segment B means:

`DCAC already voltage-limited / AC-off / CV-coupled while DC remains in CC approaching Vmax`

This supports a boundary/control-state mediated reading for the main Q80/Q90 gains in `1τ` and `10τ`, but the formal MJ1 verdict remains conservative because Segment-A residual diagnostics introduce caveats.

## 5. PyBaMM Day20B comparison

Unified PyBaMM rows:

```text
cell_or_param_set                         evidence_status                                                                   mechanism_verdict                     Q80_common_segment                     Q90_common_segment  dt_Q80_common_raw_s  dt_Q90_common_raw_s                                                                                                                                                       caveat
         Chen2020                                   valid positive_full_protocol_raw_gain_boundary_control_state_split_not_Segment_A_residual B_voltage_boundary_control_state_split B_voltage_boundary_control_state_split          1088.331044          2110.724381                                                                source=PyBaMM_Day20B_full_protocol_batch;segment_A_residual_not_recomputed_in_unified_adapter
        OKane2022                                   valid positive_full_protocol_raw_gain_boundary_control_state_split_not_Segment_A_residual B_voltage_boundary_control_state_split B_voltage_boundary_control_state_split           789.649820          1799.411700                                                                source=PyBaMM_Day20B_full_protocol_batch;segment_A_residual_not_recomputed_in_unified_adapter
       ORegan2022 valid_with_CV_current_transient_warning positive_full_protocol_raw_gain_boundary_control_state_split_not_Segment_A_residual B_voltage_boundary_control_state_split B_voltage_boundary_control_state_split          3193.416041          4295.186706 source=PyBaMM_Day20B_full_protocol_batch;segment_A_residual_not_recomputed_in_unified_adapter;DCAC_CV_current_transient_warning;DCAC_CV_charge_above_CC_peak
```

PyBaMM Day20B supports:

`positive_full_protocol_raw_gain_boundary_control_state_split_not_Segment_A_residual`

across:

- Chen2020
- OKane2022
- ORegan2022

with Q80/Q90 common anchors located in Segment B.

ORegan2022 retains the caveat:

`DCAC_CV_current_transient_warning`

## 6. Unified interpretation

The unified MJ1–PyBaMM audit supports the following bounded interpretation:

The full-protocol first-passage gains are real in the measured/simulated trajectories, but they are not mechanism-pure. The dominant supported structure is a boundary/control-state mediated first-passage gain: DC–AC reaches the voltage boundary earlier, enters AC-off / voltage-limited / CV-coupled operation while the DC reference remains in CC, and the resulting advantage persists into late CV.

The audit does not support reopening Interpretation B as a demonstrated non-geometric Segment-A acceleration mechanism.

## 7. Allowed claims for JES2 §4

Allowed:

1. MJ1 exhibits real measured full-protocol state-equivalent first-passage gains at Q80/Q90.
2. In MJ1 `1τ` and `10τ`, Q80/Q90 common anchors lie in Segment B.
3. Segment B corresponds to boundary/control-state split: DC–AC is already voltage-limited while DC remains in CC.
4. Formal MJ1 verdict remains conservative and ambiguous because prescribed Segment-A residuals are above-floor or spike-like.
5. Diagnostic audits show the above-floor prescribed residuals in `1τ` and `10τ` collapse under fitted-waveform geometry except for localized first-passage spikes.
6. PyBaMM Day20B independently supports boundary/control-state mediated full-protocol gains across three parameter sets.

## 8. Prohibited claims

Do not claim:

1. MJ1 proves non-geometric Segment-A acceleration.
2. Segment-A residual above-floor in the prescribed geometry audit is direct electrochemical mechanism evidence.
3. PyBaMM proves the physical mechanism of MJ1.
4. All full-protocol gain is “just geometry”.
5. Event timing alone is equivalent to state advancement.
6. The fitted-waveform diagnostic redefines the formal residual threshold.

## 9. Key output files

- Inventory: `/Users/louislu/pybamm-dcac-superimposed/data/day21A_step0_MJ1_file_inventory.csv`
- Load sanity: `/Users/louislu/pybamm-dcac-superimposed/data/day21A_step1_MJ1_loaded_trajectory_sanity.csv`
- Event audit: `/Users/louislu/pybamm-dcac-superimposed/data/day21A_step2_MJ1_event_acoff_audit.csv`
- Q integration summary: `/Users/louislu/pybamm-dcac-superimposed/data/day21A_step3_MJ1_Q_integration_summary.csv`
- Final-Q pair audit: `/Users/louislu/pybamm-dcac-superimposed/data/day21A_step3_MJ1_finalQ_pair_audit.csv`
- Segment assignment: `/Users/louislu/pybamm-dcac-superimposed/data/day21A_step4_MJ1_segment_assignment.csv`
- Δt segment audit long: `/Users/louislu/pybamm-dcac-superimposed/data/day21A_step5_MJ1_dtQ_segment_audit_long.csv`
- Δt segment summary: `/Users/louislu/pybamm-dcac-superimposed/data/day21A_step5_MJ1_dtQ_segment_summary.csv`
- Residual diagnostics: `/Users/louislu/pybamm-dcac-superimposed/data/day21A_step5A_MJ1_segmentA_residual_diagnostics.csv`
- Branch-jump audit: `/Users/louislu/pybamm-dcac-superimposed/data/day21A_step5B_MJ1_geometry_branch_jump_audit.csv`
- Geometry fidelity summary: `/Users/louislu/pybamm-dcac-superimposed/data/day21A_step5C_MJ1_geometry_fidelity_summary.csv`
- Diagnostic synthesis: `/Users/louislu/pybamm-dcac-superimposed/data/day21A_step5E_MJ1_residual_diagnostic_synthesis.csv`
- MJ1 verdict: `/Users/louislu/pybamm-dcac-superimposed/data/day21A_step6_MJ1_mechanism_verdict.csv`
- Unified MJ1–PyBaMM verdict: `/Users/louislu/pybamm-dcac-superimposed/data/day21A_step7_unified_MJ1_PyBaMM_mechanism_verdict.csv`

## 10. Closure status

Day21A is closed.

Next recommended action:

Write JES2 §4 as a methodological upgrade:

`raw Δt(Q) is real but not mechanism-pure; full-protocol gains decompose into current geometry, voltage-boundary timing, control-state split, late-CV preservation, and possible residual terms. In the current MJ1 audit, non-geometric Segment-A acceleration is not supported, while boundary/control-state mediated first-passage gain is the preferred interpretation with diagnostic caveats.`