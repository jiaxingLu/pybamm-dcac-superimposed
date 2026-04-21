# pybamm-dcac-superimposed

Open-source simulation framework for DC-AC superimposed charging protocols using PyBaMM.

## Status

🚧 Under active development. v0.1 target: April 2026.

## Motivation

This project implements and extends the experimental findings reported in [JES manuscript, under review] on DC-AC superimposed charging of lithium-ion cells. It provides a physics-based simulation pipeline (PyBaMM SPMe with lumped thermal coupling) for:

- Generating arbitrary DC+AC current protocols
- Extracting temperature rise, polarization, and voltage ripple metrics
- Parameter sweeps over AC amplitude and frequency
- Cross-validation against experimental data

## Installation

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Quick start

_Coming soon._

## License

MIT (tentative).

## Author

Jiaxing Lu — M.Sc. Elektro- und Informationstechnik, Hochschule Mittweida.
