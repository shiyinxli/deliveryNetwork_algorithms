from graph import Graph
if __name__ == "__main__":
    graph = Graph()
    graph.load_json("test.json")

    graph.visualize_graph()

    print("F1: check Reachability")
    result = graph.check_delivery_reachability("S")
    print(result)
    print("======================================================")

    print("F2: Develop a method determining efficient flight routes")
    cost, path = graph.dijkstra("S", "D")
    if path:
        print(f"Shortest path from S to D costs {cost} energy and goes: {' -> '.join(path)}")
    else:
        print("No path found from S to charge")
    print("======================================================")

    print("F3: calculate delivery capacity")
    delivery_nodes = {
        node_id
        for node_id, node in graph.nodes.items()
        if node.type == "delivery"
    }
    max_flow, residual = graph.calculate_delivery_capacity(
        start_hub="S",
        area_nodes=delivery_nodes
    )
    print("Max delivery capacity: ", max_flow)
    print("======================================================")

    print("F4: Assess and improve network resilience")
    min_cut_edges = graph._extract_min_cut(residual, "S")
    print("Bottle neck edges: ")
    for u, v in min_cut_edges:
        print(f"{u} -> {v}")
    print("======================================================")

    print("F5: Optimize charging station placement for large-scale coverage")
    charges = graph.optimize_charging_station_placement(1, 5)
    for item in charges:
        if item == "CHARGE":
            continue
        print(item)
    print("======================================================")

    print("F6: communication infrastructure for drones")
    mst, total_cost = graph.prim("S")
    print("nodes in the communication network: ")
    for item in mst.iter():
        print(item)
    print(f"total cost for it is {total_cost}")




    
    