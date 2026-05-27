# Non-geometric acceleration claim review after Day37

## 1. Purpose

This document freezes the claim boundary after the Day30–Day37 PyBaMM-DCAC audit sequence.

The central question is:

> Does DC–AC excitation create stable, positive, engineering-significant non-geometric terminal-Q acceleration in the current PyBaMM model framework?

The answer after Day37 is:

> Not supported under the audited Chen2020 / DFN / isothermal / prescribed-current / terminal-Q decomposition framework.

This does not mean that DC–AC has no engineering value. It means that the supported value is not a proven non-geometric terminal-Q acceleration mechanism. The supported direction is admissible waveform design under geometry, microstate, plating-margin, and future thermal / aging constraints.

---

## 2. Definitions

### 2.1 Raw state-equivalent timing gain

The project defines raw equal-terminal-Q timing gain as:

```text
Δt_raw(Q) = t_DC(Q) − t_DCAC(Q)
```

where `t(Q)` is the first-passage time at which terminal integrated charge reaches a common target `Q`.

### 2.2 Geometry contribution

The geometry contribution is computed from the prescribed current waveform alone:

```text
Δt_geom(Q) = t_DC,geom(Q) − t_DCAC,geom(Q)
```

where:

```text
Q_geom(t) = ∫ I_prescribed(t) dt
```

### 2.3 Residual contribution

The non-geometric residual is:

```text
Δt_resid(Q) = Δt_raw(Q) − Δt_geom(Q)
```

A positive, stable, engineering-significant `Δt_resid(Q)` would be evidence that DC–AC provides state-equivalent terminal-Q timing gain beyond current-waveform geometry.

### 2.4 Current interpretation rule

The project must not interpret raw `Δt_raw(Q)` as non-geometric acceleration unless `Δt_resid(Q)` supports it.

---

## 3. Evidence sequence

### 3.1 Day29 — Full-protocol Level 1–3 audit

Day29 established a full-protocol audit structure:

1. Level 1: full CC–CV state-equivalent time gain;
2. Level 2: common-CC current-geometry versus residual separation;
3. Level 3: boundary / CV lead ledger.

The important result was that common-CC residuals remained small, while full-protocol time differences could arise through event / boundary / CV trajectory effects.

Interpretation:

> Full-protocol gains must not be collapsed into CC-only non-geometric terminal-Q acceleration.

---

### 3.2 Day30 — Microstate hierarchy and geometry-residual synthesis

Day30 showed:

- DC–AC creates equal-terminal-Q microstate differences;
- electrolyte-gradient, surface-stoichiometry, and heterogeneity signals can change;
- however, raw timing gain remains geometry-dominated.

Interpretation:

> DC–AC is a dynamic excitation / microstate perturbation tool, but the observed terminal-Q timing gain is not evidence of non-geometric acceleration.

---

### 3.3 Day31 — Negative-electrode plating-margin audit

Day31 introduced negative-electrode plating-margin admissibility:

```text
primary U_NE proxy = Negative electrode surface potential difference [V]
```

Key finding:

- fixed high-amplitude DC–AC can create raw timing gain;
- but negative-electrode hard-margin risk can be crossed;
- AC amplitude strongly controls U_NE margin.

Interpretation:

> Fastest raw timing protocol is not automatically admissible.

---

### 3.4 Day32 — Cross-parameter gain–margin transfer

Day32 showed:

- timing geometry dominance transfers across Chen2020, Ecker2015, and ORegan2022;
- plating-margin admissibility is parameter-set dependent;
- fixed AC0.7 is not a universally admissible protocol.

Interpretation:

> Gain–margin transfer is not guaranteed across parameter sets.

---

### 3.5 Day33 — Plating-risk localization

Day33 localized the minimum negative-electrode potential:

```text
risk trigger = high-Q / high-SOC
             + voltage-boundary adjacency
             + AC charge-current peak phase
```

Frequency sensitivity at fixed AC0.38 showed:

- risk severity and Q-location change with frequency;
- the dominant trigger structure remains peak-current / high-Q / boundary-coupled.

Interpretation:

> Plating-margin risk is localized and state-dependent, not uniformly distributed over the trajectory.

---

### 3.6 Day34 — Rule-based state-aware scheduling proof-of-concept

Day34 tested scheduled waveform v1:

```text
0–75% Q_ref:      0.3C + 0.38C
75–85% Q_ref:     0.3C + 0.20C
>85% Q_ref:       pure 0.3C DC
```

