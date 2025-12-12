from openai import OpenAI
import os
from dotenv import load_dotenv
import os
from game import TicTacToe 
import random


load_dotenv()  # take environment variables from .env.

api_key = os.getenv("OPENAI_API_KEY")
# Ensure the API key is set
if not api_key: 
    raise RuntimeError("OPENAI_API_KEY is not set")
client = OpenAI(api_key=api_key)

# Convert board state to text representation for LLM prompt 
def board_to_text(board): 
    rows = []
    for i in range(0, 9, 3):
        row = [board[i + j] if board[i + j] != ' ' else str(i + j) for j in range(3)]
        rows.append(" | ".join(row))
    return "\n---------\n".join(rows)

def get_llm_move(game, llm_symbol="O", other_symbol="X"):
    board_str = board_to_text(game.board)
    prompt = f"""
            You are playing tic tac toe as '{llm_symbol}'. The other player is '{other_symbol}'.
            Board positions are 0–8. Empty squares are shown by their index.
            Return ONLY a single integer 0-8 for your move that is currently empty. You want to try to win, or block the opponent from winning.

            Current board:
            {board_str}

            Your move:
            """
    # Using gpt-4.1-mini for lightweight inference and gpt-5.2 for stronger play
    resp = client.chat.completions.create(
        model="gpt-5.2",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    txt = resp.choices[0].message.content.strip()
    try:
        move = int(txt)
    except ValueError:
        move = None

    # validate and fallback
    empties = game.get_empty_positions()
    if move not in empties:
        move = random.choice(empties) if empties else None
    return move


