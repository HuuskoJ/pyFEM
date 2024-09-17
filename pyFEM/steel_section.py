from pyFEM.isection import ISection


class SteelSection:
    # IPE dimensions
    # https://eurocodeapplied.com/design/en1993/ipe-hea-heb-hem-design-properties
    IPE80: 'ISection' = ISection("IPE", h=80, b=46, tw=3.8, tf=5.2, r=5)
    IPE100: 'ISection' = ISection("IPE", h=100, b=55, tw=4.1, tf=5.7, r=7)
    IPE120: 'ISection' = ISection("IPE", h=120, b=64, tw=4.4, tf=6.3, r=7)
