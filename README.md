🧩 Maze Game (Python + OpenGL)

A grid-based maze exploration game built with Python and PyOpenGL, featuring procedural maze generation, 2D/3D rendering modes, player movement, scoring, and level progression.

📸 Overview

The game generates a unique maze for every level using the Depth-First Search (DFS) Backtracking Algorithm.
Players navigate through the maze, avoid dead ends, and reach the exit while minimizing time and steps.

The project is designed with clean modular architecture:

Game Logic
Maze Generation
Player System
Rendering Engine
HUD & Debug Tools
✨ Features
✅ Procedural maze generation using DFS backtracking
✅ Real-time 2D top-down rendering
✅ Optional 3D overhead visualization
✅ Keyboard movement and player rotation
✅ Dynamic level progression
✅ Score and HUD system
✅ Debug generation visualization mode
✅ Step-by-step maze generation animation
✅ Modular and extensible project structure
🗂️ Project Structure
maze-game/
│
├── main.py               # Main game loop and GLUT callbacks
├── maze_generator.py     # Maze generation and wall logic
├── player.py             # Player movement and direction handling
├── renderer.py           # OpenGL rendering and HUD drawing
├── requirements.txt      # Project dependencies
└── README.md
⚙️ Requirements
Python 3.10+
PyOpenGL
PyOpenGL_accelerate

Dependencies are listed in:

requirements.txt
🚀 Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/your-username/maze-game.git
cd maze-game
2️⃣ Create Virtual Environment
Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
▶️ Run the Game
Windows
.\.venv\Scripts\python.exe main.py
Linux / macOS
python main.py
🎮 Controls
Key	Action
W A S D	Move player
Arrow Keys	Alternative movement
Q / E	Rotate left/right
V	Toggle 2D / 3D view
G	Toggle debug generation mode
SPACE	Step generation manually
R	Regenerate current level
ENTER	Next level after winning
ESC	Exit game
🕹️ Gameplay
Start from the maze entry point.
Navigate through the maze.
Reach the exit cell to complete the level.
Every level increases maze size and difficulty.
Score depends on:
Completion time
Number of movement steps
🧠 How Maze Generation Works

The maze uses the Depth-First Search (DFS) Recursive Backtracking Algorithm.

Algorithm Steps
Mark current cell as visited
Choose a random unvisited neighbor
Remove walls between cells
Push current cell onto stack
Move to neighbor
Backtrack when stuck
DFS Visualization
+---+---+---+
| S |   |   |
+   +---+   +
|   |   |   |
+   +   +   +
|       | E |
+---+---+---+
S → Start
E → Exit
🧩 Core Components
main.py

Handles:

GLUT window initialization
Input handling
Game loop
Level progression
Score system
HUD updates
Important Methods
setup_glut()
start()
regenerate_level()
keyboard()
special_keys()
_attempt_move()
_build_hud()
maze_generator.py

Responsible for:

Maze grid creation
DFS carving algorithm
Wall collision logic
Important Methods
generate()
step_generation()
can_move()
has_wall()
player.py

Handles:

Player coordinates
Facing direction
Movement calculations
Important Methods
rotate_left()
rotate_right()
forward_delta()
backward_delta()
strafe_left_delta()
strafe_right_delta()
try_move()
renderer.py

Responsible for all OpenGL rendering.

Rendering Features
2D rendering
3D rendering
Perspective projection
HUD overlays
Wall and floor drawing
Important Methods
set_viewport()
toggle_3d()
draw()
_draw_2d()
_draw_3d()
_draw_hud()
🖥️ Rendering Modes
🔹 2D Mode
Top-down maze visualization
Simple and efficient rendering
Best for gameplay clarity
Includes
Cell backgrounds
Maze walls
Start/end markers
Player indicator
🔹 3D Mode
Perspective overhead rendering
OpenGL transformations
Wall extrusion and floor rendering
Includes
Camera transforms
Perspective projection
3D wall geometry
🛠️ Debug Mode

Debug mode allows visualization of maze generation in real time.

Features
Animated DFS generation
Manual generation stepping
Internal path visualization
Notes
Movement is disabled while generation is incomplete
Press SPACE to advance generation manually
📊 HUD System

The HUD displays:

Current level
Score
Steps taken
Time elapsed
Rendering mode
Debug state
🧱 Architecture Design

The project follows a modular architecture:

Game Logic      → main.py
Maze Logic      → maze_generator.py
Player Logic    → player.py
Rendering Layer → renderer.py

This separation keeps the project scalable and easy to maintain.

🔧 Troubleshooting
❌ Black or Empty Window

Possible causes:

Missing GPU/OpenGL drivers
Incorrect virtual environment
OpenGL dependency issues
Solution
pip install -r requirements.txt

Update GPU drivers if needed.

❌ ImportError: OpenGL

Reinstall dependencies:

python -m pip install --upgrade pip
pip install -r requirements.txt
❌ Window Opens Then Closes

Run the project from terminal instead of double-clicking:

python main.py

Check terminal output for Python tracebacks.

📈 Future Improvements

Potential enhancements:

Enemy AI
Minimap system
Lighting and shadows
Textured walls/floors
Sound effects and music
Save/load system
Multiplayer maze racing
Procedural themes
🤝 Contributing

Contributions are welcome.

Steps
Fork the repository
Create a feature branch
git checkout -b feature-name
Commit changes
git commit -m "Added feature"
Push branch
git push origin feature-name
Open a Pull Request
📜 License

No explicit license file is currently included.

You may add an open-source license such as:

MIT License
Apache 2.0
GPL v3
👨‍💻 Author
Muhammad Saad Khalid

Computer Science Student • Python Developer • OpenGL Enthusiast

GitHub: https://github.com/zkaeshjm
LinkedIn: https://www.linkedin.com/in/muhammad-saad-khalid-1786a2252/
⭐ Support

If you like this project:

⭐ Star the repository
🍴 Fork the project
🛠️ Contribute improvements
