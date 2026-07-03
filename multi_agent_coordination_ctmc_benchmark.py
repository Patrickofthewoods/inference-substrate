import numpy as np

def run_multi_agent_coordination_ctmc(
    T=10.0,
    dt=0.01,
    n_agents=50,
    n_trajectories=5000,
    seed=123
):
    """
    Multi-agent CTMC coordination model with stronger alignment dynamics.
    """

    rng = np.random.default_rng(seed)

    A, B, C = 0, 1, 2
    n_steps = int(T / dt)

    majority_A = 0
    majority_B = 0
    majority_none = 0

    for _ in range(n_trajectories):

        # Start neutral
        states = np.full(n_agents, C, dtype=int)

        for _ in range(n_steps):

            count_A = np.sum(states == A)
            count_B = np.sum(states == B)
            count_C = np.sum(states == C)

            # Determine majority
            if count_A > count_B and count_A > count_C:
                majority = A
            elif count_B > count_A and count_B > count_C:
                majority = B
            else:
                majority = C

            # Stronger alignment dynamics
            align_strength = 0.6
            noise_strength = 0.1

            probs = np.zeros((n_agents, 3))

            for i in range(n_agents):
                s = states[i]

                if majority == C:
                    # No majority: pure noise
                    probs[i] = np.array([1/3, 1/3, 1/3])
                else:
                    # Majority exists
                    p = np.full(3, noise_strength)

                    # Strong pull toward majority
                    p[majority] += align_strength

                    # Slight preference to stay where you are
                    p[s] += 0.2

                    # Normalize
                    p = np.clip(p, 0.0, None)
                    p /= p.sum()

                    probs[i] = p

            # Sample next states
            u = rng.random(n_agents)
            cum = np.cumsum(probs, axis=1)
            next_states = (u[:, None] <= cum).argmax(axis=1)
            states = next_states

        # Final majority check
        count_A = np.sum(states == A)
        count_B = np.sum(states == B)

        if count_A > 0.6 * n_agents and count_A > count_B:
            majority_A += 1
        elif count_B > 0.6 * n_agents and count_B > count_A:
            majority_B += 1
        else:
            majority_none += 1

    return (
        T,
        majority_A / n_trajectories,
        majority_B / n_trajectories,
        majority_none / n_trajectories
    )


if __name__ == "__main__":
    T, pA, pB, pNone = run_multi_agent_coordination_ctmc(
        T=10.0,
        dt=0.01,
        n_agents=50,
        n_trajectories=5000,
        seed=123
    )

    print("=== Multi-Agent Coordination CTMC Benchmark ===")
    print(f"Time horizon T:                     {T:6.3f}")
    print(f"Empirical P(majority A at T):       {pA:8.6f}")
    print(f"Empirical P(majority B at T):       {pB:8.6f}")
    print(f"Empirical P(no strong majority at T):{pNone:8.6f}")
    print("===============================================")
