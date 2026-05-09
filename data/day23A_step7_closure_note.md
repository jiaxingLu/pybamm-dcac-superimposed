# Day23A Closure Note — MJ1 0.4C Sub-DC-Amplitude Protocol-Mode Audit

Generated: `2026-05-09T10:32:34.071560+00:00`
Git HEAD: `70e8d6a405ec267f566bab1d7fa4829900b7826d`
Notebook: `27_day23A_MJ1_0p4C_subDC_1tau_audit.ipynb`

## 1. Scope

Day23A audits the MJ1 0.4C group under fixed 1τ excitation where the AC amplitude is smaller than the DC component.

Active protocols:

- `0.4C DC`
- `0.4C + 0.1C 1τ`, κ = 0.25
- `0.4C + 0.3C 1τ`, κ = 0.75

Excluded protocol:

- `0.4C + 0.2C 1τ`, κ = 0.50

The excluded record lacks the required pre-Vmax CC segment and cannot support Q_Vmax extraction, first-passage comparison, or boundary-region assignment.

## 2. Exclusion registry

```text
                      file_name protocol_label protocol_role  use_for_audit        exclusion_status
                    0.4C DC.csv        0.4C DC  DC_reference           True                  active
   DC0.4C+AC0.2C f=0.0143Hz.csv 0.4C+0.2C 1tau          DCAC          False excluded_missing_CC_raw
   DC0.4C+AC0.3C f=0.0143Hz.csv 0.4C+0.3C 1tau          DCAC           True                  active
处理后DC0.4C+AC0.1C f=0.0143Hz.csv 0.4C+0.1C 1tau          DCAC           True                  active
```

## 3. Protocol-mode decision

Before applying Day21A/Day22A segmentation logic, Day23A audited whether the DC–AC protocols switch off AC after first reaching 4.2 V.

The audit showed that both active DC–AC files retain substantial fixed-frequency current components after Vmax.

Therefore, the original Day21A/Day22A AC-off Segment A/B/D framework is disabled.

```text
                  group_id                                  notebook  n_active_DCAC  n_AC_off_after_Vmax_supported  n_possible_full_DCAC_after_Vmax  n_ambiguous_or_unresolved                  day23a_framework_mode  generalized_boundary_framework_required   downstream_segmentation_rule  original_A_B_D_framework_allowed                                                                                                                                                                                              decision_reason
Day23A_MJ1_0p4C_subDC_1tau 27_day23A_MJ1_0p4C_subDC_1tau_audit.ipynb              2                              0                                2                          0 generalized_boundary_ordering_required                                     True use_G0_G1_G2_boundary_ordering                             False At least one active DCAC file retains substantial fixed-frequency current component after Vmax. Day21A/Day22A AC-off Segment B assumption is not valid. Use generalized boundary-ordering framework instead.
```

Day23A uses a generalized G0/G1/G2 boundary-ordering framework instead.

## 4. Generalized boundary-ordering framework

The generalized regions are:

- `G0`: shared pre-boundary region, Q <= min(Q_DC,Vmax, Q_DCAC,Vmax)
- `G1`: boundary-ordering split region, min(Q_DC,Vmax, Q_DCAC,Vmax) < Q <= max(Q_DC,Vmax, Q_DCAC,Vmax)
- `G2`: post-boundary region, Q > max(Q_DC,Vmax, Q_DCAC,Vmax)

Geometry-corrected residuals are only meaningful in G0.

G1 and G2 are not equivalent to Day21A/Day22A Segment B/D because AC continues after Vmax in Day23A.

## 5. Boundary-ordering result

```text
            protocol_pair  kappa  Q_Vmax_DC_Ah  Q_Vmax_DCAC_Ah  Q_Vmax_shift_Ah_DC_minus_DCAC boundary_ordering_by_Q      Q80_common_region Q90_common_region      Q_final_diff_status
0.4C DC vs 0.4C+0.3C 1tau   0.75      2.882411        2.729392                       0.153019             DCAC_first G0_shared_pre_boundary  G2_post_boundary final_Q_mismatch_warning
0.4C DC vs 0.4C+0.1C 1tau   0.25      2.882411        2.833590                       0.048821             DCAC_first G0_shared_pre_boundary  G2_post_boundary       final_Q_consistent
```

Both active DC–AC protocols are DCAC-first by Q. Thus, even with AC_C < DC_C, the DC–AC trajectory reaches the 4.2 V boundary at lower Q than the DC reference.

The Q_Vmax shift is amplitude-dependent:

- κ = 0.25: Q shift ≈ 0.049 Ah
- κ = 0.75: Q shift ≈ 0.153 Ah

