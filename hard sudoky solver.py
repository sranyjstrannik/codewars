import numpy as np
from copy import deepcopy
from functools import reduce


def so(pzl, sets, level=0):
    bestset = set(range(1, 10))
    index = (-1, -1)
    for i, row in enumerate(pzl):
        for j, item in enumerate(row):
            if not item:
                if len(bestset) > len(sets[i][j]):
                    bestset = sets[i][j]
                    index = (i, j)
    if index == (-1, -1): return pzl
    if len(bestset) == 0:
        return None

    # bestset found
    # now there is strong need to check if solution is only one
    check_if_not_unique_flag = False
    result = None

    for v in bestset:
        pzl_ = deepcopy(pzl)
        sets_ = deepcopy(sets)
        pzl_[index[0]][index[1]] = v
        for m in range(len(pzl[0])):
            sets_[index[0]][m] -= {v}
        for m in range(len(pzl)):
            sets_[m][index[1]] -= {v}
        ii, jj = index
        ii, jj = ii // 3, jj // 3
        for i1 in range(ii * 3, (ii + 1) * 3):
            for i2 in range(jj * 3, (jj + 1) * 3):
                sets_[i1][i2] -= {v}
        t = so(pzl_, sets_, level + 1)
        if t is not None:
            if check_if_not_unique_flag: raise Exception()
            check_if_not_unique_flag = True
            result = t
    return result


def set2(lst):
    from functools import reduce
    result = set()
    for i in lst:
        for j in i:
            result |= {j}
    return result


def sudoku_solver(puzzle):
    pzl = np.array(puzzle)
    print(pzl)
    # check dimensions
    if len(puzzle) != 9 or len(puzzle[0]) != 9:
        raise Exception()

    # check if all  elements are as required
    allinone = reduce(list.__add__, puzzle)
    if not all(isinstance(a, int) and 0 <= a < 10 for a in allinone):
        raise Exception()

    sets = [[set() for i in range(len(puzzle))] for j in range(len(puzzle[0]))]
    vert_sets = [set(i) - {0} for i in puzzle]
    horiz_sets = [set(i) - {0} for i in zip(*puzzle)]
    square_sets = [[set2(pzl[i * 3:(i + 1) * 3, j * 3:(j + 1) * 3]) - {0} for j in range(3)] for i in range(3)]

    bestset = set(range(1, 10))
    index = (-1, -1)
    for i, row in enumerate(pzl):
        # check if all non-zero elements in list are unique
        if len(set(row) - set([0])) != len(row) - (row == 0).sum():
            raise Exception()
        for j, item in enumerate(row):
            if item:
                sets[i][j] = set()
            else:
                sets[i][j] = set(range(1, 10)) - (vert_sets[i] | horiz_sets[j] | square_sets[i // 3][j // 3])
                if len(bestset) > len(sets[i][j]):
                    bestset = sets[i][j]
                    index = (i, j)
    for v in bestset:
        pzl_ = deepcopy(pzl)
        sets_ = deepcopy(sets)
        pzl_[index[0]][index[1]] = v
        sets_[index[0]][index[1]] = set()
        for m in range(len(pzl[0])):
            sets_[index[0]][m] -= {v}
        for m in range(len(pzl)):
            sets_[m][index[1]] -= {v}
        ii, jj = index
        ii, jj = ii // 3, jj // 3
        for i1 in range(ii * 3, (ii + 1) * 3):
            for i2 in range(jj * 3, (jj + 1) * 3):
                sets_[i1][i2] -= {v}
        t = so(pzl_, sets_)
        if isinstance(t, np.ndarray):
            return t.tolist()
    raise Exception()


puzzle = [[0, 0, 6, 1, 0, 0, 0, 0, 8],
          [0, 8, 0, 0, 9, 0, 0, 3, 0],
          [2, 0, 0, 0, 0, 5, 4, 0, 0],
          [4, 0, 0, 0, 0, 1, 8, 0, 0],
          [0, 3, 0, 0, 7, 0, 0, 4, 0],
          [0, 0, 7, 9, 0, 0, 0, 0, 3],
          [0, 0, 8, 4, 0, 0, 0, 0, 6],
          [0, 2, 0, 0, 5, 0, 0, 8, 0],
          [1, 0, 0, 0, 0, 2, 5, 0, 0]]

print(sudoku_solver(puzzle))