# Day 8 Stage 1+2 Portfolio Summary

**Date**: 2026-04-27  
**Goal**: Extract τ_Chen(SOC) and R0(SOC) from PyBaMM Chen2020 DFN HPPC simulations, methodologically aligned with MJ1 experimental protocol (your JES1 paper).

## Methodology

- **Model**: `pybamm.lithium_ion.DFN(options={"thermal": "lumped"})`
- **Parameters**: Chen2020 (LG M50, 5.0 Ah)
- **Solver**: IDAKLUSolver (rtol=1e-6, atol=1e-8)
- **Protocol**: Single-pulse HPPC, 5000s rest (≈48× τ_macro_neg = 105s, full negative-electrode relaxation)
- **SOC grid**: [10, 20, 30, ..., 100]% × [discharge, charge] = 20 cases
- **Fitting**: Cell-aware bi-exp on FG-relaxation, 60s window (apples-to-apples vs MJ1) and 1000s window (full slow-branch)
- **Total batch wall-clock**: 23 seconds for 20 cases (0/20 failures)

## Quantitative findings

### Finding 1: τ ratio (cross-cell, apples-to-apples)
- Chen2020 DFN τ2_60s mean: **26.17 s** (discharge), **24.85 s** (charge)
- MJ1 experiment τ2 mean: **17.7 s** (discharge), **22.3 s** (charge)
- **Chen/MJ1 ratio**: ~1.5× (much milder than initially hypothesized; v0.1 frequency-mismatch hypothesis is weakened)

### Finding 2: U-shape R0(SOC) — form/magnitude diagnosis
- **Form**: Chen2020 DFN reproduces the U-shape qualitatively (high SOC + low SOC > middle SOC), root in P2D physics
- **Sharpness at ms time scale (CD-jump)**: Chen sim 1.19× vs MJ1 exp 1.16× → **near-perfect agreement**
- **Sharpness at 10s window (cumulative polarization)**: Chen sim 1.19× vs MJ1 exp **1.63×** → MJ1 has additional low-SOC nonlinear polarization not captured by standard Chen2020 DFN
- **Magnitude offset**: Chen sim ~24 mΩ vs MJ1 ~40 mΩ; nearly constant offset across SOC suggests series contact resistance hypothesis (deferred to v0.3)

### Finding 3: bi-exp model insufficiency at SOC=100% on long windows
- SOC=100% discharge fit on 1000s window: **R²=0.9938**, residual structure shows clear non-random pattern (peak at 70s, secondary peak at 1000s)
- bi-exp converges pathologically: τ1 = τ2 = 28.16s with amplitudes 12× larger than ΔV (degenerate fit)
- **Methodological implication**: HPPC bi-exp at NMC high-SOC plateau requires ≥3 time constants OR window restriction to ≤60s
- 60s window remains robust at all SOC (max|residual| = 0.01 mV at SOC=100%)

### Finding 4: Time-scale and SOC-region dependence of sim/exp gap
- **Best agreement**: short windows (CD-jump ms-level) at mid SOC (40-60%)
- **Worst agreement**: long windows (Δt=10s) at low SOC (10-20%)
- Implication: v0.2 disambiguation must specify time-scale + SOC region; uniform "sim ≈ exp" or "sim ≠ exp" is too coarse

## Portfolio number selection
- **Primary τ_Chen column**: `tau2_secondary_60s` (60s window, robust at all SOC)
- **NOT used for primary claim**: `tau2_biexp` (1000s window, fails at SOC≥90% NMC plateau)

## Outputs
- CSV: `data/results_day8_stage2_hppc_chen2020.csv` (20 rows × ~50 columns)
- Figures:
  - `figures/07_hppc_chen2020_stage2_overview.png` (4-panel: τ_60s, τ_1000s, R0, τ_tail)
  - `figures/07_hppc_chen2020_R0_split.png` (R0_CD/EF + cross-cell)
  - `figures/07_hppc_chen2020_SOC100_dis_diagnostic.png` (bi-exp failure diagnostic)
- Module: `scripts/hppc_descriptor_pybamm.py` (cell-aware HPPC fitter, 389 lines)

## Open items (deferred to v0.3 / future PhD)
1. Series contact resistance hypothesis (R0 magnitude offset)
2. Low-SOC nonlinear polarization mechanism missing in standard Chen2020 (SEI? local electrolyte depletion?)
3. ≥3-time-constant relaxation model for NMC high-SOC plateau

## What this does NOT yet show
- v0.1 sign-agreement disagreement (48%) cause is **still partially unresolved**: τ ratio ~1.5× is too small to explain frequency-mismatch alone
- Cell-physics hypothesis (SPMe vs DFN AC-acceleration capability) NOT YET TESTED
- Stage 3 (DFN vs SPMe HPPC comparison) needed to discriminate hypotheses
