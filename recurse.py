def recurse(n):
    if n == 0:
        return 2
    out = 3 * (n - 1) + recurse(n - 1) + 1
    print(out, n)
    return out

recurse(2)