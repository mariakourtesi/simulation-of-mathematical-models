import random


def exponential_interarrivals(rate):
    """Generate the exponential interarrival times, the gap between calls."""
    return random.expovariate(rate)