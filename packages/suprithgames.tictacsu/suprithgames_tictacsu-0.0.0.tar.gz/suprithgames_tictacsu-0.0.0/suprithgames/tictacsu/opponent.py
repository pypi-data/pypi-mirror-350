# tictacsu/opponent.py

import random
from .game import TicTacToe

class Opponent:
    def choose_move(self, game: TicTacToe):
        # Choose randomly from available spots
        available = game.available_moves()
        if available:
            return random.choice(available)
        return None
