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

## Day 12+ decision tree

The downstream sequence past Day 12 depends on Day 11 plating outcome:

- **Day 11 outcome (a) — plating no effect** → Day 12 OCP slope scan as planned. If OCP scan also no effect on cell-internal phenomenon, Day 13 adds dual-phase anode (`particle phases: ("2","1")`); if still no effect, Day 14 adds `surface form: differential`. If three layers all no effect → significant scientific finding: state-layer DC-AC acceleration phenomenon has cell-form-factor dependence that standard PyBaMM physics options cannot reproduce on the M50 parameter set.

- **Day 11 outcome (b) — plating flips most cases** → Day 12 cross-parameter-set replication on O'Kane2022, Marquis2019, Mohtat2020 with plating activated, to confirm the plating effect generalizes beyond Chen2020 specifically. If confirmed across parameter sets, this is a strong cross-cell finding: lithium plating activation gates state-layer DC-AC acceleration in DFN sim.

- **Day 11 outcome (c) — plating flips selectively** → Day 12 conducts parameter scans within the plating-active and plating-inactive regions separately, mapping the activation boundary. This is the methodologically richest outcome and aligns with Lee 2025 aSPM map style.

In all branches: results are reported under the layered framing and acceptance criteria listed above. Sign-coincidence with MJ1 is reported descriptively but is not the pass/fail criterion.

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

---

## Design principles

These principles govern how releases are scoped and produced; they predate v0.1 and are retained verbatim from the original ROADMAP.

- **MVP first**: deliver a functional release before extending scope. Each version solves one coherent question end-to-end before the next begins.
- **Documented approximations**: every simplification (e.g., Chen2020 used as a parameter set for LG M50 21700 in studies comparing against MJ1 data, in the absence of a fitted MJ1 parameter set) is explicitly flagged in code comments, notebook narrative, or this ROADMAP.
- **Reproducibility**: every result (figure, metric, sign-coincidence count) traceable to a notebook cell + parameter set version + git commit hash. Negative results are retained, not deleted.
