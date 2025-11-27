from graph import Graph
if __name__ == "__main__":
    graph = Graph()
    graph.load_json("template.json")

    # Check delivery reachability from HUB
    result = graph.check_delivery_reachability("HUB")
    print(result)

    # Example shortest path from HUB to A1
    #cost, path = graph.dijkstra("HUB", "A1")
    # if path:
    #     print(f"Shortest path from HUB to A1 costs {cost} energy and goes: {' -> '.join(path)}")
    # else:
    #     print("No path found from HUB to A1")
