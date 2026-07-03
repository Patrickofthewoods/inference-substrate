"""
Kramers vs. Langevin Benchmark
------------------------------

This benchmark compares the Kramers/Transition-State-Theory escape-rate
prediction to two empirical definitions of escape in a symmetric double-well
Langevin system.

1. Kramers/TST prediction (Poisson process):
   P_escape(T) = 1 - exp(-k * T)
   where k is the continuous-time escape rate.

2. Empirical barrier-crossing probability:
   The particle merely crosses the barrier top at x = 0.
   This *overcounts* true transitions due to rapid recrossing.

3. Empirical far-well-reaching probability:
   The particle reaches the minimum of the opposite well.
   This *undercounts* true transitions because some barrier crossings
   fall back into the original well before committing.

Kramers/TST is an *upper bound* on the committed transition rate, so its
prediction should fall between the two empirical measures. This is a known
phenomenon in reaction-rate theory (transmission coefficient correction).

Runtime note:
    With n_trajectories = 20,000, a full run typically takes ~1–2 minutes.

Example output:
    Kramers escape rate k:                0.128972
    Poisson (Kramers/TST) prediction:     0.227362
    Empirical (far-well committed):       0.112050
    Empirical (barrier merely crossed):   0.370850
"""

import numpy as np

# ============================================================
# 1. Potential, derivatives, and Kramers rate
# ============================================================

def V(x, a):
    return x**4 - a * x**2

def dVdx(x, a):
    return 4*x**3 - 2*a*x

def d2Vdx2(x, a):
    return 12*x**2 - 2*a

def kramers_rate(a, D, gamma=1.0):
    x_well = np.sqrt(a / 2.0)
    x_barrier = 0.0

    DeltaV = V(x_barrier, a) - V(x_well, a)

    omega_well = np.sqrt(abs(d2Vdx2(x_well, a)))
    omega_barrier = np.sqrt(abs(d2Vdx2(x_barrier, a)))

    prefactor = (omega_well * omega_barrier) / (2.0 * np.pi * gamma)
    k_rate = prefactor * np.exp(-DeltaV / D)
    return k_rate

# ============================================================
# 2. Langevin first-passage: far-well commitment
# ============================================================

def simulate_first_passage(a, D, dt, T_max, n_trajectories):
    transitions = 0

    x_start = np.sqrt(a / 2.0)
    x_target = -np.sqrt(a / 2.0)

    for _ in range(n_trajectories):
        x = x_start
        t = 0.0

        while t < T_max:
            x += -dVdx(x, a) * dt + np.sqrt(2.0 * D * dt) * np.random.randn()

            if x < x_target:  # committed transition
                transitions += 1
                break

            t += dt

    return transitions / n_trajectories

# ============================================================
# 3. Langevin first-passage: barrier crossing only
# ============================================================

def simulate_barrier_crossing(a, D, dt, T_max, n_trajectories):
    crossings = 0

    x_start = np.sqrt(a / 2.0)
    barrier = 0.0

    for _ in range(n_trajectories):
        x = x_start
        t = 0.0

        while t < T_max:
            x += -dVdx(x, a) * dt + np.sqrt(2.0 * D * dt) * np.random.randn()

            if x < barrier:  # naive barrier crossing
                crossings += 1
                break

            t += dt

    return crossings / n_trajectories

# ============================================================
# 4. Poisson escape prediction from Kramers rate
# ============================================================

def poisson_escape_prob(k_rate, T_max):
    return 1.0 - np.exp(-k_rate * T_max)

# ============================================================
# 5. Benchmark runner
# ============================================================

def run_benchmark():
    a = 1.0
    D = 0.2
    dt = 1e-3
    T_max = 2.0
    n_trajectories = 20000  # increased for tighter confidence

    k_rate = kramers_rate(a, D)
    p_pred = poisson_escape_prob(k_rate, T_max)

    p_emp_far = simulate_first_passage(a, D, dt, T_max, n_trajectories)
    p_emp_barrier = simulate_barrier_crossing(a, D, dt, T_max, n_trajectories)

    print("\n=== Kramers vs Langevin Benchmark ===")
    print(f"Kramers escape rate k (1/time):      {k_rate:.6f}")
    print(f"Poisson escape prob by T_max:        {p_pred:.6f}")
    print(f"Empirical escape prob (far well):    {p_emp_far:.6f}")
    print(f"Empirical escape prob (barrier top): {p_emp_barrier:.6f}")
    print("==============================================\n")

if __name__ == "__main__":
    run_benchmark()
