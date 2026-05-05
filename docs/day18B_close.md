# Day 18B Close — Phase-Aware and Geometry-Corrected Δt(Q) Audit

## 1. Scope

Day 18B extends the Day 18A phase audit into a geometry-corrected protocol-matrix audit.

The work combines two linked findings:

1. **Day 18A phase audit**
   The initial AC phase is not a cosmetic setting. Under PyBaMM's sign convention, the experiment-faithful branch is the charge-first current formulation.

2. **Day 18B geometry-corrected audit**
   In prescribed-current CC mode, raw strict-net first-passage Δt(Q) is dominated by the imposed current waveform geometry. Therefore, raw Δt(Q) cannot be used as the verdict variable for non-geometric state-layer acceleration.

---

## 2. Current convention after Day 18

PyBaMM uses:

    positive current = discharge
    negative current = charge

The experiment-side NGU201 ARB waveform was generated as:

    current = dc_current + ac_amplitude · sin(angle)

where positive current corresponds to charging in the experimental convention.

The experiment-faithful PyBaMM equivalent is therefore:

    I_py = -I_DC - I_AC · sin(ωt)

This is defined as the **charge-first** branch.

The previous branch:

    I_py = -I_DC + I_AC · sin(ωt)

is defined as the **discharge-first** branch.

From Day 18 onward:

    main branch = charge-first
    discharge-first = retained only as phase contrast / feasibility audit

---

## 3. Why raw Δt(Q) is no longer sufficient

The raw state-equivalent time difference (project canonical convention; matches Masterarbeit):

    Δt_model(Q) = t_DC(Q) − t_DCAC(Q)

with positive Δt_model interpreted as DCAC reaching Q* before DC (acceleration).

Strict-net charge:

    Q_net(t) [A·h] = -∫_0^t I(τ) dτ / 3600

In prescribed-current CC operation, the current waveform is externally imposed. Therefore, before voltage-limited control changes the current trajectory, Q_net(t) is determined directly by the prescribed current function.

Battery dynamics affect:

    V(t)
    overpotential
    polarization
    Vmin / Vmax feasibility
    voltage-triggered termination
    Q_to_Vmax
    thermal and degradation-relevant states

but they do not alter Q_net(t) under a prescribed current waveform.

Therefore, raw Δt_model(Q) contains a current-waveform geometry contribution.

Day 18B introduced the analytical geometry baseline:

    Δt_geom(Q) = t_DC,geom(Q) − t_DCAC,geom(Q)

where t_DCAC,geom(Q) is the first-passage time of the analytical Q_geom(t) computed from the prescribed current function alone, and t_DC,geom(Q) is the linear DC first-passage time.

The non-geometric residual:

    Δt_resid(Q) = Δt_model(Q) − Δt_geom(Q)

Interpretation:

    raw Δt_model(Q): includes imposed-current first-passage geometry
    Δt_geom(Q):      analytical first-passage contribution from I(t)
    Δt_resid(Q):     non-geometric residual after removing current geometry

Verdict variable after Day 18:

    Δt_resid(Q), not raw Δt(Q)

---

## 4. Day 18A phase audit summary

### 4.1 Discharge-first branch

The morning v3 branch used:

    I_py = -I_DC + I_AC · sin(ωt)

This starts with a discharge-leaning AC lobe immediately after t = 0.

Consequences observed in the Route2_AC0p5C_10tau_native anchor:

    ORegan2022 became boundary_confounded by Vmin_event.
    Chen2020 and OKane2022 showed signed raw Δt(Q) consistent with
    discharge-first geometry (DCAC slower than DC).
    The result was phase-dependent and not experiment-faithful.

### 4.2 Charge-first branch

The afternoon v4 branch used:

    I_py = -I_DC - I_AC · sin(ωt)

This branch removed the initial voltage depression and restored ORegan2022 feasibility.

ORegan2022 comparison:

    v3 discharge-first:
      feasibility = boundary_confounded
      V_min_obs   = 2.500 V
      Q_to_Vmax   = NaN
      t_end       = 718 s

    v4 charge-first:
      feasibility = feasible_clean
      V_min_obs   = 3.099 V
      Q_to_Vmax   = 3.210 Ah
      t_end       = 9926 s

Conclusion:

    ORegan2022 v3 Vmin boundary was a joint condition of:
      discharge-first phase  ×
      slow native period     ×
      low-SoC start (SOC0 = 0.05).

    The phase flip alone resolved the feasibility outcome, but the
    underlying slow-τ V_min susceptibility remains. ORegan2022 still
    showed the lowest V_min_obs among the three smoke sets in Day 18B
    Group B 0.1τ (3.092 V vs ~3.286 V for Ecker), well above the cutoff
    but structurally closer to it. Any future discharge-first protocol
    design must track this susceptibility explicitly.

