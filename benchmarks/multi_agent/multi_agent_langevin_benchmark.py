import numpy as np

def multi_agent_langevin_triple_well(
    T=10.0,
    dt=0.001,
    n_agents=20,
    n_trajectories=5000,
    seed=123
):
    """
    Multi-agent Langevin dynamics in a shared triple-well potential
    with weak coupling toward the mean position.
    """

    rng = np.random.default_rng(seed)

    n_steps = int(T / dt)

    # Potential: triple well (one deep, two shallow)
    def V(x):
        # Example: asymmetric triple well
        return x**6 - 3*x**4 + 2*x**2 - 0.5*x

    def dVdx(x):
        return 6*x**5 - 12*x**3 + 4*x - 0.5

    # Noise strength
    sigma = 0.5

    # Coupling strength toward mean
    k_couple = 0.2

    # Counters for where the collective ends up
    deep_count = 0
    shallow_left_count = 0
    shallow_right_count = 0

    for _ in range(n_trajectories):
        # Initialize agents near 0
        x = rng.normal(loc=0.0, scale=0.5, size=n_agents)

        for _ in range(n_steps):
            # Compute mean position
            x_mean = np.mean(x)

            # Gradient of potential
            grad = dVdx(x)

            # Coupling term: pull toward mean
            coupling = -k_couple * (x - x_mean)

            # Langevin update
            noise = sigma * np.sqrt(dt) * rng.normal(size=n_agents)
            x = x - grad * dt + coupling * dt + noise

        # At time T, look at mean position
        x_mean = np.mean(x)

        # Classify which well the collective mean is in
        if x_mean < -1.0:
            shallow_left_count += 1
        elif x_mean > 1.0:
            shallow_right_count += 1
        else:
            deep_count += 1

    p_deep = deep_count / n_trajectories
    p_shallow_left = shallow_left_count / n_trajectories
    p_shallow_right = shallow_right_count / n_trajectories

    return T, p_deep, p_shallow_left, p_shallow_right


if __name__ == "__main__":
    T, p_deep, p_left, p_right = multi_agent_langevin_triple_well(
        T=10.0,
        dt=0.001,
        n_agents=20,
        n_trajectories=5000,
        seed=123
    )

    print("=== Multi-Agent Triple-Well Langevin Benchmark ===")
    print(f"Time horizon T:                     {T:6.3f}")
    print(f"Empirical P(deep well at T):        {p_deep:8.6f}")
    print(f"Empirical P(shallow left well at T):{p_left:8.6f}")
    print(f"Empirical P(shallow right well at T):{p_right:8.6f}")
    print("===============================================")
