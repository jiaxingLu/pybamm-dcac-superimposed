# Day22A Closure Note — MJ1 Low-Amplitude Full-Protocol Audit

Generated: `2026-05-09T09:03:47.056035+00:00`
Git HEAD: `c40e2dc2748b55e3f63f25101723ae13eaf65211`
Notebook: `26_day22A_MJ1_low_amplitude_0p3C_0p4C_audit.ipynb`

## 1. Scope

Day22A applies the Day21A full-protocol segmentation audit to a low-amplitude MJ1 group:

- `0.3C DC`
- `0.3C + 0.4C 0.1τ`
- `0.3C + 0.4C 1τ`
- `0.3C + 0.4C 10τ`

The purpose is to test whether the boundary/control-state mediated first-passage gains observed in the `0.3C + 0.7C` group weaken, remain above audit resolution, or become unresolved at lower AC amplitude.

Day22A does not claim strict disappearance because no independent repeat-based experimental noise floor is available.

## 2. Data format and timebase

Day22A includes mixed CSV formats:

- `0.1τ` and `10τ`: processed 1 Hz aligned CSV without NGU201 metadata
- `1τ` and `0.3C DC`: NGU201 LOG raw format

All files passed timebase audit with monotonic parsed or unwrapped timestamps.

## 3. Final-Q consistency

```text
              protocol_pair  Q_final_DC_Ah  Q_final_DCAC_Ah  Q_final_diff_mAh Q_final_diff_status
0.3C DC vs 0.3C+0.4C 0.1tau       3.259324         3.255150          4.174398  final_Q_consistent
 0.3C DC vs 0.3C+0.4C 10tau       3.259324         3.252939          6.384911  final_Q_consistent
  0.3C DC vs 0.3C+0.4C 1tau       3.259324         3.259023          0.300920  final_Q_consistent
```

All Day22A pairs are `final_Q_consistent`. No asymmetric final-Q caveat is required.

## 4. Experimental audit-resolution estimate

Day22A uses a DC self-consistency lower-bound floor, obtained from the `0.3C DC` reference by even/odd row splitting.

```text
                                 source          dc_reference_file  n_Q_grid  Q_lo_Ah  Q_hi_Ah  Q_grid_step_Ah  dt_even_minus_odd_mean_s  dt_even_minus_odd_median_s  dt_even_minus_odd_p95_abs_s  dt_even_minus_odd_max_abs_s  dt_full_minus_even_p95_abs_s  dt_full_minus_even_max_abs_s  dt_full_minus_odd_p95_abs_s  dt_full_minus_odd_max_abs_s  day22A_self_consistency_resolution_p95_s  day22A_self_consistency_resolution_max_s  repeat_based_noise_floor_available                                                                       floor_scope  formal_disappearance_claim_allowed
0.3C_DC_self_consistency_even_odd_split MJ1_0p3C_DC_NGU201_raw.csv       320     0.05     3.24            0.01                 -1.111225                   -1.000018                     1.414811                     8.157069                      0.006236                      0.099809                     1.408893                     8.256878                                  1.414811                                  8.256878                               False lower_bound_for_sampling_interpolation_first_passage_resolution_not_repeatability                               False
```

This is a lower-bound audit-resolution estimate for sampling, interpolation, and first-passage sensitivity. It is not a repeat-based experimental noise floor.

## 5. Segment assignment

```text
              protocol_pair  Q_Vmax_DC_Ah  Q_Vmax_DCAC_Ah  Q_Vmax_shift_Ah          Q80_common_segment                     Q90_common_segment                    Q80_nominal_segment Q90_nominal_segment
0.3C DC vs 0.3C+0.4C 0.1tau      2.962785        2.692758         0.270027 A_shared_prescribed_current B_voltage_boundary_control_state_split B_voltage_boundary_control_state_split  D_late_CV_feedback
 0.3C DC vs 0.3C+0.4C 10tau      2.962785        2.635191         0.327594 A_shared_prescribed_current B_voltage_boundary_control_state_split B_voltage_boundary_control_state_split  D_late_CV_feedback
  0.3C DC vs 0.3C+0.4C 1tau      2.962785        2.683744         0.279041 A_shared_prescribed_current B_voltage_boundary_control_state_split B_voltage_boundary_control_state_split  D_late_CV_feedback
```

