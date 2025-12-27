from typing import Optional, List


class _Node:
    def __init__(self, value: float) -> None:
        self.value: float = value
        self.left: Optional["_Node"] = None
        self.right: Optional["_Node"] = None

class BinarySearchTree:
    def __init__(self) -> None:
        self.root: Optional[_Node] = None

    # ---------- API pública ----------

    def add(self, x: float) -> None:
        self.root = self._add(self.root, float(x))

    def find(self, x: float) -> bool:
        return self._find(self.root, float(x))

    def count(self, x: float) -> int:
        return self._count(self.root, float(x))

    def inorder(self) -> List[float]:
        """Devuelve una lista ordenada con los valores del árbol."""
        return self._inorder(self.root)
    
    def to_json(self) -> str:
        return self._to_json(self.root, 0)

    def remove(self, x: float) -> None:
        self.root = self._remove(self.root, float(x))


    # ---------- helpers internos ----------

    def _add(self, node: Optional[_Node], x: float) -> _Node:
        if node is None:
            return _Node(x)
        if x < node.value:
            node.left = self._add(node.left, x)
        else:
            # duplicados van a la derecha
            node.right = self._add(node.right, x)
        return node

    def _find(self, node: Optional[_Node], x: float) -> bool:
        if node is None:
            return False
        if x == node.value:
            return True
        if x < node.value:
            return self._find(node.left, x)
        return self._find(node.right, x)
    
    def _count(self, node: Optional[_Node], x: float) -> int:
        if node is None:
            return 0
        if x == node.value:
            return 1 + self._count(node.right, x)
        if x < node.value:
            return self._count(node.left, x)
        return self._count(node.right, x)

    def _inorder(self, node: Optional[_Node]) -> List[float]:
        if node is None:
            return []
        return (
            self._inorder(node.left)
            + [node.value]
            + self._inorder(node.right)
        )

    def _to_json(self, node: Optional[_Node], level: int) -> str:

        if node is None:
            return "null"

        tab = " "*4
        indent = tab*level

        return (
            "{\n" +
            tab + indent + f"\"value\": {node.value},\n" +
            tab + indent + "\"left\": " + self._to_json(node.left, level+1) + ",\n" +
            tab + indent + "\"right\": " + self._to_json(node.right, level+1) + "\n" +
            indent + "}"
        )

    def _remove(self, node: Optional[_Node], x: float) -> Optional[_Node]:
        if node is None:
            return None

        if x < node.value:
            node.left = self._remove(node.left, x)
            return node

        if x > node.value:
            node.right = self._remove(node.right, x)
            return node

        # x == node.value → eliminar este nodo
        if node.left is None:
            return node.right
        if node.right is None:
            return node.left

        # dos hijos: reemplazar por sucesor (el mínimo del subárbol derecho)
        succ_value = self._min_value(node.right)
        node.value = succ_value
        node.right = self._remove(node.right, succ_value)
        return node

    def _min_value(self, node: _Node) -> float:
        while node.left is not None:
            node = node.left
        return node.value


if __name__ == "__main__":
    t = BinarySearchTree()
    t.add(4.0)
    print(t.to_json())
    t.add(2.0)
    t.add(5.0)
    t.add(2.0)
    print(t.to_json())

    print(t.inorder())  # [2.0, 2.0, 4.0, 5.0]
    print(t.find(5.0))  # True
    print(t.find(10.0)) # False
    print(t.count(2.0)) # 2
    t.remove(2.0)
    print(t.count(2.0)) # 1
    print(t.inorder())  # [2.0, 4.0, 5.0]
