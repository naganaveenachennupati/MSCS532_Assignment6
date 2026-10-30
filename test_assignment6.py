import random
import unittest

from array_matrix import DynamicArray, Matrix
from deterministic_select import deterministic_select
from linked_list import SinglyLinkedList
from randomized_select import randomized_select
from stack_queue import ArrayQueue, ArrayStack


class TestDeterministicSelect(unittest.TestCase):

    def test_single_element(self):
        self.assertEqual(deterministic_select([42], 1), 42)

    def test_smallest_element(self):
        self.assertEqual(deterministic_select([9, 2, 7, 1, 5], 1), 1)

    def test_largest_element(self):
        self.assertEqual(deterministic_select([9, 2, 7, 1, 5], 5), 9)

    def test_middle_element(self):
        values = [12, 3, 5, 7, 4, 19, 26]
        self.assertEqual(deterministic_select(values, 4), 7)

    def test_duplicates(self):
        values = [4, 2, 4, 1, 2, 4, 3]
        expected = sorted(values)

        for k in range(1, len(values) + 1):
            self.assertEqual(
                deterministic_select(values, k),
                expected[k - 1]
            )

    def test_all_equal(self):
        values = [7] * 20

        for k in range(1, len(values) + 1):
            self.assertEqual(deterministic_select(values, k), 7)

    def test_negative_values(self):
        values = [-10, 4, -3, 8, 0, -1]
        expected = sorted(values)

        for k in range(1, len(values) + 1):
            self.assertEqual(
                deterministic_select(values, k),
                expected[k - 1]
            )

    def test_sorted_input(self):
        values = list(range(100))
        self.assertEqual(deterministic_select(values, 50), 49)

    def test_reverse_sorted_input(self):
        values = list(range(100, 0, -1))
        self.assertEqual(deterministic_select(values, 50), 50)

    def test_large_random_input(self):
        rng = random.Random(532)
        values = [rng.randint(-5000, 5000) for _ in range(1000)]
        expected = sorted(values)

        for k in [1, 100, 500, 750, 1000]:
            self.assertEqual(
                deterministic_select(values, k),
                expected[k - 1]
            )

    def test_empty_input(self):
        with self.assertRaises(ValueError):
            deterministic_select([], 1)

    def test_invalid_k_too_small(self):
        with self.assertRaises(IndexError):
            deterministic_select([1, 2, 3], 0)

    def test_invalid_k_too_large(self):
        with self.assertRaises(IndexError):
            deterministic_select([1, 2, 3], 4)


class TestRandomizedSelect(unittest.TestCase):

    def test_single_element(self):
        rng = random.Random(532)
        self.assertEqual(randomized_select([42], 1, rng), 42)

    def test_smallest_element(self):
        rng = random.Random(532)
        self.assertEqual(
            randomized_select([9, 2, 7, 1, 5], 1, rng),
            1
        )

    def test_largest_element(self):
        rng = random.Random(532)
        self.assertEqual(
            randomized_select([9, 2, 7, 1, 5], 5, rng),
            9
        )

    def test_duplicates(self):
        values = [4, 2, 4, 1, 2, 4, 3]
        expected = sorted(values)

        for k in range(1, len(values) + 1):
            rng = random.Random(532 + k)
            self.assertEqual(
                randomized_select(values, k, rng),
                expected[k - 1]
            )

    def test_all_equal(self):
        values = [7] * 20

        for k in range(1, len(values) + 1):
            rng = random.Random(k)
            self.assertEqual(
                randomized_select(values, k, rng),
                7
            )

    def test_negative_values(self):
        values = [-10, 4, -3, 8, 0, -1]
        expected = sorted(values)

        for k in range(1, len(values) + 1):
            rng = random.Random(k)
            self.assertEqual(
                randomized_select(values, k, rng),
                expected[k - 1]
            )

    def test_sorted_input(self):
        rng = random.Random(532)
        values = list(range(100))

        self.assertEqual(
            randomized_select(values, 50, rng),
            49
        )

    def test_reverse_sorted_input(self):
        rng = random.Random(532)
        values = list(range(100, 0, -1))

        self.assertEqual(
            randomized_select(values, 50, rng),
            50
        )

    def test_multiple_random_seeds(self):
        values = list(range(200, 0, -1))
        expected = sorted(values)

        for seed in range(10):
            rng = random.Random(seed)

            self.assertEqual(
                randomized_select(values, 100, rng),
                expected[99]
            )

    def test_large_random_input(self):
        data_rng = random.Random(532)
        values = [
            data_rng.randint(-10000, 10000)
            for _ in range(1500)
        ]
        expected = sorted(values)

        for k in [1, 250, 750, 1200, 1500]:
            selection_rng = random.Random(1000 + k)

            self.assertEqual(
                randomized_select(values, k, selection_rng),
                expected[k - 1]
            )

    def test_empty_input(self):
        with self.assertRaises(ValueError):
            randomized_select([], 1)

    def test_invalid_k_too_small(self):
        with self.assertRaises(IndexError):
            randomized_select([1, 2, 3], 0)

    def test_invalid_k_too_large(self):
        with self.assertRaises(IndexError):
            randomized_select([1, 2, 3], 4)


