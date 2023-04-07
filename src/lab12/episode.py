''' 
Lab 12: Beginnings of Reinforcement Learning
We will modularize the code in pygrame_combat.py from lab 11 together.

Then it's your turn!
Create a function called run_episode that takes in two players
and runs a single episode of combat between them. 
As per RL conventions, the function should return a list of tuples
of the form (observation/state, action, reward) for each turn in the episode.
Note that observation/state is a tuple of the form (player1_health, player2_health).
Action is simply the weapon selected by the player.
Reward is the reward for the player for that turn.
'''
import sys
from pathlib import Path
sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))

import lab11.pygame_combat as pc
from lab11.turn_combat import Combat
from lab11.pygame_ai_player import PyGameAICombatPlayer
from lab11.pygame_combat import PyGameComputerCombatPlayer
 
def run_episode(player1, player2):
    current_game = Combat()
    turns_list = []
    while current_game.gameOver == False:
        reward = pc.run_turn(current_game, player1, player2)
        turn_result = ((player1.health, player2.health), player1.weapon, reward)
        turns_list.append(turn_result)
    return turns_list

if __name__ == "__main__":
    player = PyGameAICombatPlayer("Legolas")
    opponent = PyGameComputerCombatPlayer("Computer")
    result = run_episode(player, opponent)
    for entry in result:
        print(entry)