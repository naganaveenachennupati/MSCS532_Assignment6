from typing import Any, List, Optional


class ArrayStack:
    """Stack implementation backed by a dynamic array."""

    def __init__(self) -> None:
        self._data: List[Any] = []

    def push(self, value: Any) -> None:
        """Add a value to the top of the stack."""
        self._data.append(value)

    def pop(self) -> Any:
        """Remove and return the value at the top of the stack."""
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack.")

        return self._data.pop()

    def peek(self) -> Any:
        """Return the top value without removing it."""
        if self.is_empty():
            raise IndexError("Cannot peek at an empty stack.")

        return self._data[-1]

    def is_empty(self) -> bool:
        """Return True when the stack contains no elements."""
        return len(self._data) == 0

    def size(self) -> int:
        """Return the number of elements in the stack."""
        return len(self._data)

    def values(self) -> List[Any]:
        """Return a copy of the stack contents."""
        return self._data.copy()


class ArrayQueue:
    """Queue implementation backed by a circular dynamic array."""

    def __init__(self, initial_capacity: int = 4) -> None:
        if initial_capacity <= 0:
            raise ValueError("Initial capacity must be positive.")

        self._data: List[Optional[Any]] = [None] * initial_capacity
        self._front = 0
        self._size = 0

    def enqueue(self, value: Any) -> None:
        """Add a value to the rear of the queue."""
        if self._size == len(self._data):
            self._resize(len(self._data) * 2)

        rear_index = (self._front + self._size) % len(self._data)
        self._data[rear_index] = value
        self._size += 1

    def dequeue(self) -> Any:
        """Remove and return the value at the front of the queue."""
        if self.is_empty():
            raise IndexError("Cannot dequeue from an empty queue.")

        value = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % len(self._data)
        self._size -= 1

        return value

    def peek(self) -> Any:
        """Return the front value without removing it."""
        if self.is_empty():
            raise IndexError("Cannot peek at an empty queue.")

        return self._data[self._front]

    def is_empty(self) -> bool:
        """Return True when the queue contains no elements."""
        return self._size == 0

    def size(self) -> int:
        """Return the number of elements in the queue."""
        return self._size

    def values(self) -> List[Any]:
        """Return queue contents in front-to-rear order."""
        return [
            self._data[(self._front + i) % len(self._data)]
            for i in range(self._size)
        ]

    def _resize(self, new_capacity: int) -> None:
        """Resize the backing array while preserving queue order."""
        new_data: List[Optional[Any]] = [None] * new_capacity

        for i in range(self._size):
            old_index = (self._front + i) % len(self._data)
            new_data[i] = self._data[old_index]

        self._data = new_data
        self._front = 0


if __name__ == "__main__":
    stack = ArrayStack()

    stack.push(10)
    stack.push(20)
    stack.push(30)

    print("Stack:", stack.values())
    print("Stack top:", stack.peek())
    print("Stack pop:", stack.pop())
    print("Stack after pop:", stack.values())

    queue = ArrayQueue()

    queue.enqueue(10)
    queue.enqueue(20)
    queue.enqueue(30)
    queue.enqueue(40)
    queue.enqueue(50)

    print("Queue:", queue.values())
    print("Queue front:", queue.peek())
    print("Queue dequeue:", queue.dequeue())
    print("Queue after dequeue:", queue.values())