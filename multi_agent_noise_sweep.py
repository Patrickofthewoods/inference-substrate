import numpy as np

def multi_agent_langevin_noise(
    T=10.0,
    dt=0.001,
    n_agents=20,
    n_trajectories=2000,
    sigma=0.5,
    k_couple=0.2,
    seed=123
):
    rng = np.random.default_rng(seed)
    n_steps = int(T / dt)

    # Triple-well potential
    def dVdx(x):
        return 6*x**5 - 12*x**3 + 4*x - 0.5

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
    sigmas = [0.1, 0.25, 0.5, 0.75, 1.0]

    print("=== Noise Strength Sweep ===")
    for s in sigmas:
        p_deep, p_left, p_right = multi_agent_langevin_noise(sigma=s)
        print(f"sigma={s:4.2f} | deep={p_deep:.4f} | left={p_left:.4f} | right={p_right:.4f}")
