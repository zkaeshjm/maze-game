from __future__ import annotations

import sys
import time
from typing import Dict, Optional

from OpenGL.GLUT import (
    GLUT_DEPTH,
    GLUT_DOUBLE,
    GLUT_KEY_DOWN,
    GLUT_KEY_LEFT,
    GLUT_KEY_RIGHT,
    GLUT_KEY_UP,
    GLUT_RGB,
    glutCreateWindow,
    glutFullScreen,
    glutDisplayFunc,
    glutInit,
    glutInitDisplayMode,
    glutInitWindowSize,
    glutKeyboardFunc,
    glutMainLoop,
    glutPostRedisplay,
    glutReshapeFunc,
    glutSpecialFunc,
    glutSwapBuffers,
    glutTimerFunc,
)

from maze_generator import MazeGenerator
from player import Player
from renderer import Renderer


class MazeGame:
    """Main game controller and GLUT callbacks."""

    def __init__(self) -> None:
        self.window_width = 960
        self.window_height = 960

        self.base_rows = 20
        self.base_cols = 20
        self.max_size = 42

        self.level = 1
        self.total_score = 0

        self.maze = MazeGenerator(self.base_rows, self.base_cols)
        self.maze.generate()

        start_r, start_c = self.maze.start
        self.player = Player(start_r, start_c)
        self._face_player_to_open_path()

        self.renderer = Renderer(self.window_width, self.window_height)

        self.debug_mode = False
        self.debug_steps_per_tick = 2

        self.level_start_time = time.time()
        self.level_won = False
        self.win_time: Optional[float] = None

        self.move_cooldown = 0.09
        self.last_move_time = 0.0

    def setup_glut(self) -> None:
        glutInit(sys.argv)
        display_mode = int(GLUT_DOUBLE) | int(GLUT_RGB) | int(GLUT_DEPTH)
        glutInitDisplayMode(display_mode)
        glutInitWindowSize(self.window_width, self.window_height)
        glutCreateWindow(b"OpenGL Maze Game")
        glutFullScreen()

        glutDisplayFunc(self.display)
        glutReshapeFunc(self.reshape)
        glutKeyboardFunc(self.keyboard)
        glutSpecialFunc(self.special_keys)
        glutTimerFunc(16, self.timer, 0)

    def start(self) -> None:
        self.setup_glut()
        glutMainLoop()

    def regenerate_level(self, animate_debug: bool = False) -> None:
        rows = min(self.max_size, self.base_rows + (self.level - 1) * 2)
        cols = min(self.max_size, self.base_cols + (self.level - 1) * 2)
        level_seed = (self.level * 1000003) ^ (rows << 16) ^ cols
        self.maze = MazeGenerator(rows, cols, seed=level_seed)

        if animate_debug:
            self.maze.reset_grid()
        else:
            self.maze.generate()

        start_r, start_c = self.maze.start
        self.player.reset(start_r, start_c)
        self._face_player_to_open_path()
        self.level_start_time = time.time()
        self.level_won = False
        self.win_time = None

    def _face_player_to_open_path(self) -> None:
        row, col = self.player.row, self.player.col
        preferred = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in preferred:
            if self.maze.can_move(row, col, dr, dc):
                self.player.face_direction(dr, dc)
                return

    def display(self) -> None:
        hud = self._build_hud()
        self.renderer.draw(self.maze, self.player, hud, self.debug_mode)
        glutSwapBuffers()

    def reshape(self, width: int, height: int) -> None:
        self.renderer.set_viewport(width, height)

    def timer(self, _value: int) -> None:
        # Animate generation in debug mode.
        if self.debug_mode and not self.maze.finished and not self.level_won:
            for _ in range(self.debug_steps_per_tick):
                if not self.maze.step_generation():
                    break

        glutPostRedisplay()
        glutTimerFunc(16, self.timer, 0)

    def keyboard(self, key: bytes, _x: int, _y: int) -> None:
        now = time.time()

        if key == b"\x1b":
            sys.exit(0)

        if key in (b"w", b"W"):
            self._attempt_move(-1, 0, now)
        elif key in (b"s", b"S"):
            self._attempt_move(1, 0, now)
        elif key in (b"a", b"A"):
            self._attempt_move(0, -1, now)
        elif key in (b"d", b"D"):
            self._attempt_move(0, 1, now)
        elif key in (b"r", b"R"):
            self.regenerate_level(animate_debug=self.debug_mode)
        elif key in (b"g", b"G"):
            self.debug_mode = not self.debug_mode
            self.regenerate_level(animate_debug=self.debug_mode)
        elif key in (b"v", b"V"):
            self.renderer.toggle_3d()
        elif key in (b"q", b"Q"):
            self.player.rotate_left()
        elif key in (b"e", b"E"):
            self.player.rotate_right()
        elif key == b" ":
            if self.debug_mode and not self.maze.finished:
                self.maze.step_generation()
        elif key == b"\r":
            if self.level_won:
                self.level += 1
                self.regenerate_level(animate_debug=self.debug_mode)

        glutPostRedisplay()

    def special_keys(self, key: int, _x: int, _y: int) -> None:
        now = time.time()

        if key == GLUT_KEY_UP:
            self._attempt_move(-1, 0, now)
        elif key == GLUT_KEY_DOWN:
            self._attempt_move(1, 0, now)
        elif key == GLUT_KEY_LEFT:
            self._attempt_move(0, -1, now)
        elif key == GLUT_KEY_RIGHT:
            self._attempt_move(0, 1, now)

        glutPostRedisplay()

    def _attempt_move(self, dr: int, dc: int, now: float, update_facing: bool = True) -> None:
        if self.level_won:
            return
        if self.debug_mode and not self.maze.finished:
            return
        if now - self.last_move_time < self.move_cooldown:
            return

        moved = self.player.try_move(dr, dc, self.maze, update_facing=update_facing)
        if moved:
            self.last_move_time = now
            self._check_win_condition()

    def _check_win_condition(self) -> None:
        if (self.player.row, self.player.col) == self.maze.exit:
            elapsed = time.time() - self.level_start_time
            level_score = max(100, int(1800 - elapsed * 30 - self.player.steps_taken * 4))
            self.total_score += level_score
            self.level_won = True
            self.win_time = time.time()

    def _build_hud(self) -> Dict[str, object]:
        elapsed = time.time() - self.level_start_time

        lines = [
            f"Level: {self.level}",
            f"Maze Size: {self.maze.rows}x{self.maze.cols}",
            f"Time: {elapsed:05.1f}s",
            f"Steps: {self.player.steps_taken}",
            f"Score: {self.total_score}",
            f"Mode: {'3D' if self.renderer.show_3d else '2D'}",
            f"Debug Generation: {'ON' if self.debug_mode else 'OFF'}",
            "Move: WASD / Arrows | Turn: Q/E | Toggle 3D: V",
            "Toggle Debug: G | Restart: R | Exit: ESC",
        ]

        center = None
        if self.debug_mode and not self.maze.finished:
            center = "Debug mode: maze is generating... press SPACE to step manually"

        if self.level_won:
            center = "You reached the exit! Press ENTER for next level"

        return {"lines": lines, "center": center}


if __name__ == "__main__":
    game = MazeGame()
    game.start()
