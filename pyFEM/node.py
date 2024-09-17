from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass(slots=True)
class Node:
    x: float
    y: float
    z: float = 0
    supported: bool = False
    u: dict = field(default_factory=dict)
    node_id: int = field(default=None, init=False)

    @property
    def coordinate(self):
        return np.array([self.x, self.y, self.z])

    @coordinate.setter
    def coordinate(self, value):
        self.x, self.y, self.z = value

    def __add__(self, node: Node) -> Node:
        value = self.coordinate + node.coordinate
        return Node(*value)

    def __iadd__(self, node: Node) -> Node:
        self.coordinate += node.coordinate
        return self


if __name__ == '__main__':
    n1 = Node(10, 30, 30)
    n2 = Node(100, 200, 300)
