# Day 35 Closure — State-aware scheduling policy family

## 1. Purpose

Day 35 extended the Day34 single scheduled waveform into a small, interpretable family of rule-based state-aware DC–AC scheduling policies.

The goal was not to perform full optimization, MPC, Bayesian optimization, or experimental closed-loop control.

The goal was to ask:

> Which first-generation rule-based schedules provide the best trade-off between raw timing gain, negative-electrode margin, and microstate stress context?

---

## 2. Project context

The DC–AC project no longer searches for the fastest fixed sinusoidal protocol.

The current framing is:

```text
Find admissible fast protocols under:
1. state-equivalent timing gain,
2. geometry–residual separation,
3. microstate response,
4. negative-electrode plating margin,
5. future thermal / aging admissibility.
```

Lineage:

- Notebook 30: raw timing gain is geometry-dominated; microstate response exists.
- Notebook 31: Chen2020 / DFN shows a hard-margin boundary near AC≈0.386C.
- Notebook 32: timing geometry dominance transfers; plating-margin admissibility is parameter-set dependent.
- Notebook 33: plating-margin risk localizes near high-Q / voltage-boundary-adjacent operation and AC charge-current peaks.
- Notebook 34: scheduled v1 improves hard margin while retaining raw timing gain comparable to fixed AC0.38.
- Notebook 35: evaluates a small policy family to find better first-generation scheduled candidates.

---

## 3. Notebook and outputs

Notebook:

- `notebooks/35_state_aware_policy_family.ipynb`

Primary outputs:

- `data/day35_metadata.json`
- `data/day35_policy_table.csv`
- `data/day35_current_waveform_audit.csv`
- `data/day35_current_waveform_summary.csv`
- `data/day35_run_summary.csv`
- `data/day35_state_extraction_audit.csv`
- `data/day35_policy_margin_trigger_summary.csv`
- `data/day35_equalQ_timing_geom_resid_curves.csv`
- `data/day35_equalQ_timing_geom_resid_summary.csv`
- `data/day35_microstate_context_summary.csv`
- `data/day35_gain_margin_microstate_policy_ledger.csv`
- `data/day35_policy_family_final_synthesis.csv`
- `data/day35_recommended_policy_candidates.csv`

---

## 4. Model and protocol basis

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

All policy-family comparisons were made under the same Chen2020 / DFN / isothermal setting.

---

## 5. Policy family

Baselines:

| Policy | Description |
|---|---|
| `DC03` | pure DC reference |
| `fixed_AC0p38` | fixed near-boundary DC–AC baseline |
| `fixed_AC0p7` | high-amplitude stress baseline |

Scheduled policies:

| Policy | early AC | mid AC | derate threshold | AC-off threshold | Role |
|---|---:|---:|---:|---:|---|
| `sched_v1_day34` | 0.38C | 0.20C | 0.75 Q_ref | 0.85 Q_ref | Day34 baseline |
| `sched_v2_conservative` | 0.38C | 0.10C | 0.70 Q_ref | 0.80 Q_ref | conservative |
| `sched_v3_early_derate` | 0.38C | 0.20C | 0.70 Q_ref | 0.85 Q_ref | balanced |
| `sched_v4_aggressive` | 0.38C | 0.20C | 0.80 Q_ref | 0.90 Q_ref | aggressive |
| `sched_v5_low_stress` | 0.30C | 0.10C | 0.75 Q_ref | 0.85 Q_ref | low-stress |

The schedules were pre-programmed using DC-reference Q progression as a time proxy. They are not feedback controllers.

---

## 6. Timing and geometry-residual result

All DC–AC and scheduled policies retained the previous mainline result:

```text
Δt_raw_mean ≈ Δt_geom_mean
Δt_resid_mean ≈ 0
```

All non-DC policies were classified as:

```text
geometry_dominated
```

Therefore, Notebook 35 does not establish non-geometric electrochemical acceleration.

The scheduling policies are evaluated by gain–margin–microstate trade-off, not by non-geometric acceleration.

---

## 7. Key policy results

Representative results:

| Policy | Δt_raw_mean | min U_NE | Margin class |
|---|---:|---:|---|
| fixed AC0.38 | ≈69.35 s | ≈+0.57 mV | near-boundary |
| fixed AC0.7 | ≈158.67 s | ≈−25.31 mV | risk_flag |
| sched v1 | ≈70.81 s | ≈+7.75 mV | near-boundary |
| sched v2 | ≈65.69 s | ≈+24.16 mV | near-boundary |
| sched v3 | ≈67.31 s | ≈+20.50 mV | near-boundary |
| sched v4 | ≈69.35 s | ≈+4.36 mV | near-boundary |
| sched v5 | ≈55.16 s | ≈+16.26 mV | near-boundary |

The fixed AC0.7 stress case has the largest raw timing gain but remains hard-margin inadmissible.

---

## 8. Recommended candidates

### 8.1 Primary rule-based candidate: sched_v2_conservative

`sched_v2_conservative`:

```text
early AC = 0.38C
mid AC = 0.10C
derate threshold = 0.70 Q_ref
AC-off threshold = 0.80 Q_ref
```

Result:

```text
Δt_raw_mean ≈ 65.69 s
min U_NE ≈ +24.16 mV
fraction below 0 mV = 0
```

