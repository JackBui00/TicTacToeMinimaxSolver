# Unbeatable Tic-Tac-Toe Project

**Comprehensive Python Tic-Tac-Toe with unbeatable Minimax AI, Tkinter GUI, reinforcement learning, and LLM benchmarking.** All components use pure Python standard library (OpenAI optional for benchmarks).[file:1][file:5]

## Project Overview
This production-ready project delivers a complete Tic-Tac-Toe system where players choose X (first) or O (second) against an optimal AI that guarantees draws with perfect play. Key innovations include JSON-based move memory for learning optimal tie-breakers, parallel multiprocessing for AI-vs-AI verification (10k+ games), and OpenAI GPT benchmarking to compare LLM reasoning against solved Minimax.[file:5][file:2][file:4]

## Core Components

### `src/game.py` - Game Engine & AI
- 3x3 board state management, move validation, win/draw detection via 8 winning combinations
- **Minimax algorithm**: Full game tree exploration (~547k states max), position priorities (center=2, corners=1, edges=0) for natural tie-breaking
- **Reinforcement learning**: `tictactoememory.json` tracks state-action stats (wins/losses/draws), prefers proven moves among optimal choices
- `get_best_move()` balances minimax scores with learned stats and positional heuristics
- Averages <0.2s per move, unbeatable against humans/LLMs[file:5]

### `src/gui.py` - Tkinter Interface
- Symbol selection screen (X/O buttons)
- Interactive 3x3 clickable grid with disabled post-move buttons
- Auto AI responses (500ms delay for visibility), status display ("You: X, AI: O")
- Reset to main menu, "Clear AI Memory" button for fresh learning
- End-game modals (Win/Draw/AI Wins) with AI memory updates[file:3]

## Benchmarking Suite

### `src/test_runner.py` - AI-vs-AI Verification
- Multiprocessing Pool across all CPU cores for 5k-10k game pairs
- Alternates X/O starters, tracks win/draw rates (expects 100% draws with perfect play)
- Validates Minimax optimality under scale[file:2]

### `src/OpenAivsMiniMax.py` & `src/OpenAi.py` - LLM Comparison
- GPT-4.1-mini/5.2 prompted with board text ("0-8 positions, return single integer move")
- 100 games alternating sides vs Minimax, random fallback for invalid moves
- Scores LLM win rates (typically <50% vs unbeatable AI), demonstrates reasoning limits[file:4][file:6]

## Project Structure

UnbeatableTicTacToe-Minimax/
├── src/
│ ├── init.py # Exports: TicTacToe, TicTacToeGUI
│ ├── game.py # Core logic + Minimax + RL memory
│ ├── gui.py # Full Tkinter GUI
│ ├── test_runner.py # Parallel AI-vs-AI benchmarking
│ ├── OpenAivsMiniMax.py # GPT vs Minimax matches
│ └── OpenAi.py # LLM move generation + board-to-text
├── tictactoememory.json # AI learning data (auto-generated)
├── .venv/ # Python virtual environment
├── README.md # This file
└── requirements.txt # Empty (stdlib only)

text
**Usage**: `python -m venv .venv && .venv/Scripts/Activate.ps1 && python -m src.gui`[file:1][file:3]

## Performance & Validation
- **Optimality**: Forces draws vs perfect play; verified via AI-vs-AI (100% draw rate expected)
- **Learning**: Move stats evolve over sessions, refining tie-breaking
- **Speed**: <0.2s average moves despite full minimax
- **No dependencies**: Pure Python 3.10+ stdlib (OpenAI optional)[file:5][file:2]

## Future Enhancements
- Difficulty levels (random, depth-limited minimax)
- Move history/undo functionality
- Pygame animated version
- Web deployment (Streamlit/Flask)
- Alpha-beta pruning for larger boards[file:1]

**License**: MIT[file:1]