from typing import Any, List, Optional


class Node:
    """Node used by the singly linked list."""

    def __init__(self, value: Any) -> None:
        self.value = value
        self.next: Optional["Node"] = None


class SinglyLinkedList:
    """Singly linked list supporting insertion, deletion, and traversal."""

    def __init__(self) -> None:
        self.head: Optional[Node] = None
        self._size = 0

    def insert_at_beginning(self, value: Any) -> None:
        """Insert a new value at the beginning of the list."""
        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node
        self._size += 1

    def insert_at_end(self, value: Any) -> None:
        """Insert a new value at the end of the list."""
        new_node = Node(value)

        if self.head is None:
            self.head = new_node
            self._size += 1
            return

        current = self.head

        while current.next is not None:
            current = current.next

        current.next = new_node
        self._size += 1

    def insert_at_index(self, index: int, value: Any) -> None:
        """Insert a value at the specified index."""
        if index < 0 or index > self._size:
            raise IndexError("Index out of range.")

        if index == 0:
            self.insert_at_beginning(value)
            return

        current = self.head

        for _ in range(index - 1):
            if current is not None:
                current = current.next

        new_node = Node(value)

        if current is not None:
            new_node.next = current.next
            current.next = new_node

        self._size += 1

    def delete(self, value: Any) -> bool:
        """
        Delete the first occurrence of a value.

        Returns True if the value was found and deleted.
        Returns False if the value was not found.
        """
        if self.head is None:
            return False

        if self.head.value == value:
            self.head = self.head.next
            self._size -= 1
            return True

        current = self.head

        while current.next is not None:
            if current.next.value == value:
                current.next = current.next.next
                self._size -= 1
                return True

            current = current.next

        return False

    def access(self, index: int) -> Any:
        """Return the value stored at the specified index."""
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range.")

        current = self.head

        for _ in range(index):
            if current is not None:
                current = current.next

        if current is None:
            raise IndexError("Index out of range.")

        return current.value

    def traverse(self) -> List[Any]:
        """Return all list values in traversal order."""
        values: List[Any] = []
        current = self.head

        while current is not None:
            values.append(current.value)
            current = current.next

        return values

    def size(self) -> int:
        """Return the number of elements in the list."""
        return self._size

    def is_empty(self) -> bool:
        """Return True when the list contains no elements."""
        return self._size == 0


if __name__ == "__main__":
    linked_list = SinglyLinkedList()

    linked_list.insert_at_beginning(20)
    linked_list.insert_at_beginning(10)
    linked_list.insert_at_end(30)
    linked_list.insert_at_index(2, 25)

    print("Linked list:", linked_list.traverse())
    print("Access index 2:", linked_list.access(2))
    print("Delete 20:", linked_list.delete(20))
    print("After deletion:", linked_list.traverse())
    print("Size:", linked_list.size())