Interpretation:

> Best first-generation rule-based candidate in this screen. It gives substantial hard-margin improvement with only modest raw-gain sacrifice.

---

### 8.2 Balanced candidate: sched_v3_early_derate

`sched_v3_early_derate`:

```text
early AC = 0.38C
mid AC = 0.20C
derate threshold = 0.70 Q_ref
AC-off threshold = 0.85 Q_ref
```

Result:

```text
Δt_raw_mean ≈ 67.31 s
min U_NE ≈ +20.50 mV
fraction below 0 mV = 0
```

Interpretation:

> Balanced candidate. It retains slightly more raw timing gain than v2 while keeping a substantially larger margin than v1 or fixed AC0.38.

---

### 8.3 Low-transport-stress candidate: sched_v5_low_stress

`sched_v5_low_stress`:

```text
early AC = 0.30C
mid AC = 0.10C
derate threshold = 0.75 Q_ref
AC-off threshold = 0.85 Q_ref
```

Result:

```text
Δt_raw_mean ≈ 55.16 s
min U_NE ≈ +16.26 mV
```

Interpretation:

> Lower-transport-stress candidate. It reduces maximum electrolyte-gradient amplification but sacrifices more timing gain.

---

## 9. Deprioritized / rejected policies

### fixed AC0.7

Rejected as an admissible candidate:

```text
Δt_raw_mean ≈ 158.67 s
min U_NE ≈ −25.31 mV
risk_flag
```

Interpretation:

> Stress case only. Largest raw gain but violates hard negative-electrode margin.

### sched_v4_aggressive

Deprioritized:

```text
Δt_raw_mean ≈ 69.35 s
min U_NE ≈ +4.36 mV
```

Interpretation:

> Later derating leaves small margin without providing meaningful gain advantage over v1 or fixed AC0.38.

---

## 10. Microstate-context result

All AC0.38-based policies retain elevated electrolyte-gradient stress because they use AC0.38 in the early segment.

Approximate pattern:

```text
AC0.38-based policies:
max c_e_range_vs_DC ≈ 1.98
```

The low-stress policy reduces this:

```text
sched_v5_low_stress:
max c_e_range_vs_DC ≈ 1.77
```

Interpretation:

> The main scheduling benefit is not elimination of transport stress, but moving high-amplitude AC away from the high-Q / voltage-boundary risk region.

This boundary is important. The policy-family screen improves hard-margin admissibility, but it does not solve thermal, aging, or all microstate-stress concerns.

---

## 11. Main Day35 conclusion

Day35 identifies `sched_v2_conservative` and `sched_v3_early_derate` as the best first-generation rule-based scheduled candidates.

They:

1. retain geometry-dominated raw timing gain,
2. improve hard negative-electrode margin relative to fixed AC0.38 and Day34 v1,
3. avoid the 0 mV hard-margin violation of fixed AC0.7,
4. remain near-boundary under the 50 mV audit buffer,
5. do not eliminate AC-induced transport stress.

Correct conclusion wording:

> The Day35 policy-family screen identifies `sched_v2_conservative` and `sched_v3_early_derate` as the best first-generation rule-based candidates. They retain geometry-dominated raw timing gain while substantially improving hard negative-electrode margin relative to fixed AC0.38 and Day34 v1. `sched_v5_low_stress` is a lower-transport-stress alternative with larger timing-gain sacrifice. The fixed AC0.7 stress case remains inadmissible.

---

## 12. What Day35 verified

Day35 verified that:

1. The Day34 scheduled-policy concept can be expanded into an interpretable policy family.
2. Earlier derating improves hard negative-electrode margin.
3. v2 and v3 outperform Day34 v1 in gain–margin trade-off.
4. fixed AC0.7 remains inadmissible.
5. all raw gains remain geometry-dominated.
6. low-stress amplitude reduction reduces transport-gradient amplification but sacrifices timing gain.
7. a future optimization layer should tune policy parameters rather than blindly scan fixed sine waves.

---

## 13. What Day35 did not prove

Day35 did not prove that:

1. v2 or v3 is globally optimal;
2. any policy is thermally admissible;
3. any policy is aging-admissible;
4. any policy is experimentally plating-free;
5. DC–AC creates non-geometric electrochemical acceleration;
6. MPC or Bayesian optimization has been implemented;
7. the candidates transfer to other parameter sets or real MJ1 cells.

---

## 14. Next step

Day35 should be treated as the policy-family screen.

Possible next-stage work:

1. **MPC / Bayesian-optimization-ready formulation**
   - decision variables: early AC, mid AC, derating threshold, AC-off threshold, peak-current ceiling;
   - objective: retain raw timing gain;
   - constraints: U_NE margin, voltage limit, future thermal constraints.

2. **Thermal admissibility**
   - evaluate T_cell, ΔT, heat generation.

3. **Cross-parameter policy transfer**
   - test whether v2/v3 remain good candidates in Ecker2015 or other sets.

4. **Experimental / PORTUNUS bridge**
   - translate policy candidates into a reduced-order measurement-aligned model or experimental waveform design.

For now, the immediate conclusion is that v2 and v3 are the preferred first-generation rule-based candidates.
