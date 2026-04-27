"""
HPPC descriptor extractor — PyBaMM-friendly version.

Adapted from the original DAS60-based HPPC_descriptor.py for use with
PyBaMM simulation outputs. Core fitting algorithms (CDEFG identification,
bi-exponential FG-relaxation fit, recovery-time descriptors) are unchanged.

Key changes vs original:
  - Input: pandas DataFrame with columns [Time, U_KL[V], I_KL[A]] in DAS60 format
           (Time in milliseconds, I positive=charge, negative=discharge)
  - Cell-aware config: MJ1 / Chen2020 / custom timescale via dict
  - No file I/O; pure function on DataFrame
  - Single API: extract_hppc_descriptors(df, cell_config) -> dict

Usage:
    from scripts.hppc_descriptor_pybamm import extract_hppc_descriptors, CELL_CONFIGS

    row = extract_hppc_descriptors(df_hppc, CELL_CONFIGS["Chen2020"])
"""

import numpy as np
from scipy.optimize import curve_fit
from dataclasses import dataclass
from typing import Dict, Optional


# ============================================================
# Cell-specific configurations
# ============================================================
CELL_CONFIGS = {
    "MJ1": {
        "descriptor_windows_s": [20.0, 60.0],
        "primary_tau2_window_s": 60.0,
        "tau_fg_eff_window_s": 60.0,
        "tail_fit_start_s": 20.0,
        "tail_fit_end_s": 60.0,
        "uinf_window_start_s": 10.0,
        "uinf_window_end_s": 15.0,
        "name": "MJ1",
    },
    "Chen2020": {
        "descriptor_windows_s": [60.0, 1000.0],   # 60s for cross-cell ref + 1000s primary (~10 tau_macro_neg)
        "primary_tau2_window_s": 1000.0,           # corrected: tau_macro = R^2/(pi^2 D) = 105s for neg, so 10*tau ~ 1050s
        "tau_fg_eff_window_s": 1000.0,
        "tail_fit_start_s": 300.0,                 # ~3 tau_macro_neg for tail-only fit
        "tail_fit_end_s": 1000.0,
        "uinf_window_start_s": 800.0,              # near end of 1000s window
        "uinf_window_end_s": 1000.0,
        "name": "Chen2020",
    },
}


# ============================================================
# Common fitting primitives (algorithm unchanged from original)
# ============================================================
def two_exp(t, Uinf, a1, tau1, a2, tau2):
    return Uinf + a1 * np.exp(-t / tau1) + a2 * np.exp(-t / tau2)


def one_exp(t, Uinf, a, tau):
    return Uinf + a * np.exp(-t / tau)


