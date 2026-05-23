# Day 32 Closure — Cross-parameter gain–margin transfer

## 1. Purpose

Day 32 tested whether the gain–margin admissibility structure identified in Chen2020 transfers to other PyBaMM parameter sets.

Day 30 showed that DC–AC produces equal-Q microstate differences while raw state-equivalent timing gain remains geometry-dominated.

Day 31 showed that, in Chen2020 / DFN at `1.5τ_set`, DC–AC timing gain must be constrained by negative-electrode plating margin. The full-protocol hard-margin boundary was approximately:

```text
AC ≈ 0.386C
peak current ≈ 0.686C
```

Day 32 asked:

> Does this gain–margin boundary transfer to Ecker2015 and ORegan2022, or is it parameter-set dependent?

---

## 2. Notebook and outputs

Notebook:

- `notebooks/32_cross_parameter_gain_margin_transfer.ipynb`

Primary output tables:

- `data/day32_cross_parameter_protocol_table.csv`
- `data/day32_cross_parameter_run_summary.csv`
- `data/day32_cross_parameter_margin_variable_availability.csv`
- `data/day32_cross_parameter_margin_extraction_audit.csv`
- `data/day32_cross_parameter_protocol_margin_summary.csv`
- `data/day32_cross_parameter_hard_margin_boundary_summary.csv`
- `data/day32_cross_parameter_transfer_verdict.csv`
- `data/day32_cross_parameter_equalQ_dt_geom_resid_curves.csv`
- `data/day32_cross_parameter_dt_geom_resid_summary.csv`
- `data/day32_cross_parameter_gain_margin_transfer_summary.csv`

---

## 3. Model and protocol design

Parameter sets:

- `Chen2020`
- `Ecker2015`
- `ORegan2022`

Model:

- DFN

Thermal setting:

- isothermal

Frequency mode:

- set-rebased `1.5τ_set`

The reference time constant for each parameter set was taken from the Day17 `tau2_biexp` descriptor.

Current protocol family:

- DC baseline: `0.3C`
- DC–AC: `0.3C + AC`

AC amplitude scan:

```text
AC = 0.1C, 0.2C, 0.3C, 0.36C, 0.38C, 0.40C, 0.5C, 0.7C
```

Current convention:

```text
PyBaMM: +I = discharge, −I = charge
I_py(t) = −I_DC − I_AC sin(2π f t)
```

This corresponds to the charge-positive experimental waveform:

```text
I_charge(t) = I_DC + I_AC sin(2π f t)
```

---

## 4. Negative-electrode plating-margin proxy

The same virtual three-electrode plating-margin proxy from Day31 was used:

```text
U_NE_vs_Li ≈ φ_s,n − φ_e,n
```

Primary variable:

- `Negative electrode surface potential difference [V]`

Primary margin metric:

```text
min_U_NE_vs_Li = min_x(negative electrode surface potential difference)
```

Margin classes:

| Class | Criterion |
|---|---|
| `safe_margin` | min U_NE_vs_Li > 50 mV |
| `near_boundary` | 0 mV < min U_NE_vs_Li <= 50 mV |
| `risk_flag` | min U_NE_vs_Li <= 0 mV |

The 50 mV threshold is an audit buffer, not a universal physical constant. A `risk_flag` is a thermodynamic proxy warning, not proof of experimentally observed lithium plating.

---

## 5. Variable availability

All three parameter sets exposed the required negative-electrode potential variables:

- `Negative electrode surface potential difference [V]`
- `Negative electrode surface potential difference at separator interface [V]`
- `X-averaged negative electrode surface potential difference [V]`

Therefore, the plating-margin proxy was extractable for all selected parameter sets.

---

## 6. Protocol-level plating-margin transfer result

### 6.1 Chen2020

Chen2020 reproduced the Day31 result.

The DC reference is already inside the 50 mV audit buffer but remains above 0 mV:

```text
DC 0.3C:
min_U_NE ≈ +37.3 mV
margin_class = near_boundary
```

As AC amplitude increases, the hard-margin proxy crosses 0 mV inside the scanned range:

```text
estimated hard-margin boundary:
AC ≈ 0.386C
peak current ≈ 0.686C
```

Classification:

```text
transfer_class = boundary_within_scan
```

Interpretation:

> Chen2020 has a clear amplitude-dependent hard-margin boundary under the tested protocol and frequency.

---

### 6.2 Ecker2015

Ecker2015 remains above the 50 mV audit buffer across the full scanned AC-amplitude range.

Representative values:

```text
DC 0.3C:
min_U_NE ≈ +73.6 mV

0.3C + 0.7C:
min_U_NE ≈ +55.6 mV
```

Classification:

```text
transfer_class = all_scanned_amplitudes_admissible
```

Interpretation:

> No hard-margin crossing is observed for Ecker2015 within the scanned AC-amplitude range.

This does not prove universal safety. It only means that, under this PyBaMM DFN virtual three-electrode proxy and this protocol family, Ecker2015 retains substantially larger negative-electrode potential margin than Chen2020.

---

### 6.3 ORegan2022

ORegan2022 is already below the 0 mV proxy under the DC reference:

```text
DC 0.3C:
min_U_NE ≈ −98.4 mV
margin_class = risk_flag
```

Classification:

```text
transfer_class = baseline_risk_not_admissible_reference
```

Interpretation:

