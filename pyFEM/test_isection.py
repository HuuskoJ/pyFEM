from pyFEM.steel_material import Steel
from pyFEM.steel_section import SteelSection

if __name__ == "__main__":

    mat = Steel.S355
    sect = SteelSection.IPE100
    print(sect)