#   Hyrrokkin - a library for building and running executable graphs
#
#   MIT License - Copyright (C) 2022-2025  Visual Topology Ltd

def is_prime(n):
    i = 2
    while i*i <= n:
        if n % i == 0:
            return False
        i += 1
    return True

def compute_factors(n):
    i = 2
    r = n
    factors = []
    if is_prime(r):
        return [r]
    while True:
        if r % i == 0:
            factors.append(i)
            r //= i
            if is_prime(r):
                break
        else:
            i += 1
    if r > 1:
        factors.append(r)
    return factors

if __name__ == '__main__':
    import sys
    import json
    n = int(sys.argv[1])
    factors = compute_factors(n)
    print(json.dumps(factors))