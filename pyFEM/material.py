from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(kw_only=True)
class Material:
    """
    Base class for materials
    """
    name: str
    # Young's modulus
    young: float = field(default=False, init=False)
    # Poisson's ratio
    poisson: float = field(default=False, init=False)
    # Density
    density: float = field(default=False, init=False)
    # Shear Modulus
    G: float = field(default=False, init=False)
