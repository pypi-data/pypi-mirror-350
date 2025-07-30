import numpy as np


def bin2dec(number:str) -> int:
    return sum([int(digit) * 2 ** i for i, digit in enumerate(number[::-1])])


def dec2bin(number:int, digits:int) -> str:
    return bin(number)[2:].zfill(digits)


def print_statevector(statevector, decimals=3, ignore_zero_amps=True):
    def for_loop(n, N, ignore_zero_amps=ignore_zero_amps):
        start_index=1
        if ignore_zero_amps:
            for i in range(N):
                const = np.round(data[i], decimals)
                if abs(const) <= 1e-3:
                    continue
                else:
                    sv_str = f"{const} |{bin(i)[2:].zfill(n)}⟩"
                    start_index=i+1
                    break
        else:
            const = np.round(data[0], decimals)
            sv_str = f"{const} |{bin(0)[2:].zfill(n)}⟩"

        for i in range(start_index, N):
            const = np.round(data[i], decimals)
            if ignore_zero_amps and abs(const) <= 1e-3:
                    continue
            if const.real < 0:
                sv_str += f" - {-1 * const} |{bin(i)[2:].zfill(n)}⟩"
            else:
                sv_str += f" + {const} |{bin(i)[2:].zfill(n)}⟩"
        return sv_str

    n = len(statevector.dims())
    N = int(2 ** n)
    data = statevector.data
    if N <= 64:
        sv_str = for_loop(n, N, ignore_zero_amps=ignore_zero_amps)
    else:
        sv_str = for_loop(n, N, ignore_zero_amps=True)
        const = np.round(data[-1], decimals)
        if const.real < 0:
            sv_str += f" + ... - {-1 * const} |{bin(N - 1)[2:].zfill(n)}⟩"
        else:
            sv_str += f" + ... + {const} |{bin(N - 1)[2:].zfill(n)}⟩"
    print(sv_str)


def continuous_fractions(frac, tol=0.0001):
    cf = []
    while True:
        int_part = int(frac)
        float_part = frac - int_part
        if float_part < tol:
            break
        if np.ceil(frac) - frac < tol:
            int_part = round(frac)
        cf.append(int_part)
        frac = float_part ** -1
    return cf


def get_convergents(cont_fracs):
    from fractions import Fraction
    c = []
    convergents = []
    for i in range(len(cont_fracs)):
        c.append(cont_fracs[i])
        for j in range(i - 1, -1, -1):
            c[i] = cont_fracs[j] + 1 / c[i]
        convergents.append(Fraction(c[i]).limit_denominator(10000))
    return convergents


def get_ratios(phase: float):
    cont_fracs = continuous_fractions(phase)
    convergents = get_convergents(cont_fracs)
    ratios = []
    for number in convergents:
        ratios.append({"numerator": number.numerator, "denominator": number.denominator})
    return ratios