The v3 ORegan2022 result is therefore reclassified as a phase-sensitive feasibility boundary on a slow-τ structural background, not as a phase-independent native-period feasibility limitation.

---

## 5. Day 18A geometry-residual finding

For the 3-set charge-first smoke test:

    Chen2020
    OKane2022
    ORegan2022

at:

    Route2_AC0p5C_10tau_native_charge_first

the raw Δt(Q) was positive-only (DCAC reaching Q* before DC across the entire valid Q-grid), as expected from the charge-first geometry contribution. However, the signed magnitudes were fully reproduced by the analytical current-geometry baseline.

Observed pattern:

    Δt_model(Q) ≈ Δt_geom(Q)
    Δt_resid(Q) ≈ 0

Numerical residual (6 simulations, 3 sets × 2 phases, Cell 4A v4):

    max |Δt_resid(Q)| ≤ 0.034 s

Interpretation:

    The positive raw Δt(Q) under charge-first phase is a prescribed-current
    first-passage geometry effect, not evidence of non-geometric state-layer
    acceleration in the PyBaMM model.

---

## 6. Day 18B protocol matrix

Day 18B expanded the audit from a single anchor to a smoke protocol matrix.

### Parameter sets

Smoke sets:

    Ecker2015
    Chen2020
    ORegan2022

Rationale:

    Ecker2015  = fast τ anchor
    Chen2020   = reference / LG-like baseline
    ORegan2022 = slow τ / boundary-sensitive anchor

### Protocol groups

Group A:

    DC = 0.2C
    AC = 0.4C
    κ  = 2.0
    nτ = 0.1τ / 1τ / 10τ

Group B:

    DC = 0.4C
    AC = 0.6C
    κ  = 1.5
    nτ = 0.1τ / 1τ / 10τ

All protocols used:

    phase = charge_first
    descriptor = tau95_eq
    current formula = I_py = -I_DC - I_AC · sin(ωt)
    peak current constraint = |DC| + |AC| ≤ 1C

### Simulation count

    3 sets × 8 protocols = 24 simulations

This includes:

    2 DC baselines per set
    6 DCAC protocols per set

---

## 7. Cell 5B smoke simulation result

Cell 5B ran all 24 smoke simulations.

Result:

    24 / 24 feasible_clean
    0 solver_fail
    0 boundary_confounded
    0 Vmin_event

Actual wall time:

    632 s = 10.5 min

Estimated wall time:

    714 s = 11.9 min

Actual / estimate:

    89 %

Phase sanity passed for all DCAC rows.

For Group A:

    0.2C + 0.4C:
      I_initial          ≈ -0.2C
      I_min_first_period ≈ -0.6C
      I_max_first_period ≈ +0.2C

For Group B:

    0.4C + 0.6C:
      I_initial          ≈ -0.4C
      I_min_first_period ≈ -1.0C
      I_max_first_period ≈ +0.2C

The charge-first current branch was applied consistently.

---

## 8. Cell 5C Δt_resid audit result

Cell 5C computed:

    Δt_model(Q)
    Δt_geom(Q)
    Δt_resid(Q) = Δt_model(Q) − Δt_geom(Q)

for all valid DCAC-vs-DC pairs.

Pairing rule:

    DCAC_DC0p2C_AC0p4C_* → DC_0p2C
    DCAC_DC0p4C_AC0p6C_* → DC_0p4C

Total audited pairs:

    18 DCAC × DC_baseline pairs

Output files:

    data/day18B_smoke_dtQ_resid_summary.csv
    data/day18B_smoke_dtQ_resid_curves_long.csv.gz

Q-window per pair (common-window construction):

    q_lo = 0.05 · Q_nom
    q_hi = min(Q_to_Vmax_DC, Q_to_Vmax_DCAC) − 0.02 · Q_nom

Result:

    18 / 18 near_zero
    18 / 18 residual topology near_zero
    0 non_trivial
    0 invalid_Q_window
    0 mixed_sign

Overall maximum residual magnitude across the 18 pairs:

    max |Δt_resid(Q)| = 0.0441 s

This is far below all relevant decision criteria. Three margins are reported:

    Margin to per-protocol numerical floor max(5·dt_eval, 1.0) s:
      smallest margin ≈ 280×  at 1τ Chen Group B (floor = 12.27 s)
      largest  margin ≈ 28000× at 10τ rows         (floor = 50 s)

    Margin to absolute decision threshold (60 s):
      ≈ 1360×

    Residual-to-geometric ratio max|Δt_resid| / max|Δt_geom|:
      from 1×10⁻⁴ down to 1×10⁻⁶

