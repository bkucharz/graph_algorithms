import dimacs
import os


def convert_graph(init_graph, n):
    graph = [dict() for _ in range(n)]
    for edge in init_graph:
        graph[edge[0]-1][edge[1]-1] = graph[edge[0]-1].get(edge[1]-1, edge[2])
        graph[edge[1]-1][edge[0]-1] = graph[edge[1]-1].get(edge[0]-1, 0)

    return graph


def DFS(graph, n, s, t):
    visited = [False for _ in range(n)]
    parent = [None for _ in range(n)]

    def DFS_visit(u, min_w):
        nonlocal parent

        if u == t:
            return True, min_w

        visited[u] = True

        for v, w in graph[u].items():
            if not visited[v] and graph[u][v] != 0:
                parent[v] = u
                found, flow = DFS_visit(v, min(min_w, w))
                if found:
                    return True, flow
        return False, 0

    found, d_flow = DFS_visit(s, float('inf'))
    return found, d_flow, parent


def ford_fulkerson(graph, s, t, n):
    while True:
        found, flow_to_add, parent = DFS(graph, n, s, t)
        if not found:
            break

        u = t
        while u != s:
            graph[u][parent[u]] += flow_to_add
            graph[parent[u]][u] -= flow_to_add
            u = parent[u]
    a = sum(graph[t].values())
    return a


def show_results(folder, skip=[]):
    files = os.listdir(f'{folder}')
    wrong = 0
    for file in files:
        if file in skip:
            continue
        wrong_message = ''
        V, graph = dimacs.loadDirectedWeightedGraph(f'{folder}\\{file}')
        s, t = 1, V

        result = ford_fulkerson(convert_graph(graph, V), s-1, t-1, V)
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
    show_results('graphs/flow')
