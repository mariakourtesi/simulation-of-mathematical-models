import random
import math


def exponential_interarrivals(rate):
    """Generate the exponential interarrival times, the gap between calls."""
    return -math.log(random.random()) / rate
