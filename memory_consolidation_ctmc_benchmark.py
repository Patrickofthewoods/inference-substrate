import numpy as np

def run_ctmc_memory_consolidation(
    T=10.0,
    dt=0.001,
    n_trajectories=20000,
    seed=123
):
    """
    Three-state CTMC memory model:
      N: not encoded / forgotten
      S: short-term memory
      L: long-term memory

    Transitions:
      N -> S : initial encoding
      S -> L : consolidation
      S -> N : forgetting
      L -> S : rare destabilization
    """

    rng = np.random.default_rng(seed)

    # State indices
    N, S, L = 0, 1, 2

    # Transition rates (you can tune these)
    lambda_NS = 1.0   # N -> S (encoding)
    lambda_SL = 0.3   # S -> L (consolidation)
    lambda_SN = 0.5   # S -> N (forgetting)
    lambda_LS = 0.05  # L -> S (destabilization)

    # Rate matrix Q
    Q = np.array([
        [-lambda_NS,          lambda_NS,              0.0        ],  # N
        [ lambda_SN, -(lambda_SN + lambda_SL),       lambda_SL  ],  # S
        [ 0.0,               lambda_LS,        -lambda_LS       ]   # L
    ])

    # Precompute transition probabilities for small dt
    P = np.eye(3) + Q * dt

    # Ensure no negative probabilities due to discretization
    P = np.clip(P, 0.0, 1.0)
    # Renormalize rows
    P = P / P.sum(axis=1, keepdims=True)

    n_steps = int(T / dt)

    # Start all trajectories in N (not encoded)
    states = np.full(n_trajectories, N, dtype=int)

    for _ in range(n_steps):
        # For each trajectory, sample next state from row P[current_state]
        probs = P[states]  # shape (n_trajectories, 3)
        # Sample next state using multinomial over 3 states
        # We do this by cumulative sums + uniform random
        u = rng.random(n_trajectories)
        cum = np.cumsum(probs, axis=1)
        # argmax over cum >= u
        next_states = (u[:, None] <= cum).argmax(axis=1)
        states = next_states

    # Empirical probabilities at time T
    p_N = np.mean(states == N)
    p_S = np.mean(states == S)
    p_L = np.mean(states == L)

    return T, p_N, p_S, p_L


if __name__ == "__main__":
    T, p_N, p_S, p_L = run_ctmc_memory_consolidation(
        T=10.0,
        dt=0.001,
        n_trajectories=20000,
        seed=123
    )

    print("=== Memory Consolidation CTMC Benchmark ===")
    print(f"Time horizon T:                 {T:6.3f}")
    print(f"Empirical P(N  at T) (forgot):  {p_N:8.6f}")
    print(f"Empirical P(S  at T) (short):   {p_S:8.6f}")
    print(f"Empirical P(L  at T) (long):    {p_L:8.6f}")
    print("===========================================")
