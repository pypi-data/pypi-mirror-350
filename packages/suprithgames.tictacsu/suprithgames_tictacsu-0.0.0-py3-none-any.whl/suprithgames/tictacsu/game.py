# tictacsu/game.py

class TicTacToe:
    def __init__(self):
        self.board = [" " for _ in range(9)]

    def display_board(self):
        print("\n")
        for row in [self.board[i:i + 3] for i in range(0, 9, 3)]:
            print("|".join(row))
            print("-" * 5)
        print("\n")

    def make_move(self, position, player):
        if self.board[position] == " ":
            self.board[position] = player
            return True
        return False

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == " "]

    def check_winner(self, player):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        for combo in win_combinations:
            if all(self.board[i] == player for i in combo):
                return True
        return False

    def is_draw(self):
        return " " not in self.board
