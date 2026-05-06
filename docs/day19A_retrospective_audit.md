# Day 19A Retrospective Audit — Phase-aware and geometry-corrected reclassification

Date: 2026-05-06  
Status: technical audit closed  
Scope: historical PyBaMM DC–AC simulations from nb04–nb20, plus Day18B / nb22 alignment outputs

## 1. Executive summary

Day 19A reclassifies the historical PyBaMM DC–AC simulation lineage under a phase-aware and geometry-corrected framework.

The original intent was to simulate the MJ1 experimental ARB convention. After translation into PyBaMM sign convention, where positive current means discharge and negative current means charge, the experiment-faithful current is:

    I_py(t) = -|I_DC| - |I_AC| sin(ωt)

The historical nb04–nb20 implementation used:

    I_py(t) = -|I_DC| + |I_AC| sin(ωt)

This is discharge-first relative to the intended MJ1 ARB convention.

The correct framing is:

    implementation–intent phase-alignment mismatch
    reclassification, not invalidation

Historical simulations are not discarded. They are reclassified:

- DC-vs-DCAC outputs become phase-aware / geometry-corrected residual evidence.
- Same-waveform DCAC-vs-DCAC ablation outputs retain internal validity within their own phase lineage.
- Cross-notebook absolute Δt comparison is invalid unless phase convention, output lineage, Q-window, and sign convention are matched.

The central methodological finding is:

    Raw Δt(Q), before subtracting Δt_geom(Q), is phase-coupled through current geometry
    and cannot by itself be interpreted as non-geometric state-layer acceleration.

## 2. Definitions

Official sign convention:

    Δt(Q) = t_ref(Q) − t_protocol(Q)

For DC-vs-DCAC:

    Δt(Q) = t_DC(Q) − t_DCAC(Q)

Geometry decomposition:

    Δt_model(Q) = Δt_geom(Q) + Δt_resid(Q)

Day19A uses raw strict-net first-passage:

    Q_net(t) = -∫ I_py(t) dt
    t(Q*) = min{t : Q_net(t) ≥ Q*}

No rectification and no monotonic forcing are used as the primary audit convention.

## 3. Evidence register

Evidence register:

    data/day19A_step6_evidence_register.csv

Final verdict table:

    data/day19A_step6_final_verdict_summary.csv

### 3.1 Evidence blocks

