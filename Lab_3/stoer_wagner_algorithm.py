import os
import dimacs
from queue import PriorityQueue


class Node:
    def __init__(self):
        self.edges = {}  # słownik  mapujący wierzchołki do których są krawędzie na ich wagi
        self.active = True
        self.merged = []

    def add_edge(self, to, weight):
        self.edges[to] = self.edges.get(to, 0) + weight  # dodaj krawędź do zadanego wierzchołka
        # o zadanej wadze; a jeśli taka krawędź
        # istnieje, to dodaj do niej wagę

    def del_edge(self, to):
        del self.edges[to]                              # usuń krawędź do zadanego wierzchołka


def convert_graph(graph, n):
    converted_graph = [Node() for _ in range(n)]
    for x, y, c in graph:
        converted_graph[x - 1].add_edge(y - 1, c)
        converted_graph[y - 1].add_edge(x - 1, c)
    return converted_graph


def show_graph(graph):
    for vertex in graph:
        print(vertex.edges)


def merge_verticies(graph, x, y):
    if y in graph[x].edges.keys():
        graph[x].del_edge(y)
        graph[y].del_edge(x)

    for u, w in graph[x].edges.items():
        if graph[u].active:
            graph[y].add_edge(u, w)
            graph[u].add_edge(y, w)

    graph[y].merged.append(x)
    graph[x].active = False


def minimum_cut_phase(graph, n):
    a = [i for i, v in enumerate(graph) if v.active is True][0]
    S = []

    weight_sum = [0 for _ in range(len(graph))]
    visited = [False for _ in range(len(graph))]
    q = PriorityQueue()
    q.put((0, a))
    while len(S) < n:
        _, v = q.get()

        if visited[v]:
            continue
        S.append(v)

        visited[v] = True

        for u, w in graph[v].edges.items():
            if not visited[u] and graph[u].active:
                weight_sum[u] += w
                q.put((-weight_sum[u], u))

    s = S[-1]
    t = S[-2]

    result = sum([w for u, w in graph[s].edges.items() if graph[u].active])

    merge_verticies(graph, s, t)
    return result


def stoer_wagner(graph, n):
    best_result = float('inf')
    while n > 1:
        curr_result = minimum_cut_phase(graph, n)
        best_result = min(best_result, curr_result)
        n -= 1
    return best_result


def show_results(folder, skip=[]):
    files = os.listdir(f'{folder}')
    wrong = 0
    for file in files:
        if file in skip:
            continue
        wrong_message = ''
        V, graph = dimacs.loadDirectedWeightedGraph(f'{folder}\\{file}')
        s, t = 1, V

        result = stoer_wagner(convert_graph(graph, V), V)
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
    show_results('graphs', skip=['grid100x100'])
