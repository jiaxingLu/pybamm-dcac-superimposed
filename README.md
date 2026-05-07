# DC-AC Superimposed Charging — PyBaMM Validation Framework

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19788879.svg)](https://doi.org/10.5281/zenodo.19788879)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Physics-based simulation (PyBaMM SPMe + DFN, Chen2020 + lumped thermal) reproducing a DC-AC superimposed charging protocol for lithium-ion cells (LG INR18650 MJ1, 24 DC-AC + 6 DC baseline cases). Three-tier sim-vs-exp validation under strict-net charge accounting. v0.2 expands the model search to five configurations and reports findings under a layered evaluation framework that distinguishes event-layer model-validation criteria from state-layer cross-cell phenomenon-generalization observations.

**Status**: v0.2.0 development release · 30 cases × 5 model configurations (main sweep) · 14 commits · v0.1.0 archived at [10.5281/zenodo.19788879](https://doi.org/10.5281/zenodo.19788879). v0.2.0 is GitHub-only and is not minted to Zenodo; the next archived release is planned at v0.3.


> **Metric methodology update (2026-04-29, commits a15dead + 97f51dd; refined 2026-04-30, Day 12 Step 0)**: Day 11 stress testing revealed that the Q80 scalar first-passage metric used for the sign-coincidence numbers reported in this README is metric-unstable on the Chen2020/M50 sim side (16/24 cases show |Δt(Q*) range over Q20–Q90| > 5 min; 5/6 stress test cases sign-flip between Q80 scalar and A_Δt curve average). MJ1 experimental data remains metric-stable. The PyBaMM v0.3 plan adopts an area-based trajectory metric A_Δt = ∫Δt(Q)dQ as primary metric, motivated by the methodological reflection on the Δt(Q) framework that proposed A_Δt as a conceptual integral extension. The Δt(Q) concept and its derivative methods form a layered methodology: Masterarbeit (2025) introduced Δt(Q) as the state-equivalent time concept; the methodological reflection proposed A_Δt as a trajectory-integrated extension (not formalized in publication); the JES2 manuscript adopts discrete multi-slice evaluation at Q40/Q60/Q80 to study scalar-metric validity (whether Δt(Q) can be compressed into a single number); the PyBaMM project adopts the area-based A_Δt to study mechanism reachability (whether the state-layer DC-AC acceleration phenomenon emerges in simulation). Both originate from the Δt(Q) concept but address different questions and adopt different representations. A_Δt is therefore not derived from JES2, nor does PyBaMM extend JES2; the two are different projections of Δt(Q). The PyBaMM A_Δt window is per-case adaptive `[Q20=1025 mAh, max(min(Q_CC_end - 50 mAh, Q80=4101 mAh), Q40=2050 mAh)]` on Chen2020/M50 nominal capacity (5126 mAh usable), CC-only by construction. A Day 12 retrospective audit (`data/day12_pre_audit_Q_at_CC_end.csv`) confirms that Q80=4101 mAh falls in the CV phase for 18/24 sim cases, so the per-case adaptive window is in fact CC-only for all reported cases. Under this CC-only A_Δt metric, 22/24 sim cases give negative average Δt + 2/24 near-zero (|avg_dt| < 0.10 min) regardless of configuration; sim/exp sign-coincidence on the 3 cases with MJ1 raw curve data is 0/3. The Q80-scalar numbers below remain accurate but their interpretation as cross-cell phenomenon indicators is weakened by the metric instability finding. See `notebooks/14_plating_ablation.ipynb` and `data/results_day12_step0_A_dt_CC_only.csv` for the full audit.

---

## TL;DR

A 30-case batch sweep characterizes a DC-AC superimposed charging protocol in PyBaMM (SPMe and DFN with Chen2020 parameter set, representing LG M50 21700) and compares the simulation to experimental data on LG INR18650 MJ1 cells. **Chen2020 is not a calibrated proxy for MJ1**. Findings are reported under a layered evaluation framework:

- ✅ **Event layer (T_max, CC time, total time)** — sim/exp quantitative consistency is a defensible model-validation criterion. Thermal: mean ΔT_max = −1.9 °C, 93% within ±3 °C. CC kinetics: mean ΔCC = +13.1 min, sim/exp ≈ 1.07. Total time: 21/24 cases (87.5%) sign-coincidence on the AC-acceleration direction; sim mean ΔTotal = +8.4 min vs exp +9.95 min. Event-layer behavior is reproduced.
- 🔬 **State layer (Δt(Q80))** — reported as a cross-cell phenomenon-generalization observation, not as a model-quality criterion. Chen2020/M50 simulation, under the MJ1-derived frequency grid, does not robustly exhibit DC-AC state-layer acceleration cell-internally (sim mean Δt(Q80) on v0.1 SPMe ≈ −0.7 min; sign-coincidence with MJ1 on the v0.1 case set ranges from 9.1% to 62.5% across the five v0.2 main-sweep configurations under sign-zero threshold 0.10 min). MJ1 cell experiment shows the phenomenon (mean Δt(Q80) = +2.50 min). The cross-cell discrepancy is read as a substantive observation about how the phenomenon depends on cell type, not as a sim deficiency.
- 📐 **Cross-layer finding** — event-layer reproduces (87.5%) but state-layer does not robustly emerge (range 9–63% sign-coincidence) — this gap reflects that event-layer acceleration is largely captured by voltage-envelope arithmetic from AC oscillation, whereas state-layer acceleration requires deeper cell-physics mechanisms not robustly present under standard Chen2020 + DFN/SPMe physics options. The diagnostic power of the Δt(Q) metric — distinguishing apparent voltage-envelope acceleration from kinetic charge-rate acceleration — is independently verified by this sim-vs-exp gap.

> **Note on v0.1.0 sign-coincidence**: the v0.1 release notes report Δt(Q80) sign agreement at 11/23 (47.8%). The v0.2 audit (notebook 13) reconciles this against the 4-way sign-derivation in `data/results_day8_x5_4way_dt_Q80_v2.csv` and confirms 11/23 (47.8%) under sign-zero threshold |Δt| < 0.10 min — the same value as the original v0.1 report. (A previous internal note had reported 12/23; that count corresponded to the CSV's strict-sign convention, where a single boundary case `0.3+0.7C 10τ` with `dt_v01 = +0.06 min` was tagged as "+" rather than "0". The 0.10 min threshold is preferred for v0.2 reporting because |Δt| values below this are within the plausible MJ1 first-passage measurement noise; v0.3 plan item 6 will quantify the experimental noise floor formally.) Thermal and CC-kinetic channel statistics are unaffected.

---

## Evaluation framing (layered)

This section documents the methodological framework adopted in v0.2; it governs how all sign-coincidence and Δt(Q) numbers in this README are to be read.

**Event layer** — quantities that are direct measurable physical observables on a per-protocol basis (T_max, CC time, total charge time). Sim is evaluated against exp by quantitative consistency criteria (mean offset within tolerance, sign agreement on the acceleration direction). The thermal and CC-kinetic channels are validated under this layer in the standard way.

**State layer** — the Δt(Q*) metric is a derived quantity that compares first-passage time at a target net charge between a DC-AC protocol and its same-DC-rate baseline. Δt(Q*) > 0 means the AC-superimposed protocol reaches the Q-target faster than the DC-only baseline, *on the same cell*. Under v0.2's framing, the state layer is treated as follows:

- **Sim-internal claim**: for a given cell parameter set under sim, does the DC-AC protocol exhibit Δt(Q*) > 0 cell-internally? This is a property of the simulated cell, independent of MJ1.
- **Experiment-internal claim**: for the LG INR18650 MJ1 cell, does the DC-AC protocol exhibit Δt(Q*) > 0 in measurement? Reported separately.
- **Cross-cell comparison**: a sign-coincidence statistic between sim and exp on the v0.1 case set. This statistic is a *descriptive* cross-cell observation reflecting whether the state-layer phenomenon generalizes from MJ1 to the simulated cell. It is **not** a model-quality ranking and is **not** an acceptance criterion for any model configuration.

The implication for v0.2's main configuration sweep (table below): sign-coincidence counts across the five configurations describe how state-layer acceleration emerges or fails to emerge under each configuration on the Chen2020/M50 cell. They do not rank these configurations as "better" or "worse" reproductions of MJ1, because Chen2020 was never claimed as an MJ1-calibrated proxy.

The v0.3 ablation plan (notably item 1 lithium plating, item 2 OCP slope scan) is framed as: *which physics extensions or parameter modifications, when applied to Chen2020 sim, allow state-layer acceleration to emerge cell-internally*? Each ablation reports its sim-internal outcome on Chen2020 plus a descriptive comparison to MJ1 experiment; the comparison is informational, not a pass/fail criterion.

This layered framing was adopted in v0.2 after Day 9 trajectory analysis on the κ=1.5 cluster (sim Q_net oscillation as superimposed signal on retarded mean trajectory) made clear that the Chen2020/M50 cell is not exhibiting state-layer acceleration cell-internally regardless of MJ1 comparison; and after recognition that demanding sim match MJ1 over-claims when Chen2020 is parameterized for a different cell.

**Sign-zero threshold convention**: state-layer sign-coincidence in v0.2 is computed under |Δt| < 0.10 min ⇒ 0 (i.e., Δt values of magnitude below 0.10 min are treated as the "neither AC-accelerates-nor-AC-retards" category, on both sim and exp side). This threshold is a conservative noise-floor estimate; v0.3 plan item 6 will replace it with a measured MJ1 first-passage noise floor.

---

## Core finding

![Δt(Q80) sim vs exp](figures/06_sim_vs_exp_dt_Q80_scatter.png)

The figure compares simulated vs experimental time-savings at 80% state-of-charge for the v0.1 SPMe baseline on the v0.1 case set. Δt(Q80) > 0 means AC superposition reaches Q80 faster than the same-DC-rate baseline, on the cell to which the protocol is applied (sim Δt(Q80) is sim cell-internal; exp Δt(Q80) is MJ1 cell-internal).

The visible pattern — exp Δt(Q80) dominantly positive, sim Δt(Q80) distributed around zero — is the cross-cell observation that motivates the layered framing. v0.2 quantifies how this state-layer behavior responds to (i) higher-fidelity electrochemistry (DFN), (ii) initial-state protocol alignment (V_init = 2.82 V), and (iii) composite-anode + current-sigmoid hysteresis representation, on the Chen2020/M50 cell. None of the five main-sweep configurations causes the Chen2020/M50 cell to robustly exhibit state-layer acceleration cell-internally; the v0.3 plan tests whether extended physics submodels (lithium plating) and parameter modifications (OCP slope scan) change this.

---

## Validation results

### Channel-level summary (v0.1 SPMe baseline)

| Quantity | sim vs exp pattern | Statistics | Interpretation |
|---|---|---|---|
| **T_max** (29 cases) | systematic offset | mean ΔT = −1.90 °C, std = 0.84 °C, 93% within ±3 °C | Event layer ✅. Chen2020 thermal model captures qualitative behavior; offset attributable to PT100 surface vs cell-volume-averaged measurement convention plus heat-transfer coefficient calibration |
| **CC time** (23 DC-AC) | multiplicative offset | mean ΔCC = +13.1 min, sim/exp ≈ 1.07 | Event layer ✅. Chen2020 charge kinetics ~7% slower than MJ1, systematic |
| **ΔTotal time** (24 DC-AC, v0.1 SPMe) | sim/exp consistency | sign-coincidence 21/24 (87.5%); sim mean = +8.4 min, exp mean = +9.95 min | Event layer ✅. Sim reproduces the AC-shortens-total-charge-time direction on the Chen2020/M50 cell; quantitative magnitude matches within ~16% |
| **Δt(Q80)** (23 DC-AC, v0.1 SPMe) | cross-cell phenomenon report | sim mean = −0.70 min (Chen2020/M50 cell); exp mean = +2.50 min (MJ1 cell); descriptive sign-coincidence 11/23 (47.8%) | State layer 🔬. Chen2020/M50 sim does not robustly exhibit state-layer DC-AC acceleration cell-internally under the MJ1-derived frequency grid; MJ1 cell does. Reported as cross-cell observation under layered framing |

The 40-percentage-point gap between event-layer ΔTotal sign-coincidence (87.5%) and state-layer Δt(Q80) sign-coincidence (47.8%) is the primary methodological finding of v0.2: the event-layer time savings are largely a voltage-envelope arithmetic consequence of AC oscillation reaching the 4.2 V cutoff at oscillation peaks (which sim reproduces faithfully), while the state-layer net-charge-rate acceleration requires a deeper cell-physics mechanism that the Chen2020/M50 cell, under standard DFN/SPMe physics options, does not robustly exhibit cell-internally.

### Main configuration sweep on Δt(Q80) sign-coincidence (v0.2)

The values below are reported as cross-cell descriptive statistics under the layered framing, not as a ranking of model quality.

| Configuration | V_init | Cases | Sign-coincidence |
|---|---|---:|---:|
| v0.1 SPMe | 2.51 V (natural) | 23 | 11/23 (47.8%) |
| X2 DFN | 2.51 V (natural) | 23 | 11/23 (47.8%) |
| X5-A DFN + V_init protocol fix | 2.82 V (forced) | 24 | 15/24 (62.5%) |
| X6α composite + sigmoid (forced V_init) | 2.82 V (forced) | 22 | 2/22 (9.1%) |
| X6β-v2 composite + sigmoid (natural rest) | natural | 22 | 10/22 (45.5%) |

Sign-coincidence is computed under |Δt| < 0.10 min ⇒ 0 convention. Audit and reconciliation against the CSV strict-sign convention is locked in `notebooks/13_readme_v02_audit.ipynb`.

**Notes on each configuration**:
- *v0.1 SPMe / X2 DFN*: comparable sign-coincidence (~48%) on the same V_init = 2.51 V protocol suggests model-order (SPMe vs DFN) is not the determining variable on the Chen2020/M50 cell at this parameter set.
- *X5-A*: forcing V_init = 2.82 V via `pv.set_initial_state(0.01688)` aligns the sim start state with the MJ1 experimental U₀₀ = 2.82 V baseline. This change shifts sign-coincidence to 15/24 (62.5%) and recovers one κ=4 case (`0.2+0.8C 10τ`) that was Min-V-infeasible at V_init = 2.51 V (denominator goes from 23 to 24).
- *X6α / X6β-v2*: composite-anode (Si secondary phase) + current-sigmoid OCP hysteresis configurations. Two cases each (κ=4 cluster) were Min-V-infeasible (denominator 22). The dispersion between X6α (forced V_init, 9.1%) and X6β-v2 (natural rest, 45.5%) is a finding about how V_init protocol interacts with composite OCP representation; mechanistic interpretation is deferred to v0.3 controlled experiments.

**Two additional configurations** were tested in Day 9 diagnostic 7-way matrix (notebook 11) but are not part of the v0.2 main-sweep portfolio; their values are disclosed here for completeness:
- *X5β* (DFN single-phase + natural rest, V_init = 2.51 V): 17/24 (70.8%)
- *X6α-NS* (composite + NO sigmoid + forced V_init = 2.82 V): 2/22 (9.1%)

These diagnostic configurations and the dispersion among V_init protocols across the seven-configuration matrix raise testable hypotheses about V_init protocol as a controlling variable for state-layer phenomenon emergence; the v0.3 plan includes V_init-isolation experiments to test these hypotheses under controlled conditions. Raw data in `data/results_day9_7way_final_matrix.csv`.

### Trajectory analysis on the κ=1.5 cluster (Day 9)

Under the X5-A configuration, the κ=1.5 cluster (`0.2 C + 0.3 C` amplitude × {1τ, 10τ, 34.8τ} frequencies) shows a directional sim-vs-exp gap:

| Case | sim Δt(Q80) [min] | exp Δt(Q80) [min] | sim/exp sign concordance |
|---|---:|---:|:---:|
| 0.2 C + 0.3 C, 1τ | −0.58 | +0.17 | mixed |
| 0.2 C + 0.3 C, 10τ | −5.30 | +5.05 | opposite |
| 0.2 C + 0.3 C, 34.8τ | −2.15 | +15.03 | opposite |

Sign convention: Δt = t_ref − t_DCAC, positive ⇒ AC accelerates Q-target attainment relative to the same-DC-rate reference, on the cell to which the protocol applies.

The κ=1.5 cluster spans frequencies 0.0143, 0.00143, and 0.000412 Hz — a 35× ratio across ~1.5 decades (≈5 octaves). The sim sign is consistently negative across this frequency range (i.e., on the Chen2020/M50 cell, AC superposition does not produce state-layer acceleration in this κ regime). The exp sign on MJ1 is positive across the same range. This **rules out** the v0.1-era "frequency-mismatch" hypothesis that Chen2020 might exhibit AC acceleration at a different intrinsic frequency band — a frequency-grid artifact would cluster on a narrow band, not span ~5 octaves with consistent sign.

Trajectory inspection on Q_net(t) at Q80 = 4101 mAh shows the simulation carries the AC oscillation as a superimposed signal (≈200 mAh peak-to-peak in the 10τ case) on a marginally retarded mean trajectory — the oscillation peaks fail to break Q80 ahead of the 0.2 C-DC reference. The Chen2020/M50 cell, under standard DFN + Chen2020 parameters, does not exhibit a kinetic mean-trajectory acceleration under DC-AC at this κ regime.

Whether to call this "missing physics in the model" or "an intrinsic property of the Chen2020/M50 cell that differs from MJ1" depends on the framing scope. Under v0.2's layered framing, both descriptions are valid statements at different scopes:
- *On the Chen2020/M50 cell as configured*, this is a cell-internal property of the simulation under standard physics options.
- *Across cells*, this is a phenomenon-generalization observation: the κ=1.5-region acceleration found in MJ1 does not appear in the Chen2020/M50 sim.

The v0.3 ablation plan (notably item 1 lithium plating, item 2 OCP slope scan) tests which physics extensions or parameter modifications, when applied to the Chen2020/M50 sim, cause state-layer acceleration to emerge cell-internally in this κ regime.

#### Caveat on the κ=1.5, 1τ case

The exp Δt(Q80) = +0.17 min for this case is small relative to the plausible measurement-noise floor of the MJ1 first-passage time. A formal noise-floor quantification for the experimental Δt(Q*) is pending (v0.3 plan item 6). If this case falls within noise, the κ=1.5 directional pattern in MJ1 reduces from 3/3 to 2/2 (the 10τ and 34.8τ cases, both well above noise, retain their pattern).

---

## Reproducibility

**Tested on**: macOS Apple Silicon, Python 3.12.13, PyBaMM 26.3.1.

```bash
git clone https://github.com/jiaxingLu/2026_pybamm_dcac.git
cd pybamm-dcac-superimposed
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# v0.1 SPMe baseline (~25 s wall-clock)
jupyter lab notebooks/05_batch_scan.ipynb
jupyter lab notebooks/06_validation_figures.ipynb

# v0.2 model-configuration sweep
jupyter lab notebooks/07_hppc_chen2020.ipynb                         # τ_Chen extraction
jupyter lab notebooks/08_x2_dfn_mj1freq.ipynb                        # X2: DFN replication of v0.1
jupyter lab notebooks/09_x4_dfn_chenfreq.ipynb                       # X4: H2 frequency-rescaling test
jupyter lab notebooks/10_x5_dfn_corrected_protocol.ipynb             # X5: V_init = 2.82 V protocol fix
jupyter lab notebooks/11_chen2020_composite_v_init_diagnostic.ipynb  # composite + sigmoid 2×2 control matrix (also contains X5β and X6α-NS diagnostic data)
jupyter lab notebooks/12_hppc_chen2020_composite.ipynb               # composite + sigmoid HPPC stage 2
jupyter lab notebooks/13_readme_v02_audit.ipynb                      # v0.2 audit + Framing C supporting data
```

The full results JSON files are gitignored; per-configuration summary CSVs are versioned under `data/`.

### Solver convention

All v0.2 PyBaMM runs use **IDAKLU** (PyBaMM 4.x default; do not pass `solver=` explicitly). IDAKLU adapts its time step to the AC frequency content automatically. The X5-A 24-case data was numerically verified against this convention via `dt_max` sweep on rows 3 and 8 of the 4-way table — see `PyBaMM_handoff_2026-04-28.md` §"Solver Verification" for the full audit record. If a future user explicitly switches to CasadiSolver, `dt_max ≤ 5 s` must be set for AC frequencies > 10 mHz to prevent AC undersampling; without this, the AC signal is averaged out at the default ~60 s adaptive step and produces sim Δt values close to zero (a non-physical result of solver configuration, not of the model).

---

## Repository structure

```
.
├── notebooks/
│   ├── 01_hello_pybamm.ipynb                          # Environment validation
│   ├── 02_dcac_first_injection.ipynb                  # First DC-AC waveform via Interpolant
│   ├── 03_dc_baseline_0.9C.ipynb                      # End-to-end 5-phase protocol
│   ├── 04_dcac_single_case.ipynb                      # Representative single case
│   ├── 05_batch_scan.ipynb                            # 30-case sweep + run_single_case()
│   ├── 06_validation_figures.ipynb                    # v0.1 validation figures
│   ├── 07_hppc_chen2020.ipynb                         # Day 8: Chen2020 HPPC, τ_Chen extraction
│   ├── 08_x2_dfn_mj1freq.ipynb                        # Day 8 X2: DFN replication of v0.1 batch
│   ├── 09_x4_dfn_chenfreq.ipynb                       # Day 8 X4: DFN with Chen-rescaled frequency
│   ├── 10_x5_dfn_corrected_protocol.ipynb             # Day 8 X5: DFN + V_init = 2.82 V protocol fix
│   ├── 11_chen2020_composite_v_init_diagnostic.ipynb  # Day 9: composite + sigmoid 2×2 control matrix; X5β, X6α-NS diagnostic data
│   ├── 12_hppc_chen2020_composite.ipynb               # Day 9: composite + sigmoid HPPC stage 2
│   └── 13_readme_v02_audit.ipynb                      # v0.2 audit + layered framing supporting data (sign-zero threshold reconciliation, reproduction matrix)
├── figures/
│   ├── 03_dc_baseline_full_protocol.png               # v0.1: DC baseline 5-phase trace
│   ├── 04_dcac_0.3C+0.7C_10tau_full_protocol.png      # v0.1: representative DC-AC trace
│   ├── 04c_Qnet_trajectory_with_events.png            # v0.1: Q_net first-passage diagnostic
│   ├── 06_sim_vs_exp_dt_Q80_scatter.png               # v0.1 core finding (Δt(Q80))
│   ├── 06_sim_vs_exp_Tmax_scatter.png                 # v0.1 thermal validation
│   ├── 06_sim_vs_exp_CCtime_scatter.png               # v0.1 CC kinetic offset
│   ├── 07_hppc_chen2020_R0_split.png                  # Day 8: HPPC R0 split charge/discharge
│   ├── 07_hppc_chen2020_SOC50_signal.png              # Day 8: HPPC pulse signal at SOC = 50%
│   ├── 07_hppc_chen2020_SOC100_dis_diagnostic.png     # Day 8: HPPC diagnostic at SOC = 100%
│   ├── 07_hppc_chen2020_stage2_overview.png           # Day 8: HPPC τ_Chen overview
│   ├── x5_dt_Q_curves_with_V_init_check.png           # Day 8 X5: Δt(Q) full-curve + V_init alignment
│   ├── x5_dt_Q_full_curves_0.3+0.7C.png               # Day 8 X5: Δt(Q) for the 0.3 + 0.7 C subset
│   ├── day9_final_4x4_control_matrix.png              # Day 9: V_init × model 2×2 control matrix (raw)
│   ├── day9_final_4x4_control_matrix_v2.png           # Day 9: V_init × model 2×2 (normalized Q axis)
│   └── day9_0p2_0p3C_trajectory_v2.png                # Day 9: κ=1.5 trajectory diagnosis
├── data/
│   ├── figure1_master_table_cleaned.csv               # Experimental ground truth (30 cases)
│   ├── delta_tq_curve_data_strict_net.csv             # Δt(Q) full-curve trajectory data (v0.1)
│   ├── 0.3C dc.csv                                    # DC baseline reference for Δt(Q) curve
│   ├── results_day6_summary.csv                       # v0.1 SPMe per-case summary
│   ├── results_day8_x2_*.csv                          # X2 DFN summaries (mj1freq + three_way_dt_Q80)
│   ├── results_day8_x4_*.csv                          # X4 DFN with Chen-rescaled frequency
│   ├── results_day8_x5*.csv                           # X5 DFN + V_init protocol fix (5A / 5BC / 4way)
│   ├── results_day8_stage2_hppc_chen2020.csv          # HPPC τ_Chen extraction
│   └── results_day9_*.csv                             # Day 9 composite + sigmoid + control matrix CSVs (incl. 7-way diagnostic with X5β, X6α-NS)
├── scripts/
│   └── add_cc_cv_columns.py                           # Reproducible CSV augmentation
├── ROADMAP.md
├── requirements.txt
└── README.md
```

The state-layer sign-coincidence audit (sign-zero threshold reconciliation, X5β / X6α-NS diagnostic disclosure, full per-case detail) is locked in `notebooks/13_readme_v02_audit.ipynb`; that notebook also contains the reproduction matrix data underlying the layered framing's event-vs-state gap.

---

## Methodology snapshot

**Cell models compared (v0.2 main sweep)**:
- v0.1: SPMe (single particle with electrolyte) + Chen2020 standard parameters (representing LG M50 21700).
- v0.2: DFN (full pseudo-2D Doyle–Fuller–Newman) + Chen2020; composite-anode + current-sigmoid OCP hysteresis variant for X6.

All variants run with lumped thermal submodel and IDAKLU solver (see "Solver convention" above). **Chen2020 is not a calibrated proxy for the LG INR18650 MJ1 cell on which experimental data were measured**; sim and exp comparisons follow the layered framing described above.

**Protocol** (5 steps in single `pybamm.Experiment`):

1. Phase 0a: 1 C discharge to 2.5 V.
2. Phase 0b: CV hold at 2.5 V until C/136.
3. Phase 1: rest 3805 s.
4. Phase 2: DC-AC charge `I(t) = I_DC + A · sin(2π · f · t)` until V = 4.2 V (via `pybamm.step.CustomStepExplicit`).
5. Phase 3: CV hold at 4.2 V until C/68.

**V_init protocol fix (v0.2, X5-A)**: PyBaMM's natural rest after 1 C-dis-CV equilibrates to V = 2.51 V on the Chen2020/M50 cell. The MJ1 experimental protocol terminates the discharge phase at U₀₀ = 2.82 V after a 63-min rest. The 310 mV gap is attributable to Si–graphite hysteresis in the MJ1 cell that is not represented by the Chen2020 single-phase parameter set. Setting V_init = 2.82 V via `pv.set_initial_state(0.01688)` aligns the Chen2020 sim's initial voltage with the MJ1 experimental cross-protocol baseline. This change shifts the X2 DFN configuration (V_init = 2.51 V, 11/23 sign-coincidence) to X5-A (V_init = 2.82 V, 15/24 sign-coincidence) and recovers one κ=4 case (`0.2+0.8C 10τ`) that was Min-V-infeasible at 2.51 V. The shift is a property of how the protocol modification interacts with the Chen2020 OCV curve on the M50 parameter set; it is not a claim that Chen2020 is now better-aligned with MJ1 at the cell-physics level. The dispersion of sign-coincidence across V_init protocols seen in the diagnostic 7-way matrix (X5β natural rest 70.8% vs X5-A forced 62.5%; X6α forced 9.1% vs X6β-v2 natural 45.5%) raises hypotheses about V_init protocol as a controlling variable; v0.3 plan includes controlled V_init-isolation experiments.

**Composite + sigmoid investigation (v0.2, X6 + Day 9 stage 2)**: a composite-anode parameter set with current-sigmoid OCP hysteresis was tested as a representation closer to MJ1's Si–graphite chemistry. Sign-coincidence on the v0.1 case set is 2/22 (9.1%) for X6α (forced V_init = 2.82 V) and 10/22 (45.5%) for X6β-v2 (natural rest). The X6α-vs-X6β-v2 dispersion shows that V_init protocol interacts non-trivially with the composite + sigmoid configuration; the X6α-NS diagnostic (composite without sigmoid, also forced V_init, 2/22) suggests forced V_init dominates over OCP option in suppressing state-layer phenomenon emergence in this regime. **Mechanistic interpretation requires controlled experiments and is deferred to v0.3** — see ROADMAP. Stage-2 HPPC characterization on `Chen2020_composite` (notebook 12) showed that charge-direction post-pulse relaxation is non-monotonic under current-sigmoid OCV-branch switching, causing bi-exponential fit collapse (8/8 charge cases fail; R² ≈ 0); discharge-direction relaxation fits successfully (median τ₂ = 53.2 s, vs single-phase discharge median 45.4 s). For the τ_Chen value used in any cross-cell frequency-rescaling analysis, the Day 8 single-phase 60 s-window charge value at SOC = 20% (τ_Chen = 23.83 s) is retained, preserving methodological symmetry with the MJ1 experimental τ_ref = 20.29 s (also 60 s-window). The 5000 s-window value (47.0 s) is window-asymmetric to MJ1 and is not used.

**Strict-net charge accounting** (six locked constraints):

1. Signed integration: `Q_net(t) = -∫I dt` (no rectification).
2. Non-monotonic Q(t) preserved (AC reversal causes local decreases).
3. First-passage only (no interpolated averages).
4. Unified Q-grid across cases (each battery uses own capacity).
5. No signal modification, no AC smoothing.
6. Δt(Q) is a curve, not a scalar.

**Sign convention**: PyBaMM standard, +I = discharge, −I = charge. Δt(Q) sign convention: Δt = t_ref − t_DCAC, positive ⇒ AC accelerates Q-target attainment relative to the same-DC-rate reference. Sign-zero threshold for sign-coincidence reporting: |Δt| < 0.10 min ⇒ 0.

**Capacity normalization**: Q-grid Q40/Q60/Q80 referenced to each battery's own observed capacity ceiling. For the simulation, Chen2020 nominal max usable capacity is 5126 mAh, giving Q80 = 4101 mAh; for the MJ1 experiment, Q80 is referenced to the observed cell capacity 3300 mAh (LG INR18650 MJ1 measured value, which differs from the nameplate 3500 mAh).

---

## Release status

### v0.1.0 (archived)

- [x] PyBaMM 26.3.1 environment validated
- [x] Chen2020 baseline (1 C discharge)
- [x] DC-AC current injection via `CustomStepExplicit`
- [x] 5-phase protocol pipeline
- [x] DC-AC single case end-to-end (0.3 C + 0.7 C @ 10τ)
- [x] 30-case batch sweep (24 DC-AC + 6 DC baseline) on SPMe
- [x] Three-tier sim-vs-exp validation figures

### v0.2.0 (this release)

- [x] Chen2020 HPPC characterization (notebook 07): τ_Chen extraction at SOC = 20 %, both directions, single-phase reference
- [x] X2 DFN replication of v0.1 batch (notebook 08): tests SPMe-vs-DFN model-order effect on state-layer behavior
- [x] X4 DFN with Chen-rescaled frequency grid (notebook 09): rules out the simple frequency-rescaling hypothesis
- [x] X5 DFN + V_init = 2.82 V protocol fix (notebook 10): X5-A reaches state-layer sign-coincidence 15/24 (62.5%)
- [x] Day 9 V_init × model 2×2 control matrix (notebook 11): isolates V_init protocol effect from cell-physics representation; produces X5β / X6α-NS diagnostic data
- [x] Day 9 composite + sigmoid HPPC stage 2 (notebook 12): characterizes composite-OCP-induced suppression of bi-exponential charge fit
- [x] Day 9 trajectory-level diagnosis on the κ=1.5 cluster: rules out the frequency-mismatch hypothesis raised in v0.1
- [x] X5.5 numerical audit (`PyBaMM_handoff_2026-04-28.md` §"Solver Verification"): IDAKLU vs CasadiSolver dt_max sweep on rows 3 and 8; X5-A 24-case data confirmed numerically reliable
- [x] v0.2 audit + framing recalibration (notebook 13): sign-zero threshold reconciliation across CSV strict-sign vs threshold 0.10; layered evaluation framework adopted; X5β / X6α-NS diagnostic disclosure

See `ROADMAP.md` for the v0.3 plan.

---

## Citation

For citation, use the version-specific reference:

**v0.1.0** (peer-reviewable archived release):

```bibtex
@software{lu_2026_pybamm_dcac_v01,
  author    = {Lu, Jiaxing},
  title     = {{DC-AC Superimposed Charging Validation:
                PyBaMM-based sim-vs-exp framework}},
  month     = apr,
  year      = 2026,
  publisher = {Zenodo},
  version   = {v0.1.0},
  doi       = {10.5281/zenodo.19788879},
  url       = {https://doi.org/10.5281/zenodo.19788879}
}
```

**v0.2.0** (this release; GitHub-only development snapshot, not minted to Zenodo): cite the repository at the v0.2.0 git tag, e.g. `https://github.com/jiaxingLu/pybamm-dcac-superimposed/tree/v0.2.0`. The next archived release is planned at v0.3.

The corresponding experimental manuscript (in preparation) will be linked here upon publication.

---

## Author

**Jiaxing Lu** — M.Sc. Electrical Engineering, Hochschule Mittweida
Specialization: lithium-ion battery characterization and modeling

- GitHub: [@jiaxingLu](https://github.com/jiaxingLu)
- ORCID: [0009-0009-6311-6688](https://orcid.org/0009-0009-6311-6688)
- LinkedIn: [jiaxinglu](https://www.linkedin.com/in/jiaxinglu/)

## License

MIT

<!-- DAY19A_PHASE_CONVENTION_START -->
## Phase convention and Day 19A reclassification

Historical DC–AC notebooks 04–20 used a discharge-first PyBaMM waveform:

    I_py(t) = -|I_DC| + |I_AC| sin(ωt)

PyBaMM uses `I > 0` for discharge and `I < 0` for charge. The MJ1 experimental NGU201 ARB waveform corresponds to charge-first after translation into PyBaMM sign:

    I_py(t) = -|I_DC| - |I_AC| sin(ωt)

Day 19A identifies this as an implementation–intent phase-alignment mismatch. Historical simulations are reclassified rather than discarded.

Raw first-passage `Δt(Q)` is phase-coupled through current geometry. Non-geometric state-layer acceleration claims require:

    Δt_resid(Q) = Δt_model(Q) − Δt_geom(Q)

Details:

    docs/day19A_retrospective_audit.md
    data/day19A_step6_evidence_register.csv
    data/day19A_step6_final_verdict_summary.csv
<!-- DAY19A_PHASE_CONVENTION_END -->


## Day21A MJ1 full-protocol segmentation audit

The Day21A audit closes the MJ1 experimental full-protocol segmentation analysis for the 0.3C reference group and the 0.3C+0.7C DC–AC protocols at 0.1τ, 1τ, and 10τ.

The audit separates raw state-equivalent first-passage gain from mechanism attribution. The main conclusion is that the measured full-protocol gains are real, but not mechanism-pure. The preferred interpretation is a boundary/control-state mediated first-passage gain with diagnostic caveats, rather than demonstrated non-geometric Segment-A acceleration.

Key outputs:

- `docs/day21A_close.md`
- `data/day21A_step7_unified_MJ1_PyBaMM_mechanism_verdict.csv`
- `data/day21A_step8_closure_summary.csv`
- `notebooks/25_day21A_MJ1_experimental_segment_audit.ipynb`

Raw NGU201 CSV files are not tracked in Git and are excluded via `.gitignore`.

