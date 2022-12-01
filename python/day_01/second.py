"""
--- Part Two ---

By the time you calculate the answer to the Elves' question, they've already realized that the Elf carrying the most Calories of food might eventually run out of snacks.

To avoid this unacceptable situation, the Elves would instead like to know the total Calories carried by the top three Elves carrying the most Calories.
That way, even if one of those Elves runs out of snacks, they still have two backups.

In the example above, the top three Elves are the fourth Elf (with 24000 Calories), then the third Elf (with 11000 Calories), then the fifth Elf (with 10000 Calories).
The sum of the Calories carried by these three elves is 45000.

Find the top three Elves carrying the most Calories.
How many Calories are those Elves carrying in total?
"""
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Elf:
    calories: int = 0


def elves_and_their_calories(inputs: list[str]) -> list[Elf]:
    """Returns a list of Elf objects with their calories each, from the inputs."""
    elves = []
    current = Elf()

    current = Elf()
    for line in inputs:
        if line == "":
            elves.append(current)
            current = Elf()
        else:
            current.calories += int(line)
    return elves


if __name__ == "__main__":
    inputs = Path("input.txt").read_text().splitlines()
    elves = elves_and_their_calories(inputs)
    calories = [elf.calories for elf in elves]
    top3_calories = sorted(calories, reverse=True)[:3]
    print(sum(top3_calories))
