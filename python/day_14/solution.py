"""
--- Day 14: Regolith Reservoir ---

The distress signal leads you to a giant waterfall!
Actually, hang on - the signal seems like it's coming from the waterfall itself, and that doesn't make any sense.
However, you do notice a little path that leads behind the waterfall.

Correction: the distress signal leads you behind a giant waterfall!
There seems to be a large cave system here, and the signal definitely leads further inside.

As you begin to make your way deeper underground, you feel the ground rumble for a moment.
Sand begins pouring into the cave! If you don't quickly figure out where the sand is going, you could quickly become trapped!

Fortunately, your familiarity with analyzing the path of falling material will come in handy here.
You scan a two-dimensional vertical slice of the cave above you (your puzzle input) and discover that it is mostly air with structures made of rock.

Your scan traces the path of each solid rock structure and reports the x,y coordinates that form the shape of the path, where x represents distance to the right and y represents distance down.
Each path appears as a single line of text in your scan. After the first point of each path, each point indicates the end of a straight horizontal or vertical line to be drawn from the previous point.
For example:

498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9

This scan means that there are two paths of rock; the first path consists of two straight lines, and the second path consists of three straight lines.
(Specifically, the first path consists of a line of rock from 498,4 through 498,6 and another line of rock from 498,6 through 496,6.)

The sand is pouring into the cave from point 500,0.

Drawing rock as #, air as ., and the source of the sand as +, this becomes:


  4     5  5
  9     0  0
  4     0  3
0 ......+...
1 ..........
2 ..........
3 ..........
4 ....#...##
5 ....#...#.
6 ..###...#.
7 ........#.
8 ........#.
9 #########.

Sand is produced one unit at a time, and the next unit of sand is not produced until the previous unit of sand comes to rest.
A unit of sand is large enough to fill one tile of air in your scan.

A unit of sand always falls down one step if possible.
If the tile immediately below is blocked (by rock or sand), the unit of sand attempts to instead move diagonally one step down and to the left.
If that tile is blocked, the unit of sand attempts to instead move diagonally one step down and to the right.
Sand keeps moving as long as it is able to do so, at each step trying to move down, then down-left, then down-right.
If all three possible destinations are blocked, the unit of sand comes to rest and no longer moves, at which point the next unit of sand is created back at the source.

So, drawing sand that has come to rest as o, the first unit of sand simply falls straight down and then stops:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
......o.#.
#########.

The second unit of sand then falls straight down, lands on the first one, and then comes to rest to its left:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
.....oo.#.
#########.

After a total of five units of sand have come to rest, they form this pattern:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
......o.#.
....oooo#.
#########.

After a total of 22 units of sand:

......+...
..........
......o...
.....ooo..
....#ooo##
....#ooo#.
..###ooo#.
....oooo#.
...ooooo#.
#########.

Finally, only two more units of sand can possibly come to rest:

......+...
..........
......o...
.....ooo..
....#ooo##
...o#ooo#.
..###ooo#.
....oooo#.
.o.ooooo#.
#########.

Once all 24 units of sand shown above have come to rest, all further sand flows out the bottom, falling into the endless void.
Just for fun, the path any new sand takes before falling forever is shown here with ~:

.......+...
.......~...
......~o...
.....~ooo..
....~#ooo##
...~o#ooo#.
..~###ooo#.
..~..oooo#.
.~o.ooooo#.
~#########.
~..........
~..........
~..........

Using your scan, simulate the falling sand.
How many units of sand come to rest before sand starts flowing into the abyss below?

--- Part Two ---

You realize you misread the scan.
There isn't an endless void at the bottom of the scan - there's floor, and you're standing on it!

You don't have time to scan the floor, so assume the floor is an infinite horizontal line with a y coordinate equal to two plus the highest y coordinate of any point in your scan.

In the example above, the highest y coordinate of any point is 9, and so the floor is at y=11. (This is as if your scan contained one extra rock path like -infinity,11 -> infinity,11.)
With the added floor, the example above now looks like this:

        ...........+........
        ....................
        ....................
        ....................
        .........#...##.....
        .........#...#......
        .......###...#......
        .............#......
        .............#......
        .....#########......
        ....................
<-- etc #################### etc -->

To find somewhere safe to stand, you'll need to simulate falling sand until a unit of sand comes to rest at 500,0, blocking the source entirely and stopping the flow of sand into the cave.
In the example above, the situation finally looks like this after 93 units of sand come to rest:

............o............
...........ooo...........
..........ooooo..........
.........ooooooo.........
........oo#ooo##o........
.......ooo#ooo#ooo.......
......oo###ooo#oooo......
.....oooo.oooo#ooooo.....
....oooooooooo#oooooo....
...ooo#########ooooooo...
..ooooo.......ooooooooo..
#########################

Using your scan, simulate the falling sand until the source of the sand becomes blocked.
How many units of sand come to rest?
"""
from pathlib import Path


def translate_x(x: int, width: int) -> int:
    """Helper to translate x into our grid offset."""
    return x - (500 - width // 2)


if __name__ == "__main__":
    inputs = Path("input.txt").read_text().splitlines()

    # Create a sufficiently sized grid filled with air pockets
    width, height = 500, 180
    grid: list[str] = [["."] * width for _ in range(height)]

    # Now we add rocks
    abyss_y = 0
    for line in inputs:
        steps = list(map(lambda s: list(map(int, s.split(","))), line.split(" -> ")))
        for (x, y), (dest_x, dest_y) in zip(steps, steps[1:]):
            while True:
                grid[y][translate_x(x, width)] = "#"
                if x != dest_x:
                    x += 1 if x < dest_x else -1
                elif y != dest_y:
                    y += 1 if y < dest_y else -1
                else:
                    break

                # We keep track of the max y position so we know where abyss is
                if y > abyss_y:
                    abyss_y = y

    # Let's create the floor - for part 2
    for x in range(width):
        grid[abyss_y + 2][x] = "#"

    # Let it sand, let is sand, let it sand
    resting_sands: int = 0
    part1: int = 0
    sand_source = (translate_x(500, width), 0)
    path = [sand_source]

    while True:
        x, y = path.pop()
        while True:
            if part1 == 0 and y > abyss_y:
                part1 = resting_sands
            path.append((x, y))

            # We can move down
            if grid[y + 1][x] == ".":
                y += 1

            # Can't move down, we go down+left
            elif grid[y + 1][x - 1] == ".":
                y += 1
                x -= 1

            # Can't move down nor down+left, we go down+right
            elif grid[y + 1][x + 1] == ".":
                y += 1
                x += 1
            else:
                break

        # We place sand
        grid[y][x] = "o"
        resting_sands += 1
        path.pop()

        # We break out of the loop (= stop) if we blocked the source of sand
        if (x, y) == sand_source:
            break

    print("Part 1: ", part1)
    print("Part 2: ", resting_sands)
