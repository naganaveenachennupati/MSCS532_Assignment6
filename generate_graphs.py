import csv
from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt


RESULTS_DIR = Path("results")
SUMMARY_FILE = RESULTS_DIR / "selection_summary.csv"

DISTRIBUTIONS = [
    "Random",
    "Sorted",
    "Reverse Sorted",
    "Repeated",
]


def load_summary() -> List[Dict[str, str]]:
    """Load summarized benchmark results from CSV."""
    with SUMMARY_FILE.open(
        "r",
        newline="",
        encoding="utf-8"
    ) as csv_file:
        reader = csv.DictReader(csv_file)
        return list(reader)


def create_graph(
    rows: List[Dict[str, str]],
    distribution: str,
    output_filename: str
) -> None:
    """Create a performance comparison graph for one distribution."""
    distribution_rows = [
        row
        for row in rows
        if row["distribution"] == distribution
    ]

    deterministic_rows = sorted(
        [
            row
            for row in distribution_rows
            if row["algorithm"] == "Deterministic"
        ],
        key=lambda row: int(row["size"])
    )

    randomized_rows = sorted(
        [
            row
            for row in distribution_rows
            if row["algorithm"] == "Randomized"
        ],
        key=lambda row: int(row["size"])
    )

    sizes = [
        int(row["size"])
        for row in deterministic_rows
    ]

    deterministic_means = [
        float(row["mean_time_ms"])
        for row in deterministic_rows
    ]

    deterministic_std = [
        float(row["std_dev_ms"])
        for row in deterministic_rows
    ]

    randomized_means = [
        float(row["mean_time_ms"])
        for row in randomized_rows
    ]

    randomized_std = [
        float(row["std_dev_ms"])
        for row in randomized_rows
    ]

    plt.figure(figsize=(8, 5))

    plt.errorbar(
        sizes,
        deterministic_means,
        yerr=deterministic_std,
        marker="o",
        capsize=4,
        label="Deterministic Median of Medians"
    )

    plt.errorbar(
        sizes,
        randomized_means,
        yerr=randomized_std,
        marker="o",
        capsize=4,
        label="Randomized Quickselect"
    )

    plt.title(
        f"Selection Algorithm Performance - {distribution} Input"
    )
    plt.xlabel("Input Size (n)")
    plt.ylabel("Mean Runtime (ms)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_path = RESULTS_DIR / output_filename
    plt.savefig(output_path, dpi=200)
    plt.close()

    print(f"Created: {output_path}")


def main() -> None:
    """Generate all performance graphs from the locked benchmark results."""
    if not SUMMARY_FILE.exists():
        raise FileNotFoundError(
            "selection_summary.csv was not found. "
            "Run benchmark_selection.py first."
        )

    rows = load_summary()

    graph_files = {
        "Random": "random_comparison.png",
        "Sorted": "sorted_comparison.png",
        "Reverse Sorted": "reverse_sorted_comparison.png",
        "Repeated": "repeated_comparison.png",
    }

    for distribution in DISTRIBUTIONS:
        create_graph(
            rows,
            distribution,
            graph_files[distribution]
        )

    print()
    print("All performance graphs generated successfully.")


if __name__ == "__main__":
    main()