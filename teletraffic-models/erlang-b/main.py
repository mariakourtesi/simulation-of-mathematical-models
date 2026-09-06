from replication import replicate
from reporting import report


if __name__ == "__main__":
    ARRIVAL_RATE = 5
    SERVICE_RATE = 1
    CAPACITY = 5
    SEEDS = [42, 50, 58, 59, 57, 38, 39, 68, 28, 80]
    NUM_CALLS_TO_SIMULATE = 10_000_000

    results = replicate(
        SEEDS,
        confidence=0.98,
        num_calls_to_simulate= NUM_CALLS_TO_SIMULATE,
        arrival_rate=ARRIVAL_RATE,
        service_rate=SERVICE_RATE,
        capacity=CAPACITY,
    )
    report(results, ARRIVAL_RATE, SERVICE_RATE, CAPACITY)