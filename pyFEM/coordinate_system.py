from dataclasses import dataclass, field

import numpy as np


@dataclass
class CoordinateSystem:
    origin: np.ndarray = field(default_factory=lambda: np.array([0, 0, 0]))
    X: np.ndarray = field(default_factory=lambda: np.array([1, 0, 0]))
    Y: np.ndarray = field(default_factory=lambda: np.array([0, 1, 0]))
    Z: np.ndarray = field(default_factory=lambda: np.array([0, 0, 1]))
