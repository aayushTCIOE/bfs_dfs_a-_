import heapq
import random

import matplotlib

matplotlib.use("TkAgg")

import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np


def generate_maze(rows, cols, wall_probability=0.25):
    maze = [["0" for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if random.random() < wall_probability:
                maze[i][j] = "1"
    maze[0][0] = "S"
    maze[rows - 1][cols - 1] = "G"
    return maze


def heuristic(a, b):
    """Manhattan distance"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar_with_visualization(maze, delay=0.3):
    rows, cols = len(maze), len(maze[0])
    start, goal = (0, 0), (rows - 1, cols - 1)

    # Visualization format: 0 free, 1 wall, 2 start, 3 goal, 4 visited, 5 path
    visual = np.zeros((rows, cols))
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == "1":
                visual[i][j] = 1
    visual[start] = 2
    visual[goal] = 3

    cmap = colors.ListedColormap(
        ["white", "black", "orange", "red", "lightgreen", "blue"]
    )

    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start, [start]))
    visited = {start: 0}  # store cost_so_far

    plt.figure(figsize=(8, 8))
    plt.ion()
    step = 0

    while open_set:
        _, cost_so_far, current, path = heapq.heappop(open_set)
        r, c = current

        # Reached goal
        if current == goal:
            for pr, pc in path:
                if (pr, pc) not in (start, goal):
                    visual[pr][pc] = 5  # blue path
            plt.clf()
            plt.imshow(visual, cmap=cmap, vmin=0, vmax=5)
            plt.title(f"A* Final Path (steps: {len(path)})")
            plt.grid(True, color="gray", alpha=0.3)
            plt.pause(5)
            plt.ioff()
            return path

        # Mark visited
        if current != start and current != goal:
            visual[r][c] = 4  # green visited

        # Explore neighbors
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)
            if 0 <= nr < rows and 0 <= nc < cols:
                if maze[nr][nc] != "1":
                    new_cost = cost_so_far + 1
                    if neighbor not in visited or new_cost < visited[neighbor]:
                        visited[neighbor] = new_cost
                        priority = new_cost + heuristic(neighbor, goal)
                        heapq.heappush(
                            open_set, (priority, new_cost, neighbor, path + [neighbor])
                        )

        # Live animation
        if step % 5 == 0:
            plt.clf()
            plt.imshow(visual, cmap=cmap, vmin=0, vmax=5)
            plt.pause(delay)
        step += 1

    plt.ioff()
    return None


if __name__ == "__main__":
    maze = generate_maze(20, 20, wall_probability=0.25)
    astar_with_visualization(maze, delay=0.2)
