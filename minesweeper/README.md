# Portfolio
This is classic Minesweeper game implemented in python(pycharm), featuring two difficulty levels, score tracking and user interface. 

The goal of the project was to:
1. Practise python programming in a bit longer exercise
2. Implement game logic and algorithms. 
3. Have fun!

**Project structure**

saper-game/
├── main.py          # Entry point and main game loop
├── gamestates.py    # Game state management (Menu, Game, Win, Scores)
├── board.py         # Board logic and cell management
├── UI.py            # Button UI components
├── saper_sound.mp3  # Background music
├── icon_saper.png   # Game icon
└── scores.json      # Score storage (created automatically)

**Features**
- Random generated minefield two levels of difficulty and custom level (in progress)
- Recursive algorithm for automatic cell revealing
- Timer and counter for remaining flags
- Win/loss detection with message prompts. 
- Restart and new game options

**Languages & Tools**
- Python 3.12
- `Tkinter` (for GUI) or `Pygame` *(depending on your implementation)*  
- `random` module for board generation  
- `time` module for game tracking  

**Key Concepts Used**
- 2D lists (matrices) for board state  
- Recursion for empty field exploration  
- Event-driven programming (GUI interactions)  
- Exception handling and input validation  