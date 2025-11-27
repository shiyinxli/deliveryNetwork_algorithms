import json
import heapq
from hashmap import CustomHashMap, LinkedList

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
        if adj_u is None:
            adj_u = []
        self.adj.insert(u, adj_u)

        adj_u.append(Edge(u, v, energy, capacity, bidirectional))

        if bidirectional:
            adj_v = self.adj.search(v)
        if adj_v is None:
            adj_v = []
            self.adj.insert(v, adj_v)

        adj_v.append(Edge(v, u, energy, capacity, bidirectional))

    
    # F1: Check reachability from a hub
    def check_delivery_reachability(self, start="HUB"):
    # 1. Run reachability search
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
        pq = [(0, start, [])]  # (cost, node, path)

        visited = set()

        while pq:
            cost, u, path = heapq.heappop(pq)
            if u in visited:
                continue
            visited.add(u)

            path = path + [u]

            if u == target:
                return cost, path

            for e in self.adj[u]:
                if e.restricted:
                    continue
                heapq.heappush(pq, (cost + e.energy, e.v, path))

        return float("inf"), []  # no path
