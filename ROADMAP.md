# ROADMAP

This document tracks the development trajectory of the PyBaMM DC-AC superimposed charging validation framework. Each release is scoped around a coherent scientific question; the methodological priority is ablation-style isolation of one model element at a time, not multi-mechanism stacking.

---

## Released

### v0.1.0 — baseline simulation pipeline (archived: [10.5281/zenodo.19788879](https://doi.org/10.5281/zenodo.19788879))

**Scope**: establish a reproducible simulation pipeline (PyBaMM SPMe + Chen2020 + lumped thermal) for the 30-case DC-AC superimposed charging batch on LG INR18650 MJ1 cells; report three-tier sim-vs-exp validation under strict-net charge accounting.

**Deliverables**:
- 5-phase protocol pipeline via single `pybamm.Experiment`.
- `CustomStepExplicit` DC-AC current injection.
- 30-case batch sweep (24 DC-AC + 6 DC baseline).
- Three-tier validation figures: Δt(Q80), T_max, CC time.
- Strict-net Q(t) accounting with six locked constraints (see "Constraints carried forward" below).

**Scientific outcome**: thermal channel ✅, CC kinetic channel ✅, Δt(Q80) categorical mismatch ❌. Two competing hypotheses left open at v0.1: cell-physics absence vs frequency-mismatch.

### v0.2.0 — model-configuration sweep + κ=1.5 trajectory diagnosis + layered evaluation framework (GitHub-only)

**Scope**: expand the model space from a single SPMe configuration to five main-sweep configurations (SPMe / DFN / DFN + V_init protocol fix / composite + sigmoid forced V_init / composite + sigmoid natural V_init); plus two additional Day 9 diagnostic configurations (X5β single-phase + natural rest, X6α-NS composite without sigmoid). Disambiguate the v0.1 hypothesis pair via trajectory analysis on the κ=1.5 cluster. Adopt layered evaluation framework distinguishing event-layer sim/exp consistency criteria from state-layer cross-cell phenomenon-generalization observations.

**Deliverables**:
- HPPC characterization on Chen2020 (notebook 07): τ_Chen extraction at SOC = 20%, both directions, single-phase reference.
- X2 DFN replication of v0.1 batch (notebook 08): tests SPMe-vs-DFN model-order effect on state-layer behavior.
- X4 DFN with Chen-rescaled frequency grid (notebook 09): rules out the simple frequency-rescaling hypothesis.
- X5 DFN + V_init = 2.82 V protocol fix (notebook 10): X5-A reaches state-layer sign-coincidence 15/24 (62.5%); X5β diagnostic variant (natural rest) at 17/24 (70.8%).
- Day 9 V_init × model 2×2 control matrix (notebook 11): isolates V_init protocol effect from cell-physics representation; produces X5β / X6α-NS diagnostic data.
- Day 9 composite + sigmoid HPPC stage 2 (notebook 12): characterizes composite-OCP-induced suppression of bi-exponential charge fit (8/8 charge cases fail).
- Day 9 trajectory-level diagnosis on the κ=1.5 cluster: rules out the frequency-mismatch hypothesis (~5 octaves frequency span, consistent reversal sign across all three τ labels).
- X5.5 numerical audit (`PyBaMM_handoff_2026-04-28.md` §"Solver Verification"): IDAKLU vs CasadiSolver dt_max sweep on rows 3 and 8 confirms X5-A 24-case data numerically reliable.
- v0.2 audit + framing recalibration (notebook 13): sign-zero threshold reconciliation across CSV strict-sign vs threshold 0.10; layered evaluation framework adopted; X5β / X6α-NS diagnostic disclosure into README footnote.

**Scientific outcome**:
- Frequency-mismatch hypothesis ruled out at the κ=1.5 cluster.
- Cell-physics observation localized: under standard DFN + Chen2020 parameters, the Chen2020/M50 cell does not robustly exhibit state-layer DC-AC acceleration cell-internally; MJ1 cell does.
- State-layer sign-coincidence with MJ1 ranges from 9.1% to 62.5% across the five main-sweep configurations (sign-zero threshold 0.10 min). Day 9 7-way diagnostic matrix shows two additional configurations at 70.8% (X5β) and 9.1% (X6α-NS); the dispersion across V_init protocols within the diagnostic matrix raises hypotheses about V_init as a controlling variable, to be tested under controlled conditions in v0.3.

