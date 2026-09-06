import statistics


def summary_stats(values):
    """Mean and standard deviation of a sample."""
    mean = statistics.mean(values)
    stdev = statistics.stdev(values)
    return mean, stdev