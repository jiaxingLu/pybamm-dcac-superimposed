# DC-AC Superimposed Charging — PyBaMM Validation Framework

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19788879.svg)](https://doi.org/10.5281/zenodo.19788879)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Physics-based simulation (PyBaMM SPMe + DFN, Chen2020 + lumped thermal) reproducing a DC-AC superimposed charging protocol for lithium-ion cells (LG INR18650 MJ1, 24 DC-AC + 6 DC baseline cases). Three-tier sim-vs-exp validation under strict-net charge accounting; v0.2 expands the model search to five configurations and isolates the residual sign-mismatch through trajectory-level diagnosis.

**Status**: v0.2.0 development release · 30 cases × 5 model configurations · 13 commits · v0.1.0 archived at [10.5281/zenodo.19788879](https://doi.org/10.5281/zenodo.19788879). v0.2.0 is GitHub-only and is not minted to Zenodo; the next archived release is planned at v0.3.

---

## TL;DR

A 30-case batch sweep validates a DC-AC superimposed charging protocol against experimental data on LG INR18650 MJ1 cells. Three independent error channels are isolated:

- ✅ **Thermal**: systematic offset (mean ΔT_max = −1.9 °C, 93% within ±3 °C) — Chen2020 thermal model captures qualitative behavior.
- ✅ **CC kinetics**: multiplicative offset (sim/exp ≈ 1.07, range [0.99, 1.17]) — Chen2020 ~7% slower than MJ1.
- ❌ **AC kinetics**: categorical mismatch. v0.1 baseline (SPMe + Chen2020) reaches 12/23 (52.2%) sign agreement on Δt(Q80). v0.2 explores five model configurations (SPMe / DFN / DFN + V_init protocol fix / composite + sigmoid forced V_init / composite + sigmoid natural V_init); the present best is **DFN + V_init = 2.82 V protocol fix** at **15/24 (62.5%)**. Trajectory-level diagnosis on the κ=1.5 cluster rules out the frequency-mismatch hypothesis raised in v0.1 and points to absence of an AC-coupled cell-physics nonlinearity in the DFN + Chen2020 standard parameter set.

> **Note to users of v0.1.0**: the v0.1 release notes report Δt(Q80) sign agreement as 11/23 (48%). A v0.2 audit against the locked sign-derivation in `data/results_day8_x5_4way_dt_Q80_v2.csv` corrects this to **12/23 (52.2%)**; the discrepancy reflects a statistical convention change at sign-zero boundary cases (exp Δt = 0.00–0.05 min). The thermal and CC-kinetic channel statistics are unaffected.

---

## Core finding

![Δt(Q80) sim vs exp](figures/06_sim_vs_exp_dt_Q80_scatter.png)

The figure compares simulated vs experimental time-savings at 80% state-of-charge for the v0.1 SPMe baseline: Δt(Q80) > 0 means AC superposition accelerates Q80 attainment relative to the same-DC-rate baseline.

The qualitative direction-mismatch on Δt(Q80) is **not** a quantitative offset (which is observed on T_max and CC time) but a categorical mismatch — the central scientific result of this validation. v0.2 quantifies how this mismatch responds to (i) higher-fidelity electrochemistry (DFN), (ii) initial-state protocol alignment, and (iii) composite-anode + current-sigmoid hysteresis representation.

---

## Validation results

### Channel-level summary (v0.1 SPMe baseline)

| Quantity | sim vs exp pattern | Statistics | Interpretation |
|---|---|---|---|
| **T_max** (29 cases) | systematic offset | mean ΔT = −1.90 °C, std = 0.84 °C, 93% within ±3 °C | Chen2020 thermal model OK; offset attributable to PT100 surface vs cell-volume-averaged measurement convention plus heat-transfer coefficient calibration |
| **CC time** (23 DC-AC) | multiplicative offset | mean ΔCC = +13.1 min, sim/exp ≈ 1.07 | Chen2020 charge kinetics slower than MJ1, systematic |
| **Δt(Q80)** (23 DC-AC, v0.1) | **categorical mismatch** | sign agreement 12/23 (52.2%) | Under MJ1-aligned frequencies, SPMe + Chen2020 does not reproduce AC acceleration direction |

### Model-configuration sweep on Δt(Q80) sign agreement (v0.2)

| Configuration | V_init | Cases | Sign agreement | Notes |
|---|---|---:|---:|---|
| v0.1 SPMe | 2.51 V | 23 | 12/23 (52.2%) | v0.1 baseline (audited from `results_day8_x5_4way_dt_Q80_v2.csv`) |
| X2 DFN | 2.51 V | 23 | 11/23 (47.8%) | DFN replication of v0.1 protocol; rules out the "SPMe-misses-AC-physics" hypothesis (DFN ↔ SPMe internal sign agreement on the same set is comparable, both ≈ 50%) |
| **X5-A DFN + V_init protocol fix** | **2.82 V** | **24** | **15/24 (62.5%)** | Best PyBaMM configuration in v0.2; recovers one κ=4 case (`0.2+0.8C 10τ`) that was Min-V-infeasible at 2.51 V |
| X6α composite + sigmoid (forced 2.82 V) | 2.82 V | 15 | 1/15 (6.7%) | Composite-anode (Si secondary phase) + current-sigmoid OCP hysteresis; categorically worse |
| X6β-v2 composite + sigmoid (natural rest) | natural | 15 | 3/15 (20.0%) | Failure mode is in cell-physics representation, not in V_init protocol |

**Excluded from v0.1 SPMe / X2 DFN denominators**: 1 DC-AC case (`0.2+0.8C 10τ`, κ=4) hits Min V event in Chen2020 simulation under V_init = 2.51 V. This case becomes feasible under V_init = 2.82 V (X5-A), which is why X5-A's denominator is 24 rather than 23.

### Key v0.2 disambiguation: trajectory analysis on the κ=1.5 cluster

The v0.1 release left two competing hypotheses for the Δt(Q80) sign-mismatch:

1. **Cell-physics hypothesis**: SPMe + Chen2020 lacks an AC-acceleration mechanism present in MJ1.
2. **Frequency-mismatch hypothesis**: Chen2020 may exhibit AC acceleration at its own intrinsic frequency band, outside the MJ1-aligned grid.

v0.2 disambiguates these. The κ=1.5 cluster (0.2 C + 0.3 C amplitude × {1τ, 10τ, 34.8τ}) covers frequencies 0.0143, 0.00143, and 0.000412 Hz — a 35× ratio spanning ~1.5 decades (≈5 octaves). Under X5-A (best PyBaMM):

| Case | sim Δt(Q80) [min] | exp Δt(Q80) [min] | sign agreement |
|---|---:|---:|:---:|
| 0.2 C + 0.3 C, 1τ | −0.58 | +0.17 | ✗ |
| 0.2 C + 0.3 C, 10τ | −5.30 | +5.05 | ✗ |
| 0.2 C + 0.3 C, 34.8τ | −2.15 | +15.03 | ✗ |

Sign convention: Δt = t_ref − t_DCAC, positive ⇒ AC accelerates.

A frequency-mismatch artifact would cluster on a narrow frequency band; consistent reversal across ~5 octaves is incompatible with that interpretation. Trajectory inspection on Q_net(t) at Q80 = 4101 mAh shows the simulation carries the AC oscillation as a superimposed signal (≈200 mAh peak-to-peak in the 10τ case) on a marginally retarded mean trajectory — the oscillation peaks fail to break Q80 ahead of the 0.2 C-DC reference. The mismatch therefore reflects an absence of an AC-coupled cell-physics nonlinearity in DFN + Chen2020 standard parameters, not a frequency-grid artifact.

Candidate missing mechanisms — lithium-plating threshold modulation under modulated current, Si–graphite intercalation kinetic asymmetry, double-layer dynamics outside Butler–Volmer — are hypotheses motivated by trajectory observation and have not yet been ablation-tested.

#### Caveat on the κ=1.5, 1τ case

The exp Δt(Q80) = +0.17 min for this case is small relative to the plausible measurement-noise floor of the MJ1 first-passage time. A formal noise-floor quantification for the experimental Δt(Q*) is pending. If this case falls within noise, the κ=1.5 mismatch evidence base reduces from 3/3 to 2/2.

#### Bound on the "62.5% best" claim

62.5% is the current best across the five v0.2 configurations explored on the v0.1 case set. It is not a search-exhausted ceiling: alternative parameter sets (O'Kane2022, Marquis2019), SEI / plating / LAM submodels, particle-mechanics submodels, and extended Butler–Volmer kinetics have not been evaluated and are part of the v0.3 plan.

---

## Reproducibility

**Tested on**: macOS Apple Silicon, Python 3.12.13, PyBaMM 26.3.1.

```bash
git clone https://github.com/jiaxingLu/pybamm-dcac-superimposed.git
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
jupyter lab notebooks/11_chen2020_composite_v_init_diagnostic.ipynb  # composite + sigmoid 2×2 control matrix
jupyter lab notebooks/12_hppc_chen2020_composite.ipynb               # composite + sigmoid HPPC stage 2
```

The full results JSON files are gitignored; per-configuration summary CSVs are versioned under `data/`.

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
│   ├── 11_chen2020_composite_v_init_diagnostic.ipynb  # Day 9: composite + sigmoid 2×2 control matrix
│   ├── 12_hppc_chen2020_composite.ipynb               # Day 9: composite + sigmoid HPPC stage 2
│   └── 13_readme_v02_audit.ipynb                      # v0.2 audit notebook (12/23 vs 11/23 reconciliation)
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
│   └── results_day9_*.csv                             # Day 9 composite + sigmoid + control matrix CSVs
├── scripts/
│   └── add_cc_cv_columns.py                           # Reproducible CSV augmentation
├── ROADMAP.md
├── requirements.txt
└── README.md
```

The Δt(Q80) sign-agreement audit underlying the v0.1 correction (12/23 vs 11/23) is locked in `results_day8_x5_4way_dt_Q80_v2.csv`, which derives sign columns for X5-A, X2, v01, and exp on a common 24-case grid.

---

## Methodology snapshot

**Cell models compared**:
- v0.1: SPMe (single particle with electrolyte) + Chen2020 standard parameters.
- v0.2: DFN (full pseudo-2D Doyle–Fuller–Newman) + Chen2020; composite-anode + current-sigmoid OCP hysteresis variant for X6.

All variants run with lumped thermal submodel.

**Protocol** (5 steps in single `pybamm.Experiment`):

1. Phase 0a: 1 C discharge to 2.5 V.
2. Phase 0b: CV hold at 2.5 V until C/136.
3. Phase 1: rest 3805 s.
4. Phase 2: DC-AC charge `I(t) = I_DC + A · sin(2π · f · t)` until V = 4.2 V (via `pybamm.step.CustomStepExplicit`).
5. Phase 3: CV hold at 4.2 V until C/68.

**V_init protocol fix (v0.2, X5)**: PyBaMM's natural rest after 1 C-dis-CV equilibrates to V = 2.51 V. The MJ1 experimental protocol terminates the discharge phase at U00 = 2.82 V after a 63-min rest, an OCV difference attributable to Si–graphite hysteresis not captured in Chen2020 standard parameters. Setting V_init = 2.82 V via `set_initial_state(0.01688)` aligns the simulation start state with the experimental cross-protocol baseline. This single change improves DFN sign-agreement from 11/23 (47.8%) to 15/24 (62.5%) and recovers one κ=4 case (`0.2+0.8C 10τ`) that was Min-V-infeasible at 2.51 V.

**Composite + sigmoid investigation (v0.2, X6 + Day 9 stage 2)**: a composite-anode parameter set with current-sigmoid OCP hysteresis was hypothesized to better represent MJ1 Si–graphite chemistry. v0.2 sign-agreement on the v0.1 case set is 1/15 (6.7%) for forced V_init = 2.82 V and 3/15 (20.0%) for natural rest — categorically worse than single-phase. Stage-2 HPPC characterization on `Chen2020_composite` (notebook 12) isolated the failure mode: charge-direction post-pulse relaxation is non-monotonic under current-sigmoid OCV-branch switching, causing bi-exponential fit collapse (8/8 charge cases fail; R² ≈ 0, τ pinned at upper bound). Discharge-direction relaxation fits successfully (median τ₂ = 53.2 s, vs single-phase discharge median 45.4 s). For the τ_Chen value used in any frequency-rescaling analysis, the Day 8 single-phase 60 s-window charge value at SOC = 20% (τ_Chen = 23.83 s) is retained, preserving methodological symmetry with the MJ1 experimental τ_ref = 20.29 s (also 60 s-window). The 5000 s-window value (47.0 s) is window-asymmetric to MJ1 and is not used.

**Strict-net charge accounting** (six locked constraints):

1. Signed integration: `Q_net(t) = -∫I dt` (no rectification).
2. Non-monotonic Q(t) preserved (AC reversal causes local decreases).
3. First-passage only (no interpolated averages).
4. Unified Q-grid across cases (each battery uses own capacity).
5. No signal modification, no AC smoothing.
6. Δt(Q) is a curve, not a scalar.

**Sign convention**: PyBaMM standard, +I = discharge, −I = charge. Δt(Q) sign convention: Δt = t_ref − t_DCAC, positive ⇒ AC accelerates Q-target attainment relative to the same-DC-rate reference.

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
- [x] X2 DFN replication of v0.1 batch (notebook 08): rules out the SPMe-misses-AC-physics hypothesis
- [x] X4 DFN with Chen-rescaled frequency grid (notebook 09): rules out the simple frequency-rescaling hypothesis
- [x] X5 DFN + V_init = 2.82 V protocol fix (notebook 10): best PyBaMM configuration at 62.5%
- [x] Day 9 V_init × model 2×2 control matrix (notebook 11): isolates V_init protocol effect from cell-physics representation
- [x] Day 9 composite + sigmoid HPPC stage 2 (notebook 12): quantifies why composite + sigmoid fails on charge-direction relaxation
- [x] Day 9 trajectory-level diagnosis on the κ=1.5 cluster: rules out the frequency-mismatch hypothesis raised in v0.1
- [x] v0.1 Δt(Q80) sign-agreement audit (notebook 13): corrected to 12/23 (52.2%)

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