Result:

- scheduled v1 retained raw timing gain comparable to fixed AC0.38;
- min U_NE improved relative to fixed AC0.38;
- timing remained geometry-dominated;
- transport stress was not eliminated.

Interpretation:

> Day34 validated the risk-map → rule-based scheduling logic, not non-geometric acceleration.

---

### 3.7 Day35 — State-aware policy family

Day35 screened a small rule-based policy family.

Recommended candidates:

- `sched_v2_conservative`: primary first-generation rule-based candidate;
- `sched_v3_early_derate`: balanced candidate;
- `sched_v5_low_stress`: lower-transport-stress alternative.

Key result:

- all policy timing gains remained geometry-dominated;
- fixed AC0.7 remained inadmissible despite the largest raw gain.

Interpretation:

> Policy value lies in gain–margin–microstate trade-off, not in non-geometric terminal-Q acceleration.

---

### 3.8 Day36 — Double-layer surface-form sensitivity

Day36 tested:

```text
surface form = false
surface form = differential
surface form = algebraic
```

It confirmed:

- Chen2020 includes double-layer capacity parameters;
- `surface form = differential` builds and runs;
- reconstructed `C_dl · d(U_NE_xavg)/dt` proxy becomes visible;
- timing geometry dominance remains unchanged;
- `Δt_resid` remains small;
- U_NE margin classification remains unchanged.

High-frequency checks at 0.5τ and 0.1τ showed stronger double-layer proxy response but no positive non-geometric acceleration.

Interpretation:

> The absence of non-geometric terminal-Q acceleration is not explained by omission of differential double-layer dynamics under the tested conditions.

---

### 3.9 Day37 — Mechanism / parameterization sensitivity matrix

Day37 tested:

- baseline default;
- double-layer differential;
- transport flattened;
- transport nonlinearity amplified;
- combined differential + transport-nonlinearity amplified branch.

Mandatory protocols included:

- DC03;
- fixed AC0.38;
- fixed AC0.7;
- sched_v2_conservative.

Result:

```text
5 dc_reference cases
15 no_material_residual_acceleration cases
0 positive non-geometric acceleration candidates
```

All non-DC cases remained geometry-dominated.

Transport branches affected:

- U_NE margin;
- electrolyte-gradient stress;
- surface-state stress;
- high-amplitude stress severity.

But they did not create positive non-geometric terminal-Q acceleration.

Interpretation:

> The audited missing-physics / parameterization branches change admissibility and stress severity, not terminal-Q residual acceleration.

---

## 4. Supported claims

### Claim S1 — Raw timing gain exists

Supported.

DC–AC protocols can reach the same terminal-Q target earlier than DC under first-passage comparison.

### Claim S2 — Raw timing gain is mostly prescribed-current geometry

Supported.

Across Day30–Day37:

```text
Δt_raw(Q) ≈ Δt_geom(Q)
Δt_resid(Q) ≈ 0
```

### Claim S3 — DC–AC changes internal electrochemical state

Supported.

DC–AC changes:

- electrolyte concentration gradient;
- negative surface stoichiometry;
- surface heterogeneity;
- reaction overpotential;
- U_NE margin.

### Claim S4 — DC–AC can reduce negative-electrode margin

Supported.

High-amplitude DC–AC pushes U_NE closer to or below the 0 mV hard proxy.

### Claim S5 — State-aware scheduling improves hard-margin admissibility

Supported.

Scheduled policies derived from Day33 risk localization improve U_NE margin relative to fixed near-boundary and stress baselines.

### Claim S6 — fixed AC0.7 is a stress case, not an admissible candidate

Supported.

fixed AC0.7 repeatedly gives large raw gain but violates hard U_NE margin.

---

## 5. Unsupported claims

### Claim U1 — DC–AC produces stable positive non-geometric terminal-Q acceleration

Not supported.

No audited branch produced stable, positive, engineering-significant `Δt_resid(Q)`.

### Claim U2 — The absence of non-geometric acceleration was caused by missing double-layer dynamics

Not supported.

Day36 showed that `surface form = differential` does not materially change the conclusion.

### Claim U3 — Transport nonlinearity creates positive non-geometric acceleration

Not supported.

Day37 showed transport branches affect margin and microstate stress, but not terminal-Q residual acceleration.