The third ratio is the cleanest indicator: it is dimensionless, independent of dt_eval, and independent of threshold conventions. Across all 10τ rows, the residual is six orders of magnitude below the geometric baseline.

---

## 9. Key evidence table: 18 DCAC pairs

| Set | Protocol | DC ref | nτ | q_hi [Ah] | max\|Δt_geom\| [s] | max\|Δt_resid\| [s] | Residual topology | Q_to_Vmax shift [%] | Verdict |
|---|---|---|---:|---:|---:|---:|---|---:|---|
| Ecker2015 | 0.2C+0.4C 0.1τ | DC_0p2C | 0.1 | 0.1553 | 6.538 | 0.0090 | near_zero | -1.471 | near_zero |
| Ecker2015 | 0.2C+0.4C 1τ | DC_0p2C | 1 | 0.1551 | 65.39 | 0.0042 | near_zero | -1.584 | near_zero |
| Ecker2015 | 0.2C+0.4C 10τ | DC_0p2C | 10 | 0.1544 | 653.4 | 0.0274 | near_zero | -1.995 | near_zero |
| Ecker2015 | 0.4C+0.6C 0.1τ | DC_0p4C | 0.1 | 0.1519 | 4.888 | 0.0046 | near_zero | -2.266 | near_zero |
| Ecker2015 | 0.4C+0.6C 1τ | DC_0p4C | 1 | 0.1512 | 49.01 | 0.0008 | near_zero | -2.708 | near_zero |
| Ecker2015 | 0.4C+0.6C 10τ | DC_0p4C | 10 | 0.1491 | 488.9 | 0.0386 | near_zero | -4.078 | near_zero |
| Chen2020 | 0.2C+0.4C 0.1τ | DC_0p2C | 0.1 | 4.211 | 15.62 | 0.0114 | near_zero | -6.786 | near_zero |
| Chen2020 | 0.2C+0.4C 1τ | DC_0p2C | 1 | 4.025 | 156.2 | 0.0156 | near_zero | -10.81 | near_zero |
| Chen2020 | 0.2C+0.4C 10τ | DC_0p2C | 10 | 4.153 | 1561 | 0.0085 | near_zero | -8.049 | near_zero |
| Chen2020 | 0.4C+0.6C 0.1τ | DC_0p4C | 0.1 | 3.614 | 11.69 | 0.0038 | near_zero | -14.43 | near_zero |
| Chen2020 | 0.4C+0.6C 1τ | DC_0p4C | 1 | 3.499 | 117.1 | 0.0441 | near_zero | -17.08 | near_zero |
| Chen2020 | 0.4C+0.6C 10τ | DC_0p4C | 10 | 3.250 | 1171 | 0.0108 | near_zero | -22.82 | near_zero |
| ORegan2022 | 0.2C+0.4C 0.1τ | DC_0p2C | 0.1 | 4.619 | 19.09 | 0.0077 | near_zero | -0.1065 | near_zero |
| ORegan2022 | 0.2C+0.4C 1τ | DC_0p2C | 1 | 4.617 | 190.9 | 0.0276 | near_zero | -0.1582 | near_zero |
| ORegan2022 | 0.2C+0.4C 10τ | DC_0p2C | 10 | 4.533 | 1909 | 0.0438 | near_zero | -1.926 | near_zero |
| ORegan2022 | 0.4C+0.6C 0.1τ | DC_0p4C | 0.1 | 4.375 | 14.31 | 0.0041 | near_zero | -0.4133 | near_zero |
| ORegan2022 | 0.4C+0.6C 1τ | DC_0p4C | 1 | 3.009 | 142.8 | 0.0108 | near_zero | -30.82 | near_zero |
| ORegan2022 | 0.4C+0.6C 10τ | DC_0p4C | 10 | 2.352 | 1432 | 0.0033 | near_zero | -45.44 | near_zero |

---

## 10. Interpretation of the 18-pair table

Two parallel observations must be kept distinct.

**Apparent acceleration (raw Δt_model) is large and positive.** Under the canonical convention Δt = t_DC − t_DCAC with positive interpreted as DCAC reaching Q* first, raw Δt_model is positive across all 18 charge-first pairs, with magnitudes up to 1909 s (≈31.8 min) on 10τ ORegan. This is a real, measurable difference in first-passage time between DCAC and DC trajectories.

