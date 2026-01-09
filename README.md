# Algorithms and Data Structures Project Report

Team members: Jou-Pei Fang (Matr. No. 2285577\)
		          Shiyin Li (Matr. No. 2280709\)

[1. Introduction](#1-introduction)

[2. Data Structure Prerequisite](#2-data-structure-prerequisite)

[2.1 list](#21-list)

[2.1.1 LinkedList](#211-linkedlist)

[2.1.2 Array-based list (CustomArray)](#212-array-based-list-customarray)

[2.1.3 Complexity](#213-complexity)

[2.2 Hash Map](#22-hash-map)

[2.2.1 Necessity](#221-necessity)

[2.2.2 Implementation](#222-implementation)

[2.2.3 Complexity](#223-complexity)

[2.3 Min Heap](#23-min-heap)

[2.3.1 Necessity](#231-necessity)

[2.3.2 Implementation](#232-implementation)

[2.3.3 Complexity](#233-complexity)

[3. Functionality of the tool](#3-functionality-of-the-tool)

[3.1 B1: Import and visualize the drone network](#31-b1-import-and-visualize-the-drone-network)

[3.2 B2: Define no-fly zones](#32-b2-define-no-fly-zones)

[3.3 B3: Extend or modify the drone network](#33-b3-extend-or-modify-the-drone-network)

[3.4 F1: Check reachability](#34-f1-check-reachability)

[3.5 F2: Develop a method for determining efficient flight routes](#35-f2-develop-a-method-for-determining-efficient-flight-routes)

[3.6 F3: Compute delivery capacity](#36-f3-compute-delivery-capacity)

[3.7 F4: Assess and improve network resilience](#37-f4-assess-and-improve-network-resilience)

[3.8 F5: Optimize placement of charging stations for large-scale coverage](#38-f5-optimize-placement-of-charging-stations-for-large-scale-coverage)

[3.9 F6: Set up a communications infrastructure for drones](#39-f6-set-up-a-communications-infrastructure-for-drones)

## 1. Introduction 

This module defines the graph structure used in the drone delivery project. It models the delivery network as a directed graph, where each node represents
a location (hub, charging station or delivery point) and each edge represents a possible flight corridor between locations.

The graph not only stores connectivity, but also operational information such as energy cost, capacity and whether a corridor is restricted. These properties are later used by algorithms for routing, reachability analysis and constraint handling.

## 2. Data Structure Prerequisite

## 2.1 list 

In theory, a list is just an ordered collection. There are two main physical representations: 1\. Linked list; 2\. Array-based list (Python built-in list or CustomArray in our code).

### 2.1.1 LinkedList 

To realize the structure of LinkedList, we first define the class Node, where next is the pointer to the next node.

| class Node:   def \_\_init\_\_(self, data):       self.data \= data       self.next \= None |
| :---- |

In our class LinkedList, we have four functions: append, find, remove and iter. The key idea of the Linkedlist is non-contiguous memory, that each node contains the pointer to the next node.  
The advantage of LinkedList, contrast to an Array-based list is O(1) insertion/deletion; no resizing or shifting; flexible memory usage. The disadvantage of it is that it doesn’t have an index, so O(n) access(must traverse); extra memory for pointers.

### 2.1.2 Array-based list (CustomArray) 

Key idea of array is contiguous memory, each element is stored contiguously in memory, which enables indexing work. For example, when we want to do x \= arr\[i\], python computes address \= base\_address \+ i \* sizeof (pointer) , so indexing is O(1) time.  
The advantages of array-based lists are O(1) random access; cache friendly, very fast in practice; less memory overhead (no pointers). The disadvantage of it is that when inserting or deleting in the middle, the complexity is O(n); it needs resizing (copying).

### 2.1.3 Complexity 

| Operation | LinkedList | CustomArray |
| :---- | :---: | :---: |
| Access by index | O(n) | O(1) |
| Search by value | O(n) | O(n) |
| Insert at end | O(n) | O(1) |
| Insert at known position | O(1) | O(n) |
| Insert at beginning | O(1) | O(n) |
| Delete at known position | O(1) | O(n) |
| Delete by value | O(n) | O(n) |
| Pop last element | O(n) | O(1) |

## 2.2 Hash Map 

### 2.2.1 Necessity  

A hash map is necessary to provide O(1) average-time access from a node ID to its associated data (node object or adjacency list). Without a hash map, basic graph operations would degrade to O(n), making algorithms like DFS, Dijkstra, and Max-Flow inefficient. In our code, search value by the key is constantly used, like edges \= self.adj.search(u) , is appeared in Dijkstra and so on.  
In our Graph class, we need to solve two mapping problems, node\_id to Node object and node\_id to adjacent\_list.

| self.nodes \= CustomHashMap()              \# id → Nodeself.adj \= CustomHashMap()                \# id → list of Edge |
| :---- |

If the node IDs are small continuous integers, it’s also possible to use array indexing to achieve this purpose, but according to the input json file the IDs are like “HUB” or “D1”, it’s only feasible to use the hash map.

### 2.2.2 Implementation 

We used a hash function like this, which is a classic hash function for keys as strings.

| def custom\_hash(name):   code \= 0   for i, c in enumerate(str(name)):       code+= ord(c)\*(31\*\*i)   return code |
| :---- |

Then we defined the number of buckets is 73, because we assume the number of nodes in input is normally around 50, desired load factor is 0.7, and 73 is the closest prime number to the quotient of the number of elements divided by desired load factor. Here we used LinkedList as each bucket, because it had to handle collisions using separate chaining. We can also use the customArray as buckets, but compared to customArray, LinkedList has less complexity when inserting and deleting(only O(1)), and it doesn’t need to resize frequently. So LinkList is the best choice.

| class CustomHashMap:   def \_\_init\_\_(self, bucket\_count \= 73):       self.bucket\_count \= bucket\_count       self.table \= \[LinkedList() for \_ in range(bucket\_count)\] |
| :---- |

### 2.2.3 Complexity 
| Function | Average time |
| :---- | :---- |
| insert | O(1) |
| search | O(1) |
| remove | O(1) |
| items | O(n) |

## 2.3 Min Heap 

### 2.3.1 Necessity 

A min-heap is necessary to efficiently implement Dijkstra’s algorithm, because it allows extracting the node with the smallest current distance in O(log V) time. Without a min-heap, shortest-path computation would degrade from O((V+E) log V) to O(V2).  
In our code where the min-heap is actually used:

| def dijkstra(self, start, target):    pq \= CustomMinHeap()    pq.push(0, (start, \[\])) |
| :---- |

Here the priority queue is implemented as min-heap, this priority queue is ordered by energy cost, for every iteration, the algorithm tries to find the smallest total energy so far, among all discovered but unvisited nodes.

### 2.3.2 Implementation 

The CustomMinHeap uses a dynamic array (CustomArray) to store the heap elements. Each element in the heap is a tuple: (priority, value). The parent node’s priority is always less than or equal to its children’s priorities, so the smallest priority element is always at the root.  
The method push adds an element and restores heap order by bubbling up. The method pop removes the smallest element and restores heap order by bubbling down. The heap is stored in a list-like structure (CustomArray) and uses the classic array-based binary heap indexing: Parent: (index \- 1\) // 2; Left child: 2\*index \+ 1; Right child: 2\*index \+ 2\.

### 2.3.3 Complexity 

| Method | Content | Time Complexity |
| :---: | :---: | :---: |
| is\_empty | Check if heap empty | O(1) |
| peek | Return min element | O(1) |
| push | Insert element | O(log n) |
| pop | Remove min | O(log n) |
| *\_bubble*\_up | Restore heap upwards | O(log n) |
| *\_bubble\_down* | Restore heap downwards | O(log n) |
| *\_swap* | Swap two elements | O(1) |

## 3. Functionality of the tool

## 3.1 B1: Import and visualize the drone network 

**Problem type** 
This function addresses a graph construction problem, where a drone delivery network is created from a structured input file.

**Modeling decisions**  
The drone network is modeled as directed graph, where nodes represent physical locations(charging stations, hubs, delivery points) and edges represent flight corridors. Edges may be bidirectional, in which case two directed edges are created. Each edges stores: energy cost, capacity and a restriction flag.

**Chosen algorithms and justification**  
No graph algorithm is applied at this stage. The function performs a linear parsing and insertion process, reading nodes and edges directly from JSON file and inserting them into the graph. This is sufficient because the task only requires data loading and initialization.

**Data structure used**  
A hash map is used to store nodes by their identifiers for constant-time access. The graph is represented as an adjacency list, allowing efficient storage of sparse graphs. Each adjacency list entry contains Edge objects storing corridor properties.

**Alternative approaches considered**  
An adjacency matrix could have been used, but it would be inefficient in terms of space for large and sparse drone networks. Therefore, an adjacency list was chosen.

**Complexity analysis**  
Let V be the number of nodes and E the number of edges:

* Time complexity: O(V \+ E)  
* Space complexity: O(V \+ E)

## 3.2 B2: Define no-fly zones 

**Problem type**  
The goal of this function is to mark areas of the drone network where flying is prohibited. These restrictions don’t build the graph. They modify the rules about how the graph can be used. 

**Modeling decisions**  
We restrict the edges \- drones cannot travel through certain corridors in the sky. Each edge simply gets a flag that says this part of the network is blocked. This keeps the structure intact while still preventing paths from using restricted areas.  
   
**Chosen algorithms and justification**  
No graph algorithm is applied at this stage. The goal is only to annotate the graph. The function simply reads the list of restricted zones from the input, matches affected edges in the existing graph, and sets the restricted flag. 

**Data structure used**  
We use HashMap for fast lookup of nodes by identifier. An adjacency list is used for each node to store a list of outgoing edges. Each edge contains a restricted boolean field indicating whether it belongs to a no-fly zone. This avoids duplication and keeps restrictions tied directly to the existing graph. 

**Alternative approaches considered**  
We could create another structure where nodes and edges are forbidden. Keep the main graph unchanged. Routing algorithms must consult both graphs. This way, the originals stay untouched, and restrictions are clearly separated from structure. However, compared to the method that we used, it is the code is more complex and harder to maintain as the network grows. 

**Complexity analysis**  
If n elements are listed as restricted:

* **Time:** O(n), since each restriction is processed once.   
* **Space:** constant \- only flags change.

## 3.3 B3: Extend or modify the drone network 

**Problem type**  
This function deals with updating an already existing drone network. Instead of building the graph from scratch, the function must safely add new locations and corridors, remove outdated ones, or update properties such as capacity, cost, or restrictions. The main goal is to modify the network without breaking existing connectivity or algorithms that depend on it. 

**Modeling decisions**

* New delivery points, hubs, or charging stations become new nodes.   
* New flight corridors become new directed edges.  
* Existing edges can be updated (capacity/energy/restricted flag).  
* Outdated nodes/edges can be removed when necessary.   
* Duplicate nodes are not created if they already exist.  
* Edges are validated so they only connect valid nodes.  
* Removing nodes automatically removes their incident edges. 

**Chosen algorithms and justification**  
No graph algorithm is applied at this stage. Simple iterative and conditional checks are enough because the focus is on structural maintenance, not computing routes. 

**Data structure used**  
We used hash map for fast access to nodes by ID, and an adjacency list for each node stores outgoing edges. Each edge stores destination, energy, cost, capacity, and restriction state. 

**Alternative approaches considered**  
We could also rebuild the entire graph after each change, but it will cost more time and increase the risk of introducing errors each time. Keeping updates localized inside the same graph structure turned out simpler and more transparent.

**Complexity analysis**  
Let V be the number of nodes and E the number of edges:

* **Adding/updating nodes:** O(1), hash lookup.  
* **Adding/updating edges:** O(1), adjacency list.  
* **Space:** O(V \+ E), check every node and edge.

## 3.4 F1: Check reachability 

**Problem type**  
Its goal is to determine whether all delivery locations in the drone network can be reached from a given hub. The output identifies delivery nodes that are unreachable from the hub, which is critical for validating the feasibility of drone delivery operations.

**Modeling decisions**  
The drone network is modeled as a directed graph. Nodes represent locations (hub, charging stations, delivery points). Directed edges represent flight corridors. Each edge has a restricted flag indicating a no-fly zone. Only non-restricted edges are considered during reachability analysis. This ensures that the reachability check reflects real operational constraints and does not assume illegal flight paths. 

**Chosen algorithm and justification**  
A Depth-First Search (DFS) is used to explore the network starting from the hub. 

Justification:

* DFS efficiently explores all reachable nodes.  
* It is simple to implement using a stack.   
* The problem only requires knowing whether a node is reachable, not the shortest path.   
* DFS naturally handles graph traversal, ensuring that only valid flight corridors are followed. 

**Data structures used**

* Stack (list): to implement DFS traversal.  
* Set (visited): to track already visited nodes and avoid infinite loops.  
* Adjacency list: to retrieve outgoing edges efficiently.  
* LinkedList: to store delivery nodes and unreachable delivery nodes.   
* Dictionary: to access node metadata.

**Alternative approaches considered**  
We can use BFS and use a queue instead of a stack. However, BFS is used to find the shortest paths, which are not required here. DFS is simpler and equally correct for reachability.

**Complexity analysis**  
Let v be the number of nodes and e the number of edges:

* The DFS visits each node at most once: O(v)  
* Each edge is examined at most once: O(e)  
* Collecting and checking delivery nodes requires iterating over all nodes: O(v)  
* Overall time complexity: O(v+e)  
* Space complexity:  
  * Visited set: O(v)  
  * Stack: O(v) in the worst case  
  * Graph storage: O(v+e)

## 3.5 F2: Develop a method for determining efficient flight routes 

**Problem type**  
This function addresses the shortest path problem in a directed weighted graph. The objective is to determine the most energy-efficient flight route from a distribution hub to a single delivery location while avoiding no-fly zones.

**Modeling decisions**  
The drone delivery network is modeled as a directed graph. Nodes represent physical locations such as hubs, intermediate waypoints, and delivery points. Directed edges represent flight corridors between locations. Each edge is assigned a non-negative weight corresponding to the energy consumption required to traverse that corridor. No-fly zones are modeled by marking specific edges as restricted; such edges are excluded from route computation. The total energy consumption of a route is defined as the sum of the energy weights along the selected path.

**Chosen algorithm and justification**  
Dijkstra’s shortest path algorithm is used to compute the minimum-energy route from the hub to the delivery node. Since all edge weights are non-negative, Dijkstra’s algorithm guarantees an optimal solution. Restricted edges are ignored during relaxation, ensuring that no-fly zones are respected.  
The algorithm is efficient, well-established, and suitable for large-scale networks where exact shortest-path solutions are required.

**Data structure used**  
A priority queue implemented using CustomMinHeap is used to always expand the node with the lowest accumulated energy cost. A set is used to track visited nodes and prevent redundant processing. The graph is stored using adjacency lists backed by CustomHashMap for efficient access to outgoing edges.

**Complexity analysis**  
Let V be the number of nodes and E the number of edges. Time complexity is O((V \+ E)logV); space complexity is O(V \+ E).

## 3.6 F3: Compute delivery capacity 

**Problem type**  
This function addresses a maximum flow problem in a directed network. The goal is to compute the maximum number of drones that can be routed simultaneously from a distribution hub to a target urban area under capacity constraints.

**Modeling decisions**  
The drone network is modeled as a directed flow graph, where nodes represent hubs, intermediate locations, and delivery points. Edges represent flight corridors with a given capacity, indicating the maximum number of drones per hour that can traverse the corridor. Restricted corridors are excluded from the model.  
To support multiple delivery points within an urban area, a super sink node is introduced. All delivery nodes in the urban area are connected to the super sink with edges of effectively infinite capacity. This allows the computation of total delivery capacity to the entire area rather than to a single destination.

**Chosen algorithm and justification**  
A Ford-Fulkerson maximum flow algorithm using BFS-based augmenting path search (Edmonds-Karp approach) is applied. This algorithm was chosen because the problem requires maximizing flow under capacity constraints; capacities are non-negative; the network size is moderate, making Edmonds-Karp sufficiently efficient and easy to implement. BFS guarantees finding shortest augmenting path, ensuring polynomial-time termination.

**Data structure used**  
The residual graph is stored using nested hash maps (the first CustomHashMap stores the node u and the inner CustomHashMap, the inner map stores the node v and capacity between u and v). A queue implemented with a custom array (CustomArray) is used for BFS traversal. Parent relationships during BFS are stored in  a hash map to reconstruct augmenting paths.

**Alternative approaches considered**  
The goal can also be achieved using DFS and Ford-Fulkerson algorithm, namely using DFS to find augmented path, but DFS dives deep into the graph exploring one path as far as possible before backtracking. This means it might pick very long augmenting paths instead of short ones, thus can have potentially exponential runtime, whereas BFS(Edmonds-Karp) guarantees polynomial runtime – O(V \* E2).

**Complexity analysis**  
Edmonds-Karp always chooses the shortest augmenting path (fewest edges) using BFS. This rule gives the algorithm a strong structural guarantee.   
So total time \= (time per BFS) x (number of BFS runs). Firstly we look at the time per BFS, in the residual graph, BFS visits each vertex once, and it inspects each edge at most one, so one BFS \= O(E).  
Next we look at the number of BFS runs. Everytime we need to find an augmented path, we need to run BFS once, and everytime we find the augmented path, there is at least one edge going to be saturated. Because the characteristic of BFS is to return the shortest possible path, namely the augmented path’s length can increase from 1 to V-1, as the BFS runs, V is the number of vertices in the map. Each time an edge becomes critical on a shortest path, the BFS distance to its endpoint must strictly increase before it can be critical again. Since distance are at most V-1, this can happen at most O(V) times per edge, and there are E edges, so the total augmentation is O(VE). The two parts combine together and we can draw the conclusion that the complexity of Edmonds-Karp is O(VE2). By contrast, the Ford-Fulkerson using DFS chooses arbitrary paths, not shortest ones; this allows very small flow increases that undo each other via residual edges. Each augmentation increase flow by only 1 unit is possible, which makes the algorithms depend on the numeric value of capacities, and when we represent the capacity using binary, when we input 11, the capacity is actually 1024, so the runtime can be 1024 steps, so to say the runtime is exponential, whereas in Edmonds-Karp, it does not depend on the numeric value of capacities, and limits the number of augmentation by graph structure (V, E).  
The space complexity is O(V \+ E), due to storage of the residual graph and auxiliary data structures.

## 3.7 F4: Assess and improve network resilience 

**Problem type**  
This function addresses a minimum cut problem in a directed flow network. The objective is to identify the set of flight corridors whose removal disconnects the distribution hub from the delivery area.

**Modeling decisions**  
The problem is modeled using the residual graph obtained after computing the maximum flow in F3. The nodes represent physical locations in the drone network. Directed edges represent flight corridors. Residual capacities represent remaining available flow after maximum delivery capacity has been reached. The minimum cut is defined as the partition of nodes into reachable nodes from the source in the residual graph, and non-reachable nodes. All original edges that go from reachable to non-reachable nodes form the minimum cut set, representing critical flight corridors.

**Chosen algorithm and justification**  
A Breadth-First Search (BFS) is performed on the residual graph starting from the source node. After a maximum flow is computed, BFS efficiently determines all nodes reachable via edges with positive residual capacity. The Max-Flow Min-Cut Theorem guarantees that this procedure correctly identifies a minimum cut. The algorithm is simple, efficient, and directly compatible with the residual graph produced in F3.

**Data structures used**

* The residual graph is stored using nested hash maps (CustomHashMap) for efficient access to residual capacities.   
* A queue implemented using CustomArray is used to perform BFS.  
* A hash map is used to track visited nodes.  
* The resulting cut edges are stored in a custom dynamic array (CustomArray).

**Complexity analysis**  
Let V be the number of nodes and E the number of edges  
Time complexity:  
BFS on the residual graph: O(V \+ E)  
Extracting cut edges: O(E)  
Total: O(V \+ E)  
Space complexity:  
O(V \+ E) due to storage of the residual graph and visited structures.

## 3.8 F5: Optimize placement of charging stations for large-scale coverage 

**Problem type**  
The problem addressed in F5 is an optimization problem focused on facility location or k-medoid problem in the context of drone delivery networks. Specifically, it aims to place k charging stations in the drone network to minimize the average distance from any point in the network to the nearest charging station; ensure that all delivery corridors are sufficiently covered and accessible for drone recharging.  
**Modeling Decisions**  
The drone delivery network is modeled as a directed weighted graph: nodes represent locations, including hubs, delivery points, and candidate charging station locations; edges represent flight corridors with associated energy cost; some edges are restricted and thus ignored during routing; the graph supports bidirectional edges where applicable.  
The problem is modeled to find k nodes in the graph to act as charging stations.  
The edge weights(energy cost) define the distance metric used to compute shortest paths to charging stations.  
All delivery corridors(edges) must be reachable and within reasonable distance to a charging station for effective recharging.  
**Algorithm choice and Justification**  
The charging station placement problem can be formalized as k-median problem on a weighted graph, where the objective is to select k facility nodes(charging station) to minimize the average distance to demand nodes. The k-median problem is a well-known NP-hard combinatorial optimization problem, implying that finding the exact optimal solution for our charging station placement is also NP-hard. This is due to the exponential number of possible facility subsets and the computational complexity of evaluating coverage constraints. Hence, heuristic or approximation algorithms are necessary for practical, scalable solutions.  
For this question, a greedy heuristic algorithm was chosen. The core of the solution relies on repeated executions of a multi-source Dijkstra’s algorithm to compute the shortest distances from existing charging stations to all nodes in the network.

* Multi-source Dijkstra’s Algorithm:  
  This algorithm efficiently calculates the minimum energy cost from multiple sources(existing charging stations) to every other node. Using a priority queue(min-heap), it ensures the shortest paths are found considering edge weights (energy costs) are restricted edges.  
* Greedy Charging Station Selection  
  The placement proceeds iteratively by adding one charging station at a time, targeting nodes that:1. Fix uncovered corridors, edges whose endpoints are farther than a threshold distance R from any charging station, prioritizing connectivity and coverage. If no uncovered corridors remain, minimize the average distance to the nearest charging station by selecting the node farthest from any existing charging station, thus improving network-wide accessibility.

**Complexity Analysis**  
Time complexity: shortest path computations with Dijkstra’s algorithm run in O(ElogV), where V is the number of nodes and E the number of edges. For placing k charging stations, multiple Dijkstra runs may be required, leading to O(kElogV) in the worst case.  
Space complexity: storing the graph requires O(V \+ E) space for nodes and edges. 

## 3.9 F6: Set up a communications infrastructure for drones 

**Problem type**  
This function addresses the minimum spanning tree (MST) problem in a weighted graph. Its purpose is to connect all reachable locations in the drone with the minimum total energy cost, while respecting no-fly restrictions. The resulting MST represents an energy-efficient backbone network for drone movement. 

**Modeling decisions**  
The drone network is modeled as a weighted graph: nodes represent locations, edges represent flight corridors, and each edge stores an energy cost and a restriction flag. Restricted corridors are excluded from consideration, ensuring that the resulting network only uses valid flight paths. Although the graph is directed in general, Prim’s algorithm is applied assuming that usable corridors form a connected structure suitable for MST construction. 

**Chosen algorithm and justification**   
Prim’s algorithm is used to compute the minimum spanning tree. This algorithm incrementally expands the tree by always selecting the lowest-energy corridor that connects a new node to the already visited set. A priority queue is used to efficiently identify the next best corridor. Prim’s algorithm is well-suited for this task because it directly focuses on minimizing total edge weight and integrates naturally with adjacency list graph representations. 

**Data structures used**  
A custom min-heap is used to maintain the candidate corridor ordered by energy cost, ensuring efficient retrieval of the next optimal edge. A set keeps track of visited nodes to prevent cycles and repeated processing. The graph itself is stored as an adjacency list, allowing fast access to outgoing corridors for each node. The resulting minimum spanning tree is stored in a linked list to preserve insertion order. 

**Alternative approaches considered**  
Kruskal’s algorithm was considered as an alternative, but it requires sorting all edges globally and maintaining an additional union-find structure, which adds overhead and does not align well with the requirement to start from a specific node. Another option would have to permanently remove restricted corridors from the graph, but this was rejected because restrictions may change dynamically. Exhaustive enumeration of possible spanning trees was also dismissed due to its infeasible computational cost. 

**Complexity analysis**  
Let v be the number of nodes and e the number of edges:

* Each node is added to the MST once: O(v)  
* Each edge can be inserted into the heap once: O(e log e)  
* Time complexity: O(e log e)  
* Space complexity: O(v+e)