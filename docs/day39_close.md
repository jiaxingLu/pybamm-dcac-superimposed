# Day 39 Closure — Parameter-set-specific SOC/Q τ-rebased frequency scheduling

## 1. Purpose

Day39 extended Day38 from fixed-frequency amplitude/window scheduling to SOC/Q-segmented frequency scheduling.

Day38 optimized:

```text
A_AC(Q)
```

at fixed frequency. Day39 kept the Day38 amplitude/window schedule fixed and changed only:

```text
f(Q)
```

The goal was to test whether parameter-set-specific τ-based frequency scheduling improves the gain–margin–microstate trade-off.

---

## 2. Critical methodological rules

### 2.1 τ is parameter-set-specific

Day39 extracted τ descriptors specifically for:

```text
Chen2020 / DFN / isothermal
```

The τ map must not be transferred from MJ1 experiments, another chemistry, or another PyBaMM parameter set.

### 2.2 PyBaMM sign convention

The notebook used the project convention:

```text
I_charge_A > 0 = charging direction
```

and converted it to PyBaMM convention:

```text
I_py_A = −I_charge_A
```

The sign audit passed.

### 2.3 Phase continuity

Frequency-scheduled waveforms were constructed using:

```text
φ(t) = ∫ 2π f(t) dt
I_charge(t) = I_DC + A_AC(t) sin(φ(t))
```

This prevents phase reset at segment boundaries.

---

## 3. Notebook and outputs

Notebook:

- `notebooks/39_soc_tau_frequency_scheduling.ipynb`

Primary outputs:

- `data/day39_metadata.json`
- `data/day39_tau2_extraction_targets.csv`
- `data/day39_tau2_pulse_profile_sign_audit.csv`
- `data/day39_tau2_local_pulse_run_summary.csv`
- `data/day39_tau2_soc_q_map.csv`
- `data/day39_tau2_fit_curves.csv`
- `data/day39_tau_descriptor_segment_assignment.csv`
- `data/day39_tau_descriptor_comparison.csv`
- `data/day39_frequency_policy_table.csv`
- `data/day39_frequency_segment_table.csv`
- `data/day39_phase_continuous_waveform_timeseries.csv`
- `data/day39_phase_continuous_waveform_summary.csv`
- `data/day39_frequency_cycle_coverage.csv`
- `data/day39_frequency_policy_run_summary.csv`
- `data/day39_frequency_policy_margin_microstate_summary.csv`
- `data/day39_frequency_policy_equalQ_timing_curves.csv`
- `data/day39_frequency_policy_timing_geom_resid_summary.csv`
- `data/day39_frequency_policy_ledger.csv`
- `data/day39_final_frequency_policy_synthesis.csv`
- `data/day39_recommended_candidates_for_day40_thermal_audit.csv`
- `data/day39_final_claim_boundary.csv`

---

## 4. Day38 baseline carried into Day39

Day39 used the Day38 primary fixed-frequency candidate as the amplitude/window baseline:

```text
local_H_high_early_early_off
```

Amplitude/window schedule:

```text
0–0.62 Q_ref:       AC = 0.38C
0.62–0.77 Q_ref:    AC = 0.05C
>0.77 Q_ref:        AC = 0
```

Only the frequency schedule was changed.

---

## 5. τ extraction result

The local pulse-rest audit produced high-quality bi-exponential fits.

The fitted descriptors separated into two time scales:

```text
τ_fast ≈ 25–27 s
τ_slow ≈ 242–306 s
```

The previous global reference:

```text
τ_ref,set ≈ 36.3 s
```

is closer to τ_fast than τ_slow.

Interpretation:

> Day39 cannot assume that the fitted slow τ is the correct AC forcing time scale. Both fast-descriptor and slow-tail-descriptor schedules must be distinguished.

---

## 6. Frequency policies

Day39 evaluated:

| Policy | Frequency schedule | Role |
|---|---|---|
| `fixed_local_H` | fixed Day38 1.5τ_set | baseline |
| `seg_tau_fast_k1p5` | segmented τ_fast, k=1.5 | main fast-descriptor test |
| `seg_tau_slow_k1p5` | segmented τ_slow, k=1.5 | slow-tail diagnostic |
| `seg_tau_fast_k1p0` | segmented τ_fast, k=1.0 | faster forcing |
| `seg_tau_fast_k3p0` | segmented τ_fast, k=3.0 | slower / conservative fast-descriptor forcing |

