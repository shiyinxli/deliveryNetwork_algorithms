import json
import heapq
import networkx as nx
import matplotlib.pyplot as plt
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
        self.node_count = 0
        self.edge_count = 0


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
            self.node_count += 1

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
        
        names = []
        current = unreachable_delivery.head
        while current:
            names.append(current.data)
            current = current.next

        return "Unreachable delivery nodes: " + ", ".join(names)

    # F2: Shortest path (Dijkstra using energy)
    def dijkstra(self, start, target):
        pq = CustomMinHeap()
        pq.push(0, start)

        visited = set()
        prev = CustomHashMap()
        dist = CustomHashMap()
        dist.insert(start, 0)

        while not pq.is_empty():
            cost, u = pq.pop()
            if u in visited:
                continue
            visited.add(u)

            if u == target:
                path = []
                cur = target
                while cur is not None:
                    path.append(cur)
                    cur = prev.search(cur)
                path.reverse()
                return cost, path
            
            edges = self.adj.search(u)
            if edges is None:
                continue

            for e in edges:
                if not e.restricted:
                    old_cost = dist.search(e.v)
                    new_cost = cost + e.energy
                    if old_cost is None or new_cost < old_cost:
                        dist.insert(e.v, new_cost)
                        prev.insert(e.v, u)
                        pq.push(new_cost, e.v)
        return float("inf"), []
    
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

    #F6: Using prim's algorithm
    def prim(self, start):
        min_heap = CustomMinHeap()
        visited = set()
        mst = LinkedList()
        total_cost = 0

        visited.add(start)
        edges = self.adj.search(start)
        
        for e in edges:
            if not e.restricted:
                min_heap.push(e.energy, (start, e.v))

        while (not min_heap.is_empty()) and (len(visited) < self.node_count):
            energy, (u, v) = min_heap.pop()

            if v in visited:
                continue

            visited.add(v)
            mst.append((u,v, energy))
            total_cost += energy

            edges = self.adj.search(v)
            for e in edges:
                if not e.restricted and e.v not in visited:
                    min_heap.push(e.energy, (v, e.v))


        return mst, total_cost

    #F5 Charging station placement for Large-Scale Coverage
    def multi_source_dijkstra(self, sources):

        dist = CustomHashMap()
        pq = CustomMinHeap()

        # initialize
        for node_id, _ in self.nodes.items():
            dist.insert(node_id, float("inf"))

        for s in sources:
            dist.insert(s, 0)
            pq.push(0, s)

        while not pq.is_empty():
            d, u = pq.pop()
            if d > dist.search(u):
                continue

            edges = self.adj.search(u)
            if edges is None:
                continue

            for e in edges:
                if e.restricted:
                    continue
                v = e.v
                nd = d + e.energy
                if nd < dist.search(v):
                    dist.insert(v, nd)
                    pq.push(nd, v)

        return dist
    
    def find_uncovered_corridors(self, dist, R):
        uncovered = CustomArray()

        for u, edges in self.adj.items():
            for e in edges:
                if e.restricted:
                    continue
                du = dist.search(u)
                dv = dist.search(e.v)
                if du is None or dv is None:
                    continue
                if min(du, dv) > R:
                    uncovered.append((u, e.v))

        return uncovered

    def optimize_charging_station_placement(self, k, R):
        # 1. collect existing charging stations
        charging = CustomArray()
        for node_id, node in self.nodes.items():
            if node.type == "charging":
                charging.append(node_id)

        # 2. greedy placement
        for _ in range(k):
            # compute distances
            dist = self.multi_source_dijkstra(charging)

            # check uncovered corridors
            uncovered = self.find_uncovered_corridors(dist, R)

            candidate = None
            max_dist = -1

            if len(uncovered) > 0:
                # PRIORITY: fix uncovered corridors
                for (u, v) in uncovered:
                    if dist.search(u) > max_dist:
                        max_dist = dist.search(u)
                        candidate = u
                    if dist.search(v) > max_dist:
                        max_dist = dist.search(v)
                        candidate = v
            else:
                # minimize average distance → pick farthest node
                for node_id, _ in self.nodes.items():
                    d = dist.search(node_id)
                    if d > max_dist:
                        max_dist = d
                        candidate = node_id

            if candidate is None:
                break

            charging.append(candidate)

        return charging
    
    def visualize_graph(self):
        G = nx.DiGraph()

        # add nodes
        for node_id, node in self.nodes.items():
            G.add_node(node_id, label=node.type)

        # add edges
        for u, edge_list in self.adj.items():
            for edge in edge_list:
                label = f"E:{edge.energy} C:{edge.capacity}"
                G.add_edge(edge.u, edge.v, label=label)

                if edge.bidirectional:
                    G.add_edge(edge.v, edge.u, label=label)

        pos = nx.spring_layout(G, seed=42)

        # draw nodes
        nx.draw(
            G, pos,
            with_labels=True,
            node_size=2500,
            font_size=10
        )

        # draw edge labels
        edge_labels = nx.get_edge_attributes(G, "label")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        plt.title("Delivery Network Map")
        plt.show()
            
                