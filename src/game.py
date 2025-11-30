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
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                self.current_player = self.board[combo[0]]
                return self.current_player
        if ' ' not in self.board:
            return 'Draw'  # Game is a draw
        return None  # No winner yet
    

    def get_empty_positions(self):
        # return list of empty positions on the board
        return [i for i, spot in enumerate(self.board) if spot == ' ']
    
    
    def minimax(self, is_maximizing): 
        # create minimax algorithm to find best move
        pass  


    def get_best_move(self):
        # use minimax to get best move for AI
        pass 

    def reset(self):

        pass

    