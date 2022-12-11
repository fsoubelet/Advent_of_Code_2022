from collections import deque
from math import prod


class Monkey:
    def __init__(self, items: deque, operation, test):
        self.items = items
        self.operation = operation
        self.test = test
        self.inspections = 0

    def __repr__(self):
        return f"{self.operation} {self.test} {self.inspections}"

    def inspect(self, mod, is_first_part):
        item = self.items.popleft()
        optr, opnd = self.operation
        dvsr, tr, fl = self.test
        if opnd == "old":
            opnd = item
        item = (item * opnd if optr == "*" else item + opnd) % mod
        if is_first_part:
            item //= 3
        self.inspections += 1
        return tr if item % dvsr == 0 else fl, item


def monkey_business(rounds):
    with open("input.txt") as file:
        monkeys = []
        items = []
        mod = 1
        for monkey in (monkey.split("\n") for monkey in file.read().split("\n\n")):
            items = deque([int(item) for item in monkey[1].split(": ")[1].split(",")])
            operation = monkey[2].split()
            operation = operation[-2], "old" if operation[-1] == "old" else int(operation[-1])
            test = int(monkey[3].split()[-1]), int(monkey[4].split()[-1]), int(monkey[5].split()[-1])
            mod *= test[0]
            monkeys.append(Monkey(items, operation, test))
        for _ in range(rounds):
            for monkey in monkeys:
                while monkey.items:
                    to, item = monkey.inspect(mod, rounds == 20)
                    monkeys[to].items.append(item)
        return prod(sorted(monkey.inspections for monkey in monkeys)[-2:])


print(monkey_business(20))
# print(monkey_business(10_000))
