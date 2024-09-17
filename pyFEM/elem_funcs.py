import numpy as np

# from numba import njit
from pyFEM.coordinate_system import CoordinateSystem


def unit_vector(vector: np.ndarray) -> np.ndarray:
    """
    Returns the unit vector of given vector
    """

    return vector / np.linalg.norm(vector)


def line_length(p1: np.array, p2:np.array) -> float:
    return np.linalg.norm(p1, p2)

def local_stiffness_matrix(E: float, A: float, G: float, Iy: float, Iz: float,
                           J: float, L: float) -> np.ndarray:
    """
    Calculates local stiffness matrix
    """
    EA = E * A
    EIy = E * Iy
    EIz = E * Iz
    GJ = G * J
    L2 = L ** 2
    L3 = L ** 3

    # Initialize 12x12 matrix with zeros
    k_elem = np.zeros((12, 12))
    # Fill the upper right triangle of matrix
    k_elem[0, 0] = EA / L
    k_elem[0, 6] = -EA / L
    k_elem[1, 1] = 12 * EIz / L3
    k_elem[1, 5] = 6 * EIz / L2
    k_elem[1, 7] = -12 * EIz / L3
    k_elem[1, 11] = 6 * EIz / L2
    k_elem[2, 2] = 12 * EIy / L3
    k_elem[2, 4] = -6 * EIy / L2
    k_elem[2, 8] = -12 * EIy / L3
    k_elem[2, 10] = -6 * EIy / L2
    k_elem[3, 3] = GJ / L
    k_elem[3, 9] = -GJ / L
    k_elem[4, 4] = 4 * EIy / L
    k_elem[4, 8] = 6 * EIy / L2
    k_elem[4, 10] = 2 * EIy / L
    k_elem[5, 5] = 4 * EIz / L
    k_elem[5, 7] = -6 * EIz / L2
    k_elem[5, 11] = 2 * EIz / L
    k_elem[6, 6] = EA / L
    k_elem[7, 7] = 12 * EIz / L3
    k_elem[7, 11] = -6 * EIz / L2
    k_elem[8, 8] = 12 * EIy / L3
    k_elem[8, 10] = 6 * EIy / L2
    k_elem[9, 9] = GJ / L
    k_elem[10, 10] = 4 * EIy / L
    k_elem[11, 11] = 4 * EIz / L

    # Local stiffness matrix is symmetrical along diagonal
    # add transpose of the upper triangle
    k_elem += np.triu(k_elem, k=1).T
    return k_elem


def stiffness_matrix(T: np.ndarray,
                     k0: np.ndarray) -> np.ndarray:
    """
    Computes element's global stiffness matrix

    :param T: element's transformation matrix
    :param k0: element's local stiffness matrix
    :return: element's global stiffness matrix
    """
    # ke = T.transpose().dot(k0.dot(T))

    return T.transpose().dot(k0.dot(T))


def direction_cosine(vector1: np.ndarray, vector2: np.ndarray) -> np.ndarray:
    """ Calculates direction cosines between two vectors """
    #v1_unit = unit_vector(vector1)
    #v2_unit = unit_vector(vector2)

    return np.clip(
        np.dot(unit_vector(vector1), unit_vector(vector2)),
        a_min=-1.0,
        a_max=1.0)


def vector_projection(vector1: np.ndarray, vector2: np.ndarray) -> np.ndarray:
    """
    Return the vector projection from vector1 onto vector2
    https://en.wikipedia.org/wiki/Vector_projection
    """

    # a1 = np.dot(vector1, unit_vector(vector2)) * unit_vector(vector2)
    return np.dot(vector1, unit_vector(vector2)) * unit_vector(vector2)


def vector_rejection(vector1: np.ndarray, vector2: np.ndarray) -> np.ndarray:
    """
    Return the vector rejection from vector1 onto vector2
    https://en.wikipedia.org/wiki/Vector_projection
    """

    # a1 = vector_projection(vector1, vector2)
    return vector1 - vector_projection(vector1, vector2)


def direction_cosine_matrix(local_coordinate_system: CoordinateSystem,
                            global_coordinate_system: CoordinateSystem) -> np.ndarray:
    """
    Calculates direction cosine matrix
    :param l_system:
    :param g_system:
    :return:
    """
    lx = direction_cosine(local_coordinate_system.X, global_coordinate_system.X)
    ly = direction_cosine(local_coordinate_system.Y, global_coordinate_system.X)
    lz = direction_cosine(local_coordinate_system.Z, global_coordinate_system.X)
    mx = direction_cosine(local_coordinate_system.X, global_coordinate_system.Y)
    my = direction_cosine(local_coordinate_system.Y, global_coordinate_system.Y)
    mz = direction_cosine(local_coordinate_system.Z, global_coordinate_system.Y)
    nx = direction_cosine(local_coordinate_system.X, global_coordinate_system.Z)
    ny = direction_cosine(local_coordinate_system.Y, global_coordinate_system.Z)
    nz = direction_cosine(local_coordinate_system.Z, global_coordinate_system.Z)

    return np.array([[lx, mx, nx],
                     [ly, my, ny],
                     [lz, mz, nz]])


def transformation_matrix(local_coordinate_system: CoordinateSystem,
                          global_coordinate_system: CoordinateSystem) -> np.ndarray:
    """ Calculates transformation matrix from local to global coordinates

        Returns:
        --------
        :return: element's transformation matrix
        :rtype: np.array

     """
    dir_cos_matrix = direction_cosine_matrix(local_coordinate_system,
                                             global_coordinate_system)

    t_matrix = np.zeros((12, 12))
    t_matrix[0:3, 0:3] = t_matrix[3:6, 3:6] = t_matrix[6:9, 6:9] = t_matrix[9:12, 9:12] = dir_cos_matrix
    return t_matrix
