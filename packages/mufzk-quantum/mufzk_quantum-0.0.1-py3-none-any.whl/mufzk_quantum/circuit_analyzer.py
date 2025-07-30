import numpy as np


def get_unitary(*ops):
    n = len(ops)
    if n == 1:
        return ops
    elif n > 1:
        result = np.kron(ops[0], ops[1])
        if n == 2:
            return result
        else:
            for i in range(2, n):
                result = np.kron(result, ops[i])
            return result
    else:
        raise ValueError("You must provide at least 1 operator to be tensor-product.")