---

## 7. Cycle coverage audit

Cycle coverage was required because τ_slow created very long periods.

`τ_fast` schedules had usable coverage across AC-on segments.

`seg_tau_slow_k1p5` had insufficient coverage:

```text
seg_low:      weak coverage
seg_mid:      insufficient cycles
seg_derated:  insufficient cycles
```

Interpretation:

> τ_slow-based scheduling behaves more like a slow ramp / partial-wave perturbation than a periodic AC forcing schedule.

Therefore, `seg_tau_slow_k1p5` is diagnostic only.

---

## 8. PyBaMM evaluation result

All policies ran successfully.

All timing remained:

```text
geometry_dominated
```

No non-geometric terminal-Q acceleration was established.

---

## 9. Main result

The best valid frequency-scheduled candidate was:

```text
seg_tau_fast_k3p0
```

with:

```text
f(Q) = 1 / (2π · 3.0 · τ_fast(Q))
```

Representative result:

```text
Δt_raw_mean ≈ 96.5 s
min_U_NE ≈ +37.2 mV
max_c_e_range_vs_DC ≈ 1.96
```

Compared with `fixed_local_H`:

```text
fixed_local_H:
Δt_raw_mean ≈ 91.8 s
min_U_NE ≈ +37.2 mV
max_c_e_range_vs_DC ≈ 1.93
```

`seg_tau_fast_k3p0` gave:

```text
+4.7 s raw timing gain
approximately unchanged U_NE margin
slightly increased electrolyte-gradient stress
```

---

## 10. Other frequency policies

### seg_tau_fast_k1p5

Valid periodic coverage, but raw gain decreased substantially relative to fixed_local_H.

Interpretation:

> Not preferred as primary candidate.

### seg_tau_fast_k1p0

Valid periodic coverage and lower transport-stress indicator, but raw gain decreased strongly.

Interpretation:

> Too fast for the current gain-margin objective.

### seg_tau_slow_k1p5

Very large raw gain, but insufficient cycle coverage and higher microstate stress.

Interpretation:

> Diagnostic only; not a valid periodic AC candidate.

---

## 11. Microstate and thermal boundary

Day39 included microstate stress indicators:

- electrolyte concentration range;
- negative surface stoichiometry range;
- negative reaction overpotential;
- U_NE margin.

Day39 did not include thermal metrics because the model is isothermal.

Therefore, no Day39 candidate can be called thermally admissible.

---

## 12. What Day39 verified

Day39 verified that:

1. local τ extraction must be parameter-set-specific;
2. τ_fast and τ_slow represent different descriptor scales;
3. τ_fast is viable for periodic AC frequency scheduling;
4. τ_slow is diagnostic only because cycle coverage is insufficient;
5. phase-continuous frequency scheduling can be constructed cleanly;
6. `seg_tau_fast_k3p0` slightly improves fixed_local_H under isothermal electrochemical-margin criteria;
7. timing remains geometry-dominated.

---

## 13. What Day39 did not prove

Day39 did not prove that:

1. `seg_tau_fast_k3p0` is globally optimal;
2. `seg_tau_fast_k3p0` is thermally admissible;
3. `seg_tau_fast_k3p0` is aging-admissible;
4. the result transfers to other parameter sets or real MJ1 cells;
5. SOC-τ frequency scheduling should always use k=3.0;
6. MPC or feedback control has been implemented.

---

## 14. Main conclusion

Day39 supports:

> Parameter-set-specific τ_fast-based frequency scheduling is viable. Under the Day38 local_H amplitude/window schedule, `seg_tau_fast_k3p0` modestly improves the fixed-frequency baseline while preserving U_NE margin. Slow-tail τ scheduling is diagnostic only because of insufficient periodic cycle coverage. All timing remains geometry-dominated.

---

## 15. Next step

Day40 should run a thermal admissibility audit before combined BO or MPC work.

Recommended Day40 comparison set:

- `DC03_reference`
- `fixed_local_H`
- `seg_tau_fast_k3p0`
- `seg_tau_fast_k1p5`
- `seg_tau_slow_k1p5` diagnostic
- optional high-amplitude stress reference

Required thermal metrics:

- `T_cell_max`
- `ΔT_max`
- heat generation maximum
- heat generation integral
- I_rms
- comparison against DC and fixed_local_H
