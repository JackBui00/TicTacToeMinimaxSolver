import tkinter as tk
import time
from tkinter import messagebox
from game import TicTacToe
import tkinter.ttk as ttk
from OpenAi import get_llm_move

class tictactoe_gui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe")
        self.root.geometry("400x450")

        self.game = None
        self.human_symbol = None
        self.ai_symbol = None
        self.buttons = []

        
        self.ai_mode_var = tk.StringVar(value="Minimax")
        self.llm_model_var = tk.StringVar(value="gpt-4.1-mini")

        self.ai_mode = None
        self.llm_model = None

        
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
        
        # Add AI mode selection
        mode_label = tk.Label(frame, text="Choose AI Mode:", font=("Arial", 16, "bold"))
        mode_label.pack(pady=10)
        
       
        
        minimax_radio = tk.Radiobutton(frame, text="Minimax AI",
                               variable=self.ai_mode_var, value="Minimax")
        minimax_radio.pack()

        llm_radio = tk.Radiobutton(frame, text="LLM AI (OpenAI)",
                           variable=self.ai_mode_var, value="LLM")
        llm_radio.pack()

        # LLM Model selection dropdown
        model_label = tk.Label(frame, text="Choose LLM Model:", font=("Arial", 12, "bold"))
        model_label.pack(pady=5)

        # List of available LLM models
        llm_models = ["gpt-4.1-mini", "gpt-5.2"] 

        model_dropdown = ttk.Combobox(frame, textvariable=self.llm_model_var,
                              values=llm_models, state="readonly")
        
        model_dropdown.pack(pady=5)
        model_dropdown.bind("<<ComboboxSelected>>", self.on_llm_model_select)

        self.llm_model = self.llm_model_var.get()


    def start_game(self, symbol):
        # Start a new game with the chosen symbol
        self.human_symbol = symbol
        self.ai_symbol = "O" if symbol == "X" else "X"
        # Initialize game logic

        self.ai_mode = self.ai_mode_var.get()
        self.llm_model = self.llm_model_var.get()
        
            
        self.game = TicTacToe()
        
        self.game.load_memory()

        if self.human_symbol == "O":
            self.game.current_player = self.ai_symbol   # AI starts
        else:
            self.game.current_player = self.human_symbol
        
       


        self.setup_board()
        # AI goes first if human chose O
        if self.human_symbol == "O":
            self.root.after(100, self.ai_move)  

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
        ai_label = f"{self.ai_mode} ({self.llm_model})" if self.ai_mode == "LLM" else self.ai_mode
        info_label = tk.Label(
            top_frame,
            text=f"You: {self.human_symbol}  |  {ai_label} AI: {self.ai_symbol}",
            font=("Arial", 14, "bold")
        )
        info_label.pack()

        # Status for AI Thinking
        self.status_var = tk.StringVar(value="")
        status_label = tk.Label(top_frame, textvariable=self.status_var, font=("Arial", 12))
        status_label.pack()

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
        
        clear_btn = tk.Button(bottom_frame, text="Clear AI Memory", font=("Arial",12), width=15, command=self.clear_ai_memory)
        clear_btn.pack()

 

    def on_llm_model_select(self, event):
        self.llm_model = self.llm_model_var.get()
        print(f"Selected LLM Model: {self.llm_model}")
    
    def clear_ai_memory(self):
        if self.game:
            self.game.clear_memory()
            messagebox.showinfo("Success", "AI memory has been reset!")

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
                self.lock_input() # Lock input while AI thinks
                # delay movement for smoother feeling 
                self.root.after(500, self.ai_move)
        
    def lock_input(self):
        for i, button in enumerate(self.buttons):
            if self.game and self.game.board[i] == ' ':
                button.config(state="disabled")

    def unlock_input(self):
        for i, button in enumerate(self.buttons):
            if self.game.board[i] == ' ': # Only enable empty buttons
                button.config(state="normal")



    
    def ai_move(self):
        if not self.game or self.game.current_player != self.ai_symbol:
            return

        self.status_var.set("AI is thinking...")
        self.lock_input()
        self.root.after(1, self._ai_compute_and_apply)  # let UI repaint first

    def _ai_compute_and_apply(self):
        try:
            if self.ai_mode == "Minimax":
                move = self.game.get_best_move(self.ai_symbol, self.human_symbol, use_learning=True)
            else:
                move = get_llm_move(self.game, self.llm_model, self.ai_symbol, self.human_symbol)

            if move is None:
                result = self.game.check_winner()
                if result:
                    self.end_game(result)
                return

            self.game.make_move(move, self.ai_symbol)
            self.buttons[move].config(text=self.ai_symbol, state="disabled")

            result = self.game.check_winner()
            if result:
                self.end_game(result)
            else:
                self.unlock_input()
        finally:
            self.status_var.set("")  # clears immediately after move is applied


    def end_game(self, result):
        # update ai learning 
        if self.game and self.ai_symbol:
            self.game.update_from_result(result, self.ai_symbol)
            
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
