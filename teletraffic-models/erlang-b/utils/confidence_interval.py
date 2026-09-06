import statistics
import math
from scipy import stats

# --------------------------------------------------------------------------
# Replication across seeds
# --------------------------------------------------------------------------

def confidence_interval(values, confidence):
    """
    Mean and (lower, upper) CI for a small sample, using the Student's
    t-distribution (correct when the standard deviation is estimated from
    the sample rather than known).
    """
    n = len(values)
    mean = statistics.mean(values)
    stdev = statistics.stdev(values)
    standard_error = stdev / math.sqrt(n)
    # two-sided: split the remaining tail probability across both ends
    t_mult = stats.t.ppf(1 - (1 - confidence) / 2, df=n - 1)
    margin = t_mult * standard_error
    return mean, stdev, (mean - margin, mean + margin)


