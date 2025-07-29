# symbolic_factoring.py

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def COMPOSITE_q(n: int) -> bool:
    return not is_prime(n)

def is_mersenne(n: int) -> bool:
    if not is_prime(n):
        return False
    p, m = 1, 1
    while m < n:
        p += 1
        m = 2**p - 1
    return m == n

def is_twin_prime(n: int) -> bool:
    return is_prime(n) and (is_prime(n - 2) or is_prime(n + 2))

def prime_gaps(k: int) -> list[int]:
    gaps = []
    prev = None
    count = 0
    num = 1
    while count < k:
        num += 1
        if is_prime(num):
            if prev is not None:
                gaps.append(num - prev)
            prev = num
            count += 1
    return gaps

PRIME_FUNCTIONS = {
    'is_prime':      is_prime,
    'COMPOSITE?':    COMPOSITE_q,
    'MERSENNE':      is_mersenne,
    'TWIN':          is_twin_prime,
    'PRIME_GAPS':    prime_gaps,
}
