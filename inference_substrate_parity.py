import random
import math
import matplotlib.pyplot as plt


# -----------------------------
# Core parameters
# -----------------------------

# Rare-event transition probability per step
k = 0.15

# Number of Monte Carlo trials per chain length
trials = 20000

# Chain lengths from 1 to 40
ns = list(range(1, 41))


# -----------------------------
# Helper: simulate one chain
# -----------------------------

def simulate_chain(n: int, k: float) -> int:
    """
    Simulate a single chain of length n.
    Returns the number of successful transitions (steps where random() < k).
    """
    successful_steps = 0
    for _ in range(n):
        if random.random() < k:
            successful_steps += 1
    return successful_steps


# -----------------------------
# Main simulation
# -----------------------------

analytic_vals = []
empirical_vals = []

# True analytic slope: log(1 - 2k)
analytic_slope = math.log(1 - 2 * k)

for n in ns:
    # Analytic prediction: log(1 - 2p_n) = n * log(1 - 2k)
    analytic_vals.append(n * analytic_slope)

    collapses = 0
    for _ in range(trials):
        successful_steps = simulate_chain(n, k)

        # Collapse occurs if parity of successful steps is odd
        if successful_steps % 2 == 1:
            collapses += 1

    p = collapses / trials
    val = 1 - 2 * p

    if val > 0:
        empirical_vals.append(math.log(val))
    else:
        empirical_vals.append(None)


# -----------------------------
# Plotting
# -----------------------------

plt.figure(figsize=(10, 6))
plt.plot(ns, analytic_vals, 'r-', label='Analytic straight line')
plt.scatter(ns, empirical_vals, c='blue', edgecolors='none', s=25,
            label='Empirical simulation')

plt.xlabel('n (chain length)')
plt.ylabel('log(1 - 2*p)')
plt.title('Inference Substrate Parity Overlay (k = 0.15)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()

plt.savefig('inference_substrate_parity.png', dpi=300)
print("Success: 'inference_substrate_parity.png' has been saved.")
