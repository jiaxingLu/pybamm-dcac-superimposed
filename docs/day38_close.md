# Day 38 Closure — BO-ready fixed-frequency DC–AC policy optimization

## 1. Purpose

Day38 converted the Day35 rule-based state-aware DC–AC policy family into a BO-ready policy-evaluation framework.

It did not implement full Bayesian optimization and did not implement MPC.

The purpose was to define and test the evaluator contract:

```text
policy parameters θ
→ prescribed-current waveform
→ PyBaMM evaluation
→ timing / margin / microstate metrics
→ constraint verdict
→ scalar score
```

---

## 2. Context after Day37

After Day37, the project claim boundary is:

> Stable, positive, engineering-significant non-geometric terminal-Q acceleration is not supported under the audited Chen2020 / DFN / isothermal / prescribed-current framework.

Therefore, Day38 does not continue searching for non-geometric terminal-Q acceleration.

The project direction shifts to:

```text
admissible DC–AC waveform optimization
under geometry, microstate, U_NE margin, and future thermal / aging constraints
```

---

## 3. Notebook and outputs

Notebook:

- `notebooks/38_bo_ready_policy_optimization.ipynb`

Primary outputs:

- `data/day38_metadata.json`
- `data/day38_search_space.csv`
- `data/day38_policy_constraints.json`
- `data/day38_seed_policy_table.csv`
- `data/day38_seed_waveform_audit.csv`
- `data/day38_seed_waveform_summary.csv`
- `data/day38_seed_run_summary.csv`
- `data/day38_seed_state_margin_microstate_summary.csv`
- `data/day38_seed_equalQ_timing_geom_resid_curves.csv`
- `data/day38_seed_equalQ_timing_geom_resid_summary.csv`
- `data/day38_seed_bo_ready_evaluation_ledger.csv`
- `data/day38_seed_strict_margin_score_ledger.csv`
- `data/day38_local_candidate_table.csv`
- `data/day38_local_candidate_eval_raw.csv`
- `data/day38_combined_seed_local_strict_ranking.csv`
- `data/day38_final_policy_synthesis.csv`
- `data/day38_recommended_fixed_frequency_candidates.csv`
- `data/day38_final_claim_boundary.csv`

---

## 4. Policy parameterization

Day38 used a fixed-frequency amplitude/window policy class:

```text
f = 1 / (2π · 1.5τ_set)
```

Decision variables:

| Parameter | Meaning |
|---|---|
| `early_ac_c` | early-stage AC amplitude |
| `mid_ac_c` | AC amplitude after derating |
| `qfrac_derate` | Q_ref fraction where derating begins |
| `qfrac_ac_off` | Q_ref fraction where AC is switched off |

Fixed settings:

```text
DC = 0.3C
model = Chen2020 / DFN
thermal = isothermal
frequency = fixed 1.5τ_set
```

---

## 5. Search space

The Day38A search space was:

| Parameter | Range |
|---|---:|
| `early_ac_c` | 0.20–0.45 C |
| `mid_ac_c` | 0.00–0.25 C |
| `qfrac_derate` | 0.60–0.85 |
| `qfrac_ac_off` | 0.75–0.95 |

Policy-space constraints:

```text
qfrac_derate + 0.05 <= qfrac_ac_off
mid_ac_c <= early_ac_c
```

Electrochemical constraints / scoring boundaries:

```text
hard U_NE limit = 0 mV
target margin = 20 mV
50 mV = conservative audit buffer
```

---

## 6. Seed-policy evaluation

Day38B evaluated seed policies from Day35 and additional deterministic seeds.

The first strict-margin score identified:

```text
seed_conservative_low_mid
```

as the strongest seed.

Parameters:

```text
early_ac_c = 0.35
mid_ac_c = 0.05
qfrac_derate = 0.65
qfrac_ac_off = 0.78
```

Result:

```text
Δt_raw_mean ≈ 83.3 s
min_U_NE ≈ +35.1 mV
```

This seed outperformed the original Day35 `sched_v2` and `sched_v3` under the stricter margin-aware score.

---

## 7. Strict-margin score calibration

The first score version penalized hard-margin violation but did not sufficiently penalize policies too close to 0 mV.

A strict-margin score was introduced with:

```text
target_min_margin = 20 mV
```

This correctly deprioritized the aggressive seed:

