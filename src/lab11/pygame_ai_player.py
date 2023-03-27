import random
from turn_combat import CombatPlayer

""" Create PyGameAIPlayer class here"""
class PyGameAIPlayer:
    def select_action(self, state):
        return ord(str(state.current_city+1))


""" Create PyGameAICombatPlayer class here"""
class PyGameAICombatPlayer(CombatPlayer):
    def __init__(self, name):
        super().__init__(name),

    def select_action(self, state):
        self.weapon = random.randint(0, 2)
        return self.weapon
