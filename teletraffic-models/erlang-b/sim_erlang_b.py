import random
import math

import random

def exp_randomVariable(rate):
    return random.expovariate(rate)

def simulate_erlang_b(C, alpha, mean_service_time, sim_time):

    mu = 1.0 / mean_service_time      
    arrival_rate_lam = alpha * mu                 

    t = 0.0
    n_busy = 0
    departures = []

    total_arrivals = 0
    blocked_arrivals = 0

    while t < sim_time:
        # time to next arrival
        t_arrival = t + exp_randomVariable(arrival_rate_lam)

        # next departure time
        if departures:
            t_departure = min(departures)
        else:
            t_departure = float('inf')

        if t_arrival < t_departure:
            # ARRIVAL EVENT
            t = t_arrival
            total_arrivals += 1

            if n_busy < C:
                n_busy += 1
                service_time = exp_randomVariable(mu)
                departures.append(t + service_time)
            else:
                blocked_arrivals += 1
        else:
            # DEPARTURE EVENT
            t = t_departure
            n_busy -= 1
            departures.remove(t_departure)

    return blocked_arrivals / total_arrivals
