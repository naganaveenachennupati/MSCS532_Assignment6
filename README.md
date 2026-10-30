# MSCS 532 Assignment 6  
## Medians and Order Statistics & Elementary Data Structures

**Student:** Naga Naveena Chennupati  
**Student ID:** 005063666  
**Course:** MSCS 532 – Algorithms and Data Structures  
**University:** University of the Cumberlands  

---

## Overview

This project implements and analyzes selection algorithms for order statistics along with several elementary data structures in Python.

The assignment is divided into two parts:

1. **Selection Algorithms**
   - Deterministic selection using Median of Medians
   - Randomized selection using Randomized Quickselect
   - Theoretical time and space analysis
   - Empirical runtime comparison across multiple input sizes and distributions

2. **Elementary Data Structures**
   - Arrays and matrices
   - Array-based stack
   - Array-based circular queue
   - Singly linked list
   - Complexity analysis and practical trade-offs

The implementations include explicit edge-case handling, including duplicate values, empty structures, invalid indices, and invalid order-statistic requests.

---

## Project Structure

```text
MSCS532_Assignment6/
│
├── deterministic_select.py
├── randomized_select.py
├── array_matrix.py
├── stack_queue.py
├── linked_list.py
├── test_assignment6.py
├── benchmark_selection.py
├── generate_graphs.py
├── requirements.txt
├── README.md
├── NagaNaveenaChennupati_Assignment6.docx
│
└── results/
    ├── selection_trials.csv
    ├── selection_summary.csv
    ├── random_comparison.png
    ├── sorted_comparison.png
    ├── reverse_sorted_comparison.png
    └── repeated_comparison.png
```

---

# Part 1: Selection Algorithms

## Deterministic Selection — Median of Medians

`deterministic_select.py` implements a deterministic algorithm for finding the **k-th smallest element** in an array.

The implementation uses the Median of Medians strategy:

1. Divide the input into groups of at most five elements.
2. Sort each small group.
3. Collect the median from each group.
4. Recursively select the median of those medians.
5. Use that value as the pivot.
6. Partition the input into values smaller than, equal to, and greater than the pivot.
7. Continue recursively only in the partition containing the requested order statistic.

The implementation uses **1-based indexing for k**. For example, `k = 1` returns the smallest element.

### Example

```python
from deterministic_select import deterministic_select

values = [12, 3, 5, 7, 4, 19, 26]

result = deterministic_select(values, 4)

print(result)
```

Output:

```text
7
```

### Deterministic Complexity

The Median of Medians algorithm guarantees that the pivot provides sufficient progress at every recursive level.

Its recurrence can be expressed approximately as:

```text
T(n) <= T(n/5) + T(7n/10) + O(n)
```

The `T(n/5)` term represents selecting the median of the group medians, while the `T(7n/10)` term represents the largest recursive partition that may remain after partitioning.

Because the recursive subproblems together contain only a fixed fraction of the original input and partitioning requires linear work, the recurrence resolves to:

```text
O(n)
```

in the worst case.

The implementation creates temporary lists during partitioning. Therefore, it uses additional memory compared with an in-place version, while maintaining the required worst-case linear running-time behavior.

---

## Randomized Selection — Randomized Quickselect

`randomized_select.py` implements Randomized Quickselect.

Instead of calculating a deterministic pivot, the algorithm selects a pivot randomly from the current input. It then divides the input into three groups:

- values smaller than the pivot;
- values equal to the pivot;
- values greater than the pivot.

Only the partition containing the requested order statistic is processed recursively.

An optional `random.Random` object can be supplied so tests and benchmarks can be reproduced using fixed seeds.

### Example

```python
import random

from randomized_select import randomized_select

values = [12, 3, 5, 7, 4, 19, 26]
rng = random.Random(532)

result = randomized_select(values, 4, rng)

print(result)
```

Output:

```text
7
```

### Randomized Complexity

Randomized Quickselect has:

- **Expected time:** `O(n)`
- **Worst-case time:** `O(n^2)`

