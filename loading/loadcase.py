from dataclasses import dataclass, field
from pyFEM.loading.loadtype import LoadTypeEnum

@dataclass
class LoadCase:

    load_type: LoadTypeEnum = None
    loads: list = field(default_factory=list)
