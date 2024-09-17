from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

import numpy as np

import pyFEM.solver as solver
# from pyFEM.plotter import Plotter
from pyFEM.coordinate_system import CoordinateSystem
from pyFEM.loads.lineload import LineLoad
from pyFEM.pointload import PointLoad
from pyFEM.support import NodalSupport


# Protocols
# ----------
@runtime_checkable
class Node(Protocol):
    x: float
    y: float
    z: float
    coordinates: np.array
    node_id: int


@runtime_checkable
class Element(Protocol):
    n1: Node
    n2: Node


@runtime_checkable
class Support(Protocol):
    supp_id: int


@runtime_checkable
class LineLoad(Protocol):
    element: Element
    load_id: int


@dataclass
class FEModel:
    elements: dict[int: 'Element'] = field(default_factory=dict)
    supports: dict[int: 'Support'] = field(default_factory=dict)
    loads: dict[int: 'PointLoad' | 'LineLoad'] = field(default_factory=dict)
    elem_id: int = 0
    supp_id: int = 0
    load_id: int = 0
    node_id: int = 0
    global_coordinate_system: CoordinateSystem = field(default_factory=CoordinateSystem)

    #
    # def __init__(self):
    #     self.elements = {}
    #     self.supports = {}
    #     self.loads = {}
    #
    #     self.elem_id = 0
    #     self.supp_id = 0
    #     self.load_id = 0
    #     self.node_id = 0

    def renumber_supports(self, supports: list[Support]) -> None:
        """
        Renumbers supports
        """
        self.supports.clear()
        for i, supp in enumerate(supports):
            supp.supp_id = i
            self.supports[i] = supp

    def renumber_elements(self, elements: list[Element]) -> None:
        """
        Renumbers elements
        """
        self.elements.clear()
        for i, elem in enumerate(elements):
            elem.elem_id = i
            self.elements[i] = elem

    def renumber_nodes(self, nodes: list[Node]) -> None:
        """
        Renumbers nodes
        """
        self.nodes.clear()
        for i, node in enumerate(nodes):
            node.node_id = i
            self.nodes[i] = node

    def renumber(self):
        """
        Renumbers every object in model
        """
        # NODES
        self.renumber_nodes(self.node_list)
        # ELEMENTS
        self.renumber_elements(self.element_list)
        # SUPPORTS
        self.renumber_supports(self.support_list)

    @property
    def dofs(self):
        return len(self.nodes) * 6

    @property
    def support_list(self) -> list:
        """
        Returns all model's supports as list
        """
        return list(self.supports.values())

    @property
    def element_list(self) -> list:
        """
        Returns all model's elements as list
        """
        return list(self.elements.values())

    @property
    def node_list(self) -> list:
        """
        Returns all model's nodes as list
        """
        return list(self.nodes.values())

    @property
    def nodes(self):
        nodes = {}
        for elem in self.element_list:
            n1 = elem.n1
            n2 = elem.n2
            if n1.node_id not in nodes:
                nodes[n1.node_id] = n1
            if n2.node_id not in nodes:
                nodes[n2.node_id] = n2
        return nodes

    @property
    def pointloads(self):
        return [pl for pl in self.loads.values() if isinstance(pl, PointLoad)]

    @property
    def lineloads(self):
        return [ll for ll in self.loads.values() if isinstance(ll, LineLoad)]

    @property
    def global_load_vector(self) -> np.ndarray:
        """
        Computes the global load vector
        """
        forces = np.zeros(self.dofs)
        for pl in self.pointloads:
            node_id = pl.node.node_id
            idx = node_id * 6
            forces[idx:idx + 6] += pl.global_load_vector
        for ll in self.lineloads:
            n1_id = ll.element.n1.node_id
            n2_id = ll.element.n2.node_id
            llf1 = ll.global_load_vector[:6]
            llf2 = ll.global_load_vector[6:]
            idx1 = n1_id * 6
            idx2 = n2_id * 6
            forces[idx1: idx1 + 6] += llf1
            forces[idx2: idx2 + 6] += llf2

        return forces.reshape((self.dofs, 1))

    @property
    def global_stiffness_matrix(self):
        rows = np.asarray([elem.rows for elem in self.element_list])
        cols = np.asarray([elem.cols for elem in self.element_list])
        stiff_data = np.asarray([elem.stiffness_matrix for elem in self.element_list])
        return solver.global_stiffness_matrix(rows, cols, stiff_data)

    @property
    def constraint_matrix(self) -> np.ndarray:
        B_tot = np.array([])

        for supp in self.support_list:
            B = supp.B(self.dofs)
            B_tot = np.vstack((B_tot, B)) if B_tot.size else B
        return B_tot

    def linear_statics(self, load_id=0):

        U, R = solver.static_load_analysis(self.global_stiffness_matrix.toarray(),
                                           self.global_load_vector,
                                           self.constraint_matrix,
                                           self.dofs)

        for node, u in zip(self.node_list, np.split(U, len(self.nodes))):
            # OLD
            # idx = node.node_id * 6
            # u = U[idx: idx + 6]
            # node.u[load_id] = u.flatten()
            node.u[load_id] = u

        for supp in self.support_list:
            idx = supp.supp_id * 6
            r = R[idx: idx + 6]
            supp.R[load_id] = r.flatten()

    def add(self, item: object) -> None:

        if isinstance(item, Element):
            self.add_element(item)
        elif isinstance(item, NodalSupport):
            self.add_nodal_support(item)
        elif isinstance(item, PointLoad):
            self.add_pointload(item)
        elif isinstance(item, LineLoad):
            self.add_lineload(item)

    def add_element(self, element: Element) -> None:
        """
        Adds element to model
        """
        # Set nodes' id's
        n1 = element.n1
        n2 = element.n2
        if n1.node_id is None:
            n1.node_id = self.node_id
            self.node_id += 1
        if n2.node_id is None:
            n2.node_id = self.node_id
            self.node_id += 1
        # Set element's global coordinate system
        element.global_coordinate_system = self.global_coordinate_system
        element.elem_id = self.elem_id
        self.elem_id += 1
        self.elements[element.elem_id] = element

    def add_nodal_support(self, nodal_support: NodalSupport) -> None:
        """
        Adds nodal support to model
        """
        nodal_support.node.supported = True
        nodal_support.supp_id = self.supp_id
        self.supp_id += 1
        self.supports[nodal_support.supp_id] = nodal_support

    def add_pointload(self, pl: PointLoad) -> None:
        pl.load_id = self.load_id
        self.load_id += 1
        self.loads[pl.load_id] = pl

    def add_lineload(self, ll: LineLoad) -> None:
        ll.element.has_load = True
        ll.load_id = self.load_id
        self.load_id += 1
        self.loads[ll.load_id] = ll

    # def plot(self, show: bool = True):
    #     plotter = Plotter()
    #     for element in self.element_list:
    #         plotter.plot_element(element)
    #     for pl in self.pointloads:
    #         plotter.plot_pointload(pl)
    #     if show:
    #         plotter.show()
    #     else:
    #         return plotter
    #
    # def plot_deflection(self, load_id: int = 0, scale: float = 1.0):
    #     plotter = self.plot(False)
    #     for elem in self.element_list:
    #         plotter.plot_deflection(elem, load_id, scale)
    #     plotter.show()
