# Day 34 Closure — State-aware DC–AC waveform scheduling

## 1. Purpose

Day 34 translated the Day33 plating-risk localization map into a first rule-based state-aware DC–AC waveform schedule.

The purpose was not to find the fastest fixed DC–AC protocol, and it was not to implement full MPC, Bayesian optimization, or closed-loop experimental control.

The purpose was to test whether a physically motivated scheduling rule can improve negative-electrode hard-margin admissibility while retaining part of the raw state-equivalent timing gain.

The core question was:

> Can a Day33-informed, rule-based DC–AC schedule reduce high-Q / voltage-boundary plating-margin risk while preserving useful raw timing gain?

---

## 2. Notebook and outputs

Notebook:

- `notebooks/34_state_aware_dcac_waveform_scheduling.ipynb`

Primary output files:

- `data/day34_metadata.json`
- `data/day34_protocol_schedule_table.csv`
- `data/day34_current_waveform_audit.csv`
- `data/day34_current_waveform_summary.csv`
- `data/day34_run_summary.csv`
- `data/day34_state_extraction_audit.csv`
- `data/day34_protocol_margin_trigger_summary.csv`
- `data/day34_equalQ_timing_geom_resid_curves.csv`
- `data/day34_equalQ_timing_geom_resid_summary.csv`
- `data/day34_state_aware_scheduling_ledger.csv`
- `data/day34_microstate_stress_comparison.csv`
- `data/day34_scheduling_ledger_with_microstate.csv`
- `data/day34_scheduled_v1_improvement_vs_fixed_baselines.csv`

---

## 3. Model and protocol basis

Parameter set:

- `Chen2020`

Model:

- DFN

Thermal setting:

- isothermal

Frequency mode:

- set-rebased

Reference time constant:

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

The Day34 schedule follows the Day30–Day33 mainline and does not use MJ1 fixed-label frequencies.

---

## 4. Tested protocol set

Day34 compared four protocols:

| Protocol | Role |
|---|---|
| `DC 0.3C` | reference |
| fixed `0.3C + 0.38C` | near-boundary fixed DC–AC baseline |
| fixed `0.3C + 0.7C` | high-amplitude stress baseline |
| scheduled v1 | rule-based state-aware schedule |

The scheduled v1 rule was:

```text
0.00 <= Q_ref_frac < 0.75: DC 0.3C + AC 0.38C
0.75 <= Q_ref_frac < 0.85: DC 0.3C + AC 0.20C
0.85 <= Q_ref_frac       : pure DC 0.3C
```

The implementation was a time-scheduled approximation based on the DC-reference Q progression. It was not feedback control.

---

## 5. Current waveform verification

The current waveform audit confirmed:

- pure DC remains at `1.5 A`;
- fixed `AC0.38` ranges from approximately `−0.4 A` to `3.4 A`;
- fixed `AC0.7` ranges from approximately `−2.0 A` to `5.0 A`;
- scheduled v1 uses `AC0.38` before derating, `AC0.20` in the intermediate segment, and AC-off in the late segment.

The scheduled waveform derates at approximately:

```text
T_derate ≈ 134.8 min
T_AC_off ≈ 152.8 min
```

---

## 6. Run summary

The PyBaMM run summary showed:

| Protocol | t_end | Q_end |
|---|---:|---:|
| DC 0.3C | ≈179.7 min | ≈4.493 Ah |
| fixed AC0.38 | ≈155.3 min | ≈3.907 Ah |
| fixed AC0.7 | ≈143.8 min | ≈3.634 Ah |
| scheduled v1 | ≈178.3 min | ≈4.492 Ah |

Scheduled v1 reaches a Q_end close to the DC reference because AC is reduced and then switched off in the late high-Q region.

---

## 7. Timing and geometry-residual result

Equal-Q timing decomposition showed:

| Protocol | Δt_raw_mean | Δt_geom_mean | Δt_resid_mean | Class |
|---|---:|---:|---:|---|
| fixed AC0.38 | ≈69.35 s | ≈69.36 s | ≈−0.013 s | geometry-dominated |
| fixed AC0.7 | ≈158.67 s | ≈158.69 s | ≈−0.020 s | geometry-dominated |
| scheduled v1 | ≈70.81 s | ≈70.82 s | ≈−0.013 s | geometry-dominated |

The scheduled waveform preserves raw state-equivalent timing gain comparable to fixed `AC0.38`, but the gain remains prescribed-current geometry dominated.

No non-geometric electrochemical acceleration is established.

---

## 8. Negative-electrode plating-margin result

The protocol-level negative-electrode margin result was:

| Protocol | min U_NE | Margin class |
|---|---:|---|
| DC 0.3C | ≈+37.28 mV | near_boundary |
| fixed AC0.38 | ≈+0.57 mV | near_boundary |
| fixed AC0.7 | ≈−25.31 mV | risk_flag |
| scheduled v1 | ≈+7.75 mV | near_boundary |