| block | status | key_metrics | evidence_level |
| --- | --- | --- | --- |
| 19A.1 result/curve inventory | ok | n_files=45; families=legacy_day8_9_10_result_summary=28; dtQ_curve_like=9; ablation_or_metric_summary=7; other_result_csv=1; audit_readiness=legacy_summary_needs_json_schema=28; summary_or_auxiliary_only=9; sign_auditable_from_time_pairs=7; curve_dt_present_but_sign_needs_external_ground_truth=1 | inventory_support |
| 19A.1 CSV sign self-audit | ok | n_ok=7/7; inferred_sign=official_tRef_minus_tProtocol=7 | high_for_excluding_sign_bug |
| 19A.1 legacy JSON strict-net validation | ok | usable_records=247/279; q_match_mode=strict_net_minus_I=247 | high_raw_trajectory_ground_truth |
| 19A.1 Day18B residual magnitude null baseline | near_zero_null_baseline | max_abs_identity_err_s=2.274e-13; dt_resid_max_abs_s=0.044075; dt_resid_p95_abs_s=0.009089; resid_over_geom_median=4.01981e-05 | high_for_geometry_null_baseline |
| 19A.1 legacy time-axis anomaly audit | ok | n_anomalies=5; classes=duplicate_timestamps_only=5; recoverable=5/5 | high_for_trajectory_cleaning |
| 19A.2 MJ1 waveform-geometry anchor | ok | charge_first_raw_mean=337.503105s; discharge_first_raw_mean=-188.997636s; raw_cummax_max_diff=0.000000s | high_helper_anchor |
| 19A.2 geometry helper validation against Day18B/v4 | ok | n_rows=1272; n_groups=21; global_max_abs_err_s=0.098797; global_median_abs_err_s=0.000278 | high_for_helper_equivalence |
| 19A.2 trajectory helper de-dup self-test | ok | n_records=5; removed_samples=5; max_q_mismatch_mAh=3.76367e-05 | high_helper_selftest |
| 19A.3 Day8/Day9 residual topology | ok | n_pairs=198; stable_verdicts=stable_weak=102; stable_null=53; stable_intermediate_or_spiky=24; stable_distributed_nonzero=19; taxonomy=isolated_spike=59; null_residual=50; weak_distributed_residual=32; edge_or_boundary_artifact=22; distributed_residual_requires_inspection=19; mixed_or_intermediate=16 | high_raw_trajectory_retro_audit |
| 19A.3 Day8/Day9 lineage verdict | ok | n_lineages=7; lineage_verdicts=mixed_with_distributed_candidates=3; geometry_dominated_or_weak_residual=2; distributed_candidates_in_exploratory_branch=2; evidence_levels=requires_pair_level_review=3; high_for_geometry_dominated_reclassification=2; not_clean_mechanism_evidence=2 | high_for_legacy_reclassification |
| 19A.4 Day16/nb20 Q-window gate | ok | n_groups=36; refined_status=compatible=25; compatible_with_capacity_scale_warning=11; capacity_warnings=11 | supporting_window_gate |
| 19A.4 Day16/nb20 stored-first-passage residual audit | ok | n_groups=36; stable_verdicts=stable_weak=13; stable_null=11; stable_intermediate_or_spiky=9; stable_distributed_nonzero=3; taxonomy=null_residual=11; isolated_spike=8; mixed_or_intermediate=6; weak_distributed_residual=6; edge_or_boundary_artifact=3; distributed_residual_requires_inspection=2 | supporting_stored_first_passage_audit |
| 19A.5 DCAC-vs-DCAC ablation phase audit | ok | n_notebooks=5; evidence_status=same_phase_ablation_valid_internal_only=4; mixed_lineage_phase_pair_evidence=1 | high_for_ablation_evidence_reclassification |
| 19A.5 nb18 paired phase evidence | ok | n_files=3; v2_alias_byte_identical=True; phases=discharge_first=2; charge_first=1 | high_for_phase_sensitivity_evidence |

## 4. Main technical findings

### 4.1 Stored Δt sign is not the explanation

Seven time-pair-auditable CSV files were checked. All seven store Δt with the official sign convention:

    Δt = t_ref − t_protocol

Therefore, the Day18B discrepancy is not explained by an on-disk Δt sign inversion.

### 4.2 Legacy Day8/Day9 JSON provides raw-trajectory ground truth

Legacy Day8/Day9 JSON payloads preserve `t_chg`, `I_chg`, and `Q_net_trajectory`.

For all usable records, stored `Q_net_trajectory` matches strict-net integration from `I_chg` under:

    Q_net(t) = -∫ I(t) dt

### 4.3 Day18B prescribed-current CC residual is near zero

Day18B smoke curves establish a near-zero non-geometric residual baseline:

    max |Δt_resid|      = 0.044075 s
    p95 |Δt_resid|      = 0.009089 s
    median |Δt_resid|   = 0.001425 s
    median |Δt_resid| / |Δt_geom| ≈ 4e−5

This confirms that the Day18B prescribed-current CC raw Δt signal is carried by current geometry rather than non-geometric cell response.

### 4.4 Geometry helper validation

The MJ1 0.3C+0.7C 10τ charge-first geometry anchor was reproduced:

    charge-first raw mean Δt_geom = +337.503 s
    frozen reference              = +335.51 s
    error                         = +1.993 s

The geometry helper was validated against stored Day18B and Day18 v4 geometry columns using actual rebased frequency metadata:

    rows validated              = 1272
    groups validated            = 21
    global max abs error        = 0.098797 s
    global median abs error     = 0.000278 s
    global mean abs error       = 0.001171 s

The earlier 4D v1 failure was caused by using fixed MJ1 `τ_label = 11.1 s` rather than actual rebased `f_anchor_Hz` / `tau95_eq_s` metadata.

### 4.5 Day8/Day9 residual audit

