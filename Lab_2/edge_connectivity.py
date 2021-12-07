import dimacs
import os
from queue import Queue
from copy import deepcopy


def convert_graph(init_graph, n):
    graph = [dict() for _ in range(n)]
    for edge in init_graph:
        graph[edge[0]-1][edge[1]-1] = graph[edge[0]-1].get(edge[1]-1, 1)
        graph[edge[1]-1][edge[0]-1] = graph[edge[1]-1].get(edge[0]-1, 1)

    return graph


def BFS(graph, n, s, t):
    queue = Queue()
    queue.put((s, float('inf')))
    visited = [False for _ in range(n)]
    parent = [None for _ in range(n)]
    visited[s] = True

    while not queue.empty():
        u, d_flow = queue.get()

        for v, w in graph[u].items():
            if not visited[v] and w != 0:
                visited[v] = True
                queue.put((v, min(d_flow, w)))
                parent[v] = u

                if v == t:
                    return True, min(d_flow, w), parent

    return False, 0, parent


def edmonds_karp(graph, s, t, n):
    while True:
        found, flow_to_add, parent = BFS(graph, n, s, t)
        if not found:
            break

        u = t
        while u != s:
            graph[u][parent[u]] += flow_to_add
            graph[parent[u]][u] -= flow_to_add
            u = parent[u]

    return sum([1 for value in graph[t].values() if value > 0])


def connectivity(graph, n):
    min_max_flow = float('inf')
    for u in range(1, n):
        min_max_flow = min(min_max_flow, edmonds_karp(deepcopy(graph), 0, u, n))
    return min_max_flow


def show_results(folder, skip=[]):
    files = os.listdir(f'{folder}')
    print(files)
    wrong = 0
    for file in files:
        if file in skip:
            continue
        wrong_message = ''
        V, graph = dimacs.loadDirectedWeightedGraph(f'{folder}\\{file}')

        result = connectivity(convert_graph(graph, V), V)
        right_answer = int(dimacs.readSolution(f'{folder}\\{file}'))

        if result != right_answer:
            wrong += 1
            wrong_message = '\tWRONG!!!'
        print('Graph:', file, '\tGiven answer:', result, '\tExpected answer:', right_answer, wrong_message)

    if wrong == 0:
        print('All answers are correct!')
    else:
        print(f'Given {wrong} wrong answers!')


if __name__ == '__main__':
    show_results('graphs/connectivity', ['grid100x100'])
