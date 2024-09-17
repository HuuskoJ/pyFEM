from dataclasses import dataclass, field
from typing import Protocol

import numpy as np

import pyFEM.elem_funcs as ef
from pyFEM.coordinate_system import CoordinateSystem


class Node(Protocol):
    x: float
    y: float
    z: float
    coordinate: np.array
    node_id: int


class Material(Protocol):
    E: float
    G: float


class Section(Protocol):
    A: float
    Iy: float
    Iz: float
    It: float


@dataclass(slots=True)
class Element:
    n1: 'Node'
    n2: 'Node'
    section: 'Section'
    material: 'Material'
    elem_id: int = field(init=False)
    global_coordinate_system: CoordinateSystem = field(default_factory=CoordinateSystem)
    has_load: bool = False

    @property
    def up(self) -> np.ndarray:
        """
        Returns element's up -direction
        """
        return self.global_coordinate_system.Z

    @property
    def local_coordinate_system(self) -> CoordinateSystem:
        """
        Returns element's local coordinate system
        """
        if abs(1 - abs(np.dot(self.unit_vector, self.up))) <= 1e-10:
            y = np.array([0, 1, 0])
            z = np.array([1, 0, 0])
        else:
            z = ef.unit_vector(ef.vector_rejection(self.up, self.unit_vector))
            y = ef.unit_vector(np.cross(z, self.unit_vector))
        return CoordinateSystem(origin=self.n1.coordinate,
                                X=self.unit_vector,
                                Y=y,
                                Z=z)

    @property
    def coordinates(self) -> np.ndarray:
        """
        Returns element's coordinates
        """
        return np.array([self.n1.coordinate, self.n2.coordinate])

    @property
    def L(self) -> float:
        """
        Returns element's length
        """
        return np.linalg.norm(self.as_vector)

    @property
    def X(self) -> np.ndarray:
        """
        Returns element's nodes' X-coordinates
        """
        return np.asarray([self.n1.x, self.n2.x])

    @property
    def Y(self) -> np.ndarray:
        """
        Returns element's nodes' Y-coordinates
        """
        return np.asarray([self.n1.y, self.n2.y])

    @property
    def Z(self) -> np.ndarray:
        """
        Returns element's nodes' Z-coordinates
        """
        return np.asarray([self.n1.z, self.n2.z])

    @property
    def as_vector(self) -> np.ndarray:
        """
        Returns element as a vector
        """
        return self.n2.coordinate - self.n1.coordinate

    @property
    def unit_vector(self) -> np.ndarray:
        """
        Returns element's unit vector
        """
        return ef.unit_vector(self.as_vector)

    @property
    def mid_point(self) -> np.ndarray:
        """
        Returns element's mid point
        """
        return self.n1.coordinate + self.unit_vector * self.L * 0.5

    @property
    def local_stiffness_matrix(self) -> np.ndarray:
        """
        Returns element's local stiffness matrix
        """
        return ef.local_stiffness_matrix(self.material.E,
                                         self.section.A,
                                         self.material.G,
                                         self.section.Iy,
                                         self.section.Iz,
                                         self.section.It,
                                         self.L)

    @property
    def transformation_matrix(self) -> np.ndarray:
        """
        Retrurns element's transformation matrix
        """
        return ef.transformation_matrix(self.local_coordinate_system,
                                        self.global_coordinate_system)

    @property
    def stiffness_matrix(self) -> np.ndarray:
        """
        Returns element's global stiffness matrix
        """
        return ef.stiffness_matrix(self.transformation_matrix,
                                   self.local_stiffness_matrix)

    @property
    def stiffness_data(self) -> np.ndarray:
        return self.stiffness_matrix.flatten()

    @property
    def dofs(self):
        return len(self.n1.coordinate) * 2

    @property
    def idxs(self) -> np.ndarray:
        n1_id = self.n1.node_id * self.dofs
        n2_id = self.n2.node_id * self.dofs
        idxs = np.append(np.arange(n1_id, n1_id + self.dofs, dtype=np.uint32),
                         np.arange(n2_id, n2_id + self.dofs, dtype=np.uint32))
        return idxs

    @property
    def rows(self) -> np.ndarray:
        return np.repeat(self.idxs, 12)

    @property
    def cols(self) -> np.ndarray:
        return np.tile(self.idxs, 12)