The key Day22A structural result is:

- `Q80_common` lies in Segment A for all 0.3C+0.4C protocols.
- `Q90_common` lies in Segment B for all 0.3C+0.4C protocols.

This differs from Day21A `0.3C+0.7C`, where `1τ` and `10τ` had both Q80/Q90 common anchors in Segment B.

## 6. Formal verdict

```text
              protocol_pair                        evidence_status                                                   mechanism_verdict                                           interpretation_class          Q80_common_segment                     Q90_common_segment  dt_Q80_common_raw_s  dt_Q90_common_raw_s                    segment_A_above_floor_status  segment_A_dt_resid_p95_abs_s  segment_A_dt_resid_fit_p95_abs_s                          audit_resolution_status                              fitted_resolution_status                                                                                                                                                                                                                                                                                                                                      caveat
0.3C DC vs 0.3C+0.4C 0.1tau                              ambiguous                ambiguous_intermediate_prescribed_segment_A_residual         intermediate_prescribed_residual_near_audit_resolution A_shared_prescribed_current B_voltage_boundary_control_state_split             2.786872           186.719737 intermediate_between_floor_and_reopen_threshold                      2.423034                          2.849798 prescribed_p95_above_self_consistency_resolution          fitted_p95_above_self_consistency_resolution                                                   no_independent_repeat_based_experimental_noise_floor;effect_size_interpreted_relative_to_audit_resolution_not_strict_disappearance;prescribed_p95_above_self_consistency_resolution;diagnostic_fit_unreliable;diagnostic_fitted_p95_above_audit_resolution;late_CV_preservation_satisfied
 0.3C DC vs 0.3C+0.4C 10tau formal_reopened_with_diagnostic_caveat interpretation_B_formally_reopened_by_prescribed_segment_A_residual formal_prescribed_segment_A_above_floor_with_inwindow_A_anchor A_shared_prescribed_current B_voltage_boundary_control_state_split            26.556610           351.690383                                     above_floor                      9.966160                          0.930821 prescribed_p95_above_self_consistency_resolution fitted_p95_below_or_equal_self_consistency_resolution no_independent_repeat_based_experimental_noise_floor;effect_size_interpreted_relative_to_audit_resolution_not_strict_disappearance;prescribed_p95_above_self_consistency_resolution;diagnostic_fit_usable;diagnostic_fitted_p95_below_or_equal_audit_resolution;diagnostic_waveform_geometry_mismatch_likely;late_CV_preservation_satisfied
  0.3C DC vs 0.3C+0.4C 1tau formal_reopened_with_diagnostic_caveat interpretation_B_formally_reopened_by_prescribed_segment_A_residual formal_prescribed_segment_A_above_floor_with_inwindow_A_anchor A_shared_prescribed_current B_voltage_boundary_control_state_split            18.150097           215.849425                                     above_floor                     26.314894                          0.868957 prescribed_p95_above_self_consistency_resolution fitted_p95_below_or_equal_self_consistency_resolution no_independent_repeat_based_experimental_noise_floor;effect_size_interpreted_relative_to_audit_resolution_not_strict_disappearance;prescribed_p95_above_self_consistency_resolution;diagnostic_fit_usable;diagnostic_fitted_p95_below_or_equal_audit_resolution;diagnostic_waveform_geometry_mismatch_likely;late_CV_preservation_satisfied
```

Day22A formal verdicts must be interpreted with low-amplitude audit-resolution caveats.

