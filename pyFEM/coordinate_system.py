from dataclasses import dataclass

import numpy as np


@dataclass
class CoordinateSystem:
    origin: np.ndarray = np.array([0, 0, 0])
    X: np.ndarray = np.array([1, 0, 0])
    Y: np.ndarray = np.array([0, 1, 0])
    Z: np.ndarray = np.array([0, 0, 1])
