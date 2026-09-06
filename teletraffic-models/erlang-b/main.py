import argparse
from replication import replicate
from reporting import report

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Erlang-B loss-system simulation with PASTA check.")
    parser.add_argument("--arrival-rate", type=float, default=5)
    parser.add_argument("--service-rate", type=float, default=1)
    parser.add_argument("--capacity", type=int, default=5)
    parser.add_argument("--calls", type=int, default=10_000_000)
    parser.add_argument("--seeds", type=int, nargs="+", default=[42,50,58,59,57,38,39,68,28,80])
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    results = replicate(args.seeds, verbose=not args.quiet,
                        num_calls_to_simulate=args.calls, arrival_rate=args.arrival_rate,
                        service_rate=args.service_rate, capacity=args.capacity)
    report(results, args.arrival_rate, args.service_rate, args.capacity)