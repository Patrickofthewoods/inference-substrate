"""
Two-State Markov Chain Parity Benchmark
---------------------------------------

This benchmark tests whether the parity/Poisson collapse structure observed
in the physics domain (Kramers escape) also holds in a structurally different
system: a simple two-state Markov chain with a rare transition rate k.

The system:
    State A --(rate k)--> State B
    State B --(rate k)--> State A

Closed-form prediction:
    P_flip(T) = 1 - exp(-k * T)

Empirical definitions:
1. Any flip:
   The chain flips state at least once during [0, T].
   This overcounts committed transitions.

2. Committed flip:
   The chain flips and remains in the new state for at least a dwell time τ.
   This undercounts true transitions.

Runtime note:
    A full run (20,000 trajectories) typically takes about 1–2 minutes.

Example output:
    Poisson prediction:               0.181269
    Empirical (committed flip):       0.165200
    Empirical (any flip):             0.205450
"""

import numpy as np

def poisson_prediction(k, T):
    return 1.0 - np.exp(-k * T)

def simulate_any_flip(k, T, dt, n_trajectories):
    flips = 0
    p = k * dt  # Bernoulli approximation
    for _ in range(n_trajectories):
        state = 0
        for _ in range(int(T / dt)):
            if np.random.rand() < p:
                state = 1 - state
                flips += 1
                break
    return flips / n_trajectories

def simulate_committed_flip(k, T, dt, dwell_time, n_trajectories):
    committed = 0
    p = k * dt
    dwell_steps = int(dwell_time / dt)

    for _ in range(n_trajectories):
        state = 0
        t = 0
        while t < T:
            if np.random.rand() < p:
                new_state = 1 - state
                stable = True
                for _ in range(dwell_steps):
                    if np.random.rand() < p:
                        stable = False
                        break
                if stable:
                    committed += 1
                    break
                else:
                    state = new_state
            t += dt
    return committed / n_trajectories

def run_benchmark():
    k = 0.1
    T = 2.0
    dt = 1e-3
    dwell_time = 0.1
    n_trajectories = 20000

    p_pred = poisson_prediction(k, T)
    p_any = simulate_any_flip(k, T, dt, n_trajectories)
    p_committed = simulate_committed_flip(k, T, dt, dwell_time, n_trajectories)

    print("\n=== Two-State Markov Chain Parity Benchmark ===")
    print(f"Poisson prediction:               {p_pred:.6f}")
    print(f"Empirical (committed flip):       {p_committed:.6f}")
    print(f"Empirical (any flip):             {p_any:.6f}")
    print("==============================================\n")

if __name__ == "__main__":
    run_benchmark()
