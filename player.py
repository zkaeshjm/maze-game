from __future__ import annotations

from maze_generator import MazeGenerator


class Player:
    """Tile-based player constrained by maze walls."""

    def __init__(self, start_row: int = 0, start_col: int = 0) -> None:
        self.row = start_row
        self.col = start_col
        self.steps_taken = 0
        self._heading_index = 1  # 0=N, 1=E, 2=S, 3=W

    @property
    def facing(self) -> tuple[int, int]:
        headings = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        return headings[self._heading_index]

    def reset(self, row: int, col: int) -> None:
        self.row = row
        self.col = col
        self.steps_taken = 0
        self._heading_index = 1

    def rotate_left(self) -> None:
        self._heading_index = (self._heading_index - 1) % 4

    def rotate_right(self) -> None:
        self._heading_index = (self._heading_index + 1) % 4

    def face_direction(self, dr: int, dc: int) -> None:
        heading_map = {(-1, 0): 0, (0, 1): 1, (1, 0): 2, (0, -1): 3}
        if (dr, dc) in heading_map:
            self._heading_index = heading_map[(dr, dc)]

    def forward_delta(self) -> tuple[int, int]:
        return self.facing

    def backward_delta(self) -> tuple[int, int]:
        dr, dc = self.facing
        return -dr, -dc

    def strafe_left_delta(self) -> tuple[int, int]:
        dr, dc = self.facing
        return -dc, dr

    def strafe_right_delta(self) -> tuple[int, int]:
        dr, dc = self.facing
        return dc, -dr

    def try_move(self, dr: int, dc: int, maze: MazeGenerator, update_facing: bool = True) -> bool:
        if maze.can_move(self.row, self.col, dr, dc):
            self.row += dr
            self.col += dc
            self.steps_taken += 1
            if update_facing:
                self.face_direction(dr, dc)
            return True
        return False
