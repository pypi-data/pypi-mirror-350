import numpy as np


def Ux(x, N):
    from qiskit.circuit.library import UnitaryGate
    array = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -0.4762382 + 0.87931631j]])

    U = UnitaryGate(array)
    CU = U.controlled()

    k = 1
    while N > 2 ** k:
        k = k + 1

    u = np.zeros([2 ** k, 2 ** k], dtype=int)

    for i in range(N):
        u[x * i % N][i] = 1
    for i in range(N, 2 ** k):
        u[i][i] = 1

    XU = UnitaryGate(u).controlled()
    return XU