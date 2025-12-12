from game import TicTacToe
from OpenAi import get_llm_move, board_to_text
import random

def play_one_game(llm_symbol="O", minimax_symbol="X"):
    game = TicTacToe()
    game.load_memory()  # optional
    game.current_player = "X"  # X always starts

    while True:
        winner = game.check_winner()
        if winner is not None:
            return winner  # "X", "O", or "Draw"

        if game.current_player == minimax_symbol:
            move = game.get_best_move(minimax_symbol, llm_symbol, use_learning=True)
            game.make_move(move, minimax_symbol)
        else:
            move = get_llm_move(game, llm_symbol, minimax_symbol)
            if move is None:
                # safety fallback
                empties = game.get_empty_positions()
                if not empties:
                    return "Draw"
                move = random.choice(empties)
            game.make_move(move, llm_symbol)

def run_match(num_games=10):
    scores = {
        "LLM": {"X": 0, "O": 0},
        "Minimax": {"X": 0, "O": 0},
        "Draw": 0,
    }

    for i in range(num_games):
        # alternate which side the LLM plays
        if i % 2 == 0:
            llm_symbol, minimax_symbol = "O", "X"
        else:
            llm_symbol, minimax_symbol = "X", "O"

        result = play_one_game(llm_symbol=llm_symbol, minimax_symbol=minimax_symbol)

        if result == llm_symbol:
            scores["LLM"][llm_symbol] += 1
            print(f"Game {i+1}: LLM wins as {llm_symbol}")
        elif result == minimax_symbol:
            scores["Minimax"][minimax_symbol] += 1
            print(f"Game {i+1}: Minimax wins as {minimax_symbol}")
        else:
            scores["Draw"] += 1
            print(f"Game {i+1}: Draw")

    print("\nFinal scores after", num_games, "games:")
    print("LLM as X:", scores["LLM"]["X"])
    print("LLM as O:", scores["LLM"]["O"])
    print("Minimax as X:", scores["Minimax"]["X"])
    print("Minimax as O:", scores["Minimax"]["O"])
    print("Draws:", scores["Draw"])

if __name__ == "__main__":
    run_match(100)