### Scope evolution between v0.1 and v0.2

The v0.2 scope filed at the v0.1 release was a *parameter-refinement track* — Chen2020 sensitivity analysis, selective fitting for MJ1, 18650 geometric scaling, parameter cross-validation. v0.2 actually executed a *model-configuration sweep* (SPMe / DFN / DFN + V_init protocol fix / composite + sigmoid). The pivot was triggered on Day 8 by NGU201 V(t) baseline inspection, which revealed that the V_init = 2.51 V vs 2.82 V protocol mismatch — a single binary state-of-charge initialization choice — explained more sign-coincidence variance than any single-parameter perturbation reasonably could. Parameter refinement was therefore deferred and is reabsorbed into the v0.3 plan as item 7 below.

A second v0.2 development was the framing recalibration: the v0.1 release implicitly framed Δt(Q80) sign agreement as a model-quality criterion ("PyBaMM should match MJ1"). Day 9 trajectory analysis and recognition that Chen2020 was never calibrated as an MJ1 proxy led to adoption of the layered evaluation framework: event-layer uses sim/exp consistency criteria; state-layer reports cross-cell phenomenon-generalization observations descriptively, without ranking configurations.

---

## Evaluation framing (layered) — methodological constraint for all future releases

This framework, established in v0.2, governs how all sim-vs-exp comparisons are reported in this repository going forward.

**Event layer** — direct measurable physical observables (T_max, CC time, total charge time, ΔTotal sign on the AC-acceleration direction). Sim is evaluated against exp by quantitative consistency criteria. v0.1 thermal and CC-kinetic channel results are validated under this layer; v0.2 ΔTotal 87.5% sign-coincidence is validated under this layer.

**State layer** — the Δt(Q*) metric requires a notion of AC-induced kinetic acceleration that is mechanistic and depends on cell physics. State-layer results are reported under three claim types:
- Sim cell-internal: does the cell, as simulated, exhibit Δt(Q*) > 0 under the protocol?
- Exp cell-internal: does the MJ1 cell exhibit Δt(Q*) > 0 in measurement?
- Cross-cell sign-coincidence: a *descriptive* statistic, not a model-quality ranking.

**Sign-coincidence as emergent indicator, not optimization target**: under the layered framing, state-layer sign-coincidence is read as an *emergent behavior indicator* — does the state-layer phenomenon emerge in a given configuration? — not as a quantity to be maximized through model tuning. A configuration with higher sign-coincidence is not "a better model" of MJ1; it is a configuration in which the cell-internal phenomenon happens to coincide with MJ1's cell-internal phenomenon on more cases. v0.3 ablations report sign-coincidence shifts to characterize whether physics extensions cause phenomenon emergence cell-internally; they do not seek to maximize this number.

**Sign-zero threshold convention**: state-layer sign-coincidence is computed under |Δt| < 0.10 min ⇒ 0 (the conservative noise-floor estimate). v0.3 plan item 6 will replace this with a measured MJ1 first-passage noise floor.

---

## In planning

### v0.3.0 — extended-physics ablation suite + parameter-refinement track

**Scope**: characterize, under controlled ablations, which physics extensions or parameter modifications cause state-layer DC-AC acceleration to emerge cell-internally in the Chen2020/M50 sim. Each item is an isolated ablation against the X5-A baseline; multi-mechanism stacking is deferred to a later release.

**Methodology rule for all v0.3 items**: each ablation must report (a) the sim cell-internal outcome on the v0.1 case set (does state-layer acceleration emerge?), (b) the κ=1.5 cluster sub-statistics, (c) a Δt(Q) full-curve overlay against X5-A baseline on at least one representative case, and (d) a descriptive sign-coincidence vs MJ1 statistic. Item (d) is reported but not used as a pass/fail criterion. Configurations that do not change cell-internal behavior are documented and retained, not deleted.

#### Day 11 — Item 1: Lithium plating activation

**Implementation cost**: low (one PyBaMM `options` string change).
**Configuration**: `pybamm.lithium_ion.DFN(options={"thermal": "lumped", "lithium plating": "irreversible"})`. All other elements identical to X5-A baseline (Chen2020 standard parameter set, IDAKLU solver, V_init = 2.82 V via `pv.set_initial_state(0.01688)`). Run on the full 24-case 4-way table.

