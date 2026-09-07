
import statistics
from sim_erlang_b import run_simulation
from utils.stats import summary_stats
import time

# --------------------------------------------------------------------------
# Replication across seeds
# --------------------------------------------------------------------------

def replicate(seeds, verbose=True, **sim_kwargs):
    """Run the simulation once per seed and aggregate the results."""

    runs = []

    overall_start = time.perf_counter()

    for i, s in enumerate(seeds, start=1):

        run_start = time.perf_counter()

        result = run_simulation(seed=s, **sim_kwargs)
        runs.append(result)

        if verbose:
            elapsed = time.perf_counter() - run_start
            total = time.perf_counter() - overall_start

            print(f"[{i:>2}/{len(seeds)}] seed {s:>3} done  "
                  
                  f"blocking={result.call_blocking:.7f}  "

                  f"({elapsed:5.1f}s this run, {total:6.1f}s total)", flush=True)
    if verbose:
        print()  # blank line before the report tables - cosmetic use

    capacity = sim_kwargs["capacity"]
    q_mean = [statistics.mean(r.q[j] for r in runs) for j in range(capacity + 1)]
    util_mean = statistics.mean(r.utilization for r in runs)

    blocking_values = [r.call_blocking for r in runs]
    blocking_mean, blocking_stdev = summary_stats(blocking_values)

    return {
    "q_mean": q_mean,
    "utilization": util_mean,
    "blocking_mean": blocking_mean,
    "blocking_stdev": blocking_stdev,
    "n": len(seeds),
}