> ORegan2022 is not directly comparable as an admissible transfer case because the DC reference itself already violates the hard-margin proxy.

For ORegan2022, DC–AC does not create the baseline risk; the baseline is already risk-flagged under the selected model, protocol, and proxy.

---

## 7. Cross-parameter boundary summary

| Parameter set | DC margin | Boundary result | Transfer class |
|---|---:|---|---|
| Chen2020 | +37.3 mV | AC≈0.386C / peak≈0.686C | boundary within scan |
| Ecker2015 | +73.6 mV | no crossing up to AC0.7C | all scanned amplitudes admissible |
| ORegan2022 | −98.4 mV | baseline already below 0 mV | baseline-risk / not directly comparable |

Main conclusion:

> The Chen2020 hard-margin boundary is not a universal DC–AC safety limit. Negative-electrode plating-margin admissibility is strongly parameter-set dependent.

---

## 8. Geometry-residual transfer result

Day 32 also repeated the equal-Q timing and geometry-residual decomposition across parameter sets.

For all tested parameter sets and AC amplitudes:

```text
Δt_raw_mean ≈ Δt_geom_mean
Δt_resid_mean ≈ 0
```

All tested cases were classified as:

```text
dt_resid_class = geometry_dominated
```

This extends the Day30 conclusion across the selected parameter sets:

> The state-equivalent raw timing gain produced by DC–AC is dominated by prescribed-current geometry, not by non-geometric electrochemical acceleration.

This was true even when plating-margin behavior differed strongly across parameter sets.

---

## 9. Gain–margin transfer classes

The combined timing and margin table separates three cases.

### Chen2020

```text
AC <= 0.38C:
geometry_gain__near_boundary

AC >= 0.40C:
geometry_gain__risk
```

Interpretation:

> Chen2020 has geometry-dominated timing gain, but margin changes from near-boundary to hard risk as AC amplitude crosses the parameter-set-specific boundary.

### Ecker2015

```text
all scanned AC:
geometry_gain__safe_margin
```

Interpretation:

> Ecker2015 has geometry-dominated timing gain and remains above the 50 mV audit buffer across the scanned range.

### ORegan2022

```text
all scanned AC:
geometry_gain__risk
```

Interpretation:

> ORegan2022 is baseline-risk and should not be used as a normal admissibility-transfer case under this protocol.

---

## 10. Day32 main conclusion

Day 32 shows that two conclusions transfer differently:

1. **Timing geometry dominance transfers.**

   Across Chen2020, Ecker2015, and ORegan2022, raw DC–AC timing gain is geometry-dominated and Δt_resid remains near zero.

2. **Plating-margin admissibility does not transfer cleanly.**

   Chen2020 has a hard-margin boundary inside the scanned AC range. Ecker2015 remains safe-margin across the scan. ORegan2022 is baseline-risk even for DC reference.

Therefore:

```text
A DC–AC protocol cannot be judged by a universal frequency–amplitude boundary.
Admissibility is parameter-set dependent.
```

The correct framing is:

```text
fast protocol
→ geometry-residual check
→ microstate response check
→ negative-electrode plating-margin check
→ later thermal / aging admissibility check
```

---

## 11. What Day32 verified

Day 32 verified that:

1. The virtual three-electrode negative-electrode potential proxy is available for Chen2020, Ecker2015, and ORegan2022.
2. The Chen2020 hard-margin boundary from Day31 is reproduced.
3. Ecker2015 remains above the 50 mV audit buffer up to AC0.7C.
4. ORegan2022 is baseline-risk under the DC reference.
5. The admissible AC-amplitude boundary is parameter-set dependent.
6. Raw timing gain remains geometry-dominated across all tested parameter sets.
7. A protocol can be geometry-gain + safe-margin, geometry-gain + near-boundary, or geometry-gain + risk depending on the parameter set.

---

## 12. What Day32 did not prove

Day 32 did not prove that:

1. Ecker2015 is experimentally safe under DC–AC charging.
2. ORegan2022 would experimentally plate under the same current protocol.
3. The 50 mV buffer is a universal safety threshold.
4. The Chen2020 AC≈0.386C boundary transfers to real MJ1 cells.
5. The current protocol is thermally admissible.
6. DC–AC produces non-geometric fast-charging acceleration.

---

## 13. Interpretation boundary

Current boundaries:

- Parameter sets: Chen2020, Ecker2015, ORegan2022
- Model: DFN only
- Thermal condition: isothermal
- Protocol: prescribed-current DC–AC
- DC component: 0.3C
- Frequency: set-rebased 1.5τ_set
- Safety metric: negative-electrode potential proxy only
- No explicit plating submodel interpretation
- No non-isothermal thermal audit
- No aging-state transfer
- No experimental validation of the parameter-set boundaries

---

## 14. Next step

The immediate technical work can stop here for Notebook32.

Recommended next steps:

1. Add `docs/day32_close.md` and commit Notebook32.
2. Consider a later Notebook33 for thermal admissibility:
   - `T_cell`
   - `ΔT`
   - heat generation
   - thermal / aging risk
3. Consider a later MJ1 / PORTUNUS reduced-order model to connect experimental data with a measurement-aligned battery model.
4. Avoid further claiming “fastest protocol.” The correct project objective is now:

```text
admissible fast protocol under timing, geometry-residual, microstate, plating-margin, and thermal constraints
```
