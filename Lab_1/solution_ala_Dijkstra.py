# Dany jest graf nieskierowany G = (V,E), funkcja c: E -> N dająca wagi krawędziom, oraz wyróżnione wierzchołki s i t.
# Szukamy scieżki z s do t takiej, że najmniejsza waga krawędzi na tej ścieżce jest jak największa.
# Należy zwrócić najmniejszą wagę krawędzi na znalezionej ścieżce.


import dimacs
import os
from queue import PriorityQueue


def convert_graph(initial_graph, n):
    result_graph = [[] for _ in range(n)]

    for v1, v2, weight in initial_graph:
        result_graph[v1 - 1].append((v2 - 1, weight))
        result_graph[v2 - 1].append((v1 - 1, weight))

    return result_graph


def solution_Dijkstra(graph, s, t, n):
    visited = [False for _ in range(n)]
    values = [0 for _ in range(n)]
    q = PriorityQueue()
    q.put((-float('inf'), s))

    while True:
        u_value, u = q.get()
        u_value = -u_value
        visited[u] = True

        for v, w in graph[u]:
            if not visited[v]:
                if min(w, u_value) > values[v]:
                    values[v] = min(w, u_value)
                    q.put((-values[v], v))
        if u == t:
            break

    return values[t]


if __name__ == '__main__':
    files = os.listdir("graphs")
    wrong = 0
    for file in files:
        wrong_message = ''
        V, graph = dimacs.loadWeightedGraph(f'graphs\\{file}')
        s, t = 1, 2
        result = solution_Dijkstra(convert_graph(graph, V), s - 1, t - 1, V)
        right_answer = int(dimacs.readSolution(f'graphs\\{file}'))
        if result != right_answer:
            wrong += 1
            wrong_message = '\tWRONG!!!'
        print('Given answer:', result, '\tExpected answer:', right_answer, wrong_message)

    if wrong == 0:
        print('All answers are correct!')
    else:
        print(f'Given {wrong} wrong answers!')
