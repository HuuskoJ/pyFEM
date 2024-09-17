#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : result_beam
# @Date : 2022
# @Project: pyFEM
# @AUTHOR : Jaakko Huusko

from dataclasses import dataclass

import numpy as np


@dataclass
class ResultSection:
    """
    Class that handles section's forces
    """
    N: float = 0
    V_y: float = 0
    V_z: float = 0
    M_T: float = 0
    M_y: float = 0
    M_z: float = 0
    load_id: int = 0


@dataclass
class ResultBeam:
    """
    Class that handles beam's forces
    """
    sections: list[ResultSection]

