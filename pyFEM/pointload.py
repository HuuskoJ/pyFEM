from dataclasses import dataclass
from pyFEM.node import Node
import numpy as np

@dataclass
class PointLoad:

    node: Node
    Fx: float = 0
    Fy: float = 0
    Fz: float = 0
    Mx: float = 0
    My: float = 0
    Mz: float = 0


    @property
    def F(self):
        return np.asarray([self.Fx, self.Fy, self.Fz])

    @property
    def M(self):
        return np.asarray([self.Mx, self.My, self.Mz])

    @property
    def global_load_vector(self):
        return np.concatenate((self.F, self.M), axis=None)

if __name__ == "__main__":

    n1 = Node(0, 0,0)
    pl = PointLoad(n1, Fx= 100e3)
    print(pl)