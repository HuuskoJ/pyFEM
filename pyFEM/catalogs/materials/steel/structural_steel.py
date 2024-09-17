#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : steel
# @Date : 2022
# @Project: pyFEM
# @AUTHOR : Jaakko Huusko

from pyFEM.steel_material import StructuralSteel

S235: StructuralSteel = StructuralSteel(name="S235", fy=235, fu=360)
S275: StructuralSteel = StructuralSteel(name="S275", fy=275, fu=430)
S355: StructuralSteel = StructuralSteel(name="S355", fy=355, fu=490)
S450: StructuralSteel = StructuralSteel(name="S450", fy=440, fu=550)
# EN10025-3, t <= 40
S275N: StructuralSteel = StructuralSteel(name="S275N", fy=275, fu=370)
S355N: StructuralSteel = StructuralSteel(name="S355N", fy=355, fu=470)
S420N: StructuralSteel = StructuralSteel(name="S420N", fy=420, fu=520)
S460N: StructuralSteel = StructuralSteel(name="S460N", fy=460, fu=540)
# EN10219-1
S235H: StructuralSteel = StructuralSteel(name="S235H", fy=235, fu=360)
S275H: StructuralSteel = StructuralSteel(name="S275H", fy=275, fu=430)
S355H: StructuralSteel = StructuralSteel(name="S355H", fy=355, fu=510)
S275MH: StructuralSteel = StructuralSteel(name="S275MH", fy=275, fu=360)
S355MH: StructuralSteel = StructuralSteel(name="S355MH", fy=355, fu=470)
S420MH: StructuralSteel = StructuralSteel(name="S420MH", fy=420, fu=500)
S46M0H: StructuralSteel = StructuralSteel(name="S460MH", fy=460, fu=530)
