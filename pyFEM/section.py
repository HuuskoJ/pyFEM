from __future__ import annotations

from dataclasses import dataclass, field
from pyFEM.material import Material


@dataclass
class BaseSection:

    name: str = field(default=False, init=False)
    material: Material = field(default=False, init=False)
    A: float = field(default=False, init=False)
    I: list = field(default=False, init=False)


if __name__ == "__main__":

    from pyFEM.steel_section import SteelSection
    sect = SteelSection.IPE100
    sect.h += 100
    print(sect)