This supports a boundary-shift effect that scales with excitation strength, but not necessarily a gain-preserving full-protocol advantage.

## 6. Self-consistency audit-resolution estimate

Day23A uses a DC self-consistency lower-bound estimate from the 0.4C DC reference.

```text
                                 source dc_reference_file  n_Q_grid  Q_lo_Ah  Q_hi_Ah  Q_grid_step_Ah  dt_even_minus_odd_mean_s  dt_even_minus_odd_median_s  dt_even_minus_odd_p95_abs_s  dt_even_minus_odd_max_abs_s  dt_full_minus_even_p95_abs_s  dt_full_minus_even_max_abs_s  dt_full_minus_odd_p95_abs_s  dt_full_minus_odd_max_abs_s  day23A_self_consistency_resolution_p95_s  day23A_self_consistency_resolution_max_s  repeat_based_noise_floor_available                                                                       floor_scope  formal_disappearance_claim_allowed
0.4C_DC_self_consistency_even_odd_split       0.4C DC.csv       328     0.05     3.32            0.01                 -0.905408                   -0.758032                     1.371917                    10.223522                       0.24068                       1.76651                     1.612597                    11.990032                                  1.612597                                 11.990032                               False lower_bound_for_sampling_interpolation_first_passage_resolution_not_repeatability                               False
```

This is a lower-bound estimate for sampling, interpolation, and first-passage sensitivity. It is not a repeat-based experimental noise floor.

## 7. Formal generalized verdict

```text
            protocol_pair  kappa    evidence_status                                            mechanism_verdict                     interpretation_class boundary_ordering_by_Q     protocol_mode_status_DCAC      Q80_common_region Q90_common_region  dt_Q80_common_raw_s  dt_Q90_common_raw_s                     Q80_raw_resolution_status                     Q90_raw_resolution_status                              G0_residual_status  G0_dt_resid_p95_abs_s  G0_dt_resid_fit_p95_abs_s                          audit_resolution_status                     fitted_resolution_status      Q_final_diff_status                                                                                                                                                                                                                                                                                                                                                                                          caveat
0.4C DC vs 0.4C+0.3C 1tau   0.75              mixed      boundary_leading_with_G0_gain_but_post_boundary_penalty     boundary_leading_not_gain_preserving             DCAC_first possible_full_DCAC_after_Vmax G0_shared_pre_boundary  G2_post_boundary            11.038715           -86.013556          raw_anchor_positive_above_resolution          raw_anchor_negative_above_resolution                                     above_floor              12.291571                  44.952961 prescribed_p95_above_self_consistency_resolution fitted_p95_above_self_consistency_resolution final_Q_mismatch_warning                  continued_AC_after_Vmax;not_same_protocol_family_as_Day21A_Day22A;temperature_summary_missing;no_independent_repeat_based_experimental_noise_floor;effect_size_interpreted_relative_to_audit_resolution_not_strict_disappearance;final_Q_mismatch_warning;G0_prescribed_residual_above_floor;fitted_G0_residual_above_self_consistency_resolution;Q90_common_negative_raw_gain
0.4C DC vs 0.4C+0.1C 1tau   0.25 weak_or_unresolved boundary_leading_but_state_gain_unresolved_at_common_anchors subDC_small_perturbation_near_resolution             DCAC_first possible_full_DCAC_after_Vmax G0_shared_pre_boundary  G2_post_boundary             0.633266             0.567340 raw_anchor_within_self_consistency_resolution raw_anchor_within_self_consistency_resolution intermediate_between_floor_and_reopen_threshold               3.442625                  11.463178 prescribed_p95_above_self_consistency_resolution fitted_p95_above_self_consistency_resolution       final_Q_consistent continued_AC_after_Vmax;not_same_protocol_family_as_Day21A_Day22A;temperature_summary_missing;no_independent_repeat_based_experimental_noise_floor;effect_size_interpreted_relative_to_audit_resolution_not_strict_disappearance;G0_prescribed_residual_intermediate;fitted_G0_residual_above_self_consistency_resolution;Q80_common_within_audit_resolution;Q90_common_within_audit_resolution
```

## 8. Interpretation

For κ = 0.75, Day23A shows a mixed pattern: DC–AC reaches the voltage boundary earlier and has a positive Q80_common raw gain in G0, but Q90_common is negative and the G2 median raw Δt is also negative. This is classified as boundary-leading with G0 gain but post-boundary penalty.

For κ = 0.25, both Q80_common and Q90_common raw gains are within the Day23A self-consistency resolution. This is classified as boundary-leading but state-gain unresolved at common anchors.

