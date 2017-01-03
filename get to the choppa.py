import numpy as np
import json

def neighbors(node):
    n = node
    return [(n[0] - 1, n[1]), (n[0], n[1] + 1), (n[0] + 1, n[1]), (n[0], n[1] - 1)]


def find_shortest_path(grid, start_node, end_node, grid_optimum_path1=None):
    if not grid: return []
    m, n = len(grid), len(grid[0])
    if m > 100: return []

    def check(coords, m=m, n=n):
        return 0 <= coords[0] < m and 0 <= coords[1] < n

    arr = np.zeros((m, n), dtype=int)
    for i in range(m):
        for j in range(n):
            arr[i][j] = [-10000, 10000][grid[i][j].passable]

    start = [start_node.position.x, start_node.position.y]
    end = [end_node.position.x, end_node.position.y]
    q = [start]
    arr[start[0], start[1]] = 0
    while len(q):
        if arr[end[0], end[1]] < 10000:
            break
        e = q.pop(0)
        num = arr[e[0]][e[1]]
        for n in neighbors(e):
            if check(n):
                arr[n[0]][n[1]] = min(arr[n[0]][n[1]], num + 1)
                if arr[n[0]][n[1]] == num + 1: q.append([n[0], n[1]])
                # теперь нужно путь расшифровать шаг за шагом
    result = [end_node]
    last = end
    if arr[end[0], end[1]] < 10000:
        for i in range(arr[end[0], end[1]] - 1, -1, -1):
            for j in neighbors(last):
                if check(j):
                    if arr[j[0], j[1]] == i:
                        result = [grid[j[0]][j[1]]] + result
                        last = [j[0], j[1]]
        return result[:81]

    return []


class Position:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __str__(self):
        return "("+str(self.x)+","+str(self.y)+")"


class Ceil:
    def __init__(self,x,y):
        self.position = Position(x,y)
        self.passable = True

    def __str__(self):
        return [0,1][self.passable]

def make_grid(blueprint):
    strs = blueprint.split('\n')
    arr = [[Ceil(i,j) for j in range(len(strs[0]))] for i in range(len(strs))]
    for i,s in enumerate(strs):
        for j,c in enumerate(s):
            if c == '1': arr[i][j].passable = False
    return arr

blueprint = """S0110
01000
01010
00010
0001E"""

r = make_grid(blueprint)
for r in r:
    print(r)