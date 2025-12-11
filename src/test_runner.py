from game import TicTacToe
from multiprocessing import Pool, cpu_count

def play_single_game_pair(args):
    ai1_symbol, ai2_symbol = args
    g1 = TicTacToe()
    g1.current_player = ai1_symbol
    while True:
        current = g1.current_player
        ai_symbol = current
        human_symbol = ai2_symbol if current == ai1_symbol else ai1_symbol
        move = g1.get_best_move(ai_symbol, human_symbol, use_learning=False)
        if move is None:
            result1 = g1.check_winner()
            break
        g1.make_move(move, ai_symbol)
        result1 = g1.check_winner()
        if result1 is not None:
            break

    g2 = TicTacToe()
    g2.current_player = ai2_symbol
    while True:
        current = g2.current_player
        ai_symbol = current
        human_symbol = ai1_symbol if current == ai2_symbol else ai2_symbol
        move = g2.get_best_move(ai_symbol, human_symbol, use_learning=False)
        if move is None:
            result2 = g2.check_winner()
            break
        g2.make_move(move, ai_symbol)
        result2 = g2.check_winner()
        if result2 is not None:
            break

    return result1, result2

def run_experiments_parallel(n_games=10000):
    n_pairs = n_games
    args = [("X", "O")] * n_pairs

    stats_first = {"X": 0, "O": 0, "Draw": 0}
    stats_second = {"X": 0, "O": 0, "Draw": 0}
    completed = 0

    print(f"Running {n_pairs} AI-vs-AI pairs on {cpu_count()} cores...")

    with Pool(processes=cpu_count()) as pool:
        for r1, r2 in pool.imap_unordered(play_single_game_pair, args):
            completed += 1
            stats_first[r1] = stats_first.get(r1, 0) + 1
            stats_second[r2] = stats_second.get(r2, 0) + 1

            if completed % 10 == 0 or completed == n_pairs:
                pct = 100.0 * completed / n_pairs
                print(f"  completed {completed}/{n_pairs} pairs ({pct:.1f}%)")

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
    run_experiments_parallel(5000)