**Geometric explanation captures the apparent acceleration in full.** Δt_geom — computed analytically from the prescribed current waveform alone — reproduces Δt_model to within the residual magnitudes shown. The non-geometric residual is uniformly near zero (≤ 0.0441 s).

**Event-layer voltage pull-forward is also present and large.** Q_to_Vmax shift values up to −45.44 % (ORegan Group B 10τ) indicate that DCAC reaches the Vmax termination at substantially less accumulated charge than DC, due to AC peak-charging current driving voltage upward through cell polarization. This is a separate, voltage-coupled phenomenon, distinct from Δt_resid in the CC window.

The combined statement is therefore:

    Apparent (raw) acceleration is real, large, and present in all charge-first pairs.
    Voltage-event pull-forward is real, large, and protocol-dependent.
    Non-geometric state-layer acceleration in Δt(Q) is not resolved.

---

## 11. Frequency-layer interpretation

The three nτ groups do not carry equal interpretive weight.

### 10τ

    strongest residual test
    largest Δt_geom
    highest sensitivity to non-geometric residual
    primary physical conclusion layer

10τ rows show:

    max |Δt_geom| up to 1909 s
    max |Δt_resid| still below 0.05 s
    residual / geometric ratio at the 10⁻⁵ – 10⁻⁶ level

This is the strongest evidence for the residual null baseline.

### 1τ

    intermediate consistency check

1τ rows show near-zero residuals at the 10⁻⁴ – 10⁻⁵ ratio level.

### 0.1τ

    numerical noise-floor probe

0.1τ rows have much smaller geometry amplitudes and higher output-point density. They are useful for characterizing numerical floor and interpolation behavior, but should not be used as the strongest physical claim.

---

## 12. Null-baseline boundary conditions

The Day 18B smoke null baseline is valid under the following tested conditions:

    PyBaMM version: 26.3.1
    model: DFN
    model options: none
    degradation: off
    plating: off
    thermal model: off
    initial SOC: SOC0 = 0.05
    phase: charge-first
    current convention: I_py = -I_DC - I_AC · sin(ωt)
    time-scale descriptor: tau95_eq
    protocol mode: prescribed-current CC
    peak current constraint: |DC| + |AC| ≤ 1C
    sets tested: Ecker2015, Chen2020, ORegan2022
    protocol groups:
      0.2C + 0.4C at 0.1τ / 1τ / 10τ
      0.4C + 0.6C at 0.1τ / 1τ / 10τ

This is not a universal statement about all battery models, all chemistries, or all charging controls.

---

## 13. What this result does NOT mean

This result does not mean:

    MJ1 experimental acceleration is false.
    DC–AC charging cannot produce state-layer effects in real cells.
    τ-based frequency scheduling is invalid.
    aging studies are permanently irrelevant.

It means only:

    Under the tested PyBaMM DFN prescribed-current CC branch,
    DC-vs-DCAC raw Δt(Q) is fully explained by current-waveform geometry,
    and no additional non-geometric Δt_resid(Q) is resolved.

The correct conclusion is methodological:

    This PyBaMM branch does not generate non-geometric state-layer Δt(Q)
    under the tested protocol family.

---

## 14. Consequence for future PyBaMM ablations

Day 18B defines the residual null floor.

Day 18B smoke empirical maximum:

    max |Δt_resid(Q)| = 0.0441 s

This is the empirical ceiling on the numerical noise floor under the current-controlled CC null baseline. Future ablations must clear two criteria simultaneously to be interpreted as candidate non-geometric state-layer signal:

Decision rule for future ablations:

    |Δt_resid| < per-protocol numerical floor max(5·dt_eval, 1.0) s
       → numerical null

    |Δt_resid| above the per-protocol floor but < 60 s
       → small residual; inspect Q-window, phase, dt_eval, first-passage
         interpolation behaviour, and protocol feasibility

    |Δt_resid| ≥ 60 s with stable sign topology across the Q-window
       → candidate non-geometric state-layer signal;
         escalate to mechanism analysis

The 60 s absolute threshold remains the decision boundary for "physical" interpretation. The per-protocol numerical floor (1 s for 0.1τ Ecker; 12.27 s for 1τ Chen Group B; 50 s for 10τ rows) is the lower screening gate. The Day 18B smoke clears the floor by ~280× at the worst point and by 4 orders of magnitude in 10τ rows.

---

## 15. Implications for earlier PyBaMM days

### 15.1 DC-vs-DCAC comparisons

Earlier DC-vs-DCAC conclusions must be rechecked for:

    phase convention
    current-waveform geometry
    Δt_model vs Δt_geom vs Δt_resid

