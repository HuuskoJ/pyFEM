import numpy as np
from scipy import sparse


def static_load_analysis(K: np.array, F: np.array, B: np.array, ndof: int) -> tuple[np.array, np.array]:
    """
    Perform a static load analysis
    Returns:
        :U: global vector of nodal displacements
        :F_react: reaction loads
    """

    b = np.zeros((B.shape[0], 1))

    # Assemble the system of equations
    n_lr = B.shape[0]  # Number of linear constraints
    Z = np.zeros((n_lr, n_lr))
    # A_system = np.block([
    #     [K, B.T],
    #     [B, Z]
    # ])
    # A_system = sparse.csr_matrix(np.block([
    #     [K, B.T],
    #     [B, Z]
    # ]))
    # x_system = np.block([
    #     [F],  # + F_accel
    #     [b]
    # ])

    # A1 = np.concatenate((K, B.T), axis=1)
    # A2 = np.concatenate((B, Z), axis=1)
    # A_system = np.concatenate((A1, A2), axis=0)
    # x_system = np.concatenate((F, b), axis=0)

    # solution = np.linalg.solve(A_system, x_system)
    #
    # U = solution[0:ndof]
    # F_react = solution[ndof:]
    # return np.split(
    #     sparse.linalg.spsolve(
    #         A_system,
    #         x_system
    #     ),
    #     [ndof, ]
    # )
    return np.split(
        sparse.linalg.spsolve(
            sparse.csr_matrix(np.block([
                [K, B.T],
                [B, Z]
            ])),
            np.block([
                [F],  # + F_accel
                [b]
            ])
        ),
        [ndof, ]
    )
    # return np.split(np.linalg.solve(A_system, x_system), [ndof, ])


def global_stiffness_matrix(rows: np.array, cols: np.array, data_K: np.array) -> np.array:
    """

    """

    # K = sparse.coo_matrix((data_K.flatten(), (rows.flatten(), cols.flatten())), dtype=np.float_)
    # K = sparse.csr_matrix(K, dtype=np.float_)
    return sparse.csr_matrix(
        sparse.coo_matrix(
            (data_K.flatten(),
             (rows.flatten(),
              cols.flatten())
             ),
            dtype=np.float_),
        dtype=np.float_)
