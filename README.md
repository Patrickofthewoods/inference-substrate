Inference Substrate


A minimal, parity‑driven simulation framework for collapse behavior in rare‑event chains.

Overview
The Inference Substrate is a compact simulation engine built to explore how parity‑based collapse laws emerge from simple, independent rare‑event transitions. It provides a clean, reproducible implementation of the core model described in the accompanying manuscript.

This repository contains:

A full chain simulation (step‑by‑step transitions, parity collapse detection)

A minimal parity demonstration (Appendix A version)

A permanent noncommercial license protecting commercial use

A simple, readable codebase intended for research, teaching, and exploration

The project is released once, in full, and is not intended for ongoing maintenance.

Features
Full inference substrate simulation

Independent rare‑event transitions

Chain‑length scaling

Parity‑based collapse detection

Empirical vs analytic comparison

Minimal parity demonstration

Straight‑line analytic identity

Bernoulli‑only model

Reproducible verification plot

Simple, transparent code

No dependencies beyond Python + matplotlib

Easy to modify for research or teaching

Clear separation between analytic and empirical logic

Repository Structure

Code

/

├── LICENSE.txt                 # PolyForm Noncommercial License

├── README.md                   # Project documentation

├── CITATION.cff                # Academic citation metadata

├── inference\_substrate\_parity.py   # Full chain simulation

├── parity\_plot\_overlay.py          # Minimal Appendix A parity demo

└── (generated plots saved locally)

Usage



\### Full Inference Substrate Simulation

Run the full chain simulation:



```

python inference\_substrate\_parity.py

```



This produces:



```

inference\_substrate\_parity.png

```



showing empirical parity collapse behavior over chain lengths 1–40, compared against the analytic prediction:



log(1 − 2 p\_n) = n ⋅ log(1 − 2 k)



\### Minimal Parity Demonstration (Appendix A)

Run the minimal parity model:



```

python parity\_plot\_overlay.py

```



This produces:



```

parity\_plot\_overlay.png

```



which overlays empirical Bernoulli parity results on the analytic straight line.



License
This project is released under the PolyForm Noncommercial License 1.0.0.

You may use, modify, and share the code for noncommercial purposes only, including:

research

experimentation

teaching

personal study

academic work

hobby projects

Commercial use is not permitted without a separate commercial license.

To obtain commercial rights, contact:

Patrick D. Nyhan  
Licensor and copyright holder

Citation

If you use this work in academic research, please cite:



Nyhan, Patrick D.

Inference Substrate: A Minimal Parity‑Driven Collapse Model.



A formal CITATION.cff file is included in this repository.

Status
This is a one‑time release.
The project is not intended for ongoing updates or maintenance.

Contact
For commercial licensing inquiries:

Patrick D. Nyhan  
(pdn.nyhan@gmail.com)

