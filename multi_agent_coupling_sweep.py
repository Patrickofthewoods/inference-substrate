import numpy as np

def multi_agent_langevin(
    T=10.0,
    dt=0.001,
    n_agents=20,
    n_trajectories=2000,
    k_couple=0.2,
    seed=123
):
    rng = np.random.default_rng(seed)
    n_steps = int(T / dt)

    # Triple-well potential
    def V(x):
        return x**6 - 3*x**4 + 2*x**2 - 0.5*x

    def dVdx(x):
        return 6*x**5 - 12*x**3 + 4*x - 0.5

    sigma = 0.5  # noise strength

    deep = 0
    left = 0
    right = 0

    for _ in range(n_trajectories):
        x = rng.normal(0.0, 0.5, size=n_agents)

        for _ in range(n_steps):
            x_mean = np.mean(x)
            grad = dVdx(x)
            coupling = -k_couple * (x - x_mean)
            noise = sigma * np.sqrt(dt) * rng.normal(size=n_agents)
            x = x - grad * dt + coupling * dt + noise

        xm = np.mean(x)
        if xm < -1.0:
            left += 1
        elif xm > 1.0:
            right += 1
        else:
            deep += 1

    return deep/n_trajectories, left/n_trajectories, right/n_trajectories


if __name__ == "__main__":
    ks = [0.00, 0.05, 0.10, 0.20, 0.30, 0.50, 1.00]

    print("=== Coupling Strength Sweep ===")
    for k in ks:
        p_deep, p_left, p_right = multi_agent_langevin(k_couple=k)
        print(f"k={k:4.2f} | deep={p_deep:.4f} | left={p_left:.4f} | right={p_right:.4f}")