Scheduled v1 improves hard negative-electrode margin relative to fixed `AC0.38` and eliminates the hard-margin violation seen in fixed `AC0.7`.

However, scheduled v1 remains inside the conservative 50 mV audit buffer. It is therefore not a `safe_margin` protocol.

---

## 9. Microstate-context result

Day34 added a microstate-context comparison based on:

- electrolyte concentration range,
- negative surface stoichiometry range,
- negative-electrode reaction overpotential.

The result showed:

- fixed `AC0.7` strongly increases transport and polarization stress;
- fixed `AC0.38` and scheduled v1 have similar maximum electrolyte concentration range because both use `AC0.38` in the early/mid segment;
- scheduled v1 reduces surface heterogeneity and negative-electrode overpotential magnitude at the minimum-U_NE point relative to the fixed baselines.

Critical interpretation:

> scheduled v1 improves hard-margin risk localization, but it does not eliminate AC-induced transport stress.

The schedule relocates high-amplitude AC excitation away from the high-Q / voltage-boundary risk region.

---

## 10. Scheduled-v1 comparison against fixed baselines

Compared with fixed `AC0.38`, scheduled v1:

- retains comparable raw timing gain;
- improves min U_NE by approximately `+7.18 mV`;
- keeps hard-risk exposure at zero;
- does not reduce maximum electrolyte-gradient stress;
- reduces surface heterogeneity at the minimum-U_NE point;
- slightly reduces the magnitude of negative-electrode overpotential at the minimum-U_NE point.

Compared with fixed `AC0.7`, scheduled v1:

- sacrifices substantial raw timing gain;
- improves min U_NE by approximately `+33.06 mV`;
- eliminates hard-margin exposure below 0 mV;
- reduces surface heterogeneity and negative-electrode overpotential at the minimum-U_NE point.

---

## 11. Main Day34 conclusion

Day34 validates the Day33 → Day34 design logic.

Day33 identified the dominant risk trigger:

```text
high-Q / voltage-boundary-adjacent operation
+ AC charge-current peak
```

Day34 used this map to design a first rule-based schedule that reduces or removes AC before the high-Q risk region.

The scheduled waveform v1:

1. preserves raw timing gain comparable to fixed `AC0.38`;
2. remains geometry-dominated in timing interpretation;
3. improves hard negative-electrode margin relative to fixed `AC0.38`;
4. eliminates the hard-margin violation of the `AC0.7` stress case;
5. does not eliminate AC-induced transport stress;
6. remains near-boundary under the conservative 50 mV buffer.

Correct conclusion wording:

> The rule-based scheduled waveform v1 validates a plating-margin-aware scheduling principle. It improves hard negative-electrode margin by moving high-amplitude AC excitation away from the high-Q / voltage-boundary region while retaining geometry-dominated raw timing gain. It is a proof-of-concept for state-aware waveform scheduling, not a complete optimized fast-charging controller.

---

## 12. What Day34 verified

Day34 verified that:

1. A Day33-informed rule-based schedule can be implemented as a prescribed-current waveform.
2. AC derating and AC-off in high-Q regions can improve hard negative-electrode margin.
3. Scheduled v1 retains raw timing gain comparable to fixed `AC0.38`.
4. The retained raw timing gain remains geometry-dominated.
5. Scheduled v1 avoids the 0 mV hard-margin violation seen in the fixed `AC0.7` stress case.
6. Scheduled v1 remains near-boundary and does not remove 50 mV-buffer exposure.
7. Scheduled v1 does not eliminate AC-induced transport-gradient stress.

---

## 13. What Day34 did not prove

Day34 did not prove that:

1. scheduled v1 is globally optimal;
2. scheduled v1 is thermally admissible;
3. scheduled v1 is aging-admissible;
4. scheduled v1 is experimentally plating-free;
5. DC–AC creates non-geometric electrochemical acceleration;
6. a full MPC / BO controller has been implemented;
7. the policy transfers to other parameter sets or real MJ1 cells.

---

## 14. Interpretation boundary

Current boundaries:

- Parameter set: Chen2020
- Model: DFN
- Thermal condition: isothermal
- Protocol type: prescribed-current schedule
- Scheduling type: pre-programmed, not feedback
- Safety metric: U_NE thermodynamic proxy
- 50 mV threshold: audit buffer only
- No thermal model
- No aging model
- No experimental validation

---

## 15. Next step

Day34 should stop here as a proof-of-concept.

Possible next-stage work:

1. **Policy parameterization**
   - SOC / Q breakpoints,
   - AC amplitude levels,
   - AC-off threshold,
   - peak-current ceiling.

2. **MPC / BO-ready formulation**
   - objective: retain timing gain;
   - constraints: U_NE margin, voltage, future thermal limits;
   - policy parameters: scheduling breakpoints and amplitudes.

3. **Thermal admissibility**
   - evaluate T_cell, ΔT, and heat generation.

4. **PORTUNUS / experimental bridge**
   - build a measurement-aligned reduced-order battery model for MJ1.

Day34’s current result should be treated as the first rule-based scheduling baseline.
