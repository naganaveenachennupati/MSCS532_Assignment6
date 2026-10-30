import csv
import random
import statistics
import time
from pathlib import Path
from typing import Callable, Dict, List, Tuple

from deterministic_select import deterministic_select
from randomized_select import randomized_select


SIZES = [100, 500, 1000, 2000, 5000]
TRIALS = 5
BASE_SEED = 532

RESULTS_DIR = Path("results")
TRIALS_FILE = RESULTS_DIR / "selection_trials.csv"
SUMMARY_FILE = RESULTS_DIR / "selection_summary.csv"


def generate_dataset(
    distribution: str,
    size: int,
    seed: int
) -> List[int]:
    """Generate a dataset for one benchmark trial."""
    rng = random.Random(seed)

    if distribution == "Random":
        return [
            rng.randint(-10 * size, 10 * size)
            for _ in range(size)
        ]

    if distribution == "Sorted":
        return list(range(size))

    if distribution == "Reverse Sorted":
        return list(range(size - 1, -1, -1))

    if distribution == "Repeated":
        return [
            rng.randint(0, 9)
            for _ in range(size)
        ]

    raise ValueError(f"Unknown distribution: {distribution}")


def run_deterministic(values: List[int], k: int, seed: int) -> int:
    """Run deterministic Median of Medians selection."""
    return deterministic_select(values, k)


def run_randomized(values: List[int], k: int, seed: int) -> int:
    """Run Randomized Quickselect with a reproducible seed."""
    rng = random.Random(seed)
    return randomized_select(values, k, rng)


def time_selection(
    algorithm: Callable[[List[int], int, int], int],
    values: List[int],
    k: int,
    seed: int
) -> Tuple[int, int]:
    """
    Time one selection operation.

    Returns:
        selected_value: The k-th smallest value.
        elapsed_ns: Runtime in nanoseconds.
    """
    start = time.perf_counter_ns()

    selected_value = algorithm(values, k, seed)

    end = time.perf_counter_ns()

    return selected_value, end - start


def main() -> None:
    """Run all empirical selection benchmarks."""
    RESULTS_DIR.mkdir(exist_ok=True)

    algorithms: Dict[
        str,
        Callable[[List[int], int, int], int]
    ] = {
        "Deterministic": run_deterministic,
        "Randomized": run_randomized,
    }

    distributions = [
        "Random",
        "Sorted",
        "Reverse Sorted",
        "Repeated",
    ]

    trial_rows = []

    print("Running Assignment 6 selection benchmarks...")
    print()

    for distribution_index, distribution in enumerate(distributions):
        for size in SIZES:
            # Use the median order statistic for the comparison.
            k = (size + 1) // 2

            for trial in range(1, TRIALS + 1):
                data_seed = (
                    BASE_SEED
                    + distribution_index * 100000
                    + size * 10
                    + trial
                )

                values = generate_dataset(
                    distribution,
                    size,
                    data_seed
                )

                # Calculate the expected result outside the timed section.
                expected = sorted(values)[k - 1]

                for algorithm_index, (
                    algorithm_name,
                    algorithm
                ) in enumerate(algorithms.items()):

                    algorithm_seed = (
                        BASE_SEED
                        + distribution_index * 1000000
                        + size * 100
                        + trial * 10
                        + algorithm_index
                    )

                    selected_value, elapsed_ns = time_selection(
                        algorithm,
                        values,
                        k,
                        algorithm_seed
                    )

                    if selected_value != expected:
                        raise AssertionError(
                            f"{algorithm_name} returned "
                            f"{selected_value}, expected {expected}."
                        )

                    elapsed_ms = elapsed_ns / 1_000_000

                    trial_rows.append(
                        {
                            "algorithm": algorithm_name,
                            "distribution": distribution,
                            "size": size,
                            "k": k,
                            "trial": trial,
                            "time_ms": elapsed_ms,
                        }
                    )

    with TRIALS_FILE.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "algorithm",
                "distribution",
                "size",
                "k",
                "trial",
                "time_ms",
            ],
        )

        writer.writeheader()
        writer.writerows(trial_rows)

    summary_rows = []

    for distribution in distributions:
        for size in SIZES:
            for algorithm_name in algorithms:
                times = [
                    row["time_ms"]
                    for row in trial_rows
                    if row["distribution"] == distribution
                    and row["size"] == size
                    and row["algorithm"] == algorithm_name
                ]

                mean_time = statistics.mean(times)

                if len(times) > 1:
                    standard_deviation = statistics.stdev(times)
                else:
                    standard_deviation = 0.0

                summary_rows.append(
                    {
                        "algorithm": algorithm_name,
                        "distribution": distribution,
                        "size": size,
                        "mean_time_ms": mean_time,
                        "std_dev_ms": standard_deviation,
                    }
                )

    with SUMMARY_FILE.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "algorithm",
                "distribution",
                "size",
                "mean_time_ms",
                "std_dev_ms",
            ],
        )

        writer.writeheader()
        writer.writerows(summary_rows)

    print(
        f"{'Distribution':<18}"
        f"{'Size':>8}"
        f"{'Algorithm':>16}"
        f"{'Mean (ms)':>14}"
        f"{'Std Dev':>14}"
    )

    print("-" * 70)

    for row in summary_rows:
        print(
            f"{row['distribution']:<18}"
            f"{row['size']:>8}"
            f"{row['algorithm']:>16}"
            f"{row['mean_time_ms']:>14.4f}"
            f"{row['std_dev_ms']:>14.4f}"
        )

    print()
    print(f"Detailed trial results saved to: {TRIALS_FILE}")
    print(f"Summary results saved to: {SUMMARY_FILE}")
    print(
        f"Completed {len(trial_rows)} timed selection runs successfully."
    )


if __name__ == "__main__":
    main()