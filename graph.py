import json
import heapq
from data_structure import CustomHashMap, LinkedList, CustomArray, CustomMinHeap

class Node:
    def __init__(self, node_id, node_type):
        self.id = node_id
        self.type = node_type


class Edge:
    def __init__(self, u, v, energy=0, capacity=float("inf"),bidirectional=False, restricted=False):
        self.u = u
        self.v = v
        self.energy = energy
        self.capacity = capacity
        self.bidirectional = bidirectional
        self.restricted = restricted


class Graph:
    def __init__(self):
        self.nodes = CustomHashMap()              # id → Node
        self.adj = CustomHashMap()                # id → list of Edge


    # B1: Load graph from JSON file
    def load_json(self, filepath):
        with open(filepath, "r") as f:
            data = json.load(f)

        # Read nodes
        for n in data["nodes"]:
            self.add_node(n["id"], n["type"])

        # Read edges
        for e in data["edges"]:
            self.add_edge(
                e["from"],
                e["to"],
                energy=e.get("energy", 0),
                capacity=e.get("capacity", float("inf")),
                bidirectional=e.get("bidirectional", False)
            )


    # B2: No-fly zones (restrict edges)
    def set_restricted(self, u, v, restricted=True):
        for e in self.adj[u]:
            if e.v == v:
                e.restricted = restricted


    
    # B3: Modify & extend network
    def add_node(self, node_id, node_type="unknown"):
        if self.nodes.search(node_id) is None:
            self.nodes.insert(node_id, Node(node_id, node_type))
            self.adj.insert(node_id, [])

    def add_edge(self, u, v, energy=0, capacity=float("inf"), bidirectional=False):
        adj_u = self.adj.search(u)
        # if adj_u is None:
        #     adj_u = []
        # self.adj.insert(u, adj_u)

        adj_u.append(Edge(u, v, energy, capacity, bidirectional))

        if bidirectional:
            adj_v = self.adj.search(v)
            # if adj_v is None:
            #     adj_v = []
            #     self.adj.insert(v, adj_v)

            adj_v.append(Edge(v, u, energy, capacity, bidirectional))

    
    # F1: Check reachability from a hub
    def check_delivery_reachability(self, start="HUB"):
        visited = set()
        stack = [start]

        while stack:
            u = stack.pop()
            if u in visited:
                continue
            visited.add(u)

            edges = self.adj.search(u)
            if edges is None:
                    continue

            for e in edges:
                if not e.restricted:
                    stack.append(e.v)

        all_delivery = LinkedList()
        for (node_id, node_obj) in self.nodes.items():
            if node_obj.type == "delivery":
                all_delivery.append(node_id)

        
        unreachable_delivery = LinkedList()
        current = all_delivery.head
        while current:
            did = current.data
            if did not in visited:
                unreachable_delivery.append(did)
            current = current.next

        if unreachable_delivery.head is None:
            return f"All delivery nodes are reasonable from {start}."
        
        names = LinkedList()
        current = unreachable_delivery.head
        while current:
            names.append(current.data)
            current = current.next

        return "Unreachable delivery nodes: " + ", ".join(names)

    # F2: Shortest path (Dijkstra using energy)
    def dijkstra(self, start, target):
        pq = CustomMinHeap()
        pq.push(0, (start, []))  # (cost, (current_node, path_so_far))

        visited = set()

        while not pq.is_empty():
            cost, (u, path) = pq.pop()
            if u in visited:
                continue
            visited.add(u)

            path = path + [u]

            if u == target:
                return cost, path

            edges = self.adj.search(u)
            if edges is None:
                continue

            for e in edges:
                if not e.restricted:
                    pq.push(cost + e.energy, (e.v, path))

        return float("inf"), []  # no path
    
    # F3: calculate max-flow
    def _ensure_map(self, cmap, key):
        existing = cmap.search(key)
        if existing is None:
            inner = CustomHashMap()
            cmap.insert(key, inner)
            return inner
        return existing
    
    def _bfs_flow(self, residual, source, sink):
        visited = CustomHashMap()
        parent = CustomHashMap()

        queue = CustomArray()
        queue.append(source)
        visited.insert(source, True)

        while len(queue) > 0:
            u = queue.get(0)
            for i in range(1, len(queue)):
                queue.set(i-1, queue.get(i))
            queue.size -= 1
            queue.set(queue.size, None)

            neighbors = residual.search(u)
            if neighbors is None:
                continue

            for v, cap in neighbors.items():
                if cap > 0 and visited.search(v) is None:
                    visited.insert(v, True)
                    parent.insert(v, u)
                    queue.append(v)
                    if v == sink:
                        return parent

        return None

    def calculate_delivery_capacity(self, start_hub, area_nodes):
        INF = 10**12  

        residual = CustomHashMap()

        for u, edges in self.adj.items():
            inner = self._ensure_map(residual, u)
            for e in edges:
                if e.restricted:
                    continue
                
                # existing = inner.search(e.v)
                # if existing is None:
                #     inner.insert(e.v, e.capacity)
                # else:
                #     inner.insert(e.v, existing + e.capacity)
                inner.insert(e.v, e.capacity)
                
                back = self._ensure_map(residual, e.v)
                if back.search(u) is None:
                    back.insert(u, 0)


        super_sink = "SUPER_SINK"
        self._ensure_map(residual, super_sink)

        for node in area_nodes:
            inner = self._ensure_map(residual, node)
            if inner.search(super_sink) is None:
                inner.insert(super_sink, INF)
            back = self._ensure_map(residual, super_sink)
            if back.search(node) is None:
                back.insert(node, 0)

        max_flow = 0


        while True:
            parent = self._bfs_flow(residual, start_hub, super_sink)
            if parent is None:
                break


            flow = INF
            v = super_sink
            while parent.search(v) is not None:
                u = parent.search(v)
                cap = residual.search(u).search(v)
                if cap < flow:
                    flow = cap
                v = u

            v = super_sink
            while parent.search(v) is not None:
                u = parent.search(v)
                forward_map = residual.search(u)
                backward_map = residual.search(v)

                forward_cap = forward_map.search(v)
                backward_cap = backward_map.search(u)

                forward_map.insert(v, forward_cap - flow)
                backward_map.insert(u, backward_cap + flow)

                v = u

            max_flow += flow

        return max_flow, residual
    
    # F4: min-cut
    def _extract_min_cut(self, residual, source):
        # BFS to find reachable nodes in residual graph
        visited = CustomHashMap()
        queue = CustomArray()
        queue.append(source)
        visited.insert(source, True)

        while len(queue) > 0:
            u = queue.get(0)
            # pop front manually
            for i in range(1, len(queue)):
                queue.set(i-1, queue.get(i))
            queue.size -= 1
            queue.set(queue.size, None)

            neighbors = residual.search(u)
            if neighbors is None:
                continue

            for v, cap in neighbors.items():
                if cap > 0 and visited.search(v) is None:
                    visited.insert(v, True)
                    queue.append(v)

        # Build cut set
        cut_edges = CustomArray()

        # All edges from visited → NOT visited in original graph
        for u, edges in self.adj.items():
            if visited.search(u) is None:
                continue
            for e in edges:
                v = e.v
                if visited.search(v) is None:
                    cut_edges.append((u, v))

        return cut_edges


