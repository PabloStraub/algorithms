from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Optional, List


@dataclass
class _Node:
    value: float
    left: Optional["_Node"] = None
    right: Optional["_Node"] = None


class BinarySearchTree:
    def __init__(self) -> None:
        self._root: Optional[_Node] = None

    # --- API pública ---

    def __iter__(self) -> Iterator[float]:
        """Permite: for x in tree"""
        yield from self._inorder(self._root)

    def tree_add(self, x: float) -> None:
        self._root = self._add(self._root, float(x))

    def tree_find(self, x: float) -> bool:
        x = float(x)
        cur = self._root
        while cur is not None:
            if x == cur.value:
                return True
            cur = cur.left if x < cur.value else cur.right
        return False

    def tree_remove(self, x: float):
        self._root = self._remove(self._root, float(x))

    def tree_traverse(self) -> Iterator[float]:
        """Equivalente a iter(tree)."""
        return iter(self)

    def tree_to_list(self) -> List[float]:
        return list(self)

    # --- helpers internos ---

    def _add(self, node: Optional[_Node], x: float) -> _Node:
        if node is None:
            return _Node(x)
        if x < node.value:
            node.left = self._add(node.left, x)
        else:
            # duplicados van al subárbol derecho
            node.right = self._add(node.right, x)
        return node

    def _inorder(self, node: Optional[_Node]) -> Iterator[float]:
        if node is None:
            return
        yield from self._inorder(node.left)
        yield node.value
        yield from self._inorder(node.right)

    def _remove(self, node: Optional[_Node], x: float) -> Optional[_Node]:
        if node is None:
            return None

        if x < node.value:
            node.left = self._remove(node.left, x)
            return node

        if x > node.value:
            node.right = self._remove(node.right, x)
            return node

        # x == node.value
        if node.left is None:
            return node.right
        if node.right is None:
            return node.left

        # dos hijos: reemplazo por sucesor
        succ = self._min_value(node.right)
        node.value = succ
        node.right = self._remove(node.right, succ)
        return node

    def _min_value(self, node: _Node) -> float:
        while node.left is not None:
            node = node.left
        return node.value

if __name__ == "__main__":
    t = BinarySearchTree()
    t.tree_add(3.0)
    t.tree_add(1.0)
    t.tree_add(2.0)
    t.tree_add(3.0)

    print(list(t))            # [1.0, 2.0, 3.0, 3.0]

    for x in t:               # usa __iter__
        print(x)

    t.tree_remove(3.0)
    print(t.tree_to_list())   # [1.0, 2.0, 3.0]
