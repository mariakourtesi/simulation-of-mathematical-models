# Erlang-B Loss System Simulation

A discrete-event simulation (DES) of an Erlang-B (M/M/C/C) loss system, validated
against the analytical Erlang-B formula. It reports the time-based state
distribution q(j), the utilization, and demonstrates the PASTA property (call
blocking equals q(C)), together with a confidence interval computed across
several random seeds.

The project uses only the Python standard library, so there is nothing to
install.

## What it computes

- **Call blocking probability** — the fraction of arriving calls that find all
  servers busy and are lost. Measured by counting arrivals.
- **q(j)** — the fraction of time the system spends with exactly `j` servers
  busy. Measured by time-weighting each state.
- **Utilization** — the time-average number of busy servers divided by capacity.
- **PASTA check** — confirms that call blocking (an arrival-average) matches
  q(C) (a time-average). They are equal because arrivals are Poisson.
- **Confidence interval** — across the seeds, using the Student's t-distribution,
  and a check that the analytical value falls inside it.

## Layout

```
erlang-b/
├── main.py              entry point; parses arguments, runs, reports
├── replication.py       runs one simulation per seed, aggregates results
├── reporting.py         analytical Erlang-B formula + printed report
├── sim_erlang_b.py      the discrete-event simulation itself
├── Dockerfile
└── utils/
    ├── exponential_interarrivals.py   exponential inter-event times
    └── state_distribution.py     analytical q(j) distribution
```

## Run with Docker

Build the image (from inside this `erlang-b/` directory):

```bash
docker build -t erlang-b-sim .
```

Run with the defaults (capacity 5, 10,000,000 calls, 98% confidence):

```bash
docker run --rm erlang-b-sim
```

Override any parameter with flags after the image name:

```bash
docker run --rm erlang-b-sim --calls 1000000
docker run --rm erlang-b-sim --capacity 10 --arrival-rate 8 --service-rate 1
docker run --rm erlang-b-sim --seeds 1 2 3 4 5 --confidence 95
docker run --rm erlang-b-sim --quiet
```

## Run without Docker

Needs Python 3.8 or newer. From inside this directory:

```bash
python main.py --calls 1000000
```

## Options

| Flag             | Meaning                                      | Default                         |
|------------------|----------------------------------------------|---------------------------------|
| `--arrival-rate` | Mean arrivals per unit time (lambda)         | 5                               |
| `--service-rate` | Service completion rate per call (mu)        | 1                               |
| `--capacity`     | Number of servers / capacity (C)             | 5                               |
| `--calls`        | Calls counted per run, after warm-up         | 10000000                        |
| `--seeds`        | Space-separated random seeds (two or more)   | 42 50 58 59 57 38 39 68 28 80   |
| `--confidence`   | Confidence level (90, 95, 98, 99)            | 98                              |
| `--quiet`        | Suppress per-seed progress logging           | off                             |

Note: at least two seeds are required, since a standard deviation and
confidence interval cannot be computed from a single run.

## How the model works

The simulation keeps one state variable, the number of busy servers, and a
time-ordered event queue (a heap) of future arrivals and departures. Each
arrival is accepted if a server is free (and schedules its own departure) or
blocked if all servers are busy. Inter-event times are drawn from an exponential
distribution, which makes the arrival stream Poisson, the assumption the
Erlang-B formula is built on. Running long enough, and averaging across seeds,
the simulated blocking probability converges to the analytical value.