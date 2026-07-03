"""
Triple-Well Langevin Benchmark
------------------------------

Continuous stochastic dynamics with an asymmetric triple-well potential.

States (basins):
    Left well   = shallow
    Middle well = medium
    Right well  = deep

Goal:
    Start in the left well, simulate Langevin dynamics, and measure:
        - Empirical probability of being in the deep well at time T

This tests whether the minimal-assumption substrate holds in
continuous metastable systems with hierarchical basin depths.
"""

import numpy as np

# Triple-well potential U(x) = ax^4 - bx^2 + cx
# Adjust (a, b, c) to shape asymmetry.
def U(x, a=1.0, b=4.0, c=-2.0):
    return a*x**4 - b*x**2 + c*x

def dU_dx(x, a=1.0, b=4.0, c=-2.0):
    return 4*a*x**3 - 2*b*x + c

def simulate_langevin(T, dt, D, n_trajectories):
    """
    Langevin SDE:
        dx = -U'(x)*dt + sqrt(2D)*dW

    Returns:
        frac_deep: fraction of trajectories in deep well at time T
    """

    # Basin boundaries (approximate for this potential)
    # You can adjust these if you change (a, b, c)
    left_boundary   = -1.5
    middle_boundary = 0.0
    deep_boundary   = 1.5

    frac_deep = 0
    steps = int(T / dt)

    for _ in range(n_trajectories):
        # Start in left well
        x = -2.0

        for _ in range(steps):
            x += -dU_dx(x)*dt + np.sqrt(2*D)*np.random.randn()

        # Check final basin
        if x > deep_boundary:
            frac_deep += 1

    return frac_deep / n_trajectories

def run_benchmark():
    T = 10.0          # total time
    dt = 0.001        # timestep
    D = 0.15          # noise strength
    n_trajectories = 20000

    frac_deep = simulate_langevin(T, dt, D, n_trajectories)

    print("\n=== Triple-Well Langevin Benchmark ===")
    print(f"Time horizon T:             {T:.3f}")
    print(f"Empirical P(deep well at T): {frac_deep:.6f}")
    print("======================================\n")

if __name__ == "__main__":
    run_benchmark()
