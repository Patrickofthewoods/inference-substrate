# Inference Substrate

A minimal, parity-driven simulation framework for collapse behavior in rare-event chains.

## Overview
The Inference Substrate is a compact simulation engine built to explore how parity-based collapse laws emerge from simple, independent rare-event transitions. It provides a clean, reproducible implementation of the core model described in the accompanying manuscript.

This repository contains:

- A full chain simulation (step-by-step transitions, parity collapse detection)
- A minimal parity demonstration (Appendix A version)
- A physics-grounded escape-rate benchmark (Kramers vs. Langevin)
- A permanent noncommercial license protecting commercial use
- A simple, readable codebase intended for research, teaching, and exploration

The project is released once, in full, and is not intended for ongoing maintenance.

## Features
- Full inference substrate simulation
- Independent rare-event transitions
- Chain-length scaling
- Parity-based collapse detection
- Empirical vs analytic comparison
- Minimal parity demonstration
- Straight-line analytic identity
- Bernoulli-only model
- Reproducible verification plot
- Kramers/TST escape-rate benchmark against direct Langevin simulation
- Simple, transparent code
- No dependencies beyond Python + NumPy + matplotlib
- Easy to modify for research or teaching
- Clear separation between analytic and empirical logic

## Repository Structure

```
/
├── LICENSE.txt                       # PolyForm Noncommercial License
├── README.md                         # Project documentation
├── CITATION.cff                      # Academic citation metadata
├── inference_substrate_parity.py     # Full chain simulation
├── parity_plot_overlay.py            # Minimal Appendix A parity demo
├── kramers_vs_langevin_benchmark.py  # Escape-rate validation benchmark
└── (generated plots saved locally)
```

## Usage

### Full Inference Substrate Simulation

Run the full chain simulation:

```
python inference_substrate_parity.py
```

This produces:

```
inference_substrate_parity.png
```

showing empirical parity collapse behavior over chain lengths 1–40, compared against the analytic prediction:

```
log(1 − 2 p_n) = n ⋅ log(1 − 2 k)
```

### Minimal Parity Demonstration (Appendix A)

Run the minimal parity model:

```
python parity_plot_overlay.py
```

This produces:

```
parity_plot_overlay.png
```

which overlays empirical Bernoulli parity results on the analytic straight line.

### Kramers vs. Langevin Benchmark (Escape-Rate Validation)

This benchmark tests how the parity/Poisson formalism behaves when the escape rate `k` is derived from real physical parameters (via Kramers' rate) rather than assumed, providing a physics-grounded validation of the rare-event substrate.

It compares the Kramers/Transition-State-Theory (TST) escape-rate prediction to two empirical definitions of escape in a symmetric double-well Langevin system.

Kramers/TST provides a continuous-time escape rate `k`, which corresponds to a Poisson process with escape probability:

```
P_escape(T) = 1 - exp(-k * T)
```

In direct Langevin simulation, however, "escape" can be defined in two different ways:

- **Barrier-crossing (x < 0)** — The particle merely crosses the barrier top. This overcounts true transitions due to rapid recrossing.
- **Far-well commitment (x < -sqrt(a/2))** — The particle reaches the minimum of the opposite well. This undercounts true transitions because some barrier crossings fall back.

Kramers/TST is an upper bound on the committed transition rate, so its prediction should fall between these two empirical measures. This is a known phenomenon in reaction-rate theory (transmission coefficient correction).

Run it with:

```
python kramers_vs_langevin_benchmark.py
```

A full benchmark run (20,000 trajectories, ~1–2 minutes) produces:

```
Kramers escape rate k:                0.128972
Poisson (Kramers/TST) prediction:     0.227362
Empirical (far-well committed):       0.112050
Empirical (barrier merely crossed):   0.370850
```

As expected:

- Barrier-crossing overestimates
- Far-well commitment underestimates
- Kramers/TST prediction lies between them

This bracketing pattern is stable across repeated runs and reflects the known recrossing/commitment dynamics of metastable escape.

## License
This project is released under the PolyForm Noncommercial License 1.0.0.

You may use, modify, and share the code for noncommercial purposes only, including:

- research
- experimentation
- teaching
- personal study
- academic work
- hobby projects

Commercial use is not permitted without a separate commercial license.

To obtain commercial rights, contact:

Patrick D. Nyhan
Licensor and copyright holder

## Citation

If you use this work in academic research, please cite:

Nyhan, Patrick D. *Inference Substrate: A Minimal Parity-Driven Collapse Model.*

A formal CITATION.cff file is included in this repository.

## Status
This is a one-time release.
The project is not intended for ongoing updates or maintenance.

## Contact
For commercial licensing inquiries:

Patrick D. Nyhan
(pdn.nyhan@gmail.com)