Any result based only on raw Δt(Q) should be relabeled as geometry-conditioned until residual correction is added.

### 15.2 Same-protocol DCAC-vs-DCAC ablations

If both sides of an ablation use the same imposed current waveform, frequency, phase, amplitude, and Q-window, the current-geometry baseline cancels.

These results (Day 11–14 plating, OCP, transport, AsymBV α scans) are less affected by the Day 18 framework, but still require metadata verification of phase convention to ensure their interpretation has the correct experiment-faithfulness label.

### 15.3 Day 16 chemistry-shift fixed-label DC-vs-DCAC

Day 16 fixed-label DC-vs-DCAC across 8 parameter sets cleared the original 60 s absolute threshold by margin (geometric baseline ≈ 20 s under the tested anchor). The result was passed without residual correction.

Under the Day 18 framework, Day 16 must be re-audited:

    Compute Δt_model, Δt_geom, Δt_resid per pair on the Day 16 protocol grid.
    Re-classify each conclusion category:
      "geometry-explained negative"          (former negative passing 60 s threshold)
      "geometry-explained mixed"             (former mixed)
      "candidate non-geometric"              (only if residual now exceeds floor + 60 s)

The original Day 16 conclusion of "negative-or-near-zero in 28/28 pairs" is unlikely to flip topology, but the conclusion category must be updated to reflect that the negative was geometry-explained, not physics-confirmed.

### 15.4 Day 8–10 / early notebooks

A retrospective audit is required to determine:

    which current functions used discharge-first phase
    which comparisons were DC-vs-DCAC
    which conclusions need residual correction
    which previous negative results remain valid after geometry correction

---

## 16. Full 64-simulation matrix decision

The Day 18B smoke run already covers:

    fast τ set: Ecker2015
    reference set: Chen2020
    slow τ set: ORegan2022
    both protocol groups
    all three nτ values
    all charge-first protocols feasible

All 18 residuals are near zero, with ratio max|Δt_resid|/max|Δt_geom| at 10⁻⁴ to 10⁻⁶.

Therefore:

    full 64-simulation sweep is optional.

It is only justified if the purpose is:

    completeness of the null-distribution baseline
    all-8 parameter-set documentation
    publication-quality supplementary matrix

It is not required before Day 19 retrospective audit.

---

## 17. Current project status after Day 18B

    Cell 5A: passed
    Cell 5B: passed
    Cell 5C: passed (signed dt_model / dt_geom storage convention to be
                     reconciled — code-level patch only; magnitudes and
                     verdicts unchanged)

    Day 18B smoke:
      residual null baseline confirmed

    Full 64-sim sweep:
      optional

    Aging branch:
      HOLD until stable |Δt_resid| > floor emerges

    Dynamic f(SOC):
      HOLD until residual-generating model domain is identified

    Day 19:
      retrospective phase / geometry audit of Day 8–10 + Day 16
      followed by parameter-family / chemistry-shift availability audit
      followed by geometry-corrected chemistry-shift smoke test

---

## 18. Next recommended step

Start Day 19 with:

    Day 19A — retrospective audit of Day 8–10 notebooks and scripts,
              and re-audit of Day 16 chemistry-shift fixed-label DC-vs-DCAC.

Primary tasks:

    1. Identify all current function definitions across Day 8–10 + Day 16.
    2. Classify each as charge-first or discharge-first.
    3. Classify comparison type:
         DC-vs-DCAC                          (needs Δt_resid re-audit)
         DCAC-vs-DCAC same-protocol ablation (needs phase audit only)
         DCAC-vs-different-DCAC protocol     (needs phase + window check)
    4. Determine whether Δt_geom / Δt_resid correction is required.
    5. Relabel old conclusions accordingly:
         "geometry-explained …"  vs  "candidate non-geometric …"

After Day 19A, proceed to:

    Day 19B — parameter-family / chemistry-shift availability audit
              (NMC / NCA / LFP availability under PyBaMM 26.3.1 + DFN
               + initial_soc support + voltage-limit feasibility).

Then:

    Day 19C — geometry-corrected chemistry-shift smoke test
              (Chen2020 + 1 NMC/NCA contrast + 1 LFP/strong-OCP contrast,
               at Group A and Group B × 10τ only, charge-first;
               full Δt_model + Δt_geom + Δt_resid + V(Q) + Q_to_Vmax +
               CV-entry shift reporting).

Aging branch remains blocked until a stable non-geometric Δt_resid(Q) signal appears above the Day 18B null floor. Dynamic f(SOC) scheduling remains blocked until Day 19C identifies a response basin where non-geometric residual is observable.
