import tkinter as tk
import time
from tkinter import messagebox
from game import TicTacToe
class tictactoe_gui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe")
        self.root.geometry("400x450")
        self.game = None
        self.human_symbol = None
        self.ai_symbol = None
        self.buttons = []
        self.show_symbol_selection()
    
    def show_symbol_selection(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, padx = 20, pady = 20)
        frame.pack(expand = True)

        title = tk.Label(frame, text = "Choose X or O to Start", font = ("Arial", 20, "bold"))
        title.pack(pady = 10)

        btn_x = tk.Button(frame, text = "X", font = ("Arial", 16), width = 10,
                          command = lambda: self.start_game("X"))
        btn_x.pack(pady = 5)

        btn_o = tk.Button(frame, text = "O", font = ("Arial", 16), width = 10,
                          command = lambda: self.start_game("O"))
        btn_o.pack(pady = 5)

    def start_game(self, symbol):
        # Start a new game with the chosen symbol
        self.human_symbol = symbol
        self.ai_symbol = "O" if symbol == "X" else "X"
        # Initialize game logic
        self.game = TicTacToe()
        self.game.current_player = self.human_symbol

        self.setup_board()

    def setup_menu(self):
        # Create menu for game options
        pass

    def setup_board(self):
        # Set up the Tic-Tac-Toe board GUI
        for widget in self.root.winfo_children():
            widget.destroy()
        
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady = 10)
        # Display player symbols
        info_label = tk.Label(top_frame, text = f"You: {self.human_symbol}  |  AI: {self.ai_symbol}", font = ("Arial", 14, "bold"))
        info_label.pack()

        board_frame = tk.Frame(self.root)
        board_frame.pack()

        self.buttons = []
        # Create 3x3 grid of buttons for the Tic-Tac-Toe board
        for i in range (3): 
            for j in range (3): 
                idx = i * 3 + j
                btn = tk.Button(board_frame, text = " ", font = ("Arial", 28, "bold"), width = 3, height = 1, command = lambda pos=idx: self.on_human_click(pos))
                btn.grid(row = i, column = j, padx = 5, pady = 5)
                self.buttons.append(btn)
        # create reset button at bottom
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(pady=10)

        reset_btn = tk.Button(bottom_frame, text = "Main Menu", font = ("Arial", 12), width = 12, command = self.show_symbol_selection)
        reset_btn.pack()

        # Ai goes first if player is O 
        if self.human_symbol == "O":
            self.root.after(500, self.ai_move)

    def on_human_click(self, pos):
        # Handle human move
        if not self.game: 
            return 
        # make move in valid position 
        if self.game.make_move(pos, self.human_symbol):
            self.buttons[pos].config(text=self.human_symbol, state= "disabled")

            result = self.game.check_winner()
            if result:
                self.end_game(result)
            else:
                # delay movement for smoother feeling 
                self.root.after(500, self.ai_move)
        

    def ai_move(self):
        # Handle AI move
        if not self.game: 
            return
        move = self.game.get_best_move(self.ai_symbol, self.human_symbol)
        if move is None:
            # There are no valid moves left 
            result = self.game.check_winner()
            if result: 
                self.end_game(result)
            return

        self.game.make_move(move, self.ai_symbol)
        self.buttons[move].config(text=self.ai_symbol, state = "disabled")
        result = self.game.check_winner()
        if result:
            self.end_game(result)

    def end_game(self, result):
        # Display end game message
        if result == "Draw": 
            messagebox.showinfo("Game Over", "It's a Draw!")
        elif result == self.human_symbol:
            messagebox.showinfo("Game Over", "You Win!")
        else:
            messagebox.showinfo("Game Over", "AI Wins!")


    def run(self):
        # Start the GUI event loop
        self.root.mainloop()

# Entry point for running the GUI
if __name__ == "__main__":
    gui = tictactoe_gui()
    gui.run()


