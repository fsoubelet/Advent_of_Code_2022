"""
--- Day 12: Hill Climbing Algorithm ---

You try contacting the Elves using your handheld device, but the river you're following must be too low to get a decent signal.

You ask the device for a heightmap of the surrounding area (your puzzle input).
The heightmap shows the local area from above broken into a grid; the elevation of each square of the grid is given by a single lowercase letter, where a is the lowest elevation, b is the next-lowest, and so on up to the highest elevation, z.

Also included on the heightmap are marks for your current position (S) and the location that should get the best signal (E).
Your current position (S) has elevation a, and the location that should get the best signal (E) has elevation z.

You'd like to reach E, but to save energy, you should do it in as few steps as possible.
During each step, you can move exactly one square up, down, left, or right.
To avoid needing to get out your climbing gear, the elevation of the destination square can be at most one higher than the elevation of your current square; that is, if your current elevation is m, you could step to elevation n, but not to elevation o.
(This also means that the elevation of the destination square can be much lower than the elevation of your current square.)

For example:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi

Here, you start in the top-left corner; your goal is near the middle.
You could start by moving down or right, but eventually you'll need to head toward the e at the bottom.
From there, you can spiral around to the goal:

v..v<<<<
>v.vv<<^
.>vv>E^^
..v>>>^^
..>>>>>^

In the above diagram, the symbols indicate whether the path exits each square moving up (^), down (v), left (<), or right (>).
The location that should get the best signal is still E, and . marks unvisited squares.

This path reaches the goal in 31 steps, the fewest possible.

What is the fewest steps required to move from your current position to the location that should get the best signal?

--- Part Two ---

As you walk up the hill, you suspect that the Elves will want to turn this into a hiking trail.
The beginning isn't very scenic, though; perhaps you can find a better starting point.

To maximize exercise while hiking, the trail should start as low as possible: elevation a.
The goal is still the square marked E. However, the trail should still be direct, taking the fewest steps to reach its goal.
So, you'll need to find the shortest path from any square at elevation a to the square marked E.

Again consider the example from above:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi

Now, there are six choices for starting position (five marked a, plus the square marked S that counts as being at elevation a).
If you start at the bottom-left square, you can reach the goal most quickly:

...v<<<<
...vv<<^
...v>E^^
.>v>>>^^
>^>>>>>^

This path reaches the goal in only 29 steps, the fewest possible.

What is the fewest steps required to move starting from any square with elevation a to the location that should get the best signal?
"""
import string

from collections import defaultdict
from pathlib import Path


def dijkstra(graph: dict[complex, list[complex]], source: complex) -> dict[complex, int]:
    """Get graph of points and their neighbors, and return the shortest path to each point from the source."""
    Q = list(graph.keys())
    dist = {v: float("inf") for v in graph}
    dist[source] = 0

    while Q:
        u = min(Q, key=dist.get)
        Q.remove(u)

        for v in graph[u]:
            alt = dist[u] + 1
            if alt < dist[v] and points[u] - points[v] <= 1:
                dist[v] = alt

    return dist


if __name__ == "__main__":
    inputs = Path("input.txt").read_text().splitlines()

    points = {}
    graph = defaultdict(list)
    start, starts, end = None, [], None

    # Build our graph
    for y, line in enumerate(inputs):
        for x, letter in enumerate(line):
            point = complex(x, y)  # using complex as a 2d point because I'm lazy
            if letter == "S":  # start point is at the lowest altitude
                value = 0
                start = point
                starts.append(point)
            elif letter == "a":
                value = 0
                starts.append(point)  # potential starts for part 2
            elif letter == "E":  # end point is at the highest altitude
                value = 25
                end = point
            else:
                value = string.ascii_lowercase.index(letter)
            points[point] = value

    # Now for each point, we get its neighbors
    for point in points:
        for neighbor in [1 + 0j, -1 + 0j, 0 + 1j, 0 - 1j]:
            if (point + neighbor) in points:
                graph[point].append(point + neighbor)

    # Get the shortest path to each point from the end
    paths = dijkstra(graph, end)

    print(f"Part 1: {paths[start]}")  # shortest path from end to start (also from start to end)
    print(f"Part 2: {min(paths[s] for s in starts)}")  # shortest path from end to any start