Random pivot selection makes consistently poor partitions unlikely, which leads to linear expected performance.

However, the worst case is still possible if the selected pivots repeatedly create extremely unbalanced partitions.

Because this implementation creates new partition lists, it also requires auxiliary memory. Under typical balanced behavior, the total active temporary storage remains linear in the input size, while unusually unbalanced recursion can increase both recursion depth and temporary storage.

---

## Duplicate Handling

Both selection implementations use three-way partitioning:

```text
lower  = values smaller than pivot
equal  = values equal to pivot
higher = values greater than pivot
```

This allows repeated values to be handled directly and avoids unnecessary recursion when the requested order statistic falls inside the group equal to the pivot.

---

# Empirical Analysis

## Methodology

The deterministic and randomized selection algorithms were compared using four input distributions:

- Random
- Sorted
- Reverse Sorted
- Repeated values

Five input sizes were tested:

```text
100
500
1000
2000
5000
```

Each algorithm was executed **five times for every size and distribution combination**.

The benchmark therefore performed:

```text
4 distributions
× 5 sizes
× 2 algorithms
× 5 trials
= 200 timed runs
```

The requested order statistic was the median position:

```text
k = (n + 1) // 2
```

Runtime was measured using Python's `time.perf_counter_ns()`.

Correctness was validated before each measurement was accepted by comparing the selected value with the corresponding element from Python's sorted result.

Dataset generation, reference sorting, and correctness validation were kept outside the timed selection operation.

The benchmark stores:

- every individual runtime in `results/selection_trials.csv`;
- mean runtime and sample standard deviation in `results/selection_summary.csv`.

---

## Benchmark Results at n = 5000

| Input Distribution | Deterministic Median of Medians | Randomized Quickselect |
|---|---:|---:|
| Random | 5.8384 ms | 2.2337 ms |
| Sorted | 4.3026 ms | 1.7109 ms |
| Reverse Sorted | 6.9600 ms | 1.5107 ms |
| Repeated | 2.2452 ms | 1.0677 ms |

---

## Observed Results

### Random Input

Both algorithms showed efficient growth as the input size increased.

At `n = 5000`, deterministic selection averaged **5.8384 ms**, while Randomized Quickselect averaged **2.2337 ms**.

Randomized Quickselect was faster in this experiment because selecting a random pivot has less computational overhead than constructing the Median of Medians pivot.

---

### Sorted Input

The deterministic algorithm remained linear and was not harmed by the already sorted input.

At `n = 5000`:

```text
Deterministic: 4.3026 ms
Randomized:    1.7109 ms
```

Randomized selection was again faster in the measured trials.

Unlike a fixed-endpoint Quickselect strategy, randomized pivot selection does not systematically choose the smallest or largest element simply because the input is sorted.

---

### Reverse-Sorted Input

Reverse-sorted input produced the largest deterministic runtime among the four tested distributions at `n = 5000`.

The measured averages were:

```text
Deterministic: 6.9600 ms
Randomized:    1.5107 ms
```

Even though the deterministic implementation was slower, Median of Medians still preserves its worst-case linear-time guarantee.

Randomized Quickselect performed substantially faster in these experiments, but its theoretical worst case remains quadratic.

---

### Repeated Values

Repeated-value inputs were included to test both practical performance and duplicate handling.

At `n = 5000`:

```text
Deterministic: 2.2452 ms
Randomized:    1.0677 ms
```

Both implementations performed efficiently because the three-way partition can place many elements in the `equal` partition at once.

---

## Empirical Interpretation

The results demonstrate an important difference between theoretical guarantees and practical runtime.

Median of Medians provides a strong **worst-case `O(n)` guarantee**, but finding the median-based pivot requires additional computation.

Randomized Quickselect provides **expected `O(n)` performance** and was faster in every tested distribution in this experiment because its pivot-selection procedure has lower overhead.

The empirical results do not prove asymptotic complexity by themselves. They provide practical evidence that is consistent with the theoretical behavior and illustrate the constant-factor cost associated with the deterministic worst-case guarantee.

---

# Performance Visualizations

