from dataclasses import dataclass, field


@dataclass
class Results:
    internal_forces: dict = field(default_factory=dict)
    support_reactions: dict = field(default_factory=dict)

"""

internal_forces = {}
    loadid : {
    
        Fx: 0
        Fy: 0
        Fz: 
        Mx:
        My:
        Mz
    }


"""