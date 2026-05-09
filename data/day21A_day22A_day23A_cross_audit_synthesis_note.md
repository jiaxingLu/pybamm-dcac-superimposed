# Day21A–Day23A Cross-Audit Synthesis

Generated: `2026-05-09T10:43:36.115861+00:00`
Git HEAD: `d255cd1dbd4598d6e2a499864a1aca37c3dd7cb9`
Notebook: `28_day21A_day22A_day23A_cross_audit_synthesis.ipynb`

## Key conclusion

The Day21A–Day23A audits jointly show that earlier Vmax triggering under DC–AC excitation can be a real boundary event. However, boundary-leading does not automatically imply full-protocol state-equivalent gain preservation, and it does not constitute confirmed non-geometric Segment-A/G0 electrochemical acceleration.

## 1. Scope

This note synthesizes the closed MJ1 experimental audits Day21A, Day22A, and Day23A.

The purpose is to compare already-closed audit results. No trajectory, Q integration, event timing, Δt(Q), or verdict is recomputed here.

## 2. Included audit branches

### Day21A

- Protocol family: AC-off after Vmax
- Framework: A/B/D AC-off segmentation
- Group: 0.3C DC vs 0.3C + 0.7C
- κ = 2.33
- Frequencies: 0.1τ, 1τ, 10τ

### Day22A

- Protocol family: AC-off after Vmax
- Framework: A/B/D AC-off segmentation
- Group: 0.3C DC vs 0.3C + 0.4C
- κ = 1.33
- Frequencies: 0.1τ, 1τ, 10τ

### Day23A

- Protocol family: continued AC after Vmax
- Framework: G0/G1/G2 generalized boundary ordering
- Group: 0.4C DC vs 0.4C + 0.1C / 0.4C + 0.3C
- κ = 0.25 and 0.75
- Frequency: fixed 1τ
- 0.4C + 0.2C excluded due to missing pre-Vmax CC raw segment

## 3. Main MJ1 experimental synthesis table

```text
audit_day               protocol_pair         protocol_family  DC_C  AC_C    kappa  m_tau AC_off_after_Vmax_status boundary_ordering_by_Q  Q_Vmax_shift_Ah_DC_minus_DCAC                      Q80_common_region                      Q90_common_region  dt_Q80_common_raw_s  dt_Q90_common_raw_s                                                   mechanism_verdict                                  synthesis_interpretation
   Day21A 0.3C DC vs 0.3C+0.7C 0.1tau       AC_off_after_Vmax   0.3   0.7 2.333333    0.1       supported_by_audit             DCAC_first                       0.288741            A_shared_prescribed_current B_voltage_boundary_control_state_split             0.196020           351.715593                                ambiguous_defer_mechanism_commitment              mixed_A_to_B_transition_under_high_amplitude
   Day21A   0.3C DC vs 0.3C+0.7C 1tau       AC_off_after_Vmax   0.3   0.7 2.333333    1.0       supported_by_audit             DCAC_first                       0.412826 B_voltage_boundary_control_state_split B_voltage_boundary_control_state_split           139.916741           476.912802                                ambiguous_defer_mechanism_commitment     high_amplitude_AC_off_boundary_control_state_dominant
   Day21A  0.3C DC vs 0.3C+0.7C 10tau       AC_off_after_Vmax   0.3   0.7 2.333333   10.0       supported_by_audit             DCAC_first                       0.472544 B_voltage_boundary_control_state_split B_voltage_boundary_control_state_split           489.591991           908.727014                                ambiguous_defer_mechanism_commitment     high_amplitude_AC_off_boundary_control_state_dominant
   Day22A 0.3C DC vs 0.3C+0.4C 0.1tau       AC_off_after_Vmax   0.3   0.4 1.333333    0.1       supported_by_audit             DCAC_first                       0.270027            A_shared_prescribed_current B_voltage_boundary_control_state_split             2.786872           186.719737                ambiguous_intermediate_prescribed_segment_A_residual lower_amplitude_weakens_boundary_pathway_Q80_returns_to_A
   Day22A   0.3C DC vs 0.3C+0.4C 1tau       AC_off_after_Vmax   0.3   0.4 1.333333    1.0       supported_by_audit             DCAC_first                       0.279041            A_shared_prescribed_current B_voltage_boundary_control_state_split            18.150097           215.849425 interpretation_B_formally_reopened_by_prescribed_segment_A_residual lower_amplitude_weakens_boundary_pathway_Q80_returns_to_A
   Day22A  0.3C DC vs 0.3C+0.4C 10tau       AC_off_after_Vmax   0.3   0.4 1.333333   10.0       supported_by_audit             DCAC_first                       0.327594            A_shared_prescribed_current B_voltage_boundary_control_state_split            26.556610           351.690383 interpretation_B_formally_reopened_by_prescribed_segment_A_residual lower_amplitude_weakens_boundary_pathway_Q80_returns_to_A
   Day23A   0.4C DC vs 0.4C+0.1C 1tau continued_AC_after_Vmax   0.4   0.1 0.250000    1.0            not_supported             DCAC_first                       0.048821                 G0_shared_pre_boundary                       G2_post_boundary             0.633266             0.567340        boundary_leading_but_state_gain_unresolved_at_common_anchors        continued_AC_subDC_gain_unresolved_near_resolution
   Day23A   0.4C DC vs 0.4C+0.3C 1tau continued_AC_after_Vmax   0.4   0.3 0.750000    1.0            not_supported             DCAC_first                       0.153019                 G0_shared_pre_boundary                       G2_post_boundary            11.038715           -86.013556             boundary_leading_with_G0_gain_but_post_boundary_penalty     continued_AC_boundary_leading_but_not_gain_preserving
```

