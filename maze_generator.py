from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


Direction = str


@dataclass
class Cell:
    row: int
    col: int
    walls: dict = field(
        default_factory=lambda: {
            "top": True,
            "right": True,
            "bottom": True,
            "left": True,
        }
    )
    visited: bool = False


class MazeGenerator:
    """Grid-based maze generator using recursive backtracking (DFS)."""

    _DIRS = {
        "top": (-1, 0),
        "right": (0, 1),
        "bottom": (1, 0),
        "left": (0, -1),
    }

    _OPPOSITE = {
        "top": "bottom",
        "right": "left",
        "bottom": "top",
        "left": "right",
    }

    def __init__(self, rows: int = 20, cols: int = 20, seed: Optional[int] = None) -> None:
        self.rows = rows
        self.cols = cols
        self.seed = seed
        self.rng = random.Random(seed)

        self.grid: List[List[Cell]] = []
        self.stack: List[Tuple[int, int]] = []
        self.current_cell: Optional[Tuple[int, int]] = None
        self.finished: bool = False

        self.start = (0, 0)
        self.exit = (rows - 1, cols - 1)

    def reset_grid(self) -> None:
        self.grid = [[Cell(r, c) for c in range(self.cols)] for r in range(self.rows)]
        self.stack = []
        self.current_cell = (0, 0)
        self.grid[0][0].visited = True
        self.finished = False

    def generate(self) -> None:
        """Generate a full maze immediately."""
        self.reset_grid()
        while not self.finished:
            self.step_generation()

    def _in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.cols

    def _unvisited_neighbors(self, row: int, col: int) -> List[Tuple[Direction, int, int]]:
        neighbors: List[Tuple[Direction, int, int]] = []
        for direction, (dr, dc) in self._DIRS.items():
            nr, nc = row + dr, col + dc
            if self._in_bounds(nr, nc) and not self.grid[nr][nc].visited:
                neighbors.append((direction, nr, nc))
        return neighbors

    def _remove_wall_between(
        self,
        r1: int,
        c1: int,
        r2: int,
        c2: int,
        direction: Direction,
    ) -> None:
        self.grid[r1][c1].walls[direction] = False
        self.grid[r2][c2].walls[self._OPPOSITE[direction]] = False

    def step_generation(self) -> bool:
        """Run one DFS generation step.

        Returns True while work remains, and False when complete.
        """
        if self.finished:
            return False

        if self.current_cell is None:
            self.finished = True
            return False

        row, col = self.current_cell
        neighbors = self._unvisited_neighbors(row, col)

        if neighbors:
            direction, nr, nc = self.rng.choice(neighbors)
            self.stack.append((row, col))
            self._remove_wall_between(row, col, nr, nc, direction)
            self.grid[nr][nc].visited = True
            self.current_cell = (nr, nc)
            return True

        if self.stack:
            self.current_cell = self.stack.pop()
            return True

        self.current_cell = None
        self.finished = True
        return False

    def has_wall(self, row: int, col: int, side: Direction) -> bool:
        return self.grid[row][col].walls[side]

    def can_move(self, row: int, col: int, dr: int, dc: int) -> bool:
        nr, nc = row + dr, col + dc
        if not self._in_bounds(nr, nc):
            return False

        if dr == -1 and dc == 0:
            return not self.has_wall(row, col, "top")
        if dr == 1 and dc == 0:
            return not self.has_wall(row, col, "bottom")
        if dr == 0 and dc == -1:
            return not self.has_wall(row, col, "left")
        if dr == 0 and dc == 1:
            return not self.has_wall(row, col, "right")
        return False
