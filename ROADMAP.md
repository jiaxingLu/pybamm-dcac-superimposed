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

**Scientific outcome**: thermal channel (✅), CC kinetic channel (✅), Δt(Q80) categorical mismatch (❌). Two competing hypotheses left open at v0.1: cell-physics absence vs frequency-mismatch.

### v0.2.0 — model-configuration sweep + κ=1.5 trajectory diagnosis (GitHub-only)

**Scope**: expand the model space from a single SPMe configuration to five (SPMe / DFN / DFN + V_init protocol fix / composite + sigmoid forced V_init / composite + sigmoid natural V_init); disambiguate the v0.1 hypothesis pair via trajectory analysis on the κ=1.5 cluster.

**Deliverables**:
- HPPC characterization on Chen2020 (notebook 07): τ_Chen extraction at SOC = 20%, both directions, single-phase reference.
- X2 DFN replication of v0.1 batch (notebook 08): tests the SPMe-misses-AC-physics hypothesis.
- X4 DFN with Chen-rescaled frequency grid (notebook 09): tests the simple frequency-rescaling hypothesis.
- X5 DFN + V_init = 2.82 V protocol fix (notebook 10): best PyBaMM configuration at 62.5%.
- Day 9 V_init × model 2×2 control matrix (notebook 11): isolates V_init protocol effect from cell-physics representation.
- Day 9 composite + sigmoid HPPC stage 2 (notebook 12): identifies the failure mode of the composite + sigmoid representation in charge-direction post-pulse relaxation.
- Day 9 trajectory-level diagnosis on the κ=1.5 cluster: rules out the frequency-mismatch hypothesis (~5 octaves of frequency span, consistent reversal sign across all three τ labels).
- v0.1 Δt(Q80) sign-agreement audit (notebook 13): corrected to 12/23 (52.2%) from the 11/23 (48%) reported in the v0.1 release notes; X5-A protocol-fix recovery scope corrected to one κ=4 case (`0.2+0.8C 10τ`), not two as originally stated in Day 8 commit messages.

**Scientific outcome**:
- Frequency-mismatch hypothesis ruled out at the κ=1.5 cluster.
- Cell-physics hypothesis localized to: absence of an AC-coupled nonlinearity in DFN + Chen2020 standard parameters.
- 62.5% sign-agreement is the current best across five explored configurations (not a search-exhausted ceiling).

### Scope evolution between v0.1 and v0.2

The v0.2 scope filed at the v0.1 release was a *parameter-refinement track* — Chen2020 sensitivity analysis, selective fitting for MJ1 (D_s_p, D_s_n, h_cooling), 18650 geometric scaling, parameter cross-validation. v0.2 actually executed a *model-configuration sweep* (SPMe / DFN / DFN + V_init protocol fix / composite + sigmoid). The pivot was triggered on Day 8 by NGU201 V(t) baseline inspection, which revealed that the V_init = 2.51 V vs 2.82 V protocol mismatch — a single binary state-of-charge initialization choice — explained more sign-agreement variance than any single-parameter perturbation reasonably could. Parameter refinement was therefore deferred and is reabsorbed into the v0.3 plan as item 6 below.

---

## In planning

### v0.3.0 — extended-physics ablation suite + parameter-refinement track

**Scope**: test whether breaking the 62.5% sign-agreement ceiling requires moving beyond standard DFN + Chen2020. Each item below is an isolated ablation against the X5-A baseline; multi-mechanism stacking is deferred to a later release.

**Planned deliverables**:

1. **Lithium plating submodel under modulated current**
   - Activate PyBaMM plating-reaction options on the X5-A baseline.
   - Quantify κ-dependence of sign-agreement; the κ=1.5 cluster is the focal sub-statistic.
   - Hypothesis: AC modulation crosses the plating threshold asymmetrically, generating a net charging-rate enhancement that is absent in plating-disabled DFN.
   - Acceptance criterion: sign-agreement on the v0.1 case set ≥ 70% under one fixed plating parameter set, without regressing the κ < 1 subset.

2. **Particle-mechanics / Si–graphite kinetic asymmetry**
   - PyBaMM particle-mechanics submodel with chemistry-specific parameters (Si secondary phase mechanical coupling).
   - Targets the ≈ 200 mAh sim AC-amplitude under-reach in the κ=1.5 cluster identified in Day 9 trajectory analysis.
   - Acceptance criterion: κ=1.5 cluster sign-agreement ≥ 1/3 (currently 0/3 under X5-A).

