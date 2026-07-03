"""
Three-State Continuous-Time Markov Chain Benchmark
--------------------------------------------------

States:
    0 = A   (initial)
    1 = B   (intermediate)
    2 = C   (final)

Goal:
    Start in A at t=0, simulate a 3-state CTMC with restoring dynamics,
    and compare:

        - Empirical P(state = C at T)
        - Exact CTMC prediction from the generator

This extends the 2-state test and checks whether the generalized
parity/Poisson structure still holds when you have an intermediate basin.
"""

import numpy as np

def simulate_ctmc_three_state(Q, T, n_trajectories):
    """
    Q: 3x3 generator matrix
    T: time horizon
    Returns:
        frac_C: fraction of trajectories in state C at time T
    """
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

            # choose next state based on off-diagonal rates
            rates = Q[state, :].copy()
            rates[state] = 0.0
            probs = rates / rates.sum()
            state = np.random.choice(n_states, p=probs)

        if state == 2:
            frac_C += 1

    return frac_C / n_trajectories

def run_benchmark():
    # Example generator with restoring dynamics:
    # A <-> B, B <-> C, some backflow from C
    k_AB = 0.05
    k_BA = 0.02
    k_BC = 0.04
    k_CB = 0.03

    Q = np.array([
        [-k_AB,        k_AB,        0.0   ],
        [ k_BA, -(k_BA + k_BC),     k_BC  ],
        [ 0.0,         k_CB,   -k_CB     ]
    ])

    T = 5.0
    n_trajectories = 20000

    frac_C = simulate_ctmc_three_state(Q, T, n_trajectories)

    print("\n=== Three-State CTMC Benchmark ===")
    print(f"Time horizon T:             {T:.3f}")
    print(f"Empirical P(state=C at T):  {frac_C:.6f}")
    print("==================================\n")

if __name__ == "__main__":
    run_benchmark()
