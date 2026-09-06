# --------------------------------------------------------------------------
# Analytical model
# --------------------------------------------------------------------------

def erlang_b_state_distribution(capacity, offered_load):
    """
    Analytical time-stationary state distribution q(j) for an M/M/c/c
    (Erlang-B) loss system: the probability of exactly j busy servers.

        q(j) = (A^j / j!) / sum_{k=0..c} (A^k / k!)

    Returns [q(0), ..., q(capacity)], summing to 1. q(capacity) equals the
    Erlang-B blocking probability B(c, A).
    """
    terms = [1.0]  # A^0 / 0! = 1
    for j in range(1, capacity + 1):
        terms.append(terms[-1] * offered_load / j)  # A^j / j!, built incrementally
    total = sum(terms)
    return [t / total for t in terms]
