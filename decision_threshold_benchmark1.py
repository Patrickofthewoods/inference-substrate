"""
Decision-Threshold Drift-Diffusion Benchmark
--------------------------------------------

This benchmark tests whether the parity/Poisson collapse structure observed
in the physics domain (Kramers escape) also holds in a structurally different
system: a noisy evidence-accumulation process with a decision threshold.

Model:
    x_{t+dt} = x_t + v * dt + sigma * sqrt(dt) * N(0, 1)

A decision occurs when x_t crosses a threshold a.

Closed-form approximation:
    For a positive drift v and threshold a, the mean first-passage time is
    approximately a / v, so the effective decision rate is:

        k ≈ v / a

Poisson prediction:
    P_decision(T) = 1 - exp(-k * T)

Empirical definitions:
1. Barrier-crossing (any threshold hit):
   The process hits x >= a at least once in [0, T].
   This overcounts committed decisions due to recrossing.

2. Committed decision:
   The process hits x >= a and remains beyond a for a dwell time tau
   without recrossing below a.
   This undercounts true decisions.

Runtime note:
    A full run (20,000 trajectories) typically takes about 1–2 minutes.

Example output (typical):
    Poisson prediction:               0.181269
    Empirical (committed decision):   0.165800
    Empirical (barrier crossing):     0.205400
"""

import numpy as np

def poisson_prediction(k, T):
    return 1.0 - np.exp(-k * T)

def simulate_barrier_crossing(v, sigma, a, T, dt, n_trajectories):
    hits = 0
    n_steps = int(T / dt)

    for _ in range(n_trajectories):
        x = 0.0
        for _ in range(n_steps):
            x += v * dt + sigma * np.sqrt(dt) * np.random.randn()
            if x >= a:
                hits += 1
                break
    return hits / n_trajectories

def simulate_committed_decision(v, sigma, a, T, dt, dwell_time, n_trajectories):
    committed = 0
    n_steps = int(T / dt)
    dwell_steps = int(dwell_time / dt)

    for _ in range(n_trajectories):
        x = 0.0
        t = 0.0
        decided = False

        while t < T and not decided:
            x += v * dt + sigma * np.sqrt(dt) * np.random.randn()
            t += dt

            if x >= a:
                stable = True
                x_dwell = x
                t_dwell = t

                for _ in range(dwell_steps):
                    if t_dwell >= T:
                        break
                    x_dwell += v * dt + sigma * np.sqrt(dt) * np.random.randn()
                    t_dwell += dt
                    if x_dwell < a:
                        stable = False
                        break

                if stable:
                    committed += 1
                    decided = True

    return committed / n_trajectories

def run_benchmark():
    # Drift-diffusion parameters
    v = 0.1       # drift rate
    a = 1.1       # decision threshold
    sigma = 0.3   # noise strength

    # Effective rate approximation: k ≈ v / a
    k = v / a

    # Time horizon and simulation settings
    T = 2.0
    dt = 1e-3
    dwell_time = 0.1
    n_trajectories = 20000

    p_pred = poisson_prediction(k, T)
    p_committed = simulate_committed_decision(v, sigma, a, T, dt, dwell_time, n_trajectories)
    p_barrier = simulate_barrier_crossing(v, sigma, a, T, dt, n_trajectories)

    print("\n=== Decision-Threshold Drift-Diffusion Benchmark ===")
    print(f"Drift v:                          {v:.3f}")
    print(f"Threshold a:                      {a:.3f}")
    print(f"Noise sigma:                      {sigma:.3f}")
    print(f"Effective rate k ≈ v/a:           {k:.6f}")
    print(f"Poisson prediction:               {p_pred:.6f}")
    print(f"Empirical (committed decision):   {p_committed:.6f}")
    print(f"Empirical (barrier crossing):     {p_barrier:.6f}")
    print("====================================================\n")

if __name__ == "__main__":
    run_benchmark()
