# Inference Substrate

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-PolyForm%20Noncommercial-orange.svg)
![Release](https://img.shields.io/badge/Release-One--Time-green.svg)
![Model](https://img.shields.io/badge/Model-Parity--Driven-black.svg)

A minimal, composable, parity‑driven inference substrate for studying rare‑event transitions, domain‑agnostic collapse behavior, and physics‑grounded escape dynamics.

The substrate is intentionally small: its purpose is to show how much structure emerges from how little machinery — and to provide a clean, reproducible reference implementation for research, teaching, and conceptual exploration.

## Motivation

Most collapse or inference models rely on domain‑specific assumptions: quantum rules, biological constraints, neural architectures, or bespoke stochastic processes. The Inference Substrate takes the opposite approach. It asks:

> What is the simplest possible collapse law that still produces meaningful structure?

The answer is a parity law emerging from independent rare‑event transitions. This repo demonstrates that:

- parity collapse is domain‑agnostic
- it arises from minimal assumptions
- it matches analytic predictions exactly
- and when grounded in physics (via Kramers escape‑rate theory), it remains empirically correct within known theoretical bounds

The substrate is designed to be transparent, reproducible, and easy to extend.

## Overview

The Inference Substrate provides two verified components:

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

## Substrate Architecture (Updated)

The minimal inference substrate includes a small API for constructing inference primitives.
Claude's domain‑level evaluation showed:

- Ascent primitives are universal
- Collapse primitives are optional and domain‑specific
- ValidOp is unnecessary and has been removed
- The API must run cleanly with or without collapse

The refined architecture now reflects this.

### Ascent Primitives (Required)

An `AscentPrimitive` performs the domain's forward computation.
Every domain defines one.

Examples:

- Kramers ascent
- CTMC ascent
- Decision‑threshold ascent

### Collapse Primitives (Optional)

A `CollapsePrimitive` enforces a domain's validity regime only when such a regime exists.

Examples:

- Decision‑threshold has a meaningful collapse rule (regime mismatch)
- Kramers and CTMC do not

### Telemetry

Telemetry operators convert raw input into a frame the primitives can use.
The minimal substrate uses dict‑based frames.

### PrimitiveAPI (Refined)

The updated API:

- requires ascent
- allows collapse to be absent
- runs collapse only if registered
- removes ValidOp entirely
- matches empirical behavior across all tested domains

Example:

```python
from substrate.primitive_api import PrimitiveAPI, TelemetryOperator
from substrate.collapse_primitives import (
    KramersAscent,
    CTMCAscent,
    ThresholdAscent,
    RegimeMismatchRule
)

api = PrimitiveAPI(
    ascent_primitives={},
    telemetry=TelemetryOperator(),
    collapse_primitives={}
)

api.register_ascent("kramers", KramersAscent())
api.register_ascent("ctmc", CTMCAscent())

api.register_ascent("threshold", ThresholdAscent())
api.register_collapse("threshold_regime", RegimeMismatchRule())
```

This is the canonical minimal substrate.

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

## Repository Structure

```
inference-substrate/
├── LICENSE.txt
├── README.md
├── CITATION.cff
├── Manuscript.pdf
├── inference_substrate_parity.py
├── substrate/
│   ├── primitive_api.py        # refined API (ascent required, collapse optional)
│   ├── collapse_primitives.py  # ascent + collapse primitives
│   ├── primitives.py
│   ├── tests/
│   └── __init__.py
└── benchmarks/
    ├── parity/
    ├── physics/
    ├── ctmc/
    ├── decision_threshold/
    └── multi_agent/
```

## Benchmark Suite Overview

The benchmark suite evaluates how the minimal inference substrate behaves across a wide range of dynamical regimes. Each benchmark isolates a specific phenomenon and tests whether the substrate's collapse structure, parity behavior, or noise‑driven inference dynamics remain consistent.

*(Your benchmark table remains unchanged.)*

## Why This Substrate Matters

Most collapse models rely on domain‑specific assumptions.
The Inference Substrate shows that a simple, domain‑agnostic parity law emerges naturally from independent rare‑event transitions.

The physics benchmark demonstrates that this law is not an abstract curiosity: when the transition probability `k` is derived from a real metastable system, the parity prediction matches empirical behavior within the known bounds of transition‑state theory.

The substrate is intentionally minimal — its value comes from showing how much structure arises from how little machinery.

## About the Manuscript

`Manuscript.pdf` develops the parity/collapse model in detail and derives its physical embedding.
Later sections explore conceptual extensions beyond physics; these are hypotheses, not validated results.

## License

PolyForm Noncommercial License 1.0.0.
Noncommercial use only.
Commercial licensing available.

## Citation

Nyhan, Patrick D.
*Inference Substrate: A Minimal Parity‑Driven Collapse Model.*
See `CITATION.cff`.

## Status

This is a one‑time release.

## Contact

Patrick D. Nyhan
pdn.nyhan@gmail.com