For `1τ` and `10τ`, the formal prescribed-geometry audit reopens Segment-A residual because Q80_common lies in Segment A and prescribed residual p95 exceeds the audit floor. However, fitted-waveform diagnostics reduce the p95 residual below the Day22A self-consistency resolution, indicating waveform-geometry mismatch / first-passage sensitivity rather than a confirmed non-geometric electrochemical mechanism.

For `0.1τ`, the formal residual is intermediate and the fitted waveform diagnostic is unreliable. It is not mechanism evidence.

## 7. Comparison with Day21A

Compared with the Day21A `0.3C+0.7C` group, Day22A shows:

- smaller full-protocol first-passage gains at Q80/Q90 common anchors
- weaker voltage-boundary shift
- Q80_common moving from Segment B to Segment A
- no strict evidence for disappearance
- no confirmed non-geometric Segment-A acceleration mechanism

The low-amplitude result supports amplitude sensitivity of the boundary/control-state gain pathway, but within the current audit it cannot prove disappearance of the effect.

## 8. Allowed claims

Allowed:

1. Lower AC amplitude reduces Q80/Q90 common first-passage gains relative to Day21A.
2. In Day22A, Q80_common remains in Segment A, while Q90_common lies in Segment B.
3. Day22A formal Segment-A residual is above-floor for 1τ and 10τ under prescribed geometry.
4. Fitted-waveform diagnostics collapse the p95 residual below self-consistency resolution for 1τ and 10τ.
5. Day22A does not support a confirmed non-geometric Segment-A mechanism.
6. The effect cannot be said to disappear without repeat-based noise-floor evidence.

## 9. Prohibited claims

Do not claim:

1. Low-amplitude DC–AC effect disappears.
2. Day22A proves non-geometric Segment-A acceleration.
3. Fitted-waveform residual replaces the formal prescribed-geometry residual.
4. PyBaMM numerical floor is applicable as MJ1 experimental noise floor.
5. Small residuals prove persistence of a mechanism.

## 10. Key output files

- Raw CSV format inventory: `/Users/louislu/pybamm-dcac-superimposed/data/day22A_step0A_raw_csv_format_inventory.csv`
- Timebase audit: `/Users/louislu/pybamm-dcac-superimposed/data/day22A_step0B_timebase_audit.csv`
- File inventory: `/Users/louislu/pybamm-dcac-superimposed/data/day22A_step0_MJ1_0p3C_0p4C_file_inventory.csv`
- Load sanity: `/Users/louislu/pybamm-dcac-superimposed/data/day22A_step1_MJ1_0p3C_0p4C_loaded_trajectory_sanity.csv`
- Event audit: `/Users/louislu/pybamm-dcac-superimposed/data/day22A_step2_MJ1_0p3C_0p4C_event_acoff_audit.csv`
- Q integration summary: `/Users/louislu/pybamm-dcac-superimposed/data/day22A_step3_MJ1_0p3C_0p4C_Q_integration_summary.csv`
- Final-Q pair audit: `/Users/louislu/pybamm-dcac-superimposed/data/day22A_step3_MJ1_0p3C_0p4C_finalQ_pair_audit.csv`
- Resolution floor summary: `/Users/louislu/pybamm-dcac-superimposed/data/day22A_step3A_MJ1_0p3C_0p4C_resolution_floor_summary.csv`
- Segment assignment: `/Users/louislu/pybamm-dcac-superimposed/data/day22A_step4_MJ1_0p3C_0p4C_segment_assignment.csv`
- Δt summary: `/Users/louislu/pybamm-dcac-superimposed/data/day22A_step5_MJ1_0p3C_0p4C_dtQ_segment_summary.csv`
- Verdict: `/Users/louislu/pybamm-dcac-superimposed/data/day22A_step6_MJ1_0p3C_0p4C_mechanism_verdict.csv`

## 11. Closure status

Day22A is closed as a low-amplitude audit.

Next recommended step:

Commit Day22A notebook and audit outputs, excluding raw CSV files.