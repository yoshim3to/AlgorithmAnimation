# novel.py
# Push-Relabel Maximum Flow Algorithm
# A novel substitution for Dinic's algorithm (max flow).

class PushRelabel:
    def __init__(self, graph, source, sink):
        self.nodes = list(graph.keys())
        for u in graph:
            for v, _ in graph[u]:
                if v not in self.nodes:
                    self.nodes.append(v)
        self.n = len(self.nodes)
        self.source = source
        self.sink = sink
        self.capacity = {u: {v: 0 for v in self.nodes} for u in self.nodes}
        self.flow = {u: {v: 0 for v in self.nodes} for u in self.nodes}
        self.height = {u: 0 for u in self.nodes}
        self.excess = {u: 0 for u in self.nodes}

        for u in graph:
            for v, cap in graph[u]:
                self.capacity[u][v] += cap

    def push(self, u, v):
        send = min(self.excess[u], self.capacity[u][v] - self.flow[u][v])
        self.flow[u][v] += send
        self.flow[v][u] -= send
        self.excess[u] -= send
        self.excess[v] += send

    def relabel(self, u):
        min_height = float('inf')
        for v in self.nodes:
            if self.capacity[u][v] - self.flow[u][v] > 0:
                min_height = min(min_height, self.height[v])
        self.height[u] = min_height + 1

    def solve(self):
        self.height[self.source] = self.n
        self.excess[self.source] = float('inf')

        for v in self.nodes:
            if self.capacity[self.source][v] > 0:
                self.push(self.source, v)

        while True:
            excess_nodes = [u for u in self.nodes if u != self.source and u != self.sink and self.excess[u] > 0]
            if not excess_nodes:
                break
                
            u = excess_nodes[0]
            pushed = False
            for v in self.nodes:
                if self.capacity[u][v] - self.flow[u][v] > 0 and self.height[u] == self.height[v] + 1:
                    self.push(u, v)
                    pushed = True
                    break
            if not pushed:
                self.relabel(u)

        return sum(self.flow[self.source][v] for v in self.nodes)

def run_novel_algorithm(graph, source, sink):
    pr = PushRelabel(graph, source, sink)
    return pr.solve()

if __name__ == "__main__":
    test_graph = {
        'IN': [('A', 4), ('B', 3)],
        'A'     : [('C', 5)],
        'B'     : [('C', 7), ('D', 9)],
        'C'     : [('OUT', 8)],
        'D'     : [('E', 4)],
        'E'     : [('OUT', 6)],
        'OUT'   : []
    }
    max_flow = run_novel_algorithm(test_graph, 'IN', 'OUT')
    print(f"Max Flow computed by Push-Relabel (Novel Algorithm): {max_flow}")