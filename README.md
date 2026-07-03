# Inference Substrate

A minimal, parity-driven simulation toolkit for rare-event transitions — verified against real physics, not just simulated in isolation.

## What this repo actually does

Two things, both verified and reproducible:

1. **A parity-based collapse model.** For a chain of independent rare-event transitions, whether the system ends in a different state than it started depends only on the parity (odd/even count) of successful transitions. This repo simulates that directly and checks it against the closed-form analytic prediction — they match.

2. **A physics-grounded benchmark (Kramers vs. Langevin).** The parity model requires a transition probability `k`. Instead of assuming one, this benchmark derives `k` from an actual physical system — a symmetric double-well potential — using Kramers' escape-rate theory, then checks the resulting prediction against a full numerical simulation of the underlying Langevin dynamics. The results agree, within the known and explained bounds of transition-state theory.

If you just want to see it work, run:

```bash
python kramers_vs_langevin_benchmark.py
```

## Overview

The Inference Substrate is a compact simulation engine built to explore how parity-based collapse laws emerge from simple, independent rare-event transitions. It provides a clean, reproducible implementation of the core parity model, along with a physical validation of it.

This repository contains:

- A full chain simulation (step-by-step transitions, parity collapse detection)
- A minimal parity demonstration (Appendix A version)
- A physics-grounded escape-rate benchmark (Kramers vs. Langevin)
- A conceptual manuscript sketching possible extensions beyond physics
- A permanent noncommercial license protecting commercial use
- A simple, readable codebase intended for research, teaching, and exploration

The project is released once, in full, and is not intended for ongoing maintenance.

## Features

**Full inference substrate simulation**
- Independent rare-event transitions
- Chain-length scaling
- Parity-based collapse detection
- Empirical vs analytic comparison

**Minimal parity demonstration**
- Straight-line analytic identity
- Bernoulli-only model
- Reproducible verification plot

**Kramers/TST escape-rate benchmark against direct Langevin simulation**

**Simple, transparent code**
- No dependencies beyond Python + NumPy + matplotlib
- Easy to modify for research or teaching
- Clear separation between analytic and empirical logic

## Repository Structure

```
inference-substrate/
├── LICENSE.txt
├── README.md
├── CITATION.cff
├── Manuscript.pdf
├── inference_substrate_parity.py
└── benchmarks/
    ├── parity/
    │   ├── markov_chain_parity_benchmark.py
    │   └── parity_plot_overlay.py
    ├── physics/
    │   ├── kramers_vs_langevin_benchmark.py
    │   ├── poisson_vs_langevin.py
    │   └── triple_well_langevin_benchmark.py
    ├── ctmc/
    │   └── ctmc_two_state_benchmark.py
    ├── decision_threshold/
    │   ├── decision_threshold_benchmark1.py
    │   └── decision_threshold_benchmark2.py
    └── multi_agent/
        ├── multi_agent_agentcount_sweep.py
        ├── multi_agent_asymmetry_sweep.py
        ├── multi_agent_coupling_sweep.py
        ├── multi_agent_langevin_benchmark.py
        └── multi_agent_noise_sweep.py
```

## Benchmark Suite Overview

The benchmark suite evaluates how the minimal inference substrate behaves across a wide range of dynamical regimes. Each benchmark isolates a specific phenomenon and tests whether the substrate's collapse structure, parity behavior, or noise-driven inference dynamics remain consistent.

### Parity Benchmarks
- `markov_chain_parity_benchmark.py` — Tests parity structure in discrete Markov transitions.
- `parity_plot_overlay.py` — Minimal Appendix A parity demonstration.

### Physics Benchmarks
- `kramers_vs_langevin_benchmark.py` — Compares Kramers escape predictions to Langevin dynamics.
- `poisson_vs_langevin.py` — Tests Poisson collapse vs continuous Langevin noise.
- `triple_well_langevin_benchmark.py` — Multi-well metastability benchmark.

### CTMC Benchmarks
- `ctmc_two_state_benchmark.py` — Two-state exponential waiting-time benchmark.

### Decision Threshold Benchmarks
- `decision_threshold_benchmark1.py` — Basic threshold-crossing dynamics.
- `decision_threshold_benchmark2.py` — Extended threshold behavior under noise.

### Multi-Agent Benchmarks
- `multi_agent_agentcount_sweep.py` — Scaling behavior with agent count.
- `multi_agent_asymmetry_sweep.py` — Asymmetric coupling effects.
- `multi_agent_coupling_sweep.py` — Phase transitions under coupling strength.
- `multi_agent_langevin_benchmark.py` — Multi-agent Langevin substrate behavior.
- `multi_agent_noise_sweep.py` — Noise sensitivity and stability.

## Usage

### Kramers vs. Langevin Benchmark (Escape-Rate Validation)

Run:

```bash
python benchmarks/physics/kramers_vs_langevin_benchmark.py
```

This produces escape-rate comparisons between:

- Kramers/TST prediction
- empirical barrier-crossing
- empirical far-well commitment

The Kramers/TST prediction lies between the two empirical measures, as expected from metastable escape theory.

### Full Inference Substrate Simulation

Run:

```bash
python inference_substrate_parity.py
```

This produces:

- `inference_substrate_parity.png`

showing empirical parity collapse behavior over chain lengths 1–40.

### Minimal Parity Demonstration

Run:

```bash
python benchmarks/parity/parity_plot_overlay.py
```

This produces:

- `parity_plot_overlay.png`

## Installation

Requirements:
- python >= 3.10
- numpy
- scipy
- matplotlib

Install dependencies:

```bash
pip install -r requirements.txt
```

## About the Manuscript

`Manuscript.pdf` develops the parity/collapse model in detail and derives its physical embedding. Later sections explore conceptual extensions beyond physics; these are hypotheses, not validated results.

## License

PolyForm Noncommercial License 1.0.0. Noncommercial use only. Commercial licensing available.

## Citation

Nyhan, Patrick D. *Inference Substrate: A Minimal Parity-Driven Collapse Model.*
See `CITATION.cff`.

## Status

This is a one-time release.

## Contact

Patrick D. Nyhan
pdn.nyhan@gmail.com
