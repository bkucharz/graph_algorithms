# Dany jest graf nieskierowany G = (V,E), funkcja c: E -> N dająca wagi krawędziom, oraz wyróżnione wierzchołki s i t.
# Szukamy scieżki z s do t takiej, że najmniejsza waga krawędzi na tej ścieżce jest jak największa.
# Należy zwrócić najmniejszą wagę krawędzi na znalezionej ścieżce.


import dimacs
import os
from sys import setrecursionlimit

setrecursionlimit(2000)


def convert_graph(initial_graph, n):
    result_graph = [[] for _ in range(n)]

    for v1, v2, weight in initial_graph:
        result_graph[v1 - 1].append((v2 - 1, weight))
        result_graph[v2 - 1].append((v1 - 1, weight))

    return result_graph


def DFS(graph, s, t, k):
    n = len(graph)
    visited = [False for _ in range(n)]

    def DFS_visit(u, end):
        nonlocal visited

        if u == end:
            return True

        visited[u] = True

        for v, w in graph[u]:
            if not visited[v] and w >= k:
                if DFS_visit(v, end):
                    return True
        return False

    return DFS_visit(s, t)


def solution_binary_search(init_graph, s, t, n):
    graph = convert_graph(init_graph, n)
    weights = sorted(list(set([edge[2] for edge in init_graph])))
    l, r = 0, len(weights) - 1

    while l <= r:
        mid = (l + r)//2
        if DFS(graph, s, t, weights[mid]):
            l = mid + 1
        else:
            r = mid - 1
    return weights[r]


if __name__ == '__main__':
    files = os.listdir("graphs")
    wrong = 0
    for file in files:
        if file in ['grid100x100', 'rand1000_100000', 'path10000']:
            continue
        wrong_message = ''
        V, graph = dimacs.loadWeightedGraph(f'graphs\\{file}')
        s, t = 1, 2
        result = solution_binary_search(graph, s - 1, t - 1, V)
        right_answer = int(dimacs.readSolution(f'graphs\\{file}'))
        if result != right_answer:
            wrong += 1
            wrong_message = '\tWRONG!!!'
        print(file, 'Given answer:', result, '\tExpected answer:', right_answer, wrong_message)

    if wrong == 0:
        print('All answers are correct!')
    else:
        print(f'Given {wrong} wrong answers!')
