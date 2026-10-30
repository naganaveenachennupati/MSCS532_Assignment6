from typing import List


def insertion_sort(values: List[int]) -> List[int]:
    """Return a sorted copy of a small list using insertion sort."""
    result = values.copy()

    for i in range(1, len(result)):
        key = result[i]
        j = i - 1

        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1

        result[j + 1] = key

    return result


def choose_pivot(values: List[int]) -> int:
    """
    Choose a pivot using the Median of Medians strategy.

    The input is divided into groups of at most five elements.
    Each group is sorted, its median is collected, and the
    median of those medians is selected recursively.
    """
    if len(values) <= 5:
        sorted_values = insertion_sort(values)
        return sorted_values[len(sorted_values) // 2]

    medians = []

    for i in range(0, len(values), 5):
        group = values[i:i + 5]
        sorted_group = insertion_sort(group)
        medians.append(sorted_group[len(sorted_group) // 2])

    return deterministic_select(
        medians,
        (len(medians) + 1) // 2
    )


def deterministic_select(values: List[int], k: int) -> int:
    """
    Return the k-th smallest element using Median of Medians.

    The value of k uses 1-based indexing:
    k = 1 returns the smallest element.

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

    if len(values) == 1:
        return values[0]

    pivot = choose_pivot(values)

    lower = [value for value in values if value < pivot]
    equal = [value for value in values if value == pivot]
    higher = [value for value in values if value > pivot]

    if k <= len(lower):
        return deterministic_select(lower, k)

    if k <= len(lower) + len(equal):
        return pivot

    return deterministic_select(
        higher,
        k - len(lower) - len(equal)
    )


if __name__ == "__main__":
    sample = [12, 3, 5, 7, 4, 19, 26, 7, 3]

    print("Original data:", sample)
    print("3rd smallest:", deterministic_select(sample, 3))
    print("5th smallest:", deterministic_select(sample, 5))