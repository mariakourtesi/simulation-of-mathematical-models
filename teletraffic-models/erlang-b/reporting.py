from math_erlang_b import recurrentErlangformula
from utils.state_distribution import erlang_b_state_distribution
# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------

def report(results, arrival_rate, service_rate, capacity):
    offered_load = arrival_rate / service_rate
    analytical_q = erlang_b_state_distribution(capacity, offered_load)
    analytical_blocking = recurrentErlangformula(capacity, offered_load)
    q_mean = results["q_mean"]

    def row(left, right, lw, rw):
        return f"| {left:<{lw}} | {right:>{rw}} |"

    def rule(lw, rw):
        return "+" + "-" * (lw + 2) + "+" + "-" * (rw + 2) + "+"

    # ---- q(j) state distribution table (three columns) ----
    lw, cw = 8, 14
    top = "+" + "-" * (lw + 2) + "+" + "-" * (cw + 2) + "+" + "-" * (cw + 2) + "+"
    print("q(j): fraction of TIME the system spends with j servers busy")
    print(top)
    print(f"| {'state j':<{lw}} | {'simulated':>{cw}} | {'analytical':>{cw}} |")
    print(top)
    for j in range(capacity + 1):
        print(f"| {j:<{lw}} | {q_mean[j]:>{cw}.7f} | {analytical_q[j]:>{cw}.7f} |")
    print(top)
    print(f"| {'sum':<{lw}} | {sum(q_mean):>{cw}.7f} | {sum(analytical_q):>{cw}.7f} |")
    print(top)
    print()

    # ---- PASTA property table ----
    lw, rw = 40, 11
    print("PASTA property: call blocking (arrival-avg) == q(C) (time-avg)")
    print(rule(lw, rw))
    print(row("quantity", "value", lw, rw))
    print(rule(lw, rw))
    print(row("call blocking (fraction of arrivals)", f"{results['blocking_mean']:.7f}", lw, rw))
    print(row(f"q({capacity}) (fraction of time system full)", f"{q_mean[capacity]:.7f}", lw, rw))
    print(row(f"analytical Erlang-B B({capacity},{offered_load:.0f})", f"{analytical_blocking:.7f}", lw, rw))
    print(rule(lw, rw))
    print()

    # ---- summary statistics table ----
    lw, rw = 28, 24
    print(f"Summary across {results['n']} seeds")
    print(rule(lw, rw))
    print(row("metric", "value", lw, rw))
    print(rule(lw, rw))
    print(row("utilization (avg busy / C)", f"{results['utilization']:.7f}", lw, rw))
    print(row("mean call blocking", f"{results['blocking_mean']:.7f}", lw, rw))
    print(row("standard deviation", f"{results['blocking_stdev']:.7f}", lw, rw))
    print(rule(lw, rw))