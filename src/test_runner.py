from game import TicTacToe
from multiprocessing import Pool, cpu_count


def play_single_game(ai1_symbol="X", ai2_symbol="O"):
    game = TicTacToe()
    game.current_player = ai1_symbol

    while True:
        current = game.current_player
        ai_symbol = current
        human_symbol = ai2_symbol if current == ai1_symbol else ai1_symbol  # just for API

        move = game.get_best_move(ai_symbol, human_symbol, use_learning=False)
        if move is None:
            # no moves left, check result
            result = game.check_winner()
            return result

        game.make_move(move, ai_symbol)
        result = game.check_winner()
        if result is not None:
            return result

def run_experiments(n_games=1000):
    stats_first = {"X": 0, "O": 0, "Draw": 0}
    stats_second = {"X": 0, "O": 0, "Draw": 0}

    print(f"Running {n_games} games with AI1 as X...")
    for i in range(1, n_games + 1):
        result = play_single_game("X", "O")
        stats_first[result] = stats_first.get(result, 0) + 1
        if i % 100 == 0:
            print(f"  completed {i}/{n_games} games (AI1 as X)")

    print(f"\nRunning {n_games} games with AI1 as O...")
    for i in range(1, n_games + 1):
        result = play_single_game("O", "X")
        stats_second[result] = stats_second.get(result, 0) + 1
        if i % 100 == 0:
            print(f"  completed {i}/{n_games} games (AI1 as O)")

    print("\n=== AI vs AI (AI1 starts as X) ===")
    total_first = sum(stats_first.values())
    for key in ["X", "O", "Draw"]:
        count = stats_first.get(key, 0)
        pct = 100.0 * count / total_first if total_first > 0 else 0.0
        print(f"{key}: {count} ({pct:.1f}%)")

    print("\n=== AI vs AI (AI1 starts as O) ===")
    total_second = sum(stats_second.values())
    for key in ["X", "O", "Draw"]:
        count = stats_second.get(key, 0)
        pct = 100.0 * count / total_second if total_second > 0 else 0.0
        print(f"{key}: {count} ({pct:.1f}%)")

if __name__ == "__main__":
    run_experiments(1000)