```text
seed_aggressive_margin_test
```

which had high raw gain but min U_NE only around +3.6 mV.

Interpretation:

> A BO objective must penalize low-margin policies before they cross the 0 mV hard proxy.

---

## 8. Local candidate expansion

Day38C performed a local deterministic expansion around `seed_conservative_low_mid`.

This was not full Bayesian optimization. It was a local seed-improvement screen.

The best candidate found was:

```text
local_H_high_early_early_off
```

Parameters:

```text
early_ac_c = 0.38
mid_ac_c = 0.05
qfrac_derate = 0.62
qfrac_ac_off = 0.77
```

Representative result:

```text
Δt_raw_mean ≈ 91.0 s
min_U_NE ≈ +37.2 mV
max_c_e_range_vs_DC ≈ 1.93
```

This became the current primary fixed-frequency amplitude/window candidate.

---

## 9. Secondary candidate

The main conservative alternative is:

```text
local_C_earlier_derate_same_off
```

Parameters:

```text
early_ac_c = 0.35
mid_ac_c = 0.05
qfrac_derate = 0.62
qfrac_ac_off = 0.78
```

Representative result:

```text
Δt_raw_mean ≈ 84.9 s
min_U_NE ≈ +37.2 mV
max_c_e_range_vs_DC ≈ 1.85
```

Interpretation:

> local_C gives lower raw gain than local_H but also lower electrolyte-gradient amplification, making it a robustness-oriented alternative.

---

## 10. Design insight

Day38 supports a clear policy-design pattern:

```text
stronger early AC
+ early derating
+ early AC-off
= improved fixed-frequency gain–margin trade-off
```

The best policies are not those that keep AC active longest. They are those that extract early geometry-enabled gain and then avoid the high-Q / voltage-boundary risk region.

This aligns with Day33:

```text
risk = high-Q / boundary-adjacent state + AC charge-current peak
```

---

## 11. Timing interpretation

All Day38 candidates remain geometry-dominated.

Day38 does not show non-geometric terminal-Q acceleration. It uses the geometry-enabled timing benefit within an admissible waveform policy.

Correct interpretation:

> Day38 improves the gain–margin trade-off of fixed-frequency open-loop policies, not the non-geometric residual mechanism.

---

## 12. Current recommended fixed-frequency candidates

### Primary candidate

```text
local_H_high_early_early_off
```

Use as the current best fixed-frequency amplitude/window seed.

### Secondary conservative candidate

```text
local_C_earlier_derate_same_off
```

Use as a more conservative robustness-oriented candidate.

### Aggressive reference

```text
local_E_higher_early
```

High gain but more stress-sensitive; not the primary robust candidate.

---

## 13. What Day38 verified

Day38 verified that:

1. a BO-ready evaluator can be defined for fixed-frequency amplitude/window policies;
2. the evaluator returns timing, geometry-residual, U_NE, microstate, constraints, and score metrics;
3. strict margin scoring is necessary to avoid 0 mV boundary-hugging policies;
4. a local expansion found better candidates than the Day35 hand-designed seeds;
5. local_H is the current best fixed-frequency seed;
6. all results remain geometry-dominated.

---

## 14. What Day38 did not prove

Day38 did not prove that:

1. local_H is globally optimal;
2. Bayesian optimization has been completed;
3. MPC has been implemented;
4. thermal constraints are satisfied;
5. aging constraints are satisfied;
6. local_H transfers to other parameter sets;
7. SOC-dependent τ₂-rebased frequency scheduling improves or worsens the result.

---

## 15. Next step

Day39 should introduce SOC / Q-segmented τ₂-rebased frequency scheduling.

Target formulation:

```text
f(Q) = 1 / (2π · k · τ₂(Q))
```

Day39 should compare:

1. fixed-frequency `1.5τ_set`;
2. SOC-segmented τ₂-rebased frequency;
3. conservative high-Q frequency / AC-off rules.

Day40 can then combine:

```text
A_AC(Q) + f(Q)
```

under a BO-ready policy class.

---

## 16. Main conclusion

Day38 established the first BO-ready fixed-frequency DC–AC amplitude/window evaluator and identified `local_H_high_early_early_off` as the current primary fixed-frequency candidate. The result supports the transition from hand-designed schedules toward optimization-ready admissible waveform policies, while preserving the claim boundary that timing gains remain geometry-dominated.
