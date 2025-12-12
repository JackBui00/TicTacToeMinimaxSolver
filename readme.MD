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
- Averages <0.2s per move, unbeatable against humans/LLMs

### `src/gui.py` - Tkinter Interface
- Symbol selection screen (X/O buttons)
- Interactive 3x3 clickable grid with disabled post-move buttons
- Auto AI responses (500ms delay for visibility), status display ("You: X, AI: O")
- Reset to main menu, "Clear AI Memory" button for fresh learning
- End-game modals (Win/Draw/AI Wins) with AI memory updates

## Benchmarking Suite

### `src/test_runner.py` - AI-vs-AI Verification
- Multiprocessing Pool across all CPU cores for 5k-10k game pairs
- Alternates X/O starters, tracks win/draw rates (expects 100% draws with perfect play)
- Validates Minimax optimality under scale

### `src/OpenAivsMiniMax.py` & `src/OpenAi.py` - LLM Comparison
- GPT-4.1-mini/5.2 prompted with board text ("0-8 positions, return single integer move")
- 100 games alternating sides vs Minimax, random fallback for invalid moves
- Scores LLM win rates (typically <50% vs unbeatable AI), demonstrates reasoning limits

## Performance & Validation
- **Optimality**: Forces draws vs perfect play; verified via AI-vs-AI (100% draw rate expected)
- **Learning**: Move stats evolve over sessions, refining tie-breaking
- **Speed**: <0.2s average moves despite full minimax
- **No dependencies**: Pure Python 3.10+ stdlib (OpenAI optional)

## Future Enhancements
- Difficulty levels (random, depth-limited minimax)
- Move history/undo functionality
- Pygame animated version
- Web deployment (Streamlit/Flask)
- Alpha-beta pruning for larger boards

**License**: MIT