3. **Double-layer / interfacial dynamics outside Butler–Volmer**
   - Extended kinetics submodel for AC-coupled non-equilibrium effects.
   - Hypothesis: the standard Butler–Volmer formulation under-resolves transient capacitive coupling at f ≥ 0.01 Hz.
   - Acceptance criterion: improvement on the f ≥ 0.01 Hz subset (1τ-level frequencies) without regressing the f < 0.01 Hz subset.

4. **Alternative parameter sets** (O'Kane2022, Marquis2019)
   - Same protocol stack and Δt(Q) accounting, swap the parameter set only.
   - Tests parameter-set dependence at fixed model order.
   - Outcome: bound the parameter-uncertainty contribution to the 62.5% ceiling.

5. **MJ1 experimental Δt(Q*) noise-floor quantification**
   - Compute first-passage-time variance from existing MJ1 raw recordings (same-protocol replicates if available, otherwise from baseline-DC repeats).
   - Required before the κ=1.5 reversal evidence base can be reported as 3/3 rather than 2/2 + 1 boundary case.
   - Decision rule: if the κ=1.5, 1τ exp Δt = +0.17 min falls within the noise floor, that case is reclassified as inconclusive in all subsequent reports.

6. **Parameter-refinement track on Chen2020 (carried over from the original v0.2 plan)**
   - Sensitivity analysis on key Chen2020 parameters (e.g., solid-phase diffusivities D_s_p / D_s_n, heat-transfer coefficient h, electrolyte transference t_+) one at a time around literature midpoints, against the X5-A baseline.
   - Selective fitting where MJ1-measured values are available from existing experimental records (HPPC-derived R0 and τ₂ from the M.Sc. thesis dataset, observed cell capacity 3300 mAh, etc.); replace the corresponding Chen2020 default and re-run the v0.1 case set.
   - Acceptance criterion: bound the parameter-uncertainty contribution to the 62.5% ceiling. If no single-parameter perturbation within physically defensible ranges raises sign-agreement to ≥ 65%, the residual mismatch is attributable to model structure rather than parameter values.
   - Methodological priority: this track is run *in parallel* with items 1–4 and is not blocking; its purpose is to establish whether items 1–4 are necessary at all, or whether a parameter rebalancing inside DFN + Chen2020 is sufficient.

**Methodology rule for v0.3**: each ablation must report (a) sign-agreement on the v0.1 case set, (b) the κ=1.5 cluster sub-statistics, and (c) a Δt(Q) full-curve overlay against X5-A and exp on at least one representative case. Configurations that fail to break 62.5% are documented and retained, not deleted, so that the negative results are part of the public record.

**Release format**: the next archived release (Zenodo DOI) is planned at v0.3.0. Intermediate v0.2.x development commits remain GitHub-only.

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
4. **Sign convention**: Δt = t_ref − t_DCAC, positive ⇒ AC accelerates Q-target attainment relative to the same-DC-rate reference. PyBaMM internal sign: +I = discharge, −I = charge.
5. **τ_Chen for any frequency-rescaling analysis**: 23.83 s (Day 8 single-phase 60 s-window charge value at SOC = 20%), preserving methodological symmetry with the MJ1 experimental τ_ref = 20.29 s. The 5000 s-window value (47.0 s) is window-asymmetric to MJ1 and is not used.
6. **Time-domain only**: HPPC pulse + bi-exponential fitting. No EIS, Nyquist, DRT, or frequency-domain impedance characterization within this repository — a deliberate scope boundary, not an oversight.

---

## Design principles

These principles govern how releases are scoped and produced; they predate v0.1 and are retained verbatim from the original ROADMAP.

- **MVP first**: deliver a functional release before extending scope. Each version solves one coherent question end-to-end before the next begins.
- **Documented approximations**: every simplification (e.g., Chen2020 used as an MJ1 proxy in the absence of a fitted MJ1 parameter set) is explicitly flagged in code comments, notebook narrative, or this ROADMAP.
- **Reproducibility**: every result (figure, metric, sign-agreement count) traceable to a notebook cell + parameter set version + git commit hash. Negative results are retained, not deleted.
