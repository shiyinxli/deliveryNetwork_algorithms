from graph import Graph
if __name__ == "__main__":
    graph = Graph()
    graph.load_json("test.json")

    graph.visualize_graph()

    result = graph.check_delivery_reachability("S")
    print(result)

    
    cost, path = graph.dijkstra("S", "D")
    if path:
        print(f"Shortest path from S to charge costs {cost} energy and goes: {' -> '.join(path)}")
    else:
        print("No path found from S to charge")

    
    # urban_area = ["A", "B", "C", "D"]
    # capacity, residual = graph.calculate_delivery_capacity("S", urban_area)
    # print("Max drones per hour: ", capacity)
    # cut_edges = graph._extract_min_cut(residual, "S")
    # print("Min cut edges:")
    # for i in range(len(cut_edges)):
    #     u, v = cut_edges[i]
    #     print(f"{u} -> {v}")

    # mst, cost = graph.prim("S")
    # print(cost)

    # for (u, v, cost) in mst.iter():
    #     print(u, v, cost)
    
    # stations = graph.optimize_charging_station_placement(k = 2, R = 5)
    # for i in range(len(stations)):
    #     u = stations[i]
    #     print(f"{u}")