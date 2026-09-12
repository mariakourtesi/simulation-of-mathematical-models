"""
Erlang-B loss system: discrete-event simulation validated against the
analytical model, demonstrating the PASTA property (call blocking == q(C)).
"""

import random
import heapq

from dataclasses import dataclass


# --------------------------------------------------------------------------
# Simulation
# --------------------------------------------------------------------------

@dataclass
class RunResult:
    """Results of a single simulation run."""
    q: list            # simulated fraction of time in each state 0..capacity
    call_blocking: float
    utilization: float


def run_simulation(seed, arrival_rate, service_rate, capacity,
                   num_calls_to_simulate, warmup_fraction=0.05):
    """
    One Erlang-B discrete-event simulation run.

    The first warmup_fraction of calls advance the system state but are
    excluded from all statistics; the loop runs extra arrivals up front so
    that exactly num_calls_to_simulate results are counted.
    """
    busy_servers = 0
    blocked_count = 0
    accepted_count = 0
    arrivals_generated = 0

    warmup_calls = int(warmup_fraction * num_calls_to_simulate)
    total_arrivals_needed = num_calls_to_simulate + warmup_calls

    time_in_state = [0.0] * (capacity + 1)
    last_event_time = 0.0

    # Local bindings: global/attribute lookups are slower than local variable
    # lookups in CPython, and this loop runs tens of millions of times.
    rng = random.Random(seed)
    expo = rng.expovariate
    heappush = heapq.heappush
    heappop = heapq.heappop

    event_list = []
    heappush(event_list, (expo(arrival_rate), "arrival"))

    # arrivals_generated only increases, so once we're past warmup we stay
    # past warmup - track that with a flag instead of re-comparing every event.
    warmed_up = warmup_calls == 0

    while event_list:
        now, event_type = heappop(event_list)

        if warmed_up:
            time_in_state[busy_servers] += (now - last_event_time)
        last_event_time = now

        if event_type == "arrival":
            arrivals_generated += 1
            if arrivals_generated > total_arrivals_needed:
                break

            heappush(event_list, (now + expo(arrival_rate), "arrival"))

            accepted = busy_servers < capacity
            if accepted:
                busy_servers += 1
                heappush(event_list, (now + expo(service_rate), "departure"))

            if not warmed_up and arrivals_generated > warmup_calls:
                warmed_up = True

            if warmed_up:
                if accepted:
                    accepted_count += 1
                else:
                    blocked_count += 1

        elif event_type == "departure":
            busy_servers -= 1

    counted = accepted_count + blocked_count
    if counted == 0:
        raise ValueError("No calls were counted; check warm-up vs total settings.")

    total_time = sum(time_in_state)
    q = [ts / total_time for ts in time_in_state]

    call_blocking = blocked_count / counted
    avg_busy = sum(j * q[j] for j in range(capacity + 1))
    utilization = avg_busy / capacity
    return RunResult(q=q, call_blocking=call_blocking, utilization=utilization)
