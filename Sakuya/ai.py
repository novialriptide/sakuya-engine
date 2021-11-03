import typing
import random

class Decision:
    def __init__(self, method, chance: float):
        """
        :param func method: the method that will be executed
        :param float chance: the percentage of the decision happening
        """
        self.method = method
        self.chance = chance

class AI:
    def __init__(self, decisions: typing.Sequence[Decision]):
        self.decisions = self.decisions

    def update_decisions(self):
        for d in self.decisions:
            if random.randrange(0, 1) > d.chance:
                d.method()