from dataclasses import dataclass, field
from pyFEM.node import Node
from enum import Enum
import numpy as np


@dataclass
class NodalSupport:
    node: Node = None
    Tx: bool = False
    Ty: bool = False
    Tz: bool = False
    Rx: bool = False
    Ry: bool = False
    Rz: bool = False
    supp_id: int = field(default=False, init=False)
    R: dict = field(default_factory=dict)

    @property
    def as_vector(self) -> np.ndarray:
        return np.array([self.Tx, self.Ty, self.Tz,
                         self.Rx, self.Ry, self.Rz])

    def B(self, total_dofs: int) -> np.ndarray:
        nid = self.node.node_id
        idx = nid * 6
        B = np.zeros((6, total_dofs))
        B[0:6, idx: idx + 6] = self.as_vector * np.eye(6)
        return B

    def __call__(self, node):
        return NodalSupport(node, *self.as_vector)


class Support:
    Fixed = NodalSupport(None, True, True, True, True, True, True)




if __name__ == "__main__":
    n1 = Node(0, 0, 0)
    sup = NodalSupport(n1)
    print(sup)
