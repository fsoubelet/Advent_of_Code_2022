"""
--- Day 5: Supply Stacks ---

The expedition can depart as soon as the final supplies have been unloaded from the ships.
Supplies are stored in stacks of marked crates, but because the needed supplies are buried under many other crates, the crates need to be rearranged.

The ship has a giant cargo crane capable of moving crates between stacks.
To ensure none of the crates get crushed or fall over, the crane operator will rearrange them in a series of carefully-planned steps.
After the crates are rearranged, the desired crates will be at the top of each stack.

The Elves don't want to interrupt the crane operator during this delicate procedure, but they forgot to ask her which crate will end up where, and they want to be ready to unload them as soon as possible so they can embark.

They do, however, have a drawing of the starting stacks of crates and the rearrangement procedure (your puzzle input).
For example:

    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2

In this example, there are three stacks of crates.
Stack 1 contains two crates: crate Z is on the bottom, and crate N is on top.
Stack 2 contains three crates; from bottom to top, they are crates M, C, and D.
Finally, stack 3 contains a single crate, P.

Then, the rearrangement procedure is given.
In each step of the procedure, a quantity of crates is moved from one stack to a different stack.
In the first step of the above rearrangement procedure, one crate is moved from stack 2 to stack 1, resulting in this configuration:

[D]        
[N] [C]    
[Z] [M] [P]
 1   2   3 

In the second step, three crates are moved from stack 1 to stack 3.
Crates are moved one at a time, so the first crate to be moved (D) ends up below the second and third crates:

        [Z]
        [N]
    [C] [D]
    [M] [P]
 1   2   3

Then, both crates are moved from stack 2 to stack 1.
Again, because crates are moved one at a time, crate C ends up below crate M:

        [Z]
        [N]
[M]     [D]
[C]     [P]
 1   2   3

Finally, one crate is moved from stack 1 to stack 2:

        [Z]
        [N]
        [D]
[C] [M] [P]
 1   2   3

The Elves just need to know which crate will end up on top of each stack; in this example, the top crates are C in stack 1, M in stack 2, and Z in stack 3, so you should combine these together and give the Elves the message CMZ.

After the rearrangement procedure completes, what crate ends up on top of each stack?

--- Part Two ---

As you watch the crane operator expertly rearrange the crates, you notice the process isn't following your prediction.

Some mud was covering the writing on the side of the crane, and you quickly wipe it away.
The crane isn't a CrateMover 9000 - it's a CrateMover 9001.

The CrateMover 9001 is notable for many new and exciting features: air conditioning, leather seats, an extra cup holder, and the ability to pick up and move multiple crates at once.

Again considering the example above, the crates begin in the same configuration:

    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

Moving a single crate from stack 2 to stack 1 behaves the same as before:

[D]        
[N] [C]    
[Z] [M] [P]
 1   2   3 

However, the action of moving three crates from stack 1 to stack 3 means that those three moved crates stay in the same order, resulting in this new configuration:

        [D]
        [N]
    [C] [Z]
    [M] [P]
 1   2   3

Next, as both crates are moved from stack 2 to stack 1, they retain their order as well:

        [D]
        [N]
[C]     [Z]
[M]     [P]
 1   2   3

Finally, a single crate is still moved from stack 1 to stack 2, but now it's crate C that gets moved:

        [D]
        [N]
        [Z]
[M] [C] [P]
 1   2   3

In this example, the CrateMover 9001 has put the crates in a totally different order: MCD.

Before the rearrangement process finishes, update your simulation so that the Elves know where they should stand to be ready to unload the final supplies.
After the rearrangement procedure completes, what crate ends up on top of each stack?
"""
import re

from copy import deepcopy
from pathlib import Path

# ----- For Part 1 ----- #


def load_crates_positions(input_lines: str) -> dict[int, str]:
    """Load the starting positions of the crates."""
    stack_lines = input_lines[:8]  # first 8 lines
    stack_lines.reverse()  # reverse the order for parsing
    stacks = {}
    idx = 0

    for char in range(1, len(stack_lines[0]), 4):  # each stack is 4 chars apart
        stacks[idx] = ""
        for l in range(len(stack_lines)):
            stacks[idx] += stack_lines[l][char]
        stacks[idx] = stacks[idx].strip()
        idx += 1

    return stacks


def parse_move_instruction(instruction_line: str) -> tuple[int, int, int]:
    """Returns the quantity, start and end stack for the instruction."""
    quantity, start, end = re.findall(r"\d+", instruction_line)
    quantity = int(quantity)
    start = int(start) - 1
    end = int(end) - 1
    return quantity, start, end


def move(stacks: dict[int, str], instruction: str):
    """Gives the new stack state after doing the move instruction."""
    staks = deepcopy(stacks)
    quantity, start_position, end_position = parse_move_instruction(instruction)

    for _ in range(quantity):
        # which element we will move, last one in the string = top of the stack
        cargo = staks[start_position][-1]
        staks[start_position] = staks[start_position][:-1]  # removes the last element
        staks[end_position] += cargo  # with strings this appends

    return staks


# ----- For Part 2 ----- #


def move_part2(stacks: dict[int, str], instruction: str):
    """Almost the same as part 1 but several crates are moved at the same time."""
    staks = deepcopy(stacks)
    # print(instruction)
    quantity, start_position, end_position = parse_move_instruction(instruction)
    # print(quantity, start_position, end_position)

    # which elements we will move, last 'quantity' ones in the string = top of the stack
    cargo = staks[start_position][-quantity:]  # select all at once
    # print("Moving: ", cargo)
    # print("From: ", staks[start_position])
    # print("Which becomes: ", staks[start_position][:-quantity])
    # print("To: ", staks[end_position])
    # print("Which becomes: ", staks[end_position] + cargo)
    staks[start_position] = staks[start_position][:-quantity]  # removes the elements together
    staks[end_position] += cargo  # with strings this appends
    # print(stacks)
    return staks


# ----- Running ----- #

if __name__ == "__main__":
    inputs = Path("input.txt").read_text().splitlines()
    stacks = load_crates_positions(inputs)
    moves = [line for line in inputs if line.startswith("move")]

    # Part 1
    final_string = ""
    for instruction in moves:
        stacks = move(stacks, instruction)
    for crate in stacks.values():
        final_string += crate[-1]  # get the one on top
    print(f"Part 1: {final_string}")

    # Part 2
    stacks = load_crates_positions(inputs)  # reset the stacks
    final_string = ""
    for instruction in moves:
        stacks = move_part2(stacks, instruction)
    for crate in stacks.values():
        final_string += crate[-1]  # get the one on top
    print(f"Part 2: {final_string}")
