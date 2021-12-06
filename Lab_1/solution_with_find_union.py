# Dany jest graf nieskierowany G = (V,E), funkcja c: E -> N dająca wagi krawędziom, oraz wyróżnione wierzchołki s i t.
# Szukamy scieżki z s do t takiej, że najmniejsza waga krawędzi na tej ścieżce jest jak największa.
# Należy zwrócić najmniejszą wagę krawędzi na znalezionej ścieżce.


import dimacs
import os


class Node:
    def __init__(self, val=None):
        self.val = val
        self.rank = 0
        self. parent = self


def find(x):
    if x != x.parent:
        x.parent = find(x.parent)

    return x.parent

def union(x, y):
    x = find(x)
    y = find(y)
    if x == y:
        return
    if x.rank > y.rank:
        y.parent = x
    else:
        x.parent = y
        if x.rank == y.rank:
            y.rank += 1


def solution_find_union(graph, s, t, n):
    vertex_sets = [Node(i) for i in range(n)]

    A = vertex_sets[s]
    B = vertex_sets[t]

    sorted_graph = sorted(graph, key=lambda x: x[2], reverse=True)

    for edge in sorted_graph:
        v1, v2 = vertex_sets[edge[0] - 1], vertex_sets[edge[1] - 1]
        union(v1, v2)
        if find(A) is find(B):
            return edge[2]


if __name__ == '__main__':
    files = os.listdir("graphs")
    wrong = 0
    for file in files:
        wrong_message = ''
        V, graph = dimacs.loadWeightedGraph(f'graphs\\{file}')
        s, t = 1, 2
        result = solution_find_union(graph, s - 1, t - 1, V)
        right_answer = int(dimacs.readSolution(f'graphs\\{file}'))
        if result != right_answer:
            wrong += 1
            wrong_message = '\tWRONG!!!'
        print('Given answer:', result, '\tExpected answer:', right_answer, wrong_message)

    if wrong == 0:
        print('All answers are correct!')
    else:
        print(f'Given {wrong} wrong answers!')
