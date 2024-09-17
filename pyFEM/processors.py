#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : processors
# @Date : 2023
# @Project: pyFEM
# @AUTHOR : Jaakko Huusko
import esper
from components import Material, Section, Line
import elem_funcs as ef

class ElementProcessor:
    ...


class LocalStiffnessMatrixProcessor(esper.Processor):
    world: esper.World


    def process(self, *args, **kwargs):
        for ent, (mat, sect, line) in self.world.get_components(Material, Section, Line):
            lsm = ef.local_stiffness_matrix(mat.E,
                                            mat.A,
                                            mat.G,
                                            sect.Iy,
                                            sect.Iz,
                                            sect.J,
                                            ef.line_length(line.P1, line.P2)
                                            )