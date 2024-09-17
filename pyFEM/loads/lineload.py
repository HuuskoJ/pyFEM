from dataclasses import dataclass, field
import numpy as np


@dataclass
class LineLoad:
    element: 'Element'
    qx: np.ndarray | list = field(default_factory=lambda: np.zeros(2))
    qy: np.ndarray | list = field(default_factory=lambda: np.zeros(2))
    qz: np.ndarray | list = field(default_factory=lambda: np.zeros(2))
    mx: np.ndarray | list = field(default_factory=lambda: np.zeros(2))
    my: np.ndarray | list = field(default_factory=lambda: np.zeros(2))
    mz: np.ndarray | list = field(default_factory=lambda: np.zeros(2))
    load_id: int = field(default=0, init=False)

    @property
    def load_vector(self):
        return np.array([self.qx, self.qy, self.qz,
                         self.mx, self.my, self.mz]).flatten(order="F")

    @property
    def global_load_vector(self) -> np.ndarray:
        F = np.empty(12)
        L = self.element.L
        L2 = L ** 2
        qx1, qy1, qz1, mx1, my1, mz1 = self.load_vector[:6]
        qx2, qy2, qz2, mx2, my2, mz2 = self.load_vector[6:]

        F[0] = qx1 * L / 2
        F[1] = qy1 * L / 2 - mz1
        F[2] = qz1 * L / 2 + my1
        F[3] = mx1 * L / 2
        F[4] = -qz1 * L2 / 12
        F[5] = qy1 * L2 / 12

        F[6] = qx2 * L / 2
        F[7] = qy2 * L / 2 + mz2
        F[8] = qz2 * L / 2 - my2
        F[9] = mx2 * L / 2
        F[10] = qz2 * L2 / 12
        F[11] = -qy2 * L2 / 12

        return F

    @property
    def local_load_vector(self) -> np.ndarray:
        return self.element.transformation_matrix @ self.global_load_vector


if __name__ == "__main__":
    ll = LineLoad(qy=np.array([1, 2]), qz=np.array([10, 20]))
    print(ll.global_load_vector)
