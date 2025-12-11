import json
import os
import random


class TicTacToe:
    def __init__(self): 
        self.board = [' ' for _ in range(9)]  # 3x3 board
        self.current_player = None  # keep track of winner!
        self.history = {}  # to keep track of moves made
        self.state_action_trace = [] # to keep track of state-action pairs for RL
        self.memory_file = "tictactoe_memory.json"  # file to store memory data
        self.load_memory() 


    def encode_state(self, ai_symbol, human_symbol):
        mapping = { ' ': '0', ai_symbol: '1', human_symbol: '2' }
        return ''.join([mapping[spot] for spot in self.board])
    
    def load_memory(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        self.history = data
                    else:
                        self.history = {}
            except Exception:
                self.history = {}
        else:
            self.history = {}
    
    def save_memory(self):
        try: 
            with open(self.memory_file, 'w') as f:
                json.dump(self.history, f, indent = 2)
        except Exception:
            pass
    
    def record_ai_move(self, ai_symbol, human_symbol, move):
        state = self.encode_state(ai_symbol, human_symbol)
        self.state_action_trace.append((state, move))

    def update_from_result(self, result, ai_symbol):
        # reward: +1 win, -1 loss, 0 draw
        if result == ai_symbol:
            reward = 1
        elif result == "Draw":
            reward = 0
        else:
            reward = -1

        for state, move in self.state_action_trace:
            if state not in self.history:
                self.history[state] = {}
            if str(move) not in self.history[state]:
                # [wins, losses, draws]
                self.history[state][str(move)] = [0, 0, 0]
            stats = self.history[state][str(move)]
            if reward == 1:
                stats[0] += 1
            elif reward == -1:
                stats[1] += 1
            else:
                stats[2] += 1
        # clear trace for next game and persist
        self.state_action_trace = []
        self.save_memory()

    def get_move_stats_score(self, state, move):
        # Higher is better: simple win-rate style score
        if state not in self.history or str(move) not in self.history[state]:
            return 0.0  # no info yet
        wins, losses, draws = self.history[state][str(move)]
        total = wins + losses + draws
        if total == 0:
            return 0.0
        # example: win_rate - loss_rate
        return (wins - losses) / total



    
    def make_move(self, position, player):
        if self.board[position] == ' ':
            self.board[position] = player
            self.current_player = 'O' if player == 'X' else 'X'  # Switch player
            return True
        return False
    
    def check_winner(self):
        # Check rows, columns and diagonals for a win
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6)              # diagonals
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':# check for the winner 
                self.current_player = self.board[combo[0]] # winner 
                return self.current_player
        if ' ' not in self.board:
            return 'Draw'  # Game is a draw
        return None  # No winner yet
    

    def get_empty_positions(self):
        # return list of empty positions on the board
        return [i for i, spot in enumerate(self.board) if spot == ' ']
    
    def get_score(self, ai_symbol, human_symbol):
        result = self.check_winner()
        if result == ai_symbol:
            return 1
        elif result == human_symbol:
            return -1
        elif result == 'Draw':
            return 0 
    
    
    def minimax(self, is_max_turn, ai_symbol, human_symbol): 
        # create minimax algorithm to find best move
        # Base case: if the game is over, return the score of this state
        if self.check_winner() is not None:
            return self.get_score(ai_symbol, human_symbol)

    # Max player's turn
        if is_max_turn:
            best_value = float("-inf")
            for move in self.get_empty_positions():
                self.board[move] = ai_symbol # to make the move 
                value = self.minimax(False, ai_symbol, human_symbol)
                self.board[move] = ' ' # to reset the move 
                best_value = max(best_value, value)
            return best_value

    # Min player's turn
        else:
            best_value = float("inf")
            for move in self.get_empty_positions():
                self.board[move] = human_symbol
                value = self.minimax(True, ai_symbol, human_symbol)
                self.board[move] = ' '
                best_value = min(best_value, value)
            return best_value


    def get_best_move(self, ai_symbol, human_symbol, use_learning=True):
        best_score = float("-inf")
        move_scores = []

        for move in self.get_empty_positions():
            self.board[move] = ai_symbol
            score = self.minimax(False, ai_symbol, human_symbol)
            self.board[move] = ' '
            move_scores.append((move, score))
            if score > best_score:
                best_score = score

        # keep only moves with best minimax score (optimal moves)
        candidate_moves = [m for m, s in move_scores if s == best_score]

        if not use_learning or len(candidate_moves) <= 1:
            best_move = random.choice(candidate_moves) if candidate_moves else None
        else:
            # use learned stats to choose among optimal moves
            state = self.encode_state(ai_symbol, human_symbol)
            best_move = None
            best_learn_score = float("-inf")
            for m in candidate_moves:
                ls = self.get_move_stats_score(state, m)
                if ls > best_learn_score:
                    best_learn_score = ls
                    best_move = m
            # if no learned preference yet, fall back to random among candidates
            if best_move is None:
                best_move = random.choice(candidate_moves)

        # record chosen move for learning
        if best_move is not None:
            self.record_ai_move(ai_symbol, human_symbol, best_move)
        return best_move
    
    def clear_memory(self):
        self.history = {}
        self.state_action_trace = []
        if os.path.exists(self.memory_file):
            os.remove(self.memory_file)
        

    def reset(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = None

    