## 4. Day-level summaries

### Day21A — high-amplitude AC-off protocol family

```text
audit_day               protocol_pair   protocol_family  DC_C  AC_C    kappa  m_tau AC_off_after_Vmax_status boundary_ordering_by_Q  Q_Vmax_shift_Ah_DC_minus_DCAC                      Q80_common_region                      Q90_common_region  dt_Q80_common_raw_s  dt_Q90_common_raw_s                    mechanism_verdict                              synthesis_interpretation
   Day21A 0.3C DC vs 0.3C+0.7C 0.1tau AC_off_after_Vmax   0.3   0.7 2.333333    0.1       supported_by_audit             DCAC_first                       0.288741            A_shared_prescribed_current B_voltage_boundary_control_state_split             0.196020           351.715593 ambiguous_defer_mechanism_commitment          mixed_A_to_B_transition_under_high_amplitude
   Day21A   0.3C DC vs 0.3C+0.7C 1tau AC_off_after_Vmax   0.3   0.7 2.333333    1.0       supported_by_audit             DCAC_first                       0.412826 B_voltage_boundary_control_state_split B_voltage_boundary_control_state_split           139.916741           476.912802 ambiguous_defer_mechanism_commitment high_amplitude_AC_off_boundary_control_state_dominant
   Day21A  0.3C DC vs 0.3C+0.7C 10tau AC_off_after_Vmax   0.3   0.7 2.333333   10.0       supported_by_audit             DCAC_first                       0.472544 B_voltage_boundary_control_state_split B_voltage_boundary_control_state_split           489.591991           908.727014 ambiguous_defer_mechanism_commitment high_amplitude_AC_off_boundary_control_state_dominant
```

Day21A shows that high-amplitude AC-off protocols are DCAC-first by Q. For 1τ and 10τ, both Q80_common and Q90_common lie in the boundary/control-state split region. The full-protocol raw gains are therefore best interpreted as boundary/control-state mediated rather than confirmed Segment-A non-geometric acceleration.

### Day22A — lower-amplitude AC-off protocol family

```text
audit_day               protocol_pair   protocol_family  DC_C  AC_C    kappa  m_tau AC_off_after_Vmax_status boundary_ordering_by_Q  Q_Vmax_shift_Ah_DC_minus_DCAC           Q80_common_region                      Q90_common_region  dt_Q80_common_raw_s  dt_Q90_common_raw_s                                                   mechanism_verdict                                  synthesis_interpretation
   Day22A 0.3C DC vs 0.3C+0.4C 0.1tau AC_off_after_Vmax   0.3   0.4 1.333333    0.1       supported_by_audit             DCAC_first                       0.270027 A_shared_prescribed_current B_voltage_boundary_control_state_split             2.786872           186.719737                ambiguous_intermediate_prescribed_segment_A_residual lower_amplitude_weakens_boundary_pathway_Q80_returns_to_A
   Day22A   0.3C DC vs 0.3C+0.4C 1tau AC_off_after_Vmax   0.3   0.4 1.333333    1.0       supported_by_audit             DCAC_first                       0.279041 A_shared_prescribed_current B_voltage_boundary_control_state_split            18.150097           215.849425 interpretation_B_formally_reopened_by_prescribed_segment_A_residual lower_amplitude_weakens_boundary_pathway_Q80_returns_to_A
   Day22A  0.3C DC vs 0.3C+0.4C 10tau AC_off_after_Vmax   0.3   0.4 1.333333   10.0       supported_by_audit             DCAC_first                       0.327594 A_shared_prescribed_current B_voltage_boundary_control_state_split            26.556610           351.690383 interpretation_B_formally_reopened_by_prescribed_segment_A_residual lower_amplitude_weakens_boundary_pathway_Q80_returns_to_A
```

Day22A shows that lowering AC amplitude weakens the boundary pathway. Q80_common returns to the shared prescribed-current region, while Q90_common remains in the boundary/control-state split region. The effect is reduced but not strictly absent.

### Day23A — sub-DC-amplitude continued-AC protocol-mode contrast

