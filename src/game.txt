class TicTacToe:
    def __init__(self): 
        self.board = [' ' for _ in range(9)]  # 3x3 board
        self.current_player = None  # keep track of winner!
    
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


    def get_best_move(self, ai_symbol, human_symbol):
        # use minimax to get best move for AI
        best_score = float("-inf")
        best_move = None 

        for move in self.get_empty_positions():
            self.board[move] = ai_symbol
            score = self.minimax(False, ai_symbol, human_symbol)
            self.board[move] = ' ' 
            if score > best_score: 
                best_score = score 
                best_move = move
        return best_move
        

    def reset(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = None

    