class TestDynamicArray(unittest.TestCase):

    def test_append_and_access(self):
        array = DynamicArray()
        array.append(10)
        array.append(20)

        self.assertEqual(array.access(0), 10)
        self.assertEqual(array.access(1), 20)

    def test_insert(self):
        array = DynamicArray()
        array.append(10)
        array.append(30)
        array.insert(1, 20)

        self.assertEqual(array.values(), [10, 20, 30])

    def test_delete(self):
        array = DynamicArray()

        for value in [10, 20, 30]:
            array.append(value)

        removed = array.delete(1)

        self.assertEqual(removed, 20)
        self.assertEqual(array.values(), [10, 30])

    def test_resize_during_append(self):
        array = DynamicArray(initial_capacity=2)

        for value in [10, 20, 30, 40, 50]:
            array.append(value)

        self.assertEqual(
            array.values(),
            [10, 20, 30, 40, 50]
        )

    def test_insert_after_resize(self):
        array = DynamicArray(initial_capacity=2)

        array.append(10)
        array.append(30)
        array.insert(1, 20)

        self.assertEqual(
            array.values(),
            [10, 20, 30]
        )
    
    def test_invalid_index(self):
        array = DynamicArray()

        with self.assertRaises(IndexError):
            array.access(0)

        with self.assertRaises(IndexError):
            array.delete(0)

        with self.assertRaises(IndexError):
            array.insert(1, 10)


class TestMatrix(unittest.TestCase):

    def test_insert_and_access(self):
        matrix = Matrix(2, 3)
        matrix.insert(1, 2, 9)

        self.assertEqual(matrix.access(1, 2), 9)

    def test_delete(self):
        matrix = Matrix(2, 2)
        matrix.insert(0, 1, 8)

        removed = matrix.delete(0, 1)

        self.assertEqual(removed, 8)
        self.assertEqual(matrix.access(0, 1), 0)

    def test_invalid_dimensions(self):
        with self.assertRaises(ValueError):
            Matrix(0, 3)

        with self.assertRaises(ValueError):
            Matrix(3, 0)

    def test_invalid_position(self):
        matrix = Matrix(2, 2)

        with self.assertRaises(IndexError):
            matrix.access(2, 0)

        with self.assertRaises(IndexError):
            matrix.insert(0, 2, 5)


class TestArrayStack(unittest.TestCase):

    def test_push_pop_lifo(self):
        stack = ArrayStack()

        stack.push(10)
        stack.push(20)
        stack.push(30)

        self.assertEqual(stack.pop(), 30)
        self.assertEqual(stack.pop(), 20)
        self.assertEqual(stack.pop(), 10)

    def test_peek(self):
        stack = ArrayStack()
        stack.push(10)
        stack.push(20)

        self.assertEqual(stack.peek(), 20)
        self.assertEqual(stack.size(), 2)

    def test_empty_stack_errors(self):
        stack = ArrayStack()

        with self.assertRaises(IndexError):
            stack.pop()

        with self.assertRaises(IndexError):
            stack.peek()


