#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : components
# @Date : 2023
# @Project: pyFEM
# @AUTHOR : Jaakko Huusko
from dataclasses import dataclass

import numpy as np


@dataclass
class Point:
    X: float = 0
    Y: float = 0
    Z: float = 0

    def __array__(self) -> np.ndarray:
        return np.array([self.Z, self.Y, self.Z])


@dataclass
class Line:
    start_point: Point
    end_point: Point


@dataclass
class Material:
    E: float


@dataclass
class Profile:
    area: float
    Iy: float
    Iz: float
    Iyz: float
    It: float
    Iw: float


@dataclass
class CrossSection:
    material: Material
    profile: Profile


@dataclass
class Element:
    line: Line
    cross_section: CrossSection


if __name__ == '__main__':
    p1 = Point(1, 2, 3)
    p2 = Point(Z=100)
    l = Line(p1, p2)
    print(l)