The `results` directory contains four runtime comparison graphs:

- `random_comparison.png`
- `sorted_comparison.png`
- `reverse_sorted_comparison.png`
- `repeated_comparison.png`

Each graph shows the mean runtime across five trials and includes standard-deviation error bars.

---

# Part 2: Elementary Data Structures

## Arrays

`array_matrix.py` includes a `DynamicArray` implementation supporting:

- append;
- insertion by index;
- deletion by index;
- indexed access;
- length;
- retrieval of stored values.

### Complexity

| Operation | Time Complexity |
|---|---:|
| Indexed access | `O(1)` |
| Append | Amortized `O(1)` |
| Insert at arbitrary index | `O(n)` |
| Delete at arbitrary index | `O(n)` |

Indexed access is constant time, while insertion and deletion can require shifting elements.

---

# Matrices

The `Matrix` class represents a two-dimensional structure using nested arrays.

Supported operations include:

- value insertion/update;
- deletion by resetting a position;
- indexed access;
- bounds validation;
- returning matrix contents.

For a fixed matrix position, access and update are constant-time operations.

| Operation | Time Complexity |
|---|---:|
| Access | `O(1)` |
| Insert/update | `O(1)` |
| Delete/reset | `O(1)` |

---

# Array-Based Stack

`stack_queue.py` includes an `ArrayStack` implementation.

Supported operations include:

- `push`
- `pop`
- `peek`
- `is_empty`
- `size`

The stack follows **LIFO — Last In, First Out** behavior.

### Complexity

| Operation | Time Complexity |
|---|---:|
| Push | Amortized `O(1)` |
| Pop | `O(1)` |
| Peek | `O(1)` |
| Size | `O(1)` |
| Empty check | `O(1)` |

Stacks are useful in situations such as function-call management, expression evaluation, undo operations, and depth-first traversal.

---

# Array-Based Circular Queue

The `ArrayQueue` implementation uses a circular dynamic array.

Supported operations include:

- `enqueue`
- `dequeue`
- `peek`
- `is_empty`
- `size`
- automatic resizing

The queue follows **FIFO — First In, First Out** behavior.

Instead of removing index 0 and shifting all remaining elements, the queue maintains a front index and wraps around the underlying array.

### Complexity

| Operation | Time Complexity |
|---|---:|
| Enqueue | Amortized `O(1)` |
| Dequeue | `O(1)` |
| Peek | `O(1)` |
| Size | `O(1)` |
| Empty check | `O(1)` |

When the underlying array becomes full, resizing requires `O(n)` time, but because resizing occurs only occasionally, enqueue remains amortized `O(1)`.

Queues are commonly used for task scheduling, request processing, buffering, and breadth-first traversal.

---

# Singly Linked List

`linked_list.py` implements a singly linked list using `Node` objects.

Supported operations include:

- insertion at the beginning;
- insertion at the end;
- insertion at a specified index;
- deletion of the first matching value;
- indexed access;
- traversal;
- size tracking;
- empty-state checking.

### Complexity

| Operation | Time Complexity |
|---|---:|
| Insert at beginning | `O(1)` |
| Insert at end | `O(n)` |
| Insert at arbitrary index | `O(n)` |
| Delete by value | `O(n)` |
| Indexed access | `O(n)` |
| Traversal | `O(n)` |

The current implementation does not maintain a tail pointer, so inserting at the end requires traversal from the head.

---

# Arrays vs. Linked Lists

Arrays and linked lists offer different performance characteristics.

Arrays provide efficient `O(1)` indexed access and usually good memory locality. However, inserting or deleting elements in the middle can require shifting many elements.

Linked lists do not require elements to occupy contiguous positions and can insert at the beginning in `O(1)` time. However, they require additional memory for node references and do not provide constant-time indexed access.

For a stack, an array is often convenient because push and pop operations at the end are efficient.

For a queue, a basic array implementation that removes the first element can be inefficient because elements may need to shift. The circular array queue used in this project avoids that problem and provides `O(1)` dequeue operations.

