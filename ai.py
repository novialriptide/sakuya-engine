import typing
import random
import pygame

class Decision:
    def __init__(self, method, chance: float):
        """
        :param func method: the method that will be executed
        :param float chance: the percentage of the decision happening
        """
        self.method = method
        self.chance = chance

class AI:
    """
    Makes a random decision every time an update_decisions() is executed
    """
    def __init__(self, decisions: typing.Sequence[Decision], update_tick, max_decisions: int=10):
        self.decisions = decisions
        self.max_decisions = max_decisions
        self.used_ticks = []
        self.update_tick = update_tick

    def update_decisions(self, world_ticks_elapsed):
        """
        Returns the amount of decisions made
        """
        if pygame.time.get_ticks() not in self.used_ticks and world_ticks_elapsed % self.update_tick == 0:
            decisions_made = 0
            for d in self.decisions:
                if decisions_made >= self.max_decisions: break

                if d.chance > random.random():
                    d.method()
                    decisions_made += 1

            self.used_ticks.append(pygame.time.get_ticks())
            return decisions_made
        return None