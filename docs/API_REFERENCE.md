# API Reference

This document describes key classes and methods used by the maze game.

## `maze_generator.py`

### `Cell`

Data class for one maze cell.

Fields:

- `row: int`
- `col: int`
- `walls: dict`
- `visited: bool`

### `MazeGenerator`

Constructor:

- `MazeGenerator(rows: int = 20, cols: int = 20, seed: Optional[int] = None)`

Core methods:

- `reset_grid() -> None`
- `generate() -> None`
- `step_generation() -> bool`
- `has_wall(row: int, col: int, side: Direction) -> bool`
- `can_move(row: int, col: int, dr: int, dc: int) -> bool`

Internal helpers:

- `_in_bounds(row: int, col: int) -> bool`
- `_unvisited_neighbors(row: int, col: int) -> List[Tuple[Direction, int, int]]`
- `_remove_wall_between(...) -> None`

State fields:

- `rows`, `cols`, `grid`, `stack`, `current_cell`, `finished`
- `start`, `exit`

## `player.py`

### `Player`

Constructor:

- `Player(start_row: int = 0, start_col: int = 0)`

Properties:

- `facing -> tuple[int, int]`

Methods:

- `reset(row: int, col: int) -> None`
- `rotate_left() -> None`
- `rotate_right() -> None`
- `face_direction(dr: int, dc: int) -> None`
- `forward_delta() -> tuple[int, int]`
- `backward_delta() -> tuple[int, int]`
- `strafe_left_delta() -> tuple[int, int]`
- `strafe_right_delta() -> tuple[int, int]`
- `try_move(dr: int, dc: int, maze: MazeGenerator, update_facing: bool = True) -> bool`

State fields:

- `row`, `col`, `steps_taken`

## `renderer.py`

### `Renderer`

Constructor:

- `Renderer(width: int = 960, height: int = 960)`

Public methods:

- `set_viewport(width: int, height: int) -> None`
- `toggle_3d() -> None`
- `toggle_first_person() -> None`
- `draw(maze: MazeGenerator, player: Player, hud: Dict[str, object], debug_mode: bool) -> None`

Drawing methods:

- `_draw_2d(...)`
- `_draw_special_cells_2d(...)`
- `_draw_debug_current_cell_2d(...)`
- `_draw_walls_2d(...)`
- `_draw_player_2d(...)`
- `_emit_cell_quad(...)`
- `_draw_3d(...)`
- `_draw_first_person(...)`
- `_cast_ray(...)`
- `_draw_floor_3d(...)`
- `_draw_flat_marker_3d(...)`
- `_draw_walls_3d(...)`
- `_draw_box(...)`
- `_draw_player_3d(...)`
- `_draw_hud(...)`
- `_draw_text(...)`

Notes:

- The current game input flow toggles only 2D/3D overhead mode.
- The first-person methods remain present in renderer internals.

## `main.py`

### `MazeGame`

Constructor:

- `MazeGame()`

Lifecycle:

- `setup_glut() -> None`
- `start() -> None`

Gameplay:

- `regenerate_level(animate_debug: bool = False) -> None`
- `display() -> None`
- `reshape(width: int, height: int) -> None`
- `timer(_value: int) -> None`
- `keyboard(key: bytes, _x: int, _y: int) -> None`
- `special_keys(key: int, _x: int, _y: int) -> None`

Internal helpers:

- `_face_player_to_open_path() -> None`
- `_attempt_move(dr: int, dc: int, now: float, update_facing: bool = True) -> None`
- `_check_win_condition() -> None`
- `_build_hud() -> Dict[str, object]`

Entry point:

- If executed directly: creates `MazeGame` and calls `start()`.
