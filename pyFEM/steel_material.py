from __future__ import annotations

from dataclasses import dataclass, field

from pyFEM.material import Material


@dataclass(slots=True, kw_only=True)
class StructuralSteel(Material):

    fy: float
    fu: float

    # Constant material properties for steel
    young: float = 210e3
    poisson: float = 0.3
    density: float = 7850e-9
    G: float = 81e3

    @property
    def E(self):
        return self.young

    @property
    def nu(self):
        return self.poisson

    @property
    def rho(self):
        return self.density



if __name__ == "__main__":
    from pyFEM.catalogs.materials.steel import structural_steel as steel
    sm = steel.S420N
    print(sm)
