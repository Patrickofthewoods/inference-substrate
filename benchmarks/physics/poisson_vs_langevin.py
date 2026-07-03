import numpy as np
import time

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

            if x < x_target:   # committed transition
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

            if x < barrier:    # naive barrier crossing
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
    n_trajectories = 5000

    k_rate = kramers_rate(a, D)

    # Poisson prediction
    p_pred = poisson_escape_prob(k_rate, T_max)

    # Far-well committed transitions
    p_emp_far = simulate_first_passage(a, D, dt, T_max, n_trajectories)

    # Barrier-crossing transitions
    p_emp_barrier = simulate_barrier_crossing(a, D, dt, T_max, n_trajectories)

    print("\n=== Kramers / Poisson vs Langevin Benchmark ===")
    print(f"Kramers escape rate k (1/time):      {k_rate:.6f}")
    print(f"Poisson escape prob by T_max:        {p_pred:.6f}")
    print(f"Empirical escape prob (far well):    {p_emp_far:.6f}")
    print(f"Empirical escape prob (barrier top): {p_emp_barrier:.6f}")
    print("==============================================\n")

if __name__ == "__main__":
    run_benchmark()
