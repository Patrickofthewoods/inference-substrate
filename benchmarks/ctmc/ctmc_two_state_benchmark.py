"""
Two-State Continuous-Time Markov Chain Benchmark
------------------------------------------------

Goal:
    Test whether the generalized parity/Poisson collapse structure that
    worked for Kramers escape also holds for a simple two-state CTMC
    with genuine exponential waiting times and restoring dynamics.

System:
    States: A (0), B (1)

    Generator matrix Q:
        Q = [ -k_AB    k_AB ]
            [  k_BA   -k_BA ]

    From state i, the waiting time to leave is Exp(rate_i),
    where rate_i = -Q[i, i], and the next state is chosen
    according to Q[i, j] / rate_i.

We start in state A at t=0 and ask:

    - What is the probability of being in state B at time T?
    - How does that compare to the exact two-state CTMC formula?

Exact two-state CTMC formula (for general k_AB, k_BA):
    Stationary probability of B:
        pi_B = k_AB / (k_AB + k_BA)

    Probability of being in B at time t, starting from A:
        P_B(t) = pi_B * (1 - exp(-(k_AB + k_BA) * t))

Note:
    The probability of "ever leaving A" in [0, T] is exactly
    1 - exp(-k_AB * T) by definition of the exponential CDF.
    Comparing that to a naive Poisson 1 - exp(-k_AB * T) is
    tautological and not evidence about the substrate.
"""

import numpy as np

def exact_two_state_ctmc_P_B(k_AB, k_BA, T):
    k_total = k_AB + k_BA
    pi_B = k_AB / k_total
    return pi_B * (1.0 - np.exp(-k_total * T))

def simulate_ctmc_two_state(k_AB, k_BA, T, n_trajectories):
    """
    Simulate a two-state CTMC using exact exponential waiting times.

    Returns:
        frac_B: fraction of trajectories in state B at time T
        frac_flip: fraction that ever left A during [0, T]
    """
    frac_B = 0
    frac_flip = 0

    for _ in range(n_trajectories):
        t = 0.0
        state = 0  # 0 = A, 1 = B
        ever_left_A = False

        while t < T:
            if state == 0:
                rate = k_AB
                next_state = 1
            else:
                rate = k_BA
                next_state = 0

            dt = np.random.exponential(1.0 / rate)

            if t + dt >= T:
                break

            t += dt
            state = next_state

            if state == 1:
                ever_left_A = True

        if state == 1:
            frac_B += 1
        if ever_left_A:
            frac_flip += 1

    return frac_B / n_trajectories, frac_flip / n_trajectories

def run_benchmark():
    k_AB = 0.1   # rate from A to B
    k_BA = 0.1   # rate from B to A

    T = 2.0
    n_trajectories = 20000

    p_exact = exact_two_state_ctmc_P_B(k_AB, k_BA, T)
    frac_B, frac_flip = simulate_ctmc_two_state(k_AB, k_BA, T, n_trajectories)

    print("\n=== Two-State CTMC Benchmark ===")
    print(f"k_AB (A→B):                      {k_AB:.3f}")
