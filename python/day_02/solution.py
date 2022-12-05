"""
--- Day 2: Rock Paper Scissors ---

The Elves begin to set up camp on the beach.
To decide whose tent gets to be closest to the snack storage, a giant Rock Paper Scissors tournament is already in progress.

Rock Paper Scissors is a game between two players.
Each game contains many rounds; in each round, the players each simultaneously choose one of Rock, Paper, or Scissors using a hand shape.
Then, a winner for that round is selected: Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock.
If both players choose the same shape, the round instead ends in a draw.

Appreciative of your help yesterday, one Elf gives you an encrypted strategy guide (your puzzle input) that they say will be sure to help you win.
"The first column is what your opponent is going to play: A for Rock, B for Paper, and C for Scissors.
The second column--" Suddenly, the Elf is called away to help with someone's tent.

The second column, you reason, must be what you should play in response: X for Rock, Y for Paper, and Z for Scissors.
Winning every time would be suspicious, so the responses must have been carefully chosen.

The winner of the whole tournament is the player with the highest score.
Your total score is the sum of your scores for each round.
The score for a single round is the score for the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors) plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).

Since you can't be sure if the Elf is trying to help you or trick you, you should calculate the score you would get if you were to follow the strategy guide.

For example, suppose you were given the following strategy guide:

A Y
B X
C Z

This strategy guide predicts and recommends the following:

    In the first round, your opponent will choose Rock (A), and you should choose Paper (Y). This ends in a win for you with a score of 8 (2 because you chose Paper + 6 because you won).
    In the second round, your opponent will choose Paper (B), and you should choose Rock (X). This ends in a loss for you with a score of 1 (1 + 0).
    The third round is a draw with both players choosing Scissors, giving you a score of 3 + 3 = 6.

In this example, if you were to follow the strategy guide, you would get a total score of 15 (8 + 1 + 6).

What would your total score be if everything goes exactly according to your strategy guide?

--- Part Two ---

The Elf finishes helping with the tent and sneaks back over to you.
"Anyway, the second column says how the round needs to end: X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win. Good luck!"

The total score is still calculated in the same way, but now you need to figure out what shape to choose so the round ends as indicated.
The example above now goes like this:

    In the first round, your opponent will choose Rock (A), and you need the round to end in a draw (Y), so you also choose Rock. This gives you a score of 1 + 3 = 4.
    In the second round, your opponent will choose Paper (B), and you choose Rock so you lose (X) with a score of 1 + 0 = 1.
    In the third round, you will defeat your opponent's Scissors with Rock for a score of 1 + 6 = 7.

Now that you're correctly decrypting the ultra top secret strategy guide, you would get a total score of 12.

Following the Elf's instructions for the second column, what would your total score be if everything goes exactly according to your strategy guide?
"""
from pathlib import Path

# ----- For Part 1 ----- #

shape_to_points = {"rock": 1, "paper": 2, "scissors": 3}
outcome_to_points = {"win": 6, "draw": 3, "loss": 0}
letter_to_shape = {"a": "rock", "b": "paper", "c": "scissors", "x": "rock", "y": "paper", "z": "scissors"}
letter_to_outcome = {"x": "loss", "y": "draw", "z": "win"}


def round_score(own_shape: str, outcome: str) -> int:
    """Returns the score of the round."""
    shape_score = shape_to_points[own_shape.lower()]
    outcome_score = outcome_to_points[outcome.lower()]
    return shape_score + outcome_score


def round_outcome(opponent_shape: str, own_shape: str) -> str:
    """Returns your winning outcome for the round knowing the opponnent and your shape."""
    if opponent_shape == own_shape:
        return "draw"

    if opponent_shape == "rock":
        if own_shape == "paper":
            return "win"
        return "loss"

    if opponent_shape == "paper":
        if own_shape == "scissors":
            return "win"
        return "loss"

    if opponent_shape == "scissors":
        if own_shape == "rock":
            return "win"
        return "loss"


# ----- For Part 2 ----- #


def find_own_shape(opponent_shape: str, outcome: str) -> str:
    """Returns the shape to play to reach the desired round outcome based on the opponent's shape."""
    if outcome.lower() == "draw":
        return opponent_shape

    elif outcome.lower() == "win":
        if opponent_shape.lower() == "rock":
            return "paper"
        elif opponent_shape.lower() == "paper":
            return "scissors"
        else:
            return "rock"

    else:  # we need to lose
        if opponent_shape.lower() == "rock":
            return "scissors"
        elif opponent_shape.lower() == "paper":
            return "rock"
        else:
            return "paper"


if __name__ == "__main__":
    rounds = Path("input.txt").read_text().splitlines()

    total_score = 0
    for round in rounds:
        opponent_letter, own_letter = round.split()
        opponent_shape = letter_to_shape[opponent_letter.lower()]
        own_shape = letter_to_shape[own_letter.lower()]
        outcome = round_outcome(opponent_shape, own_shape)
        total_score += round_score(own_shape, outcome)

    print("Part 1: ", total_score)

    total_score = 0
    for round in rounds:
        opponent_letter, outcome_letter = round.split()
        opponent_shape = letter_to_shape[opponent_letter.lower()]
        wanted_outcome = letter_to_outcome[outcome_letter.lower()]
        own_shape = find_own_shape(opponent_shape, wanted_outcome)
        outcome = round_outcome(opponent_shape, own_shape)
        total_score += round_score(own_shape, outcome)

    print("Part 2: ", total_score)
