"""
Erlang-B loss system: discrete-event simulation validated against the
analytical model, demonstrating the PASTA property (call blocking == q(C)).
"""

import random


import heapq

from dataclasses import dataclass
from utils.exponential_interarrivals import exponential_interarrivals


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

    # How much time the system spends in each state: initialise it based on the states it will have
    time_in_state = [0.0] * (capacity + 1) # [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    last_event_time = 0.0

    event_list = []
    random.seed(seed)
    heapq.heappush(event_list, (exponential_interarrivals(arrival_rate), "arrival"))

    while event_list:
        now, event_type = heapq.heappop(event_list)

        # credit the elapsed interval to whichever state we were in (post warm-up)
        if arrivals_generated > warmup_calls:
            time_in_state[busy_servers] += (now - last_event_time)
        last_event_time = now
    

        if event_type == "arrival":
            arrivals_generated += 1
            if arrivals_generated > total_arrivals_needed:
                break

            heapq.heappush(event_list,
                           (now + exponential_interarrivals(arrival_rate), "arrival"))

            accepted = busy_servers < capacity
            if accepted:
                busy_servers += 1
                heapq.heappush(event_list,
                               (now + exponential_interarrivals(service_rate), "departure"))

            if arrivals_generated > warmup_calls:
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
    # normalise: what proportion of the total time was spent in each state
    q = [ts / total_time for ts in time_in_state] # divide each state's time by the total time

    call_blocking = blocked_count / counted
    avg_busy = sum(j * q[j] for j in range(capacity + 1)) # average of busy servers in each state
    utilization = avg_busy / capacity
    return RunResult(q=q, call_blocking=call_blocking, utilization=utilization)




