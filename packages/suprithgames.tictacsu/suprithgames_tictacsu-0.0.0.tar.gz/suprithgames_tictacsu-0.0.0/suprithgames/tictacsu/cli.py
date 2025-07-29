# tictacsu/cli.py

from .game import TicTacToe
from .opponent import Opponent
from .history import save_result, get_history, clear_history

def play_game():
    game = TicTacToe()
    opponent = Opponent()
    current_player = "X"  # Human
    computer = "O"

    print("🎮 Welcome to Tic Tac Toe!")
    player_name = input("Enter your name: ")

    while True:
        game.display_board()

        if current_player == "X":
            try:
                move = int(input("Choose your move (0-8): "))
                if move not in game.available_moves():
                    print("Invalid move. Try again.")
                    continue
                game.make_move(move, "X")
            except ValueError:
                print("Please enter a number between 0 and 8.")
                continue
        else:
            move = opponent.choose_move(game)
            print(f"Computer chose: {move}")
            game.make_move(move, "O")

        if game.check_winner(current_player):
            game.display_board()
            winner = player_name if current_player == "X" else "Computer"
            print(f"🏆 {winner} wins!")
            save_result(winner, "Win")
            break

        if game.is_draw():
            game.display_board()
            print("🤝 It's a draw!")
            save_result("Draw", "Draw")
            break

        current_player = "O" if current_player == "X" else "X"

    print("\n📜 Game History:")
    for line in get_history():
        print(line.strip())

if __name__ == "__main__":
    play_game()