**Acceptance criteria** (three meaningful outcomes):

> (a) **Plating does not change X5-A sign on most cases** → plating is not the key switch for state-layer DC-AC acceleration emergence on the M50 cell → Day 12 proceeds with item 2 (OCP slope scan).
>
> (b) **Plating flips the sign on most cases** → plating is the key switch for state-layer phenomenon emergence on the M50 cell → Day 12 proceeds with cross-parameter-set replication (O'Kane2022, Marquis2019, Mohtat2020) to confirm the finding generalizes beyond Chen2020.
>
> (c) **Plating flips the sign in some (DC, AC, f) regions and not others** → identify the plating activation boundary in the (DC, AC, f) space → Day 12 conducts parameter scans within the activation and non-activation regions separately, mapping the boundary. This is the most scientifically informative outcome and aligns with the methodological style of Lee 2025 aSPM map.

Mechanism interpretation: lithium plating in DFN sim introduces a non-linear current-density-dependent loss that may activate asymmetrically under DC-AC modulation. The hypothesis tested is whether the AC oscillation crosses a plating-onset threshold during the negative-current half-cycle, producing an asymmetric net charging response that is absent in plating-disabled DFN.

Literature support: Frenander 2026 (NMC NE Li-plating + SEI dominant degradation), Bhoir 2021 (PCN advantage attributed to "avoiding Li-plating regime"), Guo 2024 (NMC532 pulse charging post-mortem evidence), Lee 2025 (aSPM + Li-plating overpotential map methodology).

#### Day 12 — Item 2: OCP slope scan

**Implementation cost**: medium (parametric modification of `Negative electrode OCP [V]` and/or `Positive electrode OCP [V]` functions in Chen2020 ParameterValues object).

**Rationale** (Day 9 7-way diagnostic matrix): the X6 family configurations (composite + sigmoid OCP, with various V_init protocols) showed sign-coincidence dispersion that suggests OCP plateau slope and hysteresis representation may be controlling variables for state-layer phenomenon emergence in sim. Day 12 tests this hypothesis under controlled conditions: vary OCP slope parametrically, hold all other configuration elements at X5-A baseline.

**Configuration**: X5-A baseline with one of the following OCP modifications applied (one ablation per modification, not stacked):
- *Flatten*: replace OCP function with a multiplicatively flatter version (e.g., scale dV/dx by 0.5 in a chosen SOC range).
- *Steepen*: replace OCP function with a multiplicatively steeper version (e.g., scale dV/dx by 1.5 in the same range).
- *Plateau-shift*: shift the OCP plateau location in SOC.

**Acceptance criteria**:

> (a) **OCP slope modification does not change cell-internal Δt(Q80) sign distribution** → OCP slope is not a primary controlling variable in the standard Chen2020 OCP shape range → next ablations focus on physics submodels (item 3 onwards).
>
> (b) **OCP slope modification flips Δt(Q80) sign on most cases** → OCP slope is a primary controlling variable; the M50 cell as configured may have an OCP geometry that suppresses state-layer acceleration where MJ1's OCP geometry permits it → next steps include OCP geometry comparison between Chen2020 and MJ1 (where MJ1 OCP data are available from existing experimental records).
>
> (c) **OCP slope modification flips sign in specific (DC, AC, f, SOC) regions** → identify the OCP-controlled region of state-layer phenomenon emergence; map under controlled OCP variations.

**Caveat on interpretation**: OCP slope modifications in PyBaMM do not necessarily correspond to physical OCP shapes of any real cell; they are sim sensitivity probes. Conclusions drawn are "OCP slope is a controlling variable in Chen2020/M50 sim", not "OCP geometry causally explains the MJ1 phenomenon".

#### Day 13+ — Items 3-7 (lower implementation priority)

**Item 3: Particle mechanics / Si–graphite kinetic asymmetry**
PyBaMM particle-mechanics submodel with chemistry-specific parameters (Si secondary phase mechanical coupling). Targets the ≈ 200 mAh sim AC-amplitude under-reach in the κ=1.5 cluster identified in Day 9 trajectory analysis. Acceptance criterion: cell-internal κ=1.5 cluster Δt(Q80) sign-distribution changes from baseline (currently all negative under X5-A) to mixed or all-positive under particle-mechanics activation.

**Item 4: Double-layer / extended kinetics**
Extended kinetics submodel for AC-coupled non-equilibrium effects beyond standard Butler–Volmer. Tests whether the standard BV formulation under-resolves transient capacitive coupling at f ≥ 0.01 Hz. Acceptance criterion: cell-internal Δt(Q80) sign distribution on the f ≥ 0.01 Hz subset shifts under extended kinetics activation, without regressing the f < 0.01 Hz subset.

**Item 5: Alternative parameter sets** (O'Kane2022, Marquis2019)
Same protocol stack and Δt(Q) accounting, swap the parameter set only. Tests parameter-set dependence at fixed model order. Acceptance criterion: cell-internal state-layer phenomenon emergence pattern is reported for each parameter set; differences inform which parameter ranges support the phenomenon.

**Item 6: MJ1 experimental Δt(Q*) noise-floor quantification**
Compute first-passage-time variance from existing MJ1 raw recordings (same-protocol replicates if available, otherwise from baseline-DC repeats). Required before the κ=1.5 cluster directional pattern in MJ1 can be reported as 3/3 rather than 2/2 + 1 boundary case. Decision rule: if the κ=1.5, 1τ exp Δt = +0.17 min falls within the noise floor, that case is reclassified as inconclusive in all subsequent reports. The measured noise floor will replace the current 0.10 min threshold for sign-coincidence reporting.

**Item 7: Parameter-refinement track on Chen2020** (carried over from the original v0.2 plan)
Sensitivity analysis on key Chen2020 parameters (D_s_p / D_s_n / heat-transfer h / electrolyte transference t_+) one at a time around literature midpoints, against the X5-A baseline. Selective fitting where MJ1-measured values are available from existing experimental records (HPPC-derived R0 and τ₂, observed cell capacity 3300 mAh, etc.); replace the corresponding Chen2020 default and re-run the v0.1 case set. Acceptance criterion: bound the parameter-uncertainty contribution to cell-internal Δt(Q80) behavior. If no single-parameter perturbation within physically defensible ranges produces qualitative state-layer behavior change, the residual structure is attributable to model architecture rather than parameter values. This track runs in parallel with items 1–4 and is not blocking; its purpose is to disambiguate model structure from parameter values as the primary controlling variable.

**Release format**: the next archived release (Zenodo DOI) is planned at v0.3.0. Intermediate v0.2.x development commits remain GitHub-only.

---

## v0.3.0 progress — Days 11–18B (executed)

The v0.3.0 plan as filed at the v0.2 release named seven ablation items against the X5-A baseline, with state-layer sign-coincidence (raw Δt sign vs MJ1) as the descriptive observable. Days 11–17 executed items 1, 2, and 5, and added three emergent items (AsymBV α scan, τ_ref re-derivation, phase audit). Day 18 then introduced a methodological reframing: under prescribed-current CC operation, raw Δt(Q) is dominated by the imposed current-waveform geometry and cannot serve as the verdict variable for non-geometric state-layer acceleration. Day 18B established a Δt_resid null baseline; from Day 19 onward, DC-vs-DCAC verdicts use Δt_resid rather than raw-Δt sign-coincidence.

### Day 11 — Item 1: Lithium plating (irreversible + partially reversible)

**Outcome**: branch (a). Plating in the physically reasonable parameter range (OKane2022 defaults, k_pl = 1e-9 m/s) does not flip cell-internal Δt(Q80) sign on the X5-A 24-case grid.
**Numbers**: 1/24 Q80 sign change vs X5-A; 0/24 A_Δt curve sign change; max |Δavg| = 0.084 min; plating loss 18–23 mAh on 5 Ah; CC time −5 to −7 %. Commit `a15dead`.
**Status**: closed. Day 12 proceeds with item 2 (OCP slope scan) and a 4-tier mechanism audit.

### Day 12 — Mechanism audit ranking + window lock

**Outcome**: 4-tier mechanism audit established. NOT SUPPORTED in tested range under raw-Δt verdict: solver, frequency, Q80 artifact, default plating, NE OCP A.1. A_Δt window per case fixed across baseline + all ablations (no self-adaptive windows).
**Status**: window rule locked. Commit `c036fd9`.

### Day 13 — Items 2–3 ablation grid: PE OCP + transport (D_s_n) + AsymBV α

**Outcome**: 6 ablations (PE_A1a / PE_A2a + B_Dsn_up/down + asymBV_α_up/down). 0 sign flips across 47 valid PE+B cases and 36 AsymBV cases (12 invalid_window resolved in Day 14 #1). Trajectory naive 1/95 vs robust 7/95 — confirmed threshold-classification artifact, not mechanism.
**Status**: multi-level null Day 11 + 12 + 13. Continuous shape metric introduced (Day 14 #0).

### Day 14 — Continuous shape metric + AsymBV α closure

**Outcome**: continuous MARD shape distance closes the trajectory-classification artifact. Sign-topology preserved at grid level (40/40 mismatches in near-zero <5 %peak, 0 in stable subset). AsymBV α scan technically closed via cross-α Q_hi from AsymBV-own Q_CC_end. Direct charge ≠ discharge asymmetry control verified on PyBaMM 26.x AsymBV (`Butler-Volmer transfer coefficient`): α weights oxidation branch, 1 − α weights reduction branch — non-textbook α_c convention. Empirical labels `α_up` / `α_down` adopted instead of theoretical charging-favoured / disfavoured.
**Status**: closed. Commits `fc2938a`, `4bd1285`.

### Day 15 — Item 3 prep: X6 phase clean test (deferred)

**Outcome**: 3 X6 phases all deferred or reframed. X6α (Chen2020 composite + sigmoid V_init unanchorable, plateau ≥ 3.31 V); X6β (physical-MJ1-init V_init = 2.51 V vs Day 9 V_init = 2.82 V, ΔV = −308 mV → V_min < 2.5 V in 3/24 baseline DCAC including severe 0.2 + 0.8 C / 10τ V_min = 1.71 V); X6γ (Chen2020 lacks lith / delith OCP and hyst decay).
**Cross-phase finding**: PyBaMM 26.3.1 + Chen2020 isolation bounded by chem-shift × V_min audit. Hard rule for chem-shift / mech-isolation: must include V_min audit (V_min_charge, V_below_2p5_fraction, low_voltage_class). Sign-topology only interpretable if class ∈ {clean} or {transient with frac < 0.02}.
**Status**: reframed as protocol-feasibility audit. Commits `baa713e`, `f99054d`, `2ccd48a`.

### Day 16 — Item 5: Alternative parameter sets (8-set chem-shift)

**Outcome**: 8 DFN sets / 5 layered-oxide groups. 4 DCAC fixed τ_label = 11.1 s + set_soc(0.05). 44/48 admissible, 4/48 infeasible_Vmin (5 Ah @ DC 0.2 + AC 1.0 / 10τ). 28 DC-vs-DCAC pairs: 0 positive_only / mixed under raw-Δt verdict at 60 s absolute + 0.5 % relative threshold. Negative-or-near-zero topology extends LG M50 → 5 layered-oxide groups under fixed τ_label and the tested subset.
**Hard rule from Day 16**: DCAC main protocol space |DC| + |AC| ≤ 1 C (MJ1-aligned); > 1 C is boundary regime only. Current function must use `pybamm.sin`; `model.events` kept.
**Status**: closed under raw-Δt verdict. **Re-audit pending under Δt_resid framework (Day 19A scope)** — 60 s threshold was cleared by margin (geometric baseline order ~10 s, exact value pending Day 19A computation), so the existing negative-or-near-zero topology is unlikely to flip but the conclusion category must be relabeled from "negative-or-near-zero" to "geometry-explained negative-or-near-zero".

### Day 17 — τ_ref re-derivation across 8 sets

**Outcome**: HPPC 1 C / 10 s + 600 s relax @ SoC ~10 % via set_soc(0.05) + 0.2 C / 900 s. Verdict STRUCTURED BROAD: tau2_biexp(600 s) max/min = 3.561 across 7 + 1 outlier (Ecker2015 outlier on 1 C < 1 A failure; 7-set ratio ~1.62). Spearman 0.590 between recovery-time family (tau_FG_eff / t95 / t99) and bi-exp family (fit-window sensitive).
**Decision**: Day 18 main descriptor for first τ rebasing = `tau_FG_eff`; secondary sensitivity = `tau2_secondary_60s`.
**Status**: closed (notebook 21).

### Day 18A — Phase audit

**Outcome**: PyBaMM positive = discharge; experiment-faithful PyBaMM equivalent of NGU201 ARB (`current = dc + ac · sin`) is the **charge-first** branch

    I_py = -I_DC - I_AC · sin(ωt)

which flips the v3 discharge-first convention used Day 8–17. v3 ORegan2022 V_min boundary reclassified as joint condition of discharge-first phase × slow native period × low-SoC start. Charge-first 3-set × 2-protocol smoke clean; max |Δt_resid| ≤ 0.034 s (Cell 4A v4).
**Status**: closed.

### Day 18B — Geometry-corrected protocol-matrix audit

**Outcome**: 3 sets (Ecker2015, Chen2020, ORegan2022) × 8 protocols (2 DC baselines + 6 charge-first DCAC at 0.1 τ / 1 τ / 10 τ for Group A 0.2C+0.4C and Group B 0.4C+0.6C) × SoC0 = 0.05 → 24 sims feasible_clean. 18 DCAC × DC_baseline pairs audited via

    Δt_resid(Q) = Δt_model(Q) − Δt_geom(Q)

where Δt_geom is computed analytically from the prescribed current waveform alone.
**18/18 near_zero. Overall max |Δt_resid| = 0.0441 s** across the matrix; ≥108× margin to per-protocol numerical floor `max(5·dt_eval, 1.0) s`; ≥1360× margin to the 60 s absolute threshold; 10⁻⁶ to 10⁻⁵ residual-to-geometric ratio at 10 τ. Apparent (raw) Δt_model under charge-first reaches up to ≈31.8 min on 10 τ ORegan but is fully explained by current-waveform geometry. Voltage-event pull-forward present and large (Q_to_Vmax shift up to −45.4 % on 10 τ ORegan Group B), but is a separate voltage-coupled phenomenon outside the CC-window Δt_resid.
**Cell 4A v4 closed-form result generalizes**: under prescribed-current CC, model dynamics affect V(t), termination, polarization, overpotential, and Q_to_Vmax but not Q_net(t); the state layer cannot express through Δt(Q).
**Status**: closed. Full 64-sim sweep optional. Details: `docs/day18B_close.md`.

---

## Δt_resid framework (Day 18B framing update)

For DC-vs-DCAC comparisons under prescribed-current CC operation, the verdict observable is now:

    Δt_resid(Q) = Δt_model(Q) − Δt_geom(Q)

where Δt_geom(Q) is the first-passage time difference computed analytically from the prescribed I(t) alone, and Δt_model(Q) is the same computed on the simulated Q_net(t) trajectory. Raw Δt_model(Q) is no longer the verdict variable for DC-vs-DCAC; it is reported alongside Δt_geom for transparency and as descriptive event-layer information.

Sign convention follows Constraint 4: `Δt = t_ref − t_DCAC, positive ⇒ AC accelerates`.

**Decision rule for future ablations**:

> (a) **|Δt_resid| < per-protocol numerical floor max(5·dt_eval, 1.0) s** → numerical null; not interpretable as state-layer signal.
>
> (b) **above floor but < 60 s** → small residual; inspect Q-window construction, phase metadata, dt_eval discretization, first-passage interpolation behaviour, and protocol feasibility before mechanistic interpretation.
>
> (c) **≥ 60 s with stable sign topology across the Q-window** → candidate non-geometric state-layer signal; escalate to mechanism analysis.

**Applicability scope of the Day 18B null floor**:

    PyBaMM 26.3.1 / DFN / no model options / no degradation / no plating / no thermal
    SoC0 = 0.05
    charge-first phase
    prescribed-current CC mode
    |DC| + |AC| ≤ 1 C
    sets tested: Ecker2015, Chen2020, ORegan2022
    protocol grid: 0.2C+0.4C and 0.4C+0.6C × 0.1τ / 1τ / 10τ

Not a universal claim about all chemistries, all controls, or all SoC ranges.

**DCAC-vs-DCAC same-protocol ablations** (Day 11–14 plating / OCP / transport / AsymBV α): geometric bias cancels by construction across both sides of the ablation, so the Day 11–14 raw-Δt conclusions remain valid for their stated scope. Phase-convention metadata still requires verification under Day 19A.

**0.1 τ rows** are reclassified as a numerical noise-floor probe layer: retained for floor characterization and interpolation behaviour, but not used as primary physical claim about presence or absence of state-layer effects. Strongest physical evidence comes from 10 τ rows where Δt_geom is largest and relative residual sensitivity is highest.

**Cell 5C signed-storage convention reconciliation**: Cell 5C v2 originally stored the signed `dt_model_s` and `dt_geom_s` columns with opposite sign to project canonical (Constraint 4). Patched after Day 18B close. All `max|·|` statistics and all near_zero verdicts unchanged. Long-format CSV `data/day18B_smoke_dtQ_resid_curves_long.csv.gz` and the summary CSV signed-mean columns regenerated under canonical sign convention.

---

## Day 19+ plan (post-18B)

### Day 19A — Retrospective phase + geometry audit

**Scope**: Day 8–10 notebooks + Day 16 chemistry-shift fixed-label DC-vs-DCAC.

**Procedure**: for each DC-vs-DCAC entry,

1. identify current function definition;
2. classify phase (charge-first / discharge-first);
3. classify comparison type (DC-vs-DCAC / DCAC-vs-DCAC same-protocol / DCAC-vs-different-DCAC);
4. determine whether geometry correction is required;
5. relabel conclusion category — `geometry-explained …` if residual is below floor + 60 s; `candidate non-geometric …` only if both criteria are exceeded.

**Output**: `data/day19A_retrospective_audit.csv` with columns `notebook | cell_or_script | protocol | current_formula | phase_label | comparison_type | raw_dt_valid | geometry_correction_required | old_verdict | new_status | commit_hash`.

### Day 19B — PyBaMM parameter-family availability audit

**Scope**: PyBaMM 26.3.1 internal parameter sets, no simulation.

**Procedure**: audit each parameter set on four axes — runnable with plain `pybamm.lithium_ion.DFN()`, supports `initial_soc = 0.05`, voltage cutoffs and Q_nom, chemistry classification (layered oxide NMC / NCA / LFP-plateau / other).

**Output**: `data/day19B_parameter_family_availability.csv`.

### Day 19C — Geometry-corrected chemistry-shift smoke

**Scope**: Chen2020 baseline + 1 NMC/NCA contrast (selected from 19B) + 1 LFP / strong-OCP contrast (selected from 19B).

**Configuration**: charge-first; Group A (DC = 0.2 C, AC = 0.4 C) and Group B (DC = 0.4 C, AC = 0.6 C); 10 τ only. Full reporting per pair: Δt_model + Δt_geom + Δt_resid + V(Q) + Q_to_Vmax + CV-entry shift.

**Acceptance criteria**:

> (a) **All chemistries: |Δt_resid| < per-protocol floor + 60 s** → DFN under prescribed-current CC does not generate non-geometric state-layer Δt(Q) across the tested chemistry range. Search extends to OCP-shape / voltage-boundary coupling axes outside the CC window.
>
> (b) **One or more chemistries: |Δt_resid| ≥ floor + 60 s with stable sign topology** → response basin identified. Aging branch and f(SOC) scheduling unlock; chemistry-specific mechanism analysis follows on the responsive parameter set.
>
> (c) **Mixed-sign or insufficient-window cases** → narrow protocol grid, re-audit window construction, possibly extend nτ to 1 τ for robustness before drawing chemistry-level conclusions.

---

## HOLD conditions (post-18B)

- **Aging branch**: HOLD until stable |Δt_resid| > Day 18B floor emerges in some PyBaMM model domain. Until a responsive domain is identified, aging studies risk being elaborate prescribed-current geometry rather than state-layer phenomena.
- **Dynamic f(SOC) / tau_ref(SOC) scheduling**: HOLD until Day 19C identifies a chemistry / OCP / voltage-control branch where non-geometric Δt_resid is observable. f(SOC) is the long-term Level-3 control paradigm but cannot be designed against a null response basin.
- **Items 3, 4, 6, 7 of v0.3 plan** (particle mechanics, double-layer extended kinetics, MJ1 Δt(Q*) noise-floor quantification, Chen2020 parameter refinement): deferred pending Day 19C outcome. Items remain valid as candidates within the v0.3.0 release boundary; ordering depends on which response basin (if any) Day 19C identifies.

---

## Long-term direction

Beyond v0.3, the framework's open questions extend in three directions; none is on a fixed schedule.

- **Cross-cell generalization**: re-run the same protocol stack on parameter sets representing different cell chemistries (NMC811, NCA, LFP) at the same κ-grid. Tests whether the AC-acceleration mechanism is chemistry-specific or generic.
- **Frequency-domain comparison** with non-PyBaMM impedance frameworks (literature DRT, Bessman 2018 high-frequency model class). Caveat: the present framework is strictly time-domain — frequency-domain extension requires a separate methodological track and is not within the scope of this repository.
- **Manuscript-side integration**: align the simulation methodology with the experimental manuscript (in preparation) so that the joint reading is cross-citable.

---

## Constraints carried forward

These constraints are locked across all future versions; deviations require an explicit rationale and a separate document.

1. **Strict-net charge accounting**: Q_net(t) = -∫I dt — no rectification, no AC smoothing, no monotonization.
2. **First-passage time on a common Q-grid** — no interpolated averages; Δt(Q) is a curve, not a scalar.
3. **Per-battery capacity normalization** — sim and exp Q-targets reference each cell's own observed capacity, not the nameplate. Sim Q80 = 4101 mAh (Chen2020 nominal max usable 5126 mAh × 0.80); exp Q80 referenced to the LG INR18650 MJ1 measured capacity 3300 mAh.
4. **Sign convention**: Δt = t_ref − t_DCAC, positive ⇒ AC accelerates Q-target attainment relative to the same-DC-rate reference. PyBaMM internal sign: +I = discharge, −I = charge. Sign-zero threshold for sign-coincidence reporting: |Δt| < 0.10 min ⇒ 0.
5. **τ_Chen for any frequency-rescaling analysis**: 23.83 s (Day 8 single-phase 60 s-window charge value at SOC = 20%), preserving methodological symmetry with the MJ1 experimental τ_ref = 20.29 s. The 5000 s-window value (47.0 s) is window-asymmetric to MJ1 and is not used.
6. **Time-domain only**: HPPC pulse + bi-exponential fitting. No EIS, Nyquist, DRT, or frequency-domain impedance characterization within this repository — a deliberate scope boundary, not an oversight.
7. **Solver convention**: All PyBaMM runs use IDAKLU (PyBaMM 4.x default; do not pass `solver=` explicitly). IDAKLU adapts its time step to the AC frequency content automatically. The X5-A 24-case data was numerically verified against this convention via dt_max sweep on rows 3 and 8 (see `PyBaMM_handoff_2026-04-28.md` §"Solver Verification"). If CasadiSolver is used explicitly, `dt_max ≤ 5 s` must be set for AC frequencies > 10 mHz to prevent AC undersampling.
8. **Layered evaluation framework** (adopted v0.2, see "Evaluation framing (layered)" above): event-layer uses sim/exp quantitative consistency criteria; state-layer uses cell-internal phenomenon emergence criteria, with cross-cell observations reported descriptively. State-layer sign-coincidence is read as an emergent behavior indicator, not a model-quality optimization target.

For DC-vs-DCAC verdicts under prescribed-current CC operation (Day 18B onward), the verdict variable is the residual Δt_resid(Q) = Δt_model(Q) − Δt_geom(Q), with Δt_geom computed analytically from the prescribed current waveform alone. Raw-Δt sign-coincidence remains valid as a descriptive cross-cell statistic under the layered evaluation framework (Constraint 8) but is no longer the primary verdict variable. Decision criterion and applicability scope: see "Δt_resid framework (Day 18B framing update)".

---

## Design principles

These principles govern how releases are scoped and produced; they predate v0.1 and are retained verbatim from the original ROADMAP.

- **MVP first**: deliver a functional release before extending scope. Each version solves one coherent question end-to-end before the next begins.
- **Documented approximations**: every simplification (e.g., Chen2020 used as a parameter set for LG M50 21700 in studies comparing against MJ1 data, in the absence of a fitted MJ1 parameter set) is explicitly flagged in code comments, notebook narrative, or this ROADMAP.
- **Reproducibility**: every result (figure, metric, sign-coincidence count) traceable to a notebook cell + parameter set version + git commit hash. Negative results are retained, not deleted.
