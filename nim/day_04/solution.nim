#[
--- Day 4: Camp Cleanup ---

Space needs to be cleared before the last supplies can be unloaded from the ships, and so several Elves have been assigned the job of cleaning up sections of the camp.
Every section has a unique ID number, and each Elf is assigned a range of section IDs.

However, as some of the Elves compare their section assignments with each other, they've noticed that many of the assignments overlap.
To try to quickly find overlaps and reduce duplicated effort, the Elves pair up and make a big list of the section assignments for each pair (your puzzle input).

For example, consider the following list of section assignment pairs:

2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8

For the first few pairs, this list means:

    Within the first pair of Elves, the first Elf was assigned sections 2-4 (sections 2, 3, and 4), while the second Elf was assigned sections 6-8 (sections 6, 7, 8).
    The Elves in the second pair were each assigned two sections.
    The Elves in the third pair were each assigned three sections: one got sections 5, 6, and 7, while the other also got 7, plus 8 and 9.

This example list uses single-digit section IDs to make it easier to draw; your actual list might contain larger numbers. Visually, these pairs of section assignments look like this:

.234.....  2-4
.....678.  6-8

.23......  2-3
...45....  4-5

....567..  5-7
......789  7-9

.2345678.  2-8
..34567..  3-7

.....6...  6-6
...456...  4-6

.23456...  2-6
...45678.  4-8

Some of the pairs have noticed that one of their assignments fully contains the other.
For example, 2-8 fully contains 3-7, and 6-6 is fully contained by 4-6.
In pairs where one assignment fully contains the other, one Elf in the pair would be exclusively cleaning sections their partner will already be cleaning, so these seem like the most in need of reconsideration.
In this example, there are 2 such pairs.

In how many assignment pairs does one range fully contain the other?

--- Part Two ---

It seems like there is still quite a bit of duplicate work planned.
Instead, the Elves would like to know the number of pairs that overlap at all.

In the above example, the first two pairs (2-4,6-8 and 2-3,4-5) don't overlap, while the remaining four pairs (5-7,7-9, 2-8,3-7, 6-6,4-6, and 2-6,4-8) do overlap:

    5-7,7-9 overlaps in a single section, 7.
    2-8,3-7 overlaps all of the sections 3 through 7.
    6-6,4-6 overlaps in a single section, 6.
    2-6,4-8 overlaps in sections 4, 5, and 6.

So, in this example, the number of overlapping assignment pairs is 4.

In how many assignment pairs do the ranges overlap?
]#
import std/sets
import std/sequtils
import std/strutils

let sections = readFile("input.txt").splitLines()

# ----- For Part 1 ----- #

proc elf_sections(input_line: string): (HashSet[int], HashSet[int]) =
    # """Parses a line from the input, returns the sections assigned for each of the 2 elves."""
    let
        elf1: string = input_line.split(",")[0]
        elf1_start: int = elf1.split("-")[0].parseInt
        elf1_end: int = elf1.split("-")[1].parseInt

        elf2: string = input_line.split(",")[1]
        elf2_start: int = elf2.split("-")[0].parseInt
        elf2_end: int = elf2.split("-")[1].parseInt

        elf1_sections: seq[int] = toSeq(elf1_start..elf1_end)
        elf2_sections: seq[int] = toSeq(elf2_start..elf2_end)

        elf1_set: HashSet[int] = toHashSet(elf1_sections)
        elf2_set: HashSet[int] = toHashSet(elf2_sections)

    return (elf1_set, elf2_set)


var overlaps: Natural = 0
for line in sections:
    let (elf1, elf2) = elf_sections(line)
    if elf1 <= elf2 or elf2 <= elf1: # elf1 is a subset of elf2 or vice versa
        overlaps += 1
echo "Part 1: ", overlaps


# ----- For Part 1 ----- #

overlaps = 0
for line in sections:
    let (elf1, elf2) = elf_sections(line)
    if intersection(elf1, elf2).toSeq().len > 0: # the intersection isn't empty
        overlaps += 1
echo "Part 2: ", overlaps