Day8/Day9 residual decomposition covered 198 admissible DC-vs-DCAC pairs.

    pairs decomposed = 198
    errors           = 0
    phase            = 198 / 198 discharge_first

Topology result:

    stable null or weak          = 155 / 198
    stable distributed nonzero   = 19 / 198
    stable intermediate/spiky    = 24 / 198
    isolated spike taxonomy      = 59 cases
    edge/boundary artifact       = 22 cases

The max-based `inspect_residual` class overstates residual structure. Many cases are isolated spikes or boundary artifacts rather than stable non-geometric residuals.

### 4.6 Day16 / nb20 audit

The Day16 / nb20 Q-window gate passed for all 36 groups.

    compatible                              = 25
    compatible with capacity-scale warning  = 11
    excluded                                = 0

The Day16 stored-first-passage residual audit decomposed all 36 groups:

    stable weak                     = 13
    stable null                     = 11
    stable intermediate/spiky       = 9
    stable distributed nonzero      = 3

Day16 supports the same reclassification pattern at lower evidential level because raw current trajectories are unavailable.

### 4.7 DCAC-vs-DCAC ablation phase audit

Ablation notebooks were reclassified as follows:

| Notebook | Closure lineage | Evidence status |
|---|---|---|
| nb14 / Day11 plating | discharge-first | same-phase internal evidence |
| nb15 / Day12 OCP | discharge-first | same-phase internal evidence |
| nb16 / Day13 transport / kinetics | discharge-first | same-phase internal evidence |
| nb18 / Day14 AsymBV | mixed v1/v2 | phase-pair evidence |
| nb19 / Day14 X6 | discharge-first | same-phase internal evidence |

nb18 is the strongest phase-pair evidence:

    v1 = historically labelled wrong_phase
       = reclassified as charge-first / experiment-faithful branch

    v2 = discharge-first / nb16-aligned production branch

    v2 production and v2_aligned_phase are byte-identical aliases.

## 5. Final verdict table

| verdict_id | claim | status | action_for_docs |
| --- | --- | --- | --- |
| V1 | Historical nb04–nb20 DCAC implementation was discharge-first relative to the MJ1 charge-first ARB intent. | supported | Primary Day19A finding. |
| V2 | CSV stored Δt sign inversion is not the explanation for Day18B discrepancy. | supported | Secondary finding; downstream of phase mismatch. |
| V3 | Raw Δt(Q) before geometry correction is phase-coupled and not a non-geometric state-layer observable by itself. | supported | JES2 §4 candidate methodological claim. |
| V4 | Day18B prescribed-current CC simulations establish a near-zero non-geometric residual baseline. | supported | Use as null-baseline evidence. |
| V5 | Day8/Day9 legacy DC-vs-DCAC branch is mostly geometry-dominated or weak after topology audit. | supported_with_exceptions | Use for reclassification, not mechanism proof. |
| V6 | Day16/nb20 supports the same reclassification pattern at lower evidential level. | supporting | Use as supporting audit, not primary proof. |
| V7 | DCAC-vs-DCAC ablation outputs retain internal validity only within same-phase lineages. | supported | Use for evidence-level classification. |
| V8 | Day19A reclassifies historical simulations rather than discarding them. | supported | Commit message / README / ROADMAP wording. |

## 6. Wording rule

Use:

    implementation–intent phase-alignment mismatch
    reclassification, not invalidation
    phase-aware and geometry-corrected residual framework

Avoid:

    not an error
    alternative designed branch
    PyBaMM proved there is no state-layer acceleration

Correct technical boundary:

    Within prescribed-current CC simulations audited so far, raw Δt(Q) is largely
    explained by current geometry, and non-geometric Δt_resid(Q) remains near zero
    or weak in clean lineages. This does not invalidate full-protocol MJ1 measured
    first-passage gain, which still requires segmented voltage-boundary and
    CV-coupled audit.

## 7. Next steps

Day19A is closed technically. The next step is a segmented full-protocol audit:

    AC-on prescribed-current CC geometry
    voltage-boundary event timing
    AC-off transition
    CV feedback trajectory
    possible non-geometric residual

This belongs to Day20+ and should be committed separately from Day19A.
