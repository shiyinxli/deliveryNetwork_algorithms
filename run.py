from graph import Graph
if __name__ == "__main__":
    graph = Graph()
    graph.load_json("test.json")

    # Check delivery reachability from HUB
    # result = graph.check_delivery_reachability("HUB")
    # print(result)

    #Example shortest path from HUB to A1
    # cost, path = graph.dijkstra("HUB", "A1")
    # if path:
    #     print(f"Shortest path from HUB to A1 costs {cost} energy and goes: {' -> '.join(path)}")
    # else:
    #     print("No path found from HUB to A1")
    
    # urban_area = ["A", "B", "C", "D"]
    # capacity, residual = graph.calculate_delivery_capacity("S", urban_area)
    # print("Max drones per hour: ", capacity)
    # cut_edges = graph._extract_min_cut(residual, "S")
    # print("Min cut edges:")
    # for i in range(len(cut_edges)):
    #     u, v = cut_edges[i]
    #     print(f"{u} -> {v}")

    mst, cost = graph.prim("S")
    print(cost)

    for (u, v, cost) in mst.iter():
        print(u, v, cost)