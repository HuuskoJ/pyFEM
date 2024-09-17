from pyFEM.element import Element
import pyFEM.catalogs.materials.steel.structural_steel as steel
from pyFEM.steel_section import SteelSection
from pyFEM.node import Node
from pyFEM.model import FEModel
from pyFEM.support import Support
from pyFEM.pointload import PointLoad
from pyFEM.loads.lineload import LineLoad
from plotter import Plotter

def model_test():
    # Node
    n1 = Node(0, 0, 0)
    n2 = Node(0, 0, 5000)
    n3 = Node(10000, 0, 5000)
    n4 = Node(10000, 0, 0)
    # Section
    s = SteelSection.IPE100
    # Material
    m = steel.S355
    # Element
    e1 = Element(n1, n2, s, m)
    e2 = Element(n2, n3, s, m)
    e3 = Element(n3, n4, s, m)
    #e4 = Element(n4, n1, s, m)
    elements = [e1, e2, e3]
    model = FEModel()
    for ele in elements:
        model.add(ele)
    # NodalSupport
    sup1 = Support.Fixed(n1)
    sup2 = Support.Fixed(n4)
    supports = [sup1, sup2]
    for sup in supports:
        model.add(sup)
    # PointLoad
    pl1 = PointLoad(n2, Fx=-200e3)
    #model.add(pl1)
    # Lineload
    ll1 = LineLoad(e2, qz=[-100, -100])
    model.add(ll1)

    model.linear_statics()
    print(sup1.R[0])
    print(sup2.R[0])
    model.plot_deflection()



def column_test():
    # FEModel
    model = FEModel()
    # Nodes
    n1 = Node(0, 0, 0)
    n2 = Node(0, 0, 5000)
    # Section
    s = SteelSection.IPE100
    # Material
    m = steel.S355
    # Element
    e1 = Element(n1, n2, s, m)
    model.add(e1)
    # Support
    supp = Support.Fixed(n1)
    model.add(supp)
    # Point Load
    pl = PointLoad(n2, Fy=100e3)
    model.add(pl)

    model.linear_statics()
    model.plot_deflection()

def element_test():
    n1 = Node(10, 20, 40)
    n2 = Node(20, 40, 20)
    n3 = Node(50, 50, 30)
    s = SteelSection.IPE100
    m = steel.S355
    e = Element(n1, n2, s, m)
    print(e.stiffness_matrix)

def column_time_test(num_elems=100):
    import time
    # FEModel
    model = FEModel()
    # Nodes
    n1 = Node(0, 0, 0)

    supp = Support.Fixed(n1)
    model.add(supp)
    # Section
    s = SteelSection.IPE100
    # Material
    m = steel.S355
    L = 5000 / num_elems
    for i in range(num_elems):
        z = L*(i +1)
        n2 = Node(0, 0, z)
        # Element
        e1 = Element(n1, n2, s, m)
        model.add(e1)
        n1 = n2
    # Point Load
    pl = PointLoad(n2, Fx=100e3)
    model.add(pl)
    for _ in range(1):
        start = time.process_time()
        model.linear_statics()
        end = time.process_time()
        print(f"pyFEM: {end - start :.2f} s")



def frame_time_test(num_elems=100, L: float = 5000) -> None:
    import time
    # FEModel
    model = FEModel()
    # Column bottom nodes
    n0 = Node(0, 0, 0)
    n1 = Node(L, 0, 0)
    # Beam first node
    n2 = Node(0, 0, L)
    # Supports
    supp1 = Support.Fixed(n0)
    supp2 = Support.Fixed(n1)
    model.add(supp1)
    model.add(supp2)
    # Section
    s = SteelSection.IPE100
    # Material
    m = steel.S355
    delta_L = L / num_elems
    for i in range(num_elems):
        z = delta_L*(i +1)
        n01 = Node(0, 0, z)
        n11 = Node(L, 0, z)
        # Element
        e0 = Element(n0, n01, s, m)
        e1 = Element(n1, n11, s, m)
        model.add(e0)
        model.add(e1)
        n0 = n01
        n1 = n11


    for j in range(num_elems):
        z = delta_L * (j + 1)
        n21 = Node(z, 0, L)

        if j == 0:
            n2 = n01
        if j == num_elems - 1:
            n21 = n11

        # Element
        e2 = Element(n2, n21, s, m)
        model.add(e2)
        n2 = n21
        # Lineloads
        ll = LineLoad(e2, qz=[-100, -100])
        model.add(ll)

    # Point Load
    pl = PointLoad(n01, Fx=100e3)
    model.add(pl)


    start = time.process_time()
    model.linear_statics()
    end = time.process_time()
    print(f"pyFEM: {end - start :.2f} s")
    for sup in model.supports.values():
        print(sup.R)
    plotter = Plotter()
    plotter.plot_deflection(model, plot_nodes=False)

if __name__ == "__main__":
    num_elements = 100
    #print(timeit.timeit(frame_time_test, number=10, setup=f"num_elems = {num_elements}"))
    frame_time_test(num_elements)
    #metku_frame_test(num_elements)