def fit_fg_relaxation(t_s_rel, U):
    """Bi-exponential fit with sorted tau1 < tau2."""
    U0 = float(U[0])
    Utail = float(np.median(U[max(0, len(U) - max(10, len(U)//10)):]))
    Uinf0 = Utail
    d0 = U0 - Uinf0
    a1_0 = 0.6 * d0
    a2_0 = 0.4 * d0
    T = max(1e-6, float(t_s_rel[-1] - t_s_rel[0]))
    tau1_0 = max(0.05, 0.2 * T)
    tau2_0 = max(1.0, 0.8 * T)

    p0 = [Uinf0, a1_0, tau1_0, a2_0, tau2_0]
    lb = [-np.inf, -np.inf, 1e-4, -np.inf, 1e-3]
    ub = [np.inf, np.inf, 1e5, np.inf, 1e6]   # extended ub for Chen2020

    popt, _ = curve_fit(two_exp, t_s_rel, U, p0=p0, bounds=(lb, ub), maxfev=20000)
    Uhat = two_exp(t_s_rel, *popt)
    resid = U - Uhat
    rmse = float(np.sqrt(np.mean(resid**2)))
    ss_res = float(np.sum(resid**2))
    ss_tot = float(np.sum((U - np.mean(U))**2) + 1e-12)
    r2 = float(1.0 - ss_res / ss_tot)

    Uinf, a1, tau1, a2, tau2 = popt
    if tau1 > tau2:
        popt = [Uinf, a2, tau2, a1, tau1]
    return popt, rmse, r2


def fit_tail_single_exp(t_s_rel, U):
    U0 = float(U[0])
    Utail = float(np.median(U[max(0, len(U) - max(10, len(U)//5)):]))
    d0 = U0 - Utail
    T = max(1e-6, float(t_s_rel[-1] - t_s_rel[0]))
    tau0 = max(0.5, 0.5 * T)

    p0 = [Utail, d0, tau0]
    lb = [-np.inf, -np.inf, 1e-4]
    ub = [np.inf, np.inf, 1e6]

    popt, _ = curve_fit(one_exp, t_s_rel, U, p0=p0, bounds=(lb, ub), maxfev=20000)
    Uhat = one_exp(t_s_rel, *popt)
    resid = U - Uhat
    rmse = float(np.sqrt(np.mean(resid**2)))
    ss_res = float(np.sum(resid**2))
    ss_tot = float(np.sum((U - np.mean(U))**2) + 1e-12)
    r2 = float(1.0 - ss_res / ss_tot)
    return popt, rmse, r2


@dataclass
class DescriptorFit:
    window_s: float
    tau1: float = float("nan")
    tau2: float = float("nan")
    rmse: float = float("nan")
    r2: float = float("nan")
    uinf: float = float("nan")
    success: bool = False


def fit_descriptor_window(t_ms, U, F_ms, window_s):
    fit = DescriptorFit(window_s=window_s)
    fit_mask = (t_ms >= F_ms) & (t_ms <= F_ms + window_s * 1000.0)
    if np.sum(fit_mask) < 20:
        return fit
    t_fit_ms = t_ms[fit_mask]
    U_fit = U[fit_mask]
    t_fit_s_rel = (t_fit_ms - F_ms) / 1000.0
    try:
        popt, rmse, r2 = fit_fg_relaxation(t_fit_s_rel, U_fit)
        Uinf, _, tau1, _, tau2 = popt
        fit.tau1 = float(tau1)
        fit.tau2 = float(tau2)
        fit.rmse = float(rmse)
        fit.r2 = float(r2)
        fit.uinf = float(Uinf)
        fit.success = True
        return fit
    except Exception:
        return fit


# ============================================================
# CDEFG point detection (unchanged from original)
# ============================================================
def median_in_window(t_ms, y, center_ms, half_window_ms):
    lo = center_ms - half_window_ms
    hi = center_ms + half_window_ms
    m = (t_ms >= lo) & (t_ms <= hi)
    if not np.any(m):
        k = int(np.argmin(np.abs(t_ms - center_ms)))
        return float(y[k])
    return float(np.median(y[m]))


def detect_pulse_by_phi(t_ms, I, rest_abs_I_thr=0.2, phi_on=0.9, phi_off=0.1, pulse_abs_thr_A=1.0):
    rest_mask = np.abs(I) < rest_abs_I_thr
    I0 = float(np.median(I[rest_mask])) if np.any(rest_mask) else float(np.median(I))

    dI_abs = np.abs(I - I0)
    pulse_mask = dI_abs > pulse_abs_thr_A
    if not np.any(pulse_mask):
        raise ValueError(f"No pulse plateau detected: |I-I0| > {pulse_abs_thr_A} A not found.")

    Ip = float(np.median(I[pulse_mask]))
    denom = abs(Ip - I0) if abs(Ip - I0) > 1e-12 else 1e-12
    phi = dI_abs / denom

    ton_candidates = np.where(phi >= phi_on)[0]
    if len(ton_candidates) == 0:
        raise ValueError("Cannot find ton.")
    ton_idx = int(ton_candidates[0])

    toff_candidates = np.where((np.arange(len(I)) > ton_idx) & (phi <= phi_off))[0]
    if len(toff_candidates) == 0:
        raise ValueError("Cannot find toff.")
    toff_idx = int(toff_candidates[0])
    return I0, Ip, ton_idx, toff_idx


def is_discharge_pulse(I0, Ip):
    """DAS60 convention: I < 0 = discharge into battery."""
    return Ip < I0


def pick_E_by_paperdef(t_ms, U, ton_ms, toff_ms, discharge):
    start_ms = ton_ms + 100.0
    end_ms = toff_ms - 50.0
    if end_ms <= start_ms:
        start_ms = ton_ms
        end_ms = toff_ms
    m = (t_ms >= start_ms) & (t_ms <= end_ms)
    if not np.any(m):
        return min(ton_ms + 9800.0, toff_ms - 50.0)
    idx_local = np.argmin(U[m]) if discharge else np.argmax(U[m])
    idx = np.where(m)[0][0] + idx_local
    return float(t_ms[idx])


def pick_Uinf(t_ms, U, toff_ms, cell_config):
    """Adapted: window is cell-specific."""
    w_start = toff_ms + cell_config["uinf_window_start_s"] * 1000.0
    w_end = toff_ms + cell_config["uinf_window_end_s"] * 1000.0
    m = (t_ms >= w_start) & (t_ms <= w_end)
    if np.any(m):
        return float(np.median(U[m]))
    n = len(U)
    tail_n = max(50, n // 10)
    return float(np.median(U[-tail_n:]))


def pick_G_by_99pct(t_ms, U, toff_ms, Uf, Uinf):
    denom = (Uinf - Uf)
    if abs(denom) < 1e-9:
        return float(toff_ms), float(Uf)
    m = t_ms >= toff_ms
    t2 = t_ms[m]
    U2 = U[m]
    r = (U2 - Uf) / denom
    idxs = np.where(r >= 0.99)[0]
    if len(idxs) == 0:
        return float(t2[-1]), float(U2[-1])
    k = int(idxs[0])
    return float(t2[k]), float(U2[k])


def compute_recovery_time(t_ms, U, F_ms, Uf, Uinf, level):
    denom = Uinf - Uf
    if abs(denom) < 1e-12:
        return float("nan")
    target = Uf + level * denom
    m = t_ms >= F_ms
    t2 = t_ms[m]
    U2 = U[m]
    if denom > 0:
        idx = np.where(U2 >= target)[0]
    else:
        idx = np.where(U2 <= target)[0]
    if len(idx) == 0:
        return float("nan")
    return float((t2[int(idx[0])] - F_ms) / 1000.0)


def compute_recovery_time_windowed(t_ms, U, F_ms, Uf, Uinf, level, max_window_s):
    denom = Uinf - Uf
    if abs(denom) < 1e-12:
        return float("nan")
    target = Uf + level * denom
    m = (t_ms >= F_ms) & (t_ms <= F_ms + max_window_s * 1000.0)
    t2 = t_ms[m]
    U2 = U[m]
    if len(t2) == 0:
        return float("nan")
    if denom > 0:
        idx = np.where(U2 >= target)[0]
    else:
        idx = np.where(U2 <= target)[0]
    if len(idx) == 0:
        return float("nan")
    return float((t2[int(idx[0])] - F_ms) / 1000.0)


# ============================================================
# Main API
# ============================================================
def extract_hppc_descriptors(df, cell_config, soc=None, pulse_direction=None,
                              pick_window_ms=20.0):
    """
    Extract HPPC descriptors from a single-pulse HPPC trace.

    Parameters
    ----------
    df : pandas.DataFrame
        Columns required: 'Time' (ms), 'U_KL[V]' (volts), 'I_KL[A]' (amps, DAS60 convention).
        Should contain a single pulse: rest -> pulse -> rest.
    cell_config : dict
        From CELL_CONFIGS or custom dict with 'descriptor_windows_s', etc.
    soc : float or None
        SOC label (for output bookkeeping)
    pulse_direction : str or None
        'discharge' or 'charge' (auto-detected if None)
    pick_window_ms : float
        Half-window for median voltage at CDEFG points.

    Returns
    -------
    dict
        Descriptor row with keys: SOC, mode, tau_FG_20s, tau2_biexp, tau_FG_eff_window,
        eff_window_s, t95, t99, tau_tail, R0, fit_R2_*, etc.
    """
    t_ms = df["Time"].to_numpy()
    U = df["U_KL[V]"].to_numpy()
    I = df["I_KL[A]"].to_numpy()
    half_w = pick_window_ms / 2.0

    # Detect pulse
    I0, Ip, ton_idx, toff_idx = detect_pulse_by_phi(t_ms, I)
    ton_ms = float(t_ms[ton_idx])
    toff_ms = float(t_ms[toff_idx])
    discharge = is_discharge_pulse(I0, Ip)

    if pulse_direction is None:
        pulse_direction = "discharge" if discharge else "charge"

    # CDEFG points
    delay_ms = 50.0 if discharge else 20.0
    C = ton_ms - 600.0
    D = ton_ms + delay_ms
    F = toff_ms + delay_ms
    E = pick_E_by_paperdef(t_ms, U, ton_ms, toff_ms, discharge)

    Uc = median_in_window(t_ms, U, C, half_w)
    Ud = median_in_window(t_ms, U, D, half_w)
    Ue = median_in_window(t_ms, U, E, half_w)
    Uf = median_in_window(t_ms, U, F, half_w)

    # R0
    dI = (Ip - I0) if abs(Ip - I0) > 1e-12 else 1e-12
    R0_cd = abs((Ud - Uc) / dI)
    R0_ef = abs((Ue - Uf) / dI)
    R0_avg = 0.5 * (R0_cd + R0_ef)

    Uinf = pick_Uinf(t_ms, U, toff_ms, cell_config)
    G, Ug = pick_G_by_99pct(t_ms, U, toff_ms, Uf, Uinf)

    # Multi-window descriptor fits
    fit_map = {}
    for ws in sorted(set(cell_config["descriptor_windows_s"] + [cell_config["primary_tau2_window_s"]])):
        fit_map[ws] = fit_descriptor_window(t_ms, U, F, ws)

    # Recovery-time descriptors
    t95 = compute_recovery_time(t_ms, U, F, Uf, Uinf, 0.95)
    t99 = compute_recovery_time(t_ms, U, F, Uf, Uinf, 0.99)
    tau_fg_eff = compute_recovery_time_windowed(
        t_ms, U, F, Uf, Uinf, 0.632, cell_config["tau_fg_eff_window_s"]
    )

    # Tail single-exp
    tail_mask = (t_ms >= F + cell_config["tail_fit_start_s"] * 1000.0) & \
                (t_ms <= F + cell_config["tail_fit_end_s"] * 1000.0)
    tail_tau = float("nan")
    tail_r2 = float("nan")
    if np.sum(tail_mask) >= 10:
        try:
            t_tail = (t_ms[tail_mask] - (F + cell_config["tail_fit_start_s"] * 1000.0)) / 1000.0
            U_tail = U[tail_mask]
            popt_t, rmse_t, r2_t = fit_tail_single_exp(t_tail, U_tail)
            tail_tau = float(popt_t[2])
            tail_r2 = float(r2_t)
        except Exception:
            pass

    primary_ws = cell_config["primary_tau2_window_s"]
    secondary_ws = 60.0 if 60.0 in fit_map else None

    row = {
        "cell": cell_config["name"],
        "SOC": soc,
        "mode": pulse_direction,
        "tau1_primary": fit_map[primary_ws].tau1 if primary_ws in fit_map else float("nan"),
        "tau2_biexp": fit_map[primary_ws].tau2 if primary_ws in fit_map else float("nan"),
        "primary_window_s": primary_ws,
        "tau1_secondary_60s": fit_map[secondary_ws].tau1 if secondary_ws else float("nan"),
        "tau2_secondary_60s": fit_map[secondary_ws].tau2 if secondary_ws else float("nan"),
        "tau_FG_eff": tau_fg_eff,
        "eff_window_s": cell_config["tau_fg_eff_window_s"],
        "t95": t95,
        "t99": t99,
        "tau_tail": tail_tau,
        "R0": R0_avg,
        "R0_CD": R0_cd,
        "R0_EF": R0_ef,
        "fit_R2_primary": fit_map[primary_ws].r2 if primary_ws in fit_map else float("nan"),
        "fit_R2_60s": fit_map[secondary_ws].r2 if secondary_ws else float("nan"),
        "fit_RMSE_primary": fit_map[primary_ws].rmse if primary_ws in fit_map else float("nan"),
        "tail_R2": tail_r2,
        "Uinf": Uinf,
        "Uc": Uc, "Ud": Ud, "Ue": Ue, "Uf": Uf, "Ug": Ug,
        "I0": I0, "Ip": Ip,
        "ton_ms": ton_ms, "toff_ms": toff_ms,
        "C_ms": C, "D_ms": D, "E_ms": E, "F_ms": F, "G_ms": G,
    }
    return row
