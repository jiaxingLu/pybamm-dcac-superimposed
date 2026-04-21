# Project Roadmap

## v0.1 (current): Core simulation pipeline

- [x] PyBaMM environment (Python 3.12, PyBaMM 26.3.1)
- [x] Chen2020 baseline (1C discharge hello world)
- [ ] DC-AC current waveform injection via `pybamm.Interpolant`
- [ ] Frequency sweep (0.1 Hz — 1 kHz)
- [ ] Amplitude sweep (0 — 150% of DC current)
- [ ] Validation against JES experimental data

## v0.2 (future): Parameter refinement

- [ ] Parameter sensitivity analysis on Chen2020
- [ ] Selective fitting for LG INR18650 MJ1 (D_s_p, D_s_n, h_cooling)
- [ ] Scaled geometric parameters for 18650 form factor
- [ ] Cross-validation of fitted parameters

## v0.3 (aspirational): Full parameterization

- [ ] OCV curve extraction from experimental slow-discharge data
- [ ] HPPC-based kinetic parameter identification
- [ ] Publishable parameter set derivation

---

## Design principles

- **MVP first**: deliver a functional v0.1 before extending scope.
- **Documented approximations**: every simplification (e.g., Chen2020 as MJ1 proxy) is explicitly flagged in code or docs.
- **Reproducibility**: every result (figure, metric) traceable to a notebook cell + parameter set version.
