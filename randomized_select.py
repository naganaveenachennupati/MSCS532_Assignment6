import random
from typing import List, Optional


def randomized_select(
    values: List[int],
    k: int,
    rng: Optional[random.Random] = None
) -> int:
    """
    Return the k-th smallest element using Randomized Quickselect.

    The value of k uses 1-based indexing:
    k = 1 returns the smallest element.

    Args:
        values: List of integer values.
        k: Desired order statistic using 1-based indexing.
        rng: Optional random number generator for reproducible tests.

    Raises:
        ValueError: If values is empty.
        IndexError: If k is outside the valid range.
    """
    if not values:
        raise ValueError("Cannot select from an empty list.")

    if k < 1 or k > len(values):
        raise IndexError(
            "k must be between 1 and the length of the list."
        )

    if rng is None:
        rng = random.Random()

    if len(values) == 1:
        return values[0]

    pivot = values[rng.randrange(len(values))]

    lower = [value for value in values if value < pivot]
    equal = [value for value in values if value == pivot]
    higher = [value for value in values if value > pivot]

    if k <= len(lower):
        return randomized_select(lower, k, rng)

    if k <= len(lower) + len(equal):
        return pivot

    return randomized_select(
        higher,
        k - len(lower) - len(equal),
        rng
    )


if __name__ == "__main__":
    sample = [12, 3, 5, 7, 4, 19, 26, 7, 3]
    rng = random.Random(532)

    print("Original data:", sample)
    print("3rd smallest:", randomized_select(sample, 3, rng))
    print("5th smallest:", randomized_select(sample, 5, rng))