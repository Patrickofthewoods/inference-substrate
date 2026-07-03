import random
import math
import matplotlib.pyplot as plt
import os

# 1. Single-run simulation
def single_run(n, k):
    successful_transitions = 0
    for _ in range(n):
        if random.random() < k:
            successful_transitions += 1
    return (successful_transitions % 2 == 1)

# 2. Collapse frequency estimator
def collapse_frequency(n, k, trials=20000):
    count = sum(1 for _ in range(trials) if single_run(n, k))
    return count / trials

# 3. Parameters
k = 0.15
max_n = 50
trials = 20000

xs_empirical, ys_empirical = [], []
xs_analytic, ys_analytic = [], []

# 4. Compute empirical and analytic values
slope = math.log(1 - 2*k)

for n in range(1, max_n + 1):
    # Analytic
    xs_analytic.append(n)
    ys_analytic.append(n * slope)
    
    # Empirical
    p = collapse_frequency(n, k, trials)
    value = 1 - 2*p
    if value > 0:  # Guard against math domain error (log of zero/negative)
        xs_empirical.append(n)
        ys_empirical.append(math.log(value))

# 5. Plotting
plt.figure(figsize=(10, 6))

# Analytic line (smooth) + dots
plt.plot(xs_analytic, ys_analytic, '-', color='red')
plt.plot(xs_analytic, ys_analytic, 'o', color='red', label='Analytic straight line')

# Empirical dots
plt.plot(xs_empirical, ys_empirical, 'o', color='blue', label='Empirical simulation')

plt.xlabel('n (chain length)')
plt.ylabel('log(1 - 2*p)')
plt.title('Parity Plot Overlay (k = 0.15)')
plt.grid(True)
plt.legend()

# 6. Save PNG directly to your Desktop
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'parity_plot_overlay.png')
plt.savefig(desktop_path, dpi=300, bbox_inches='tight')
print(f"SUCCESS! Plot saved directly to: {desktop_path}")
