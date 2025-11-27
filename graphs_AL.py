import sys


# This class implements an EdgeNode, an element in the adjacency list that represents an edge in the graph
class EdgeNode:
    def __init__(self, y, weight=0):
        # parameter y: the destination vertex
        # parameter weight: the weight of the edge
        self.y = y
        self.weight = weight
        self.next = None


# This class implements a simple adjacency list.

class GraphAL:

    def __init__(self, max_vertices, directed=False):
        # initializes a graph
        # parameter max_vertices: maximum number of vertices
        # parameter directed: Boolean to indicate whether the graph is directed or undirected
        self.max_vertices = max_vertices
        self.nvertices = 0  # Number of vertices
        self.nedges = 0  # Number of edges
        self.directed = directed  # Directed graph indicator
        self.edges = [None] * (max_vertices + 1)  # Adjacency list (1-based indexing)
        self.degree = [0] * (max_vertices + 1)  # Degree of each vertex

    def add_vertex(self):
        # adds a vertex to a graph
        if self.nvertices < self.max_vertices:
            self.nvertices += 1
        else:
            print("Maximum number of vertices reached.")

    def add_edge(self, x, y, weight=0):
        # adds an edge from x to y to the graph
        # parameter x: Source vertex.
        # parameter y: Destination vertex.
        # parameter weight: Weight of the edge.

        # add the edge from x to y
        node = EdgeNode(y, weight)
        node.next = self.edges[x]
        self.edges[x] = node

        # Update the (out-)degree of vertex x
        self.degree[x] += 1

        # If undirected, add the reverse edge
        if not self.directed:
            node = EdgeNode(x, weight)
            node.next = self.edges[y]
            self.edges[y] = node
            self.degree[y] += 1

        # Increment the edge count
        self.nedges += 1

    def display(self):
        # display the adjacency list of the graph
        print(f"Graph: {self.nvertices} vertices, {self.nedges} edges, {'directed' if self.directed else 'undirected'}")
        for i in range(1, self.nvertices + 1):
            print(f"Vertex {i} (degree {self.degree[i]}):", end=" ")
            current = self.edges[i]
            while current:
                print(f"-> ({current.y}, weight={current.weight})", end=" ")
                current = current.next
            print()

    def prim_mst(self, start):
        # This function computes the MST using Prim's algorithm
        # parameter start: start node for the algorithm

        intree = [False] * (self.max_vertices + 1)  # Tracks vertices that are already in the MST, initially none
        distance = [sys.maxsize] * (self.max_vertices + 1)  # Cost (weight of the connecting edge) to add a vertex to the MST
        parent = [-1] * (self.max_vertices + 1)  # Tracks parent of each vertex in the MST
        weight = 0  # Total weight of the MST

        # Initialize the start vertex
        distance[start] = 0
        v = start

        while not intree[v]:
            intree[v] = True

            # If not the start vertex, include the edge in the MST
            if parent[v] != -1:
                print(f"Edge ({parent[v]}, {v}) in tree with weight {distance[v]}")
                weight += distance[v]

            # Update distances for adjacent vertices
            current = self.edges[v]
            while current:
                w = current.y
                if not intree[w] and distance[w] > current.weight:
                    distance[w] = current.weight
                    parent[w] = v
                current = current.next

            # Find the next vertex to process

            dist = sys.maxsize
            for i in range(1, self.nvertices + 1):
                if not intree[i] and distance[i] < dist:
                    dist = distance[i]
                    v = i

        return weight


    def dijkstra(self, start):
        #  Dijkstra's algorithm to find the shortest paths from a start vertex to all other vertices.
        #  parameter graph: The graph object containing vertices and edges.
        #  parameter start: The starting vertex.
        #  return: A tuple containing the distances and the parent array.

        known = [False] * (self.max_vertices + 1)  # # Is the vertex (and its distance to the start node) already known?
        distance = [MAXINT] * (self.max_vertices + 1)  # Shortest known distance to each vertex
        parent = [-1] * (self.max_vertices + 1)  # Tracks the shortest path tree

        # Initialize the start vertex
        distance[start] = 0  # Distance from start to the start node is 0
        v = start

        while not known[v]:
            known[v] = True

            # Update distances for all unknown neighbors of the current node
            neighbor = self.edges[v]
            while neighbor:
                w = neighbor.y
                if not known[w] and distance[w] > distance[v] + neighbor.weight:
                    distance[w] = distance[v] + neighbor.weight
                    parent[w] = v
                neighbor = neighbor.next

            # Select the next vertex with the smallest distance
            dist = sys.maxsize
            for i in range(1, self.nvertices + 1):
                if not known[i] and distance[i] < dist:
                    dist = distance[i]
                    v = i

        return distance, parent