### Claim U4 — Raw Δt(Q) alone proves internal electrochemical acceleration

Rejected.

Raw Δt(Q) must be decomposed into geometry and residual components.

---

## 6. Deferred claims

### Claim D1 — Dynamic OCP / hysteresis may affect voltage-boundary or CV behavior

Deferred.

Day37 found callable OCP functions but no supported Chen2020 / DFN dynamic-OCP or hysteresis branch in the current audit.

This mechanism is not disproven.

### Claim D2 — Thermal admissibility

Deferred.

Current Day30–Day37 mainline remains isothermal.

Thermal effects may alter:

- transport;
- reaction kinetics;
- U_NE margin;
- heat generation;
- safe waveform admissibility.

### Claim D3 — Aging admissibility

Deferred.

SEI, plating, LAM, and aging-coupled validation remain outside the current DC–AC scheduling proof chain.

### Claim D4 — Experimental transfer to MJ1

Deferred.

PyBaMM Chen2020 / DFN results do not automatically transfer to MJ1 experimental cells.

### Claim D5 — Full-protocol CV / voltage-boundary advantage

Partially open.

CC-only terminal-Q residual is unsupported, but full-protocol event / boundary / CV trajectory may still produce engineering value.

---

## 7. Metric-identifiability limits

The current decomposition answers a specific question:

> Does DC–AC reach the same terminal charge earlier for reasons beyond prescribed-current waveform geometry?

For prescribed-current terminal-Q first-passage, this is a stringent metric. Because terminal Q is the time integral of terminal current, most timing gain is structurally expected to be geometric unless a branch introduces:

- faradaic-efficiency differences;
- side reactions;
- capacitive storage large enough to separate terminal charge from state progression;
- voltage-control feedback;
- significant state-path dependence.

The current audits did not find such a positive residual under the tested model classes.

This means:

> The metric is appropriate for preventing overclaim, but it may not capture all engineering benefits of DC–AC.

Potential benefits may appear instead in:

- voltage-boundary timing;
- CV trajectory;
- plating-margin headroom;
- thermal headroom;
- aging mitigation;
- controllability / observability;
- admissible policy design.

---

## 8. Current best scientific interpretation

The current evidence supports the following interpretation:

> DC–AC does not currently appear to be a non-geometric terminal-Q acceleration mechanism in the audited PyBaMM model class. It is better interpreted as a dynamic excitation and waveform-scheduling method whose engineering value depends on admissibility constraints, microstate response, voltage-boundary behavior, and future thermal / aging constraints.

---

## 9. Recommended project direction

The project should stop using non-geometric terminal-Q acceleration as the central success criterion.

The stronger direction is:

```text
admissible DC–AC waveform optimization
under geometry, microstate, U_NE margin, and future thermal / aging constraints
```

Immediate next-stage candidates:

1. **BO-ready policy optimization**
   - Optimize early AC, mid AC, derating threshold, AC-off threshold, and possibly tau_factor.

2. **Thermal admissibility branch**
   - Add heat generation, cell temperature, and ΔT constraints.

3. **MPC-ready formulation**
   - Define state vector, control vector, constraints, objective, and reduced-order surrogate.

4. **Experimental / PORTUNUS bridge**
   - Translate policy candidates into experimentally executable waveforms and reduced-order validation.

---

## 10. Claim-safe wording

Use:

> DC–AC produces geometry-dominated raw terminal-Q timing gains and measurable microstate / plating-margin effects. State-aware scheduling can improve hard-margin admissibility while retaining part of the raw gain.

Do not use:

> DC–AC has been proven to accelerate charging through a non-geometric electrochemical mechanism.

Use:

> In the current PyBaMM prescribed-current terminal-Q framework, stable positive non-geometric acceleration is not supported.

Do not use:

> Non-geometric acceleration is impossible in real batteries.

Use:

> Full-protocol, voltage-boundary, thermal, aging, hysteresis, and experimental transfer mechanisms remain separate open questions.

---

## 11. Final conclusion

After Day37, the project’s defensible conclusion is:

> Stable, positive, engineering-significant non-geometric terminal-Q acceleration is not supported under the audited Chen2020 / DFN / isothermal / prescribed-current framework, even after adding double-layer dynamics and electrolyte-transport parameterization sensitivity. The supported research direction is no longer to prove non-geometric terminal-Q acceleration, but to optimize admissible DC–AC waveform policies under multi-physics constraints.
