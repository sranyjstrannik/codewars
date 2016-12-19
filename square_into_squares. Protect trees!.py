def decompose(n, flag=False):
    # if flag it means we will find decomposition for n below
    if flag:
        if int(n ** 0.5) ** 2 == n:
            return [round(int(n ** 0.5))]
        if n == 2: return None
        if n == 1: return [1]
        for i in range(n - 1, n//2, -1):
            if not (i ** 0.5) % 1:
                t = decompose(n - i, True)
                if t: return t+[round(i ** 0.5)]
        return None
    # if not flag it means we will find decomposition for n*n
    else:
        for i in range(n - 1, n//2, -1):
            t = decompose(n * n - i * i, True)
            if t:
                return t+[i]
        return None


print(decompose(11))
print(decompose(50))