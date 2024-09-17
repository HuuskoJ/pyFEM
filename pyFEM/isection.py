from dataclasses import dataclass
from pyFEM.section import BaseSection
import numpy as np


def area(h, b, tf, tw, r):
    # Area of section [mm^2]
    A = 2.0 * tf * b + (h - 2.0 * tf) * tw + (4.0 - np.pi) * r ** 2.0
    return A


def shear_area(h, b, tf, tw, r):
    # Shear area of section [mm^2]
    Ashear = A - 2.0 * b * tf + (tw + 2.0 * r) * tf
    return Ashear


def perimeter(h, b, tf, tw, r):
    # Perimeter of cross-section
    Au = 4 * (b - 2 * r) + 2 * (h - 2 * tw) + 2 * np.pi * r


def Iy(h, b, tf, tw, r):
    # Second moment of area, I_y is stronger direction [mm^4]
    Iy = 1.0 / 12.0 * (b * h ** 3.0 - (b - tw) * (
                h - 2.0 * tf) ** 3.0) + 0.03 * r ** 4 + 0.2146 * r ** 2.0 * (
                 h - 2.0 * tf - 0.4468 * r) ** 2.0
    return Iy


def Iz(h, b, tf, tw, r):
    # Second moment of area, I_y is stronger direction [mm^4]
    Iz = 1.0 / 12.0 * (2.0 * tf * b ** 3.0 + (
                h - 2.0 * tf) * tw ** 3.0) + 0.03 * r ** 4.0 + 0.2146 * r ** 2.0 * (
                 tw + 0.4468 * r) ** 2.0
    return Iz


def It(h, b, tf, tw, r):
    # Torsional constant [mm^4]
    a1 = -0.042 + 0.2204 * tw / tf + 0.1355 * r / tf - 0.0865 * r * tw / tf ** 2 - 0.0725 * tw ** 2 / tf ** 2
    D1 = ((tf + r) ** 2 + (r + 0.25 * tw) * tw) / (2 * r + tf)
    It = 2.0 / 3.0 * b * tf ** 3 + (
                h - 2 * tf) * tw ** 3 / 3.0 + 2 * a1 * D1 ** 4 - 0.420 * tf ** 4
    return It


def Iw(h, b, tf, tw, r):
    # Warping constant [mm^6]
    Iw = (tf * b ** 3.0) / 24.0 * (h - tf) ** 2.0
    return Iw


def Wply(h, b, tf, tw, r):
    # Plastic section modulus [mm^3]
    Wply = (tw * h ** 2.0) / 4.0 + (b - tw) * (h - tf) * tf + (
                4.0 - np.pi) / 2.0 * r ** 2.0 * (h - 2.0 * tf) + (
                   3.0 * np.pi - 10.0) / 3.0 * r ** 3.0
    return Wply


def Wplz(h, b, tf, tw, r):
    # Plastic section modulus [mm^3]
    Wplz = (b ** 2.0 * tf) / 2.0 + (
                h - 2.0 * tf) / 4.0 * tw ** 2.0 + r ** 3.0 * (
                       10.0 / 3.0 - np.pi) + (
                   2.0 - np.pi / 2.0) * tw * r ** 2.0
    return Wplz


def Wely(h, b, tf, tw, r):
    # Elastic section modulus [mm^3]
    Wely = Iy(h, b, tf, tw, r) / (0.5 * h)
    return Wely


def Welz(h, b, tf, tw, r):
    # Elastic section modulus [mm^3]
    Welz = Iz(h, b, tf, tw, r) / (0.5 * b)
    return Welz


@dataclass
class ISection(BaseSection):
    sect_type: str
    h: float
    b: float
    tw: float
    tf: float
    r: float

    @property
    def dimensions(self):
        return self.h, self.b, self.tf, self.tw, self.r

    @property
    def A(self):
        return area(*self.dimensions)

    @property
    def Iy(self):
        return Iy(*self.dimensions)

    @property
    def Iz(self):
        return Iz(*self.dimensions)

    @property
    def I(self):
        return self.Iy, self.Iz

    @property
    def It(self):
        return It(*self.dimensions)

    @property
    def name(self):
        return self.sect_type + " " + str(self.h)