```text
audit_day             protocol_pair         protocol_family  DC_C  AC_C  kappa  m_tau AC_off_after_Vmax_status boundary_ordering_by_Q  Q_Vmax_shift_Ah_DC_minus_DCAC      Q80_common_region Q90_common_region  dt_Q80_common_raw_s  dt_Q90_common_raw_s                                            mechanism_verdict                              synthesis_interpretation
   Day23A 0.4C DC vs 0.4C+0.1C 1tau continued_AC_after_Vmax   0.4   0.1   0.25    1.0            not_supported             DCAC_first                       0.048821 G0_shared_pre_boundary  G2_post_boundary             0.633266             0.567340 boundary_leading_but_state_gain_unresolved_at_common_anchors    continued_AC_subDC_gain_unresolved_near_resolution
   Day23A 0.4C DC vs 0.4C+0.3C 1tau continued_AC_after_Vmax   0.4   0.3   0.75    1.0            not_supported             DCAC_first                       0.153019 G0_shared_pre_boundary  G2_post_boundary            11.038715           -86.013556      boundary_leading_with_G0_gain_but_post_boundary_penalty continued_AC_boundary_leading_but_not_gain_preserving
```

Day23A is not the same protocol family as Day21A/Day22A. AC continues after Vmax, so the original A/B/D AC-off segmentation is disabled. Day23A uses G0/G1/G2 generalized boundary ordering.

For κ = 0.25, Q80/Q90 common raw gains are within self-consistency resolution, giving an unresolved state-gain result.

For κ = 0.75, DCAC is boundary-leading and has positive Q80_common raw gain, but Q90_common becomes negative. This establishes that boundary-leading does not imply full-protocol gain preservation.

## 5. PyBaMM context rows

The Day21A closure file included PyBaMM Day20B context rows. These are preserved separately and excluded from the main MJ1 experimental synthesis table.

```text
audit_day                                               protocol_pair   protocol_family                                                                   mechanism_verdict
   Day21A   Chen2020: 0.2C DC vs 0.2C+0.5C charge-first full protocol AC_off_after_Vmax positive_full_protocol_raw_gain_boundary_control_state_split_not_Segment_A_residual
   Day21A  OKane2022: 0.2C DC vs 0.2C+0.5C charge-first full protocol AC_off_after_Vmax positive_full_protocol_raw_gain_boundary_control_state_split_not_Segment_A_residual
   Day21A ORegan2022: 0.2C DC vs 0.2C+0.5C charge-first full protocol AC_off_after_Vmax positive_full_protocol_raw_gain_boundary_control_state_split_not_Segment_A_residual
```

## 6. Cross-audit interpretation

The combined Day21A–Day23A result supports the following structure:

1. Raw Δt(Q) gains are real first-passage differences, but they are not mechanism-pure.
2. In the AC-off protocol family, increasing AC amplitude moves Q80/Q90 common anchors into the boundary/control-state split region.
3. Lowering AC amplitude weakens this boundary pathway and can return Q80_common to the shared prescribed-current region.
4. In the continued-AC protocol-mode family, boundary-leading can occur even when AC_C < DC_C.
5. Boundary-leading alone is insufficient: Day23A κ = 0.75 shows positive G0/Q80 gain but negative Q90/G2 gain.
6. No closed audit confirms clean non-geometric Segment-A or G0 electrochemical acceleration.

## 7. Allowed claims

Allowed:

1. Day21A and Day22A support a boundary/control-state mediated interpretation within the AC-off protocol family.
2. Day22A shows that lower AC amplitude weakens the boundary pathway relative to Day21A.
3. Day23A shows that continued-AC protocols require a different G0/G1/G2 framework.
4. Day23A shows that DCAC-first boundary ordering can occur even under sub-DC AC amplitude.
5. Day23A also shows that boundary-leading does not guarantee full-protocol gain preservation.
6. Across all three audits, raw Δt(Q) must be interpreted by protocol region and protocol mode.

## 8. Prohibited claims

Do not claim:

1. Segment-A or G0 non-geometric electrochemical acceleration has been confirmed.
2. Day23A is directly comparable to Day21A/Day22A as the same AC-off protocol family.
3. Boundary-leading is equivalent to full-protocol acceleration.
4. Q90/G2 raw gains in Day23A are late-CV preservation in the Day21A/Day22A sense.
5. Temperature effects can be quantified in Day23A; temperature summaries are missing.

## 9. Key output files

- Main MJ1 synthesis table: `/Users/louislu/pybamm-dcac-superimposed/data/day21A_day22A_day23A_cross_audit_synthesis_table.csv`
- Excluded PyBaMM context table: `/Users/louislu/pybamm-dcac-superimposed/data/day21A_day22A_day23A_cross_audit_excluded_pybamm_context.csv`
- Source inventory: `/Users/louislu/pybamm-dcac-superimposed/data/day21A_day22A_day23A_cross_audit_source_inventory.csv`

## 10. Closure

This notebook closes the Day21A–Day23A cross-audit synthesis layer.

Next recommended step:

Use the synthesis table as the source for cross-audit visualization and documentation.