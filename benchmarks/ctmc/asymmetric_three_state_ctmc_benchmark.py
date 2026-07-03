"""
Asymmetric Three-State CTMC Benchmark
-------------------------------------

States:
    0 = A (shallow)
    1 = B (medium)
    2 = C (deep)

Goal:
    Start in A at t=0, simulate an asymmetric 3-state CTMC with
    restoring dynamics and a deeper final basin, and measure:

        - Empirical P(state = C at T)

This tests how the substrate behaves when one basin is much "deeper"
(i.e., harder to leave) than the others.
"""

import numpy as np

def simulate_ctmc_three_state(Q, T, n_trajectories):
    n_states = Q.shape[0]
    frac_C = 0.0

    for _ in range(n_trajectories):
        t = 0.0
        state = 0  # start in A

        while t < T:
            rate_out = -Q[state, state]
            if rate_out <= 0:
                break

            dt = np.random.exponential(1.0 / rate_out)
            if t + dt >= T:
                break

            t += dt

            rates = Q[state, :].copy()
            rates[state] = 0.0
            probs = rates / rates.sum()
            state = np.random.choice(n_states, p=probs)

        if state == 2:
            frac_C += 1

    return frac_C / n_trajectories

def run_benchmark():
    # Asymmetric generator:
    # A is shallow, B is medium, C is deep.
    k_AB = 0.08   # A -> B (fairly easy)
    k_BA = 0.04   # B -> A (moderate backflow)

    k_BC = 0.05   # B -> C (moderate)
    k_CB = 0.01   # C -> B (rare: deep basin)

    Q = np.array([
        [-k_AB,        k_AB,        0.0   ],
        [ k_BA, -(k_BA + k_BC),     k_BC  ],
        [ 0.0,         k_CB,   -k_CB     ]
    ])

    T = 10.0
    n_trajectories = 30000

    frac_C = simulate_ctmc_three_state(Q, T, n_trajectories)

    print("\n=== Asymmetric Three-State CTMC Benchmark ===")
    print(f"Time horizon T:             {T:.3f}")
    print(f"Empirical P(state=C at T):  {frac_C:.6f}")
    print("=============================================\n")

if __name__ == "__main__":
    run_benchmark()
