from typing import Any, List


class DynamicArray:
    """Dynamic array implemented with explicit capacity management."""

    def __init__(self, initial_capacity: int = 4) -> None:
        if initial_capacity <= 0:
            raise ValueError("Initial capacity must be positive.")

        self._capacity = initial_capacity
        self._size = 0
        self._data: List[Any] = [None] * self._capacity

    def _resize(self, new_capacity: int) -> None:
        """Resize the underlying storage."""
        new_data: List[Any] = [None] * new_capacity

        for i in range(self._size):
            new_data[i] = self._data[i]

        self._data = new_data
        self._capacity = new_capacity

    def insert(self, index: int, value: Any) -> None:
        """Insert a value at the specified index."""
        if index < 0 or index > self._size:
            raise IndexError("Index out of range.")

        if self._size == self._capacity:
            self._resize(self._capacity * 2)

        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]

        self._data[index] = value
        self._size += 1

    def delete(self, index: int) -> Any:
        """Delete and return the value at the specified index."""
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range.")

        removed_value = self._data[index]

        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]

        self._data[self._size - 1] = None
        self._size -= 1

        return removed_value

    def access(self, index: int) -> Any:
        """Return the value at the specified index."""
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range.")

        return self._data[index]

    def append(self, value: Any) -> None:
        """Append a value to the end of the array."""
        self.insert(self._size, value)

    def values(self) -> List[Any]:
        """Return the logical array contents."""
        return [
            self._data[i]
            for i in range(self._size)
        ]

    def __len__(self) -> int:
        return self._size


class Matrix:
    """Two-dimensional matrix supporting basic element operations."""

    def __init__(
        self,
        rows: int,
        columns: int,
        default: Any = 0
    ) -> None:
        if rows <= 0 or columns <= 0:
            raise ValueError(
                "Rows and columns must be positive integers."
            )

        self.rows = rows
        self.columns = columns
        self._default = default

        self._data = [
            [default for _ in range(columns)]
            for _ in range(rows)
        ]

    def _validate_position(
        self,
        row: int,
        column: int
    ) -> None:
        if row < 0 or row >= self.rows:
            raise IndexError("Row index out of range.")

        if column < 0 or column >= self.columns:
            raise IndexError("Column index out of range.")

    def insert(
        self,
        row: int,
        column: int,
        value: Any
    ) -> None:
        """Insert or replace a value at a matrix position."""
        self._validate_position(row, column)
        self._data[row][column] = value

    def delete(
        self,
        row: int,
        column: int
    ) -> Any:
        """Delete a value by resetting the cell to its default."""
        self._validate_position(row, column)

        removed_value = self._data[row][column]
        self._data[row][column] = self._default

        return removed_value

    def access(
        self,
        row: int,
        column: int
    ) -> Any:
        """Return the value stored at a matrix position."""
        self._validate_position(row, column)
        return self._data[row][column]

    def values(self) -> List[List[Any]]:
        """Return a copy of the matrix contents."""
        return [
            row.copy()
            for row in self._data
        ]


if __name__ == "__main__":
    array = DynamicArray()

    array.append(10)
    array.append(20)
    array.insert(1, 15)

    print("Array after insertion:", array.values())
    print("Access index 1:", array.access(1))
    print("Deleted value:", array.delete(1))
    print("Array after deletion:", array.values())

    matrix = Matrix(2, 3)

    matrix.insert(0, 1, 7)
    matrix.insert(1, 2, 9)

    print("Matrix:", matrix.values())
    print(
        "Access row 1, column 2:",
        matrix.access(1, 2)
    )
    print(
        "Deleted matrix value:",
        matrix.delete(1, 2)
    )
    print(
        "Matrix after deletion:",
        matrix.values()
    )