import heapq
import random
import time
from collections import deque

import matplotlib.pyplot as plt
import networkx as nx


# Create a random connected weighted graph
def create_random_graph(num_nodes=50, num_edges=100):
    G = nx.gnm_random_graph(num_nodes, num_edges)
    while not nx.is_connected(G):
        G = nx.gnm_random_graph(num_nodes, num_edges)
    for u, v in G.edges():
        G.edges[u, v]["weight"] = random.randint(1, 10)
    return G


G = create_random_graph()
pos = nx.spring_layout(G)

# Display graph
plt.figure(figsize=(10, 8))
nx.draw(G, pos, with_labels=True, node_size=300, node_color="skyblue")
nx.draw_networkx_edge_labels(
    G, pos, edge_labels={(u, v): d["weight"] for u, v, d in G.edges(data=True)}
)
plt.title("Random Graph with 50 Nodes")
plt.show()

start_node = 0


# BFS level mapping
def bfs_levels(graph, start):
    level_dict = {}
    queue = deque([(start, 0)])
    visited = {start}

    while queue:
        node, level = queue.popleft()
        level_dict[node] = level
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, level + 1))

    return level_dict


# Color nodes by BFS level
levels = bfs_levels(G, start_node)
level_colors = [levels.get(node, 0) for node in G.nodes()]

plt.figure(figsize=(10, 8))
nodes = nx.draw_networkx_nodes(
    G, pos, node_color=level_colors, cmap=plt.cm.viridis, node_size=300
)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_edge_labels(
    G, pos, edge_labels={(u, v): d["weight"] for u, v, d in G.edges(data=True)}
)
plt.title("Graph Nodes Colored by BFS Levels")
plt.colorbar(nodes, label="Level")
plt.show()


# Basic BFS
def bfs(graph, start, goal=None):
    visited_order = []
    queue = deque([start])
    visited = {start}

    while queue:
        node = queue.popleft()
        visited_order.append(node)

        if goal is not None and node == goal:
            break

        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return visited_order


# DFS
def dfs(graph, start, goal=None):
    visited_order = []
    stack = [start]
    visited = set()

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            visited_order.append(node)

            if goal is not None and node == goal:
                break

            for neighbor in sorted(graph.neighbors(node), reverse=True):
                if neighbor not in visited:
                    stack.append(neighbor)
    return visited_order


# Uniform Cost Search
def ucs(graph, start, goal=None):
    visited_order = []
    pq = [(0, start)]
    visited = set()

    while pq:
        cost, node = heapq.heappop(pq)
        if node not in visited:
            visited.add(node)
            visited_order.append(node)

            if goal is not None and node == goal:
                break

            for neighbor in graph.neighbors(node):
                if neighbor not in visited:
                    new_cost = cost + graph.edges[node, neighbor]["weight"]
                    heapq.heappush(pq, (new_cost, neighbor))

    return visited_order


# Measure times
start_time = time.time()
bfs_order = bfs(G, start_node)
bfs_time = time.time() - start_time

start_time = time.time()
dfs_order = dfs(G, start_node)
dfs_time = time.time() - start_time

start_time = time.time()
ucs_order = ucs(G, start_node)
ucs_time = time.time() - start_time

# Print results
print("\nBFS")
print(f"Visited Order: {bfs_order}")
print(f"Total Nodes Visited: {len(bfs_order)}")
print(f"Execution Time: {bfs_time:.6f} seconds")

print("\nDFS")
print(f"Visited Order: {dfs_order}")
print(f"Total Nodes Visited: {len(dfs_order)}")
print(f"Execution Time: {dfs_time:.6f} seconds")

print("\nUCS")
print(f"Visited Order: {ucs_order}")
print(f"Total Nodes Visited: {len(ucs_order)}")
print(f"Execution Time: {ucs_time:.6f} seconds")

print("\nTime Complexities:")
print("BFS : O(V + E)")
print("DFS : O(V + E)")
print("UCS : O(E log V)")  # more accurate
