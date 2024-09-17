import matplotlib.pyplot as plt
import numpy as np

from pyFEM.model import FEModel


class Plotter:

    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")

    def plot_node(self, node, color: str = 'b'):
        if node.supported:
            color = 'r'
        self.ax.scatter(*node.coordinate, color=color)
        self.ax.text(*node.coordinate, node.node_id)

    def plot_element(self, element, linestyle="-", color: str="k", plot_nodes: bool = True):
        if element.has_load:
            color = 'r'
        if plot_nodes:
            self.plot_node(element.n1)
            self.plot_node(element.n2)
        self.ax.plot(element.X, element.Y, element.Z, color=color,
                     lw=element.section.A / 1000,
                     linestyle=linestyle)

        text = str(element.elem_id) + ": " + element.section.name
        # self.ax.text(*element.mid_point, text)

    def plot_pointload(self, pl):
        length = np.linalg.norm(pl.F) / 1e3
        c0 = pl.node.coordinate - pl.F / 1e3
        self.ax.quiver(*c0, *pl.F, length=length, normalize=True)

    def plot_element_deflection(self, element, load_id=0, scale=1.0, color: str = "k", plot_nodes: bool=False):

        u1 = element.n1.u[load_id][:3]
        u2 = element.n2.u[load_id][:3]
        c1 = element.n1.coordinate.copy()
        c2 = element.n2.coordinate.copy()
        element.n1.coordinate = c1 + u1 * scale
        element.n2.coordinate = c2 + u2 * scale
        self.plot_element(element, linestyle="--", color=color, plot_nodes=plot_nodes)
        element.n1.coordinate = c1
        element.n2.coordinate = c2

    def plot(self, model: FEModel, show: bool = True, color: str = 'k', plot_nodes: bool = True):
        for element in model.element_list:
            self.plot_element(element, linestyle="-", plot_nodes=plot_nodes)
        for pl in model.pointloads:
            self.plot_pointload(pl)
        if show:
            self.show()

    def plot_deflection(self, model: FEModel, load_id: int = 0, scale: float = 1.0, plot_nodes: bool = True):
        self.plot(model=model, show=False, plot_nodes=plot_nodes)
        for elem in model.element_list:
            self.plot_element_deflection(elem, load_id, scale, color="red", plot_nodes=plot_nodes)
        self.show()

    def show(self):
        plt.show()
