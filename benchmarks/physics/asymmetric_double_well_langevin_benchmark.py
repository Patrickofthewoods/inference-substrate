"""
Asymmetric Double-Well Langevin Benchmark
-----------------------------------------

This benchmark simulates overdamped Langevin dynamics in an *asymmetric*
double-well potential of the form:

    U(x) = a*x**4 - b*x**2 + c*x

The linear term (c*x) breaks symmetry and creates:
    - a shallow left well
    - a deep right well

Despite the old filename, this potential has **two** wells, not three.

Goal:
    Start in the left well and measure the empirical probability of ending
    in the deep well at time T, and compare it to the Kramers/Transition-State
    Theory (TST) prediction for the same potential.

Runtime note:
    With T = 10, dt = 1e-3, and n_trajectories = 20,000, this benchmark
    performs ~2e8 integration steps and can take several minutes.
"""

import numpy as np

# ============================================================
# 1. Potential and derivatives
# ============================================================

def U(x, a=1.0, b=4.0, c=-2.0):
    return a*x**4 - b*x**2 + c*x

def dU_dx(x, a=1.0, b=4.0, c=-2.0):
    return 4*a*x**3 - 2*b*x + c

def d2U_dx2(x, a=1.0, b=4.0, c=-2.0):
    return 12*a*x**2 - 2*b

# ============================================================
# 2. Stationary points: wells and barrier
# ============================================================

def find_wells_and_barrier(a=1.0, b=4.0, c=-2.0):
    """
    Solve dU/dx = 0 for the cubic:
        4*a*x^3 - 2*b*x + c = 0

    For typical parameters (a>0, b>0, moderate |c|), this yields:
        - two minima (left, right)
        - one barrier (middle)
    """
    coeffs = [4*a, 0.0, -2*b, c]
    roots = np.roots(coeffs)
    roots = np.real(roots[np.isreal(roots)])  # discard complex parts

    # Sort roots by x coordinate
    roots = np.sort(roots)

    if len(roots) != 3:
        raise RuntimeError("Expected three real stationary points for this potential.")

    x_left, x_barrier, x_right = roots
    return x_left, x_barrier, x_right

def poisson_escape_prob(k_rate, T):
    """
    Poisson escape probability by time T:
        P_escape(T) = 1 - exp(-k * T)
    """
    return 1.0 - np.exp(-k_rate * T)

# ============================================================
# 3. Langevin simulation (empirical committed transitions)
# ============================================================

def simulate_langevin(T, dt, D, n_trajectories, a, b, c, x_right):
    """
    Overdamped Langevin SDE:
        dx = -U'(x)*dt + sqrt(2*D*dt)*N(0,1)

    Returns:
        frac_deep: fraction of trajectories in the deep well at time T
    """

    # Deep-well boundary: actual right minimum
    deep_boundary = x_right

    frac_deep = 0
    steps = int(T / dt)

    for _ in range(n_trajectories):
        # Start in left well (slightly left of the left minimum)
        x = -2.0

        for _ in range(steps):
            drift = -dU_dx(x, a, b, c) * dt
            noise = np.sqrt(2 * D * dt) * np.random.randn()
            x += drift + noise

        # Check final basin: committed to deep right well
        if x > deep_boundary:
            frac_deep += 1

    return frac_deep / n_trajectories

# ============================================================
# 4. Benchmark runner
# ============================================================

def run_benchmark():
    # Potential and noise parameters
    a = 1.0
    b = 4.0
    c = -2.0

    T = 10.0          # total time
    dt = 0.001        # timestep
    D = 0.15          # noise strength
    n_trajectories = 20000

    # Find wells and barrier once
    x_left, x_barrier, x_right = find_wells_and_barrier(a, b, c)

    # Barrier height relative to left well
    DeltaU = U(x_barrier, a, b, c) - U(x_left, a, b, c)

    # Curvatures at well and barrier
    omega_well = np.sqrt(abs(d2U_dx2(x_left, a, b, c)))
    omega_barrier = np.sqrt(abs(d2U_dx2(x_barrier, a, b, c)))

    # Kramers/Transition-State-Theory escape rate
    gamma = 1.0
    prefactor = (omega_well * omega_barrier) / (2.0 * np.pi * gamma)
    k_rate = prefactor * np.exp(-DeltaU / D)
    p_kramers = poisson_escape_prob(k_rate, T)

    # Empirical Langevin result (using the same x_right)
    p_empirical = simulate_langevin(T, dt, D, n_trajectories, a, b, c, x_right)

    print("\n=== Asymmetric Double-Well Langevin Benchmark ===")
    print(f"Potential: U(x) = {a}*x^4 - {b}*x^2 + {c}*x")
    print(f"Left minimum x_left:              {x_left:.6f}")
    print(f"Barrier top x_barrier:            {x_barrier:.6f}")
    print(f"Right minimum x_right:            {x_right:.6f}")
    print(f"Barrier height ΔU (left→barrier): {DeltaU:.6f}")
    print()
    print(f"Kramers escape rate k (1/time):   {k_rate:.6f}")
    print(f"Poisson escape prob by T={T:.3f}: {p_kramers:.6f}")
    print(f"Empirical P(deep well at T):      {p_empirical:.6f}")
    print("===============================================\n")

if __name__ == "__main__":
    run_benchmark()