class TestArrayQueue(unittest.TestCase):

    def test_enqueue_dequeue_fifo(self):
        queue = ArrayQueue()

        queue.enqueue(10)
        queue.enqueue(20)
        queue.enqueue(30)

        self.assertEqual(queue.dequeue(), 10)
        self.assertEqual(queue.dequeue(), 20)
        self.assertEqual(queue.dequeue(), 30)

    def test_peek(self):
        queue = ArrayQueue()
        queue.enqueue(10)
        queue.enqueue(20)

        self.assertEqual(queue.peek(), 10)
        self.assertEqual(queue.size(), 2)

    def test_resize(self):
        queue = ArrayQueue(initial_capacity=2)

        for value in range(10):
            queue.enqueue(value)

        self.assertEqual(queue.values(), list(range(10)))

    def test_circular_wraparound(self):
        queue = ArrayQueue(initial_capacity=4)

        for value in [1, 2, 3, 4]:
            queue.enqueue(value)

        self.assertEqual(queue.dequeue(), 1)
        self.assertEqual(queue.dequeue(), 2)

        queue.enqueue(5)
        queue.enqueue(6)

        self.assertEqual(queue.values(), [3, 4, 5, 6])

    def test_wraparound_and_resize(self):
        queue = ArrayQueue(initial_capacity=4)

        for value in [1, 2, 3, 4]:
            queue.enqueue(value)

        queue.dequeue()
        queue.dequeue()

        queue.enqueue(5)
        queue.enqueue(6)
        queue.enqueue(7)

        self.assertEqual(
            queue.values(),
            [3, 4, 5, 6, 7]
        )

    def test_empty_queue_errors(self):
        queue = ArrayQueue()

        with self.assertRaises(IndexError):
            queue.dequeue()

        with self.assertRaises(IndexError):
            queue.peek()

    def test_invalid_capacity(self):
        with self.assertRaises(ValueError):
            ArrayQueue(initial_capacity=0)


class TestSinglyLinkedList(unittest.TestCase):

    def test_insert_at_beginning(self):
        linked_list = SinglyLinkedList()

        linked_list.insert_at_beginning(20)
        linked_list.insert_at_beginning(10)

        self.assertEqual(
            linked_list.traverse(),
            [10, 20]
        )

    def test_insert_at_end(self):
        linked_list = SinglyLinkedList()

        linked_list.insert_at_end(10)
        linked_list.insert_at_end(20)
        linked_list.insert_at_end(30)

        self.assertEqual(
            linked_list.traverse(),
            [10, 20, 30]
        )

    def test_insert_at_index(self):
        linked_list = SinglyLinkedList()

        linked_list.insert_at_end(10)
        linked_list.insert_at_end(30)
        linked_list.insert_at_index(1, 20)

        self.assertEqual(
            linked_list.traverse(),
            [10, 20, 30]
        )

    def test_delete_head(self):
        linked_list = SinglyLinkedList()

        for value in [10, 20, 30]:
            linked_list.insert_at_end(value)

        self.assertTrue(linked_list.delete(10))
        self.assertEqual(
            linked_list.traverse(),
            [20, 30]
        )

    def test_delete_middle(self):
        linked_list = SinglyLinkedList()

        for value in [10, 20, 30]:
            linked_list.insert_at_end(value)

        self.assertTrue(linked_list.delete(20))
        self.assertEqual(
            linked_list.traverse(),
            [10, 30]
        )

    def test_delete_missing_value(self):
        linked_list = SinglyLinkedList()
        linked_list.insert_at_end(10)

        self.assertFalse(linked_list.delete(99))
        self.assertEqual(
            linked_list.traverse(),
            [10]
        )

    def test_access(self):
        linked_list = SinglyLinkedList()

        for value in [10, 20, 30]:
            linked_list.insert_at_end(value)

        self.assertEqual(linked_list.access(0), 10)
        self.assertEqual(linked_list.access(2), 30)

    def test_invalid_index(self):
        linked_list = SinglyLinkedList()

        with self.assertRaises(IndexError):
            linked_list.access(0)

        with self.assertRaises(IndexError):
            linked_list.insert_at_index(1, 10)

    def test_size_and_empty_state(self):
        linked_list = SinglyLinkedList()

        self.assertTrue(linked_list.is_empty())

        linked_list.insert_at_end(10)
        linked_list.insert_at_end(20)

        self.assertFalse(linked_list.is_empty())
        self.assertEqual(linked_list.size(), 2)


if __name__ == "__main__":
    unittest.main()