import numpy as np
from scipy.linalg import qr


def get_phase(arraylike_object:np.ndarray) -> float:
    if len(arraylike_object.shape) == 2:
        z = arraylike_object[-1, -1]
    elif len(arraylike_object.shape) == 1:
        z = arraylike_object[-1]
    phi = np.arctan(z.imag / z.real)
    if z.real < 0:
        phi += np.pi
    elif z.real > 0 > z.imag:
        phi += 2 * np.pi
    return phi


# randomly create a NxN-dimensional unitary operator
def random_unitary(num_qubits=1, dtype="float"):
    assert num_qubits >= 1, f"num_qubits should be greater than or equal to 1."
    if dtype == "float":
        N = int(2 ** num_qubits)
        H = np.random.randn(N, N)
        Q, R = qr(H)
    elif dtype == "complex":
        N = int(2 ** num_qubits)
        H_real = np.random.randn(N, N)
        H_imag = np.random.randn(N, N)
        Q, R = qr(H_real + 1j*H_imag)
    else:
        raise AttributeError(f"dtype should be either 'float' or 'complex', not {dtype}")
    return Q


# create a NxN-dimensional unitary operator whose diagonal entries are 1 and the last one is a random phase
def random_phase_unitary(num_qubits=1):
    assert num_qubits >= 1, f"num_qubits should be greater than or equal to 1."
    phi = np.random.randint(0, 359)
    N = int(2 ** num_qubits)
    U = np.eye(N=N, dtype="complex")
    U[-1, -1] = np.exp(1j*phi)
    return U


# randomly create a N-dimensional quantum state
def random_state(num_qubits=1, dtype="float"):
    assert num_qubits >= 1, f"num_qubits should be greater than or equal to 1."
    if dtype == "float":
        angle = 2 * np.pi * np.random.random()
        state = np.array([np.cos(angle), np.sin(angle)])
        if num_qubits == 1:
            return state
        else:
            for _ in range(num_qubits - 1):
                angle = 2 * np.pi * np.random.random()
                state = np.kron(state, np.array([np.cos(angle), np.sin(angle)]))
            return state
    elif dtype == "complex":
        return random_state(num_qubits) + 1j * random_state(num_qubits)
    else:
        raise AttributeError(f"dtype should be either 'float' or 'complex', not {dtype}")


def order_finder_unitary(x,N):
    k = int(np.ceil(np.log2(N)))
    Ux = np.zeros([2 ** k, 2 ** k], dtype = int)
    for i in range(N):
        Ux[x * i % N][i] = 1
    for i in range(N, 2**k):
        Ux[i][i] = 1
    return Ux
