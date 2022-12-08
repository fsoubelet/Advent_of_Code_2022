"""
--- Day 8: Treetop Tree House ---

The expedition comes across a peculiar patch of tall trees all planted carefully in a grid.
The Elves explain that a previous expedition planted these trees as a reforestation effort.
Now, they're curious if this would be a good location for a tree house.

First, determine whether there is enough tree cover here to keep a tree house hidden.
To do this, you need to count the number of trees that are visible from outside the grid when looking directly along a row or column.

The Elves have already launched a quadcopter to generate a map with the height of each tree (your puzzle input). For example:

30373
25512
65332
33549
35390

Each tree is represented as a single digit whose value is its height, where 0 is the shortest and 9 is the tallest.

A tree is visible if all of the other trees between it and an edge of the grid are shorter than it.
Only consider trees in the same row or column; that is, only look up, down, left, or right from any given tree.

All of the trees around the edge of the grid are visible - since they are already on the edge, there are no trees to block the view.
In this example, that only leaves the interior nine trees to consider:

    The top-left 5 is visible from the left and top. (It isn't visible from the right or bottom since other trees of height 5 are in the way.)
    The top-middle 5 is visible from the top and right.
    The top-right 1 is not visible from any direction; for it to be visible, there would need to only be trees of height 0 between it and an edge.
    The left-middle 5 is visible, but only from the right.
    The center 3 is not visible from any direction; for it to be visible, there would need to be only trees of at most height 2 between it and an edge.
    The right-middle 3 is visible from the right.
    In the bottom row, the middle 5 is visible, but the 3 and 4 are not.

With 16 trees visible on the edge and another 5 visible in the interior, a total of 21 trees are visible in this arrangement.

Consider your map; how many trees are visible from outside the grid?

--- Part Two ---

Content with the amount of tree cover available, the Elves just need to know the best spot to build their tree house: they would like to be able to see a lot of trees.

To measure the viewing distance from a given tree, look up, down, left, and right from that tree; stop if you reach an edge or at the first tree that is the same height or taller than the tree under consideration.
(If a tree is right on the edge, at least one of its viewing distances will be zero.)

The Elves don't care about distant trees taller than those found by the rules above; the proposed tree house has large eaves to keep it dry, so they wouldn't be able to see higher than the tree house anyway.

In the example above, consider the middle 5 in the second row:

30373
25512
65332
33549
35390

    Looking up, its view is not blocked; it can see 1 tree (of height 3).
    Looking left, its view is blocked immediately; it can see only 1 tree (of height 5, right next to it).
    Looking right, its view is not blocked; it can see 2 trees.
    Looking down, its view is blocked eventually; it can see 2 trees (one of height 3, then the tree of height 5 that blocks its view).

A tree's scenic score is found by multiplying together its viewing distance in each of the four directions.
For this tree, this is 4 (found by multiplying 1 * 1 * 2 * 2).

However, you can do even better: consider the tree of height 5 in the middle of the fourth row:

30373
25512
65332
33549
35390

    Looking up, its view is blocked at 2 trees (by another tree with a height of 5).
    Looking left, its view is not blocked; it can see 2 trees.
    Looking down, its view is also not blocked; it can see 1 tree.
    Looking right, its view is blocked at 2 trees (by a massive tree of height 9).

This tree's scenic score is 8 (2 * 2 * 1 * 2); this is the ideal spot for the tree house.

Consider each tree on your map. What is the highest scenic score possible for any tree?
"""
from pathlib import Path

import numpy as np


def make_grid(inputs: list[str]) -> np.ndarray:
    """Loads inputs and returns a 2D numpy array grid."""
    grid = []
    for line in inputs:
        grid.append([int(element) for element in line])
    return np.array(grid)


# ----- Part 1 ----- #


def is_tree_visible(grid: np.ndarray, row: int, col: int) -> bool:
    """Returns True if the tree at (row, col) is visible from outside the grid."""
    tree_val = grid[row, col]
    nrows, ncols = grid.shape

    # Check all trees above the current tree: looking from the top
    for i in range(row - 1, -1, -1):
        if grid[i][col] >= tree_val:  # if a tree on the way is higher
            break  # stop checking, not visible from this direction
    else:  # otherwise it's visible, we can return
        return True  # return so we don't check from other directions and count as visible several times

    # Check all trees below current tree: looking from the bottom
    for i in range(row + 1, ncols):
        if grid[i][col] >= tree_val:  # if a tree on the way is higher
            break  # stop checking, not visible from this direction
    else:  # otherwise it's visible, we can return
        return True  # return so we don't check from other directions and count as visible several times

    # Check all trees to the left of current tree: looking from the left
    for neighbour in reversed(grid[row][:col]):
        if neighbour >= tree_val:  # if a tree on the way is higher
            break  # stop checking, not visible from this direction
    else:  # otherwise it's visible, we can return
        return True  # return so we don't check from other directions and count as visible several times

    # Check all trees to the right of current tree: looking from the right
    for neighbour in grid[row][col + 1 :]:
        if neighbour >= tree_val:  # if a tree on the way is higher
            break  # stop checking, not visible from this direction
    else:  # otherwise it's visible, we can return
        return True  # stop checking, not visible from this direction

    return False  # not visible from any direction


# ----- Part 2 ----- #


def scenic_score(grid: np.ndarray, row: int, col: int) -> int:
    """Returns the scenic score of the tree at (row, col)."""
    tree_val = grid[row][col]
    up, down, left, right = 0, 0, 0, 0  # viewing distance in each direction

    # Check viewing distance above current tree
    for i in range(row - 1, -1, -1):
        up += 1
        if grid[i][col] >= tree_val:
            break

    # Check viewing distance below current tree
    for i in range(row + 1, len(grid)):
        down += 1
        if grid[i][col] >= tree_val:
            break

    # Check viewing distance left of current tree
    for neighbour in reversed(grid[row][:col]):
        left += 1
        if neighbour >= tree_val:
            break

    # Check viewing distance right of current tree
    for neighbour in grid[row][col + 1 :]:
        right += 1
        if neighbour >= tree_val:
            break

    return up * down * right * left  # scenic score is the product of these


# ----- Running ----- #

if __name__ == "__main__":
    inputs = Path("input.txt").read_text().splitlines()
    grid: np.ndarray = make_grid(inputs)
    nrows, ncols = grid.shape

    # Part 1
    visible_trees = (nrows + ncols) * 2 - 4  # all trees on the edges are visible
    # Checking the inner trees
    for row in range(1, nrows - 1):
        for col in range(1, ncols - 1):
            if is_tree_visible(grid, row, col):
                visible_trees += 1
    print("Part 1:", visible_trees)

    # Part 2
    highest_scenic_score = 0
    for row in range(1, nrows - 1):
        for col in range(1, ncols - 1):
            current_tree_score = scenic_score(grid, row, col)
            if current_tree_score > highest_scenic_score:
                highest_scenic_score = current_tree_score
    print("Part 2:", highest_scenic_score)
