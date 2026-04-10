from collections import deque

class Edge:
    def __init__(self, u, v, cap, flow=0, rev=None):
        self.u = u
        self.v = v
        self.cap = cap
        self.flow = flow
        self.rev = rev

def dinic_generator(graph, source, sink):
    adj = {}
    nodes = list(graph.keys())
    for u in nodes:
        adj[u] = []
        
    for u, edges in graph.items():
        for v, cap in edges:
            if v not in adj:
                adj[v] = []
                nodes.append(v)
            e1 = Edge(u, v, cap)
            e2 = Edge(v, u, 0)
            e1.rev = e2
            e2.rev = e1
            adj[u].append(e1)
            adj[v].append(e2)
            
    def get_graph_state(augmenting_path=None):
        state_graph = {}
        for u in nodes:
            state_graph[u] = []
            for e in adj[u]:
                if e.cap > 0: # Only include original forward edges
                    state_graph[u].append((e.v, e.cap, e.flow))
        return {
            "graph": state_graph,
            "augmenting_path": augmenting_path,
            "done": False
        }

    level = {}
    
    def bfs():
        for u in nodes:
            level[u] = -1
        level[source] = 0
        q = deque([source])
        while q:
            u = q.popleft()
            for e in adj[u]:
                if level[e.v] < 0 and e.flow < e.cap:
                    level[e.v] = level[u] + 1
                    q.append(e.v)
        return level[sink] >= 0

    def dfs(u, ptr, pushed, path):
        if u == sink or pushed == 0:
            return pushed
        for i in range(ptr[u], len(adj[u])):
            ptr[u] = i
            e = adj[u][i]
            if level[u] + 1 != level[e.v] or e.flow == e.cap:
                continue
            
            path.append(e)
            tr = dfs(e.v, ptr, min(pushed, e.cap - e.flow), path)
            if tr == 0:
                path.pop()
                continue
                
            e.flow += tr
            e.rev.flow -= tr
            return tr
        return 0

    max_flow = 0
    yield get_graph_state()

    while bfs():
        ptr = {u: 0 for u in nodes}
        while True:
            path = []
            pushed = dfs(source, ptr, float('inf'), path)
            if not pushed:
                break
            max_flow += pushed
            aug_path_nodes = [e.u for e in path] + [path[-1].v] if path else []
            yield get_graph_state(augmenting_path=aug_path_nodes)
            
    final_state = get_graph_state()
    final_state["done"] = True
    final_state["max_flow"] = max_flow
    yield final_state
