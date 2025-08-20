import random
from collections import deque

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


def bfs_with_visualization(maze):
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

    frontier = deque([(start, [start])])
    visited = {start}

    plt.figure(figsize=(8, 8))
    plt.ion()

    step = 0
    while frontier:
        (r, c), path = frontier.popleft()

        if (r, c) == goal:
            # Color path blue
            for pr, pc in path:
                if (pr, pc) not in (start, goal):
                    visual[pr][pc] = 5

            plt.clf()
            plt.imshow(visual, cmap=cmap, vmin=0, vmax=5)
            plt.title(f"BFS Final Path (steps: {len(path)})")
            plt.grid(True, color="gray", alpha=0.3)
            plt.pause(5)  # keep it on screen for a while
            plt.ioff()
            return path

        if (r, c) != start and (r, c) != goal:
            visual[r][c] = 4

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if maze[nr][nc] != "1" and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    frontier.append(((nr, nc), path + [(nr, nc)]))

        if step % 5 == 0:
            plt.clf()
            plt.imshow(visual, cmap=cmap, vmin=0, vmax=5)
            # plt.title(f"BFS Exploring... step {step}")
            plt.pause(0.3)
        step += 1


if __name__ == "__main__":
    maze = generate_maze(20, 20, wall_probability=0.25)
    bfs_with_visualization(maze)