Therefore, Day23A does not support a persistent full-protocol gain under sub-DC AC amplitude. It also does not confirm non-geometric G0 electrochemical acceleration.

## 9. Relation to Day21A and Day22A

Day23A is not directly comparable to Day21A/Day22A as the same protocol family.

Day21A and Day22A used an AC-off-after-Vmax protocol assumption:

- DC–AC applied during CC
- AC switched off at first Vmax
- post-Vmax region interpreted as AC-off voltage-boundary / CV-coupled behavior

Day23A violates this protocol assumption because AC continues after Vmax.

Thus, Day23A is best interpreted as a protocol-mode contrast:

- sub-DC AC amplitude
- fixed 1τ excitation
- continued AC after Vmax
- generalized boundary-ordering instead of AC-off segmentation

## 10. Allowed claims

Allowed:

1. Day23A confirms that both active sub-DC AC protocols are DCAC-first by Q.
2. The boundary shift increases from κ = 0.25 to κ = 0.75.
3. κ = 0.25 produces only unresolved common-anchor state gain within audit resolution.
4. κ = 0.75 produces early G0 gain but loses the advantage at Q90/G2.
5. Day23A demonstrates that boundary-leading does not necessarily imply gain preservation.
6. Day23A is a different protocol-mode family from Day21A/Day22A due to continued AC after Vmax.

## 11. Prohibited claims

Do not claim:

1. Day23A proves non-geometric G0 electrochemical acceleration.
2. Day23A is directly comparable to Day21A/Day22A as an identical AC-off protocol.
3. Day23A proves disappearance of DC–AC effects.
4. G2 raw gain or penalty is late-CV preservation in the Day21A/Day22A sense.
5. Temperature effects can be quantified; temperature summaries are missing.

## 12. Key output files

- Raw format inventory: `/Users/louislu/pybamm-dcac-superimposed/data/day23A_step0A_raw_csv_format_inventory.csv`
- Exclusion audit: `/Users/louislu/pybamm-dcac-superimposed/data/day23A_step0A5_file_exclusion_audit.csv`
- Active inventory: `/Users/louislu/pybamm-dcac-superimposed/data/day23A_step0A5_active_raw_csv_format_inventory.csv`
- Timebase audit: `/Users/louislu/pybamm-dcac-superimposed/data/day23A_step0B_timebase_audit.csv`
- Protocol-mode audit: `/Users/louislu/pybamm-dcac-superimposed/data/day23A_step0C_protocol_mode_acoff_audit.csv`
- Framework decision: `/Users/louislu/pybamm-dcac-superimposed/data/day23A_step0D_framework_decision.csv`
- Audit contract: `/Users/louislu/pybamm-dcac-superimposed/data/day23A_audit_contract_schema_thresholds.json`
- File inventory: `/Users/louislu/pybamm-dcac-superimposed/data/day23A_step0_MJ1_0p4C_subDC_file_inventory.csv`
- Load sanity: `/Users/louislu/pybamm-dcac-superimposed/data/day23A_step1_MJ1_0p4C_subDC_loaded_trajectory_sanity.csv`
- Event audit: `/Users/louislu/pybamm-dcac-superimposed/data/day23A_step2_MJ1_0p4C_subDC_event_protocol_boundary_audit.csv`
- Q integration summary: `/Users/louislu/pybamm-dcac-superimposed/data/day23A_step3_MJ1_0p4C_subDC_Q_integration_summary.csv`
- Final-Q audit: `/Users/louislu/pybamm-dcac-superimposed/data/day23A_step3_MJ1_0p4C_subDC_finalQ_pair_audit.csv`
- Resolution summary: `/Users/louislu/pybamm-dcac-superimposed/data/day23A_step3A_MJ1_0p4C_subDC_resolution_floor_summary.csv`
- G0/G1/G2 assignment: `/Users/louislu/pybamm-dcac-superimposed/data/day23A_step4_MJ1_0p4C_subDC_G0G1G2_assignment.csv`
- Δt summary: `/Users/louislu/pybamm-dcac-superimposed/data/day23A_step5_MJ1_0p4C_subDC_dtQ_Gregion_summary.csv`
- Generalized verdict: `/Users/louislu/pybamm-dcac-superimposed/data/day23A_step6_MJ1_0p4C_subDC_generalized_verdict.csv`
- Closure CSV: `/Users/louislu/pybamm-dcac-superimposed/data/day23A_step7_closure_summary.csv`

## 13. Closure status

Day23A is closed as a generalized sub-DC-amplitude protocol-mode audit.

Next recommended step:

Commit Day23A notebook and audit outputs, excluding raw CSV files.