A linked-list queue could also support `O(1)` enqueue and dequeue operations if both head and tail references were maintained, although each node would require additional reference storage.

The preferred structure therefore depends on the required operations, memory considerations, access patterns, and implementation complexity.

---

# Practical Applications

## Arrays and Matrices

Arrays are useful when data needs frequent indexed access, such as lookup tables, collections of measurements, and numerical processing.

Matrices are commonly used for tabular data, image representations, graph adjacency matrices, scientific calculations, and numerical computing.

## Stacks

Stacks are useful for:

- function calls;
- expression parsing;
- undo/redo behavior;
- backtracking;
- depth-first search.

## Queues

Queues are useful for:

- task scheduling;
- print queues;
- message processing;
- network buffering;
- breadth-first search.

## Linked Lists

Linked lists can be useful when data changes dynamically and sequential traversal is more important than direct indexed access. Examples include maintaining ordered sequences, implementing certain queues or stacks, and representing relationships in more advanced structures.

---

# Testing and Validation

Automated testing is provided in:

```text
test_assignment6.py
```

The final test suite contains **55 tests**.

The tests cover:

- deterministic selection;
- randomized selection;
- duplicate values;
- all-equal values;
- negative numbers;
- sorted input;
- reverse-sorted input;
- large random inputs;
- invalid `k` values;
- empty input;
- array insertion, deletion, and access;
- matrix operations and invalid positions;
- stack LIFO behavior and underflow;
- queue FIFO behavior;
- circular wraparound;
- queue resizing;
- queue wraparound followed by resizing;
- linked-list insertion;
- linked-list deletion;
- traversal;
- indexed access;
- empty and invalid-index cases.

Final verification:

```text
Ran 55 tests in 0.013s

OK
```

---

# How to Run the Project

## 1. Requirements

Python 3 is required.

Install the graphing dependency with:

```bash
pip install -r requirements.txt
```

---

## 2. Run Deterministic Selection

```bash
python deterministic_select.py
```

---

## 3. Run Randomized Selection

```bash
python randomized_select.py
```

---

## 4. Run Array and Matrix Demonstration

```bash
python array_matrix.py
```

---

## 5. Run Stack and Queue Demonstration

```bash
python stack_queue.py
```

---

## 6. Run Linked List Demonstration

```bash
python linked_list.py
```

---

## 7. Run All Automated Tests

```bash
python -m unittest -v test_assignment6.py
```

Expected final status:

```text
Ran 55 tests in ...
OK
```

---

## 8. Generate Benchmark Results

```bash
python benchmark_selection.py
```

This creates:

```text
results/selection_trials.csv
results/selection_summary.csv
```

---

## 9. Generate Performance Graphs

```bash
python generate_graphs.py
```

This creates:

```text
results/random_comparison.png
results/sorted_comparison.png
results/reverse_sorted_comparison.png
results/repeated_comparison.png
```

---

# Summary of Findings

The project demonstrates that both deterministic and randomized selection algorithms can achieve linear behavior under their respective theoretical guarantees.

The **Median of Medians** approach provides deterministic `O(n)` worst-case selection by ensuring that each pivot removes a meaningful fraction of the remaining input.

**Randomized Quickselect** provides expected `O(n)` time with a simpler pivot-selection process, although its theoretical worst case remains `O(n^2)`.

In the empirical study, Randomized Quickselect was faster than the deterministic implementation across all tested sizes and distributions. This illustrates the practical cost of the stronger worst-case guarantee provided by Median of Medians.

The elementary data-structure implementations also demonstrate that no single structure is optimal for every use case. Arrays offer direct indexed access, linked lists provide flexible node-based organization, stacks support LIFO processing, and queues support FIFO processing. Appropriate structure selection depends on the operations performed most frequently, memory requirements, and application needs.

---

# Final Report

The detailed Assignment 6 report is included as:

```text
NagaNaveenaChennupati_Assignment6.docx
```

It contains the implementation discussion, theoretical analysis, empirical results, performance visualizations, elementary data-structure analysis, practical applications, testing discussion, limitations, and conclusion.