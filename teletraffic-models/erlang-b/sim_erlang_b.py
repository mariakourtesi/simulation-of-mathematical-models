import random
import math
import heapq

from math_erlang_b import recurrentErlangformula

   
arrival_rate = 5 # rate of arrivals per minute
service_rate = 1 # rate of departures per minute
capacity = 5

busy = 0
blocked_count = 0

accepted_count = 0
arrivals_generated = 0

num_calls_to_simulate = 1_000_000
warmup_calls = int(0.10 * num_calls_to_simulate)   # first 5%, discard from stats


event_list = []

random.seed(42) 

# Step 1: first call arrives
first_arrival_time = -math.log(random.random()) / arrival_rate
heapq.heappush(event_list, (first_arrival_time, "arrival"))

while event_list:
    time, event_type = heapq.heappop(event_list)

    print("time", time)
    print("event_type", event_type)


    if event_type == "arrival":
        arrivals_generated += 1
        if arrivals_generated > num_calls_to_simulate:
            break

        # schedule the NEXT arrival regardless of what happens to this one
        next_arrival_time = time + (-math.log(random.random()) / arrival_rate)
        heapq.heappush(event_list, (next_arrival_time, "arrival"))

        accepted = busy < capacity

        if accepted:
            # accept the call
            busy += 1
            # accepted_count += 1
            service_time = -math.log(random.random()) / service_rate
            departure_time = time + service_time
            heapq.heappush(event_list, (departure_time, "departure"))

        if arrivals_generated > warmup_calls:   # <- only count post-warm-up
            if accepted:
                accepted_count += 1
            else:
                blocked_count += 1

    elif event_type == "departure":
        busy -= 1

print("accepted:", accepted_count)
print("blocked:", blocked_count)
print("Simulation blocking probability:", blocked_count / (accepted_count + blocked_count))


mathematicalModel = recurrentErlangformula(capacity, arrival_rate/service_rate)
print("analytical model CBP", mathematicalModel)