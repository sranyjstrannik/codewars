import numpy as np
import cProfile
# будем вдобавок хранить еще и суммы, чтоб

bigN = 50000000
a = np.array([0] * bigN, dtype=np.bool_)
a[0] = a[1] = True
for i in range(2, bigN):
    if not a[i]:
        a[i + i::i] = True


def profile(func):
    """Decorator for run function profile"""
    # скопирован отсюда https://habrahabr.ru/company/mailru/blog/202832/
    def wrapper(*args, **kwargs):
        profile_filename = func.__name__ + '.prof'
        profiler = cProfile.Profile()
        result = profiler.runcall(func, *args, **kwargs)
        profiler.dump_stats(profile_filename)
        return result
    return wrapper


@profile
def find_primes_sextuplet(sum_limit, a=a, bigN=bigN):
    start_from = 17 + (sum_limit - 4 - 6 - 10 - 12 - 16) // 6
    i = start_from
    if not i % 2: i += 1
    while i < bigN:
        if a[i] == a[i - 4] == a[i - 6] == a[i - 10] == a[i - 12] == a[i - 16] == False:
            return [i - 16, i - 12, i - 10, i - 6, i - 4, i]
        i += 2

@profile
def find_primes_sextupletG(sum_limit):
    global a, bigN
    start_from = 17 + (sum_limit - 4 - 6 - 10 - 12 - 16) // 6
    i = start_from
    if not i % 2: i += 1
    while i < bigN:
        if a[i] == a[i - 4] == a[i - 6] == a[i - 10] == a[i - 12] == a[i - 16] == False:
            return [i - 16, i - 12, i - 10, i - 6, i - 4, i]
        i += 2

@profile
def find_primes_sextuplet_1(sum_limit, a=a, bigN=bigN):
    start_from = 17 + (sum_limit - 4 - 6 - 10 - 12 - 16) // 6
    i = start_from
    if not i % 2: i += 1
    while i < bigN:
        if not a[i]:
            if not a[i - 4]:
                if not a[i - 6]:
                    if not a[i - 10]:
                        if not a[i - 12]:
                            if not a[i - 16]:
                                return [i - 16, i - 12, i - 10, i - 6, i - 4, i]
        i += 2


@profile
def find_primes_sextuplet_1G(sum_limit):
    global a, bigN
    start_from = 17 + (sum_limit - 4 - 6 - 10 - 12 - 16) // 6
    i = start_from
    if not i % 2: i += 1
    while i < bigN:
        if not a[i]:
            if not a[i - 4]:
                if not a[i - 6]:
                    if not a[i - 10]:
                        if not a[i - 12]:
                            if not a[i - 16]:
                                return [i - 16, i - 12, i - 10, i - 6, i - 4, i]
        i += 2

t = find_primes_sextuplet(29700000)
t = find_primes_sextuplet_1(29700000)
# Ха, разница больше чем в тридцать раз
# TODO: почитать про то, как устроенно вычисление условных выражений в питоне

# для интереса еще можно посмотреть, что будет, если a и bigN выставить global
t = find_primes_sextupletG(29700000)
t = find_primes_sextuplet_1G(29700000)
# Да, разница есть, причем значительная: ~25%
