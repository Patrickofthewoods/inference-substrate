# Inference Substrate

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-PolyForm%20Noncommercial-orange.svg)
![Release](https://img.shields.io/badge/Release-One--Time-green.svg)
![Model](https://img.shields.io/badge/Model-Parity--Driven-black.svg)

A minimal, composable, parity‑driven simulation framework for studying rare‑event transitions, collapse behavior, and physics‑grounded escape dynamics.

## Motivation

Most collapse or inference models rely on domain‑specific assumptions: quantum rules, biological constraints, neural architectures, or bespoke stochastic processes. The Inference Substrate takes the opposite approach. It asks:

> What is the simplest possible collapse law that still produces meaningful structure?

The answer is a parity law emerging from independent rare‑event transitions. This repo demonstrates that:

- parity collapse is domain‑agnostic
- it arises from minimal assumptions
- it matches analytic predictions exactly
- and when grounded in physics (via Kramers escape‑rate theory), it remains empirically correct within known theoretical bounds

The substrate is intentionally small. Its purpose is to show how much structure emerges from how little machinery — and to provide a clean, reproducible reference implementation for research, teaching, and conceptual exploration.

## Overview

The Inference Substrate is a compact simulation engine for exploring how parity‑based collapse laws emerge from independent rare‑event transitions. It provides:

- a clean implementation of the core parity‑collapse identity
- a physics‑grounded validation using Kramers escape‑rate theory
- direct Langevin simulations for empirical comparison
- a minimal substrate API for building collapse primitives and inference processes

The goal is clarity: a small, transparent codebase demonstrating how parity laws arise, how they behave, and how they connect to real physical systems.

## Quickstart

Clone the repository:

```bash
git clone https://github.com/Patrickofthewoods/inference-substrate.git
cd inference-substrate
```

Install minimal dependencies:

```bash
pip install numpy scipy matplotlib
```

Run the physics‑grounded benchmark:

```bash
python benchmarks/physics/kramers_vs_langevin_benchmark.py
```

Run the full parity‑collapse chain simulation:

```bash
python inference_substrate_parity.py
```

Run the minimal Appendix A parity demonstration:

```bash
python benchmarks/parity/parity_plot_overlay.py
```

## What This Repo Actually Does

Two verified, reproducible components:

### 1. Parity‑Based Collapse Model

For a chain of independent rare‑event transitions, whether the system ends in a different state than it started depends only on the parity (odd/even count) of successful transitions.

This repo:

- simulates the chain directly
- computes empirical parity outcomes
- compares them to the closed‑form analytic prediction
- shows exact agreement

### 2. Physics‑Grounded Escape‑Rate Benchmark (Kramers vs Langevin)

The parity model requires a transition probability `k`. Instead of assuming one, this benchmark:

- derives `k` from a symmetric double‑well potential
- uses Kramers' escape‑rate theory
- compares the prediction to full Langevin dynamics

The results agree within the known bounds of transition‑state theory.

To see it immediately:

```bash
python kramers_vs_langevin_benchmark.py
```

## Substrate API Overview

Although the repo is parity‑focused, it also includes a minimal substrate API for constructing collapse primitives and running inference processes.

### Example

```python
from substrate.primitive_api import Substrate
from substrate.collapse_primitives import CollapseToZero

S = Substrate()
S.add_primitive(CollapseToZero(rate=0.1))

result = S.run(initial_state=1.0, steps=1000)
print(result)
```

## Features

- Composable primitives (collapse, ascent, bounded change)
- Unified substrate API (build, run, serialize, inspect)
- Deterministic + stochastic modes
- Minimal dependencies
- Physics‑aligned benchmarks
- Manuscript‑ready figures and parity tests

## Repository Structure

```
inference-substrate/
├── LICENSE.txt
├── README.md
├── CITATION.cff
├── Manuscript.pdf
├── inference_substrate_parity.py
├── substrate/
│   ├── primitive_api.py
│   ├── collapse_primitives.py
│   ├── primitives.py
│   ├── tests/
│   └── __init__.py
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

The benchmark suite evaluates how the minimal inference substrate behaves across a wide range of dynamical regimes. Each benchmark isolates a specific phenomenon and tests whether the substrate's collapse structure, parity behavior, or noise‑driven inference dynamics remain consistent.

### Benchmark Summary

| Benchmark | Domain | Purpose | File |
|---|---|---|---|
| Markov Chain Parity | Parity | Tests discrete parity transitions | `benchmarks/parity/markov_chain_parity_benchmark.py` |
| Parity Overlay | Parity | Minimal Appendix A demonstration | `benchmarks/parity/parity_plot_overlay.py` |
| Kramers vs Langevin | Physics | Escape‑rate validation | `benchmarks/physics/kramers_vs_langevin_benchmark.py` |
| Poisson vs Langevin | Physics | Poisson collapse vs continuous noise | `benchmarks/physics/poisson_vs_langevin.py` |
| Triple‑Well Langevin | Physics | Multi‑well metastability | `benchmarks/physics/triple_well_langevin_benchmark.py` |
| CTMC Two‑State | CTMC | Exponential waiting‑time benchmark | `benchmarks/ctmc/ctmc_two_state_benchmark.py` |
| Decision Threshold 1 | Decision | Basic threshold crossing | `benchmarks/decision_threshold/decision_threshold_benchmark1.py` |
| Decision Threshold 2 | Decision | Threshold behavior under noise | `benchmarks/decision_threshold/decision_threshold_benchmark2.py` |
| Agent Count Sweep | Multi‑Agent | Scaling with agent count | `benchmarks/multi_agent/multi_agent_agentcount_sweep.py` |
| Asymmetry Sweep | Multi‑Agent | Asymmetric coupling effects | `benchmarks/multi_agent/multi_agent_asymmetry_sweep.py` |
| Coupling Sweep | Multi‑Agent | Phase transitions under coupling | `benchmarks/multi_agent/multi_agent_coupling_sweep.py` |
| Langevin Multi‑Agent | Multi‑Agent | Multi‑agent Langevin substrate | `benchmarks/multi_agent/multi_agent_langevin_benchmark.py` |
| Noise Sweep | Multi‑Agent | Noise sensitivity and stability | `benchmarks/multi_agent/multi_agent_noise_sweep.py` |

## Usage

### Kramers vs Langevin Benchmark

```bash
python benchmarks/physics/kramers_vs_langevin_benchmark.py
```

Produces escape‑rate comparisons between:

- Kramers/TST prediction
- empirical barrier‑crossing
- empirical far‑well commitment

The Kramers/TST prediction lies between the two empirical measures, as expected.

### Full Inference Substrate Simulation

```bash
python inference_substrate_parity.py
```

Outputs:

```
inference_substrate_parity.png
```

showing empirical parity collapse behavior over chain lengths 1–40.

### Minimal Parity Demonstration

```bash
python benchmarks/parity/parity_plot_overlay.py
```

Outputs:

```
parity_plot_overlay.png
```

## Installation

Requirements:

- python ≥ 3.10
- numpy
- scipy
- matplotlib

Install:

```bash
pip install -r requirements.txt
```

## Why This Substrate Matters

Most collapse models rely on domain‑specific assumptions. The Inference Substrate shows that a simple, domain‑agnostic parity law emerges naturally from independent rare‑event transitions.

The physics benchmark demonstrates that this law is not an abstract curiosity: when the transition probability `k` is derived from a real metastable system, the parity prediction matches empirical behavior within the known bounds of transition‑state theory.

The substrate is intentionally minimal — its value comes from showing how much structure arises from how little machinery.

## About the Manuscript

`Manuscript.pdf` develops the parity/collapse model in detail and derives its physical embedding. Later sections explore conceptual extensions beyond physics; these are hypotheses, not validated results.

## License

PolyForm Noncommercial License 1.0.0.
Noncommercial use only.
Commercial licensing available.

## Citation

Nyhan, Patrick D.
Inference Substrate: A Minimal Parity‑Driven Collapse Model.
See `CITATION.cff`.

## Status

This is a one‑time release.

## Contact

Patrick D. Nyhan
pdn.nyhan@gmail.com
