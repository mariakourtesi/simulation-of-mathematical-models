import statistics
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from sim_erlang_b import run_simulation
from utils.stats import summary_stats

# --------------------------------------------------------------------------
# Replication across seeds
# --------------------------------------------------------------------------

def _run_one(seed, sim_kwargs):
    """Top-level helper so it can be pickled and sent to a worker process."""
    start = time.perf_counter()
    result = run_simulation(seed=seed, **sim_kwargs)
    elapsed = time.perf_counter() - start
    return seed, result, elapsed


def replicate(seeds, verbose=True, workers=None, **sim_kwargs):
    """Run the simulation once per seed, in parallel across processes, and aggregate the results."""

    overall_start = time.perf_counter()
    results_by_seed = {}

    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(_run_one, s, sim_kwargs): s for s in seeds}

        for i, future in enumerate(as_completed(futures), start=1):
            seed, result, elapsed = future.result()
            results_by_seed[seed] = result

            if verbose:
                total = time.perf_counter() - overall_start
                print(f"[{i:>2}/{len(seeds)}] seed {seed:>3} done  "
                      f"blocking={result.call_blocking:.7f}  "
                      f"({elapsed:5.1f}s this run, {total:6.1f}s total)", flush=True)

    # Reassemble in the caller's original seed order (order doesn't affect the
    # aggregate stats, just keeps output reproducible).
    runs = [results_by_seed[s] for s in seeds]

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