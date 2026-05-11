from __future__ import annotations
# pyright: reportWildcardImportFromLibrary=false

import math
from typing import Dict, List, Optional, Tuple

from OpenGL.GL import *
from OpenGL.GLU import gluLookAt, gluPerspective
from OpenGL import GLUT

from maze_generator import MazeGenerator
from player import Player


_HUD_FONT = getattr(GLUT, "GLUT_BITMAP_HELVETICA_18", None)


class Renderer:
    """Handles all OpenGL rendering for 2D and optional 3D maze views."""

    def __init__(self, width: int = 960, height: int = 960) -> None:
        self.width = width
        self.height = height
        self.show_3d = False
        self.first_person = False

        self.bg_color = (0.08, 0.09, 0.12, 1.0)
        self.path_color = (0.12, 0.14, 0.18)
        self.wall_color = (0.95, 0.95, 0.95)
        self.start_color = (0.20, 0.70, 0.35)
        self.exit_color = (0.90, 0.25, 0.20)
        self.player_color = (0.95, 0.78, 0.20)
        self.debug_cell_color = (0.30, 0.55, 1.0)

    def set_viewport(self, width: int, height: int) -> None:
        self.width = max(1, width)
        self.height = max(1, height)
        glViewport(0, 0, self.width, self.height)

    def toggle_3d(self) -> None:
        self.show_3d = not self.show_3d

    def toggle_first_person(self) -> None:
        self.first_person = not self.first_person

    def draw(self, maze: MazeGenerator, player: Player, hud: Dict[str, object], debug_mode: bool) -> None:
        glClearColor(*self.bg_color)
        clear_mask = int(GL_COLOR_BUFFER_BIT) | int(GL_DEPTH_BUFFER_BIT)
        glClear(clear_mask)

        if self.show_3d:
            if self.first_person:
                self._draw_first_person(maze, player)
            else:
                glEnable(GL_DEPTH_TEST)
                glEnable(GL_LIGHTING)
                glEnable(GL_LIGHT0)
                self._draw_3d(maze, player)
                glDisable(GL_COLOR_MATERIAL)
                glDisable(GL_NORMALIZE)
                glDisable(GL_LIGHTING)
                glDisable(GL_LIGHT0)
        else:
            glDisable(GL_DEPTH_TEST)
            glDisable(GL_LIGHTING)
            self._draw_2d(maze, player, debug_mode)

        self._draw_hud(hud)

    def _draw_2d(self, maze: MazeGenerator, player: Player, debug_mode: bool) -> None:
        glDisable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, maze.cols, 0, maze.rows, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Draw path background per cell.
        glColor3f(*self.path_color)
        glBegin(GL_QUADS)
        for row in range(maze.rows):
            for col in range(maze.cols):
                x0, y0 = col, maze.rows - row - 1
                x1, y1 = x0 + 1, y0 + 1
                glVertex2f(x0, y0)
                glVertex2f(x1, y0)
                glVertex2f(x1, y1)
                glVertex2f(x0, y1)
        glEnd()

        self._draw_special_cells_2d(maze)

        if debug_mode and maze.current_cell is not None:
            self._draw_debug_current_cell_2d(maze, maze.current_cell)

        self._draw_walls_2d(maze)
        self._draw_player_2d(maze, player)

    def _draw_special_cells_2d(self, maze: MazeGenerator) -> None:
        sr, sc = maze.start
        er, ec = maze.exit

        glBegin(GL_QUADS)

        glColor3f(*self.start_color)
        self._emit_cell_quad(maze, sr, sc, inset=0.10)

        glColor3f(*self.exit_color)
        self._emit_cell_quad(maze, er, ec, inset=0.10)

        glEnd()

    def _draw_debug_current_cell_2d(self, maze: MazeGenerator, current_cell: Tuple[int, int]) -> None:
        row, col = current_cell
        glColor3f(*self.debug_cell_color)
        glBegin(GL_QUADS)
        self._emit_cell_quad(maze, row, col, inset=0.25)
        glEnd()

    def _draw_walls_2d(self, maze: MazeGenerator) -> None:
        glColor3f(*self.wall_color)
        glLineWidth(2.0)
        glBegin(GL_LINES)

        for row in range(maze.rows):
            for col in range(maze.cols):
                cell = maze.grid[row][col]
                x = col
                y = maze.rows - row - 1

                if cell.walls["top"]:
                    glVertex2f(x, y + 1)
                    glVertex2f(x + 1, y + 1)
                if cell.walls["right"]:
                    glVertex2f(x + 1, y + 1)
                    glVertex2f(x + 1, y)
                if cell.walls["bottom"]:
                    glVertex2f(x + 1, y)
                    glVertex2f(x, y)
                if cell.walls["left"]:
                    glVertex2f(x, y)
                    glVertex2f(x, y + 1)

        glEnd()

    def _draw_player_2d(self, maze: MazeGenerator, player: Player) -> None:
        glColor3f(*self.player_color)
        glBegin(GL_QUADS)
        self._emit_cell_quad(maze, player.row, player.col, inset=0.25)
        glEnd()

    def _emit_cell_quad(self, maze: MazeGenerator, row: int, col: int, inset: float = 0.0) -> None:
        x0, y0 = col + inset, maze.rows - row - 1 + inset
        x1, y1 = col + 1 - inset, maze.rows - row - inset
        glVertex2f(x0, y0)
        glVertex2f(x1, y0)
        glVertex2f(x1, y1)
        glVertex2f(x0, y1)

    def _draw_3d(self, maze: MazeGenerator, player: Player) -> None:
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glClearDepth(1.0)
        
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        aspect = self.width / float(self.height)
        gluPerspective(60.0, aspect, 0.1, 200.0)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        if self.first_person:
            eye_x = float(player.col) + 0.5
            eye_y = 0.55
            eye_z = float(player.row) + 0.5
            dr, dc = player.facing
            # Maze rows map to +Z in 3D coordinates.
            look_x = eye_x + float(dc)
            look_z = eye_z + float(dr)
            gluLookAt(eye_x, eye_y, eye_z, look_x, eye_y, look_z, 0.0, 1.0, 0.0)
        else:
            cx = maze.cols / 2.0
            cz = maze.rows / 2.0
            gluLookAt(cx, max(maze.rows, maze.cols) * 1.2, cz + max(maze.rows, maze.cols) * 0.7, cx, 0.0, cz, 0.0, 1.0, 0.0)

        if not self.first_person:
            glEnable(GL_LIGHTING)
            glEnable(GL_LIGHT0)
            glEnable(GL_COLOR_MATERIAL)
            glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
            glEnable(GL_NORMALIZE)

            glLightfv(GL_LIGHT0, GL_POSITION, (2.0, 6.0, 2.0, 1.0))
            glLightfv(GL_LIGHT0, GL_AMBIENT, (0.30, 0.30, 0.30, 1.0))
            glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.95, 0.95, 0.95, 1.0))
            glLightfv(GL_LIGHT0, GL_SPECULAR, (0.50, 0.50, 0.50, 1.0))
            glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (0.10, 0.10, 0.10, 1.0))
            glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 16.0)

        self._draw_floor_3d(maze)
        self._draw_walls_3d(maze)
        if not self.first_person:
            self._draw_player_3d(maze, player)
        
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

    def _draw_first_person(self, maze: MazeGenerator, player: Player) -> None:
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glDisable(GL_LIGHT0)
        glDisable(GL_COLOR_MATERIAL)
        glDisable(GL_NORMALIZE)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, self.width, self.height, 0, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # Sky and floor.
        glBegin(GL_QUADS)
        glColor3f(0.10, 0.11, 0.15)
        glVertex2f(0.0, 0.0)
        glVertex2f(float(self.width), 0.0)
        glVertex2f(float(self.width), float(self.height) * 0.5)
        glVertex2f(0.0, float(self.height) * 0.5)

        glColor3f(0.06, 0.07, 0.09)
        glVertex2f(0.0, float(self.height) * 0.5)
        glVertex2f(float(self.width), float(self.height) * 0.5)
        glVertex2f(float(self.width), float(self.height))
        glVertex2f(0.0, float(self.height))
        glEnd()

        # Raycast one vertical slice per screen column.
        pos_x = float(player.col) + 0.5
        pos_y = float(player.row) + 0.5
        dir_x = float(player.facing[1])
        dir_y = float(player.facing[0])
        if dir_x == 0.0 and dir_y == 0.0:
            dir_x = 1.0

        fov_radians = math.radians(66.0)
        plane_scale = math.tan(fov_radians * 0.5)
        plane_x = -dir_y * plane_scale
        plane_y = dir_x * plane_scale

        for screen_x in range(self.width):
            camera_x = 2.0 * screen_x / float(self.width) - 1.0
            ray_dir_x = dir_x + plane_x * camera_x
            ray_dir_y = dir_y + plane_y * camera_x
            hit_distance, side_axis, hit_negative_side = self._cast_ray(maze, pos_x, pos_y, ray_dir_x, ray_dir_y)

            hit_distance = max(hit_distance, 0.0001)
            line_height = int(self.height / hit_distance)
            draw_start = max(0, (self.height - line_height) // 2)
            draw_end = min(self.height - 1, draw_start + line_height)

            shade = 1.0 / (1.0 + hit_distance * 0.12)
            if side_axis == 1:
                shade *= 0.82
            if hit_negative_side:
                shade *= 0.92

            glColor3f(
                max(0.0, min(1.0, self.wall_color[0] * shade)),
                max(0.0, min(1.0, self.wall_color[1] * shade)),
                max(0.0, min(1.0, self.wall_color[2] * shade)),
            )

            glBegin(GL_QUADS)
            glVertex2f(float(screen_x), float(draw_start))
            glVertex2f(float(screen_x + 1), float(draw_start))
            glVertex2f(float(screen_x + 1), float(draw_end))
            glVertex2f(float(screen_x), float(draw_end))
            glEnd()

        # Simple crosshair.
        center_x = self.width * 0.5
        center_y = self.height * 0.5
        glColor3f(0.95, 0.85, 0.20)
        glBegin(GL_LINES)
        glVertex2f(center_x - 10.0, center_y)
        glVertex2f(center_x + 10.0, center_y)
        glVertex2f(center_x, center_y - 10.0)
        glVertex2f(center_x, center_y + 10.0)
        glEnd()

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

    def _cast_ray(
        self,
        maze: MazeGenerator,
        pos_x: float,
        pos_y: float,
        ray_dir_x: float,
        ray_dir_y: float,
    ) -> Tuple[float, int, bool]:
        map_x = int(pos_x)
        map_y = int(pos_y)

        delta_dist_x = abs(1.0 / ray_dir_x) if ray_dir_x != 0.0 else float("inf")
        delta_dist_y = abs(1.0 / ray_dir_y) if ray_dir_y != 0.0 else float("inf")

        if ray_dir_x < 0.0:
            step_x = -1
            side_dist_x = (pos_x - map_x) * delta_dist_x
        else:
            step_x = 1
            side_dist_x = (map_x + 1.0 - pos_x) * delta_dist_x

        if ray_dir_y < 0.0:
            step_y = -1
            side_dist_y = (pos_y - map_y) * delta_dist_y
        else:
            step_y = 1
            side_dist_y = (map_y + 1.0 - pos_y) * delta_dist_y

        hit_side_axis = 0
        hit_negative_side = False

        while 0 <= map_x < maze.cols and 0 <= map_y < maze.rows:
            if side_dist_x < side_dist_y:
                prev_x = map_x
                prev_y = map_y
                side_dist_x += delta_dist_x
                map_x += step_x
                if step_x > 0:
                    hit_wall = maze.grid[prev_y][prev_x].walls["right"]
                    hit_negative_side = False
                else:
                    hit_wall = maze.grid[prev_y][prev_x].walls["left"]
                    hit_negative_side = True
                hit_side_axis = 0
                perp_wall_dist = side_dist_x - delta_dist_x
            else:
                prev_x = map_x
                prev_y = map_y
                side_dist_y += delta_dist_y
                map_y += step_y
                if step_y > 0:
                    hit_wall = maze.grid[prev_y][prev_x].walls["bottom"]
                    hit_negative_side = False
                else:
                    hit_wall = maze.grid[prev_y][prev_x].walls["top"]
                    hit_negative_side = True
                hit_side_axis = 1
                perp_wall_dist = side_dist_y - delta_dist_y

            if hit_wall:
                return perp_wall_dist, hit_side_axis, hit_negative_side

        return 9999.0, hit_side_axis, hit_negative_side

    def _draw_floor_3d(self, maze: MazeGenerator) -> None:
        glColor3f(0.18, 0.21, 0.28)
        glBegin(GL_QUADS)
        glNormal3f(0.0, 1.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(float(maze.cols), 0.0, 0.0)
        glVertex3f(float(maze.cols), 0.0, float(maze.rows))
        glVertex3f(0.0, 0.0, float(maze.rows))
        glEnd()

        sr, sc = maze.start
        er, ec = maze.exit
        self._draw_flat_marker_3d(sc, sr, 0.18, self.start_color)
        self._draw_flat_marker_3d(ec, er, 0.18, self.exit_color)

    def _draw_flat_marker_3d(self, col: int, row: int, y: float, color: Tuple[float, float, float]) -> None:
        z = float(row)
        x = float(col)
        glColor3f(*color)
        glBegin(GL_QUADS)
        glVertex3f(x + 0.15, y, z + 0.15)
        glVertex3f(x + 0.85, y, z + 0.15)
        glVertex3f(x + 0.85, y, z + 0.85)
        glVertex3f(x + 0.15, y, z + 0.85)
        glEnd()

    def _draw_walls_3d(self, maze: MazeGenerator) -> None:
        glColor3f(0.86, 0.88, 0.92)
        wall_h = 1.0
        thick = 0.08

        for row in range(maze.rows):
            for col in range(maze.cols):
                cell = maze.grid[row][col]
                x = float(col)
                z = float(row)

                if cell.walls["top"]:
                    self._draw_box(x, 0.0, z, 1.0, wall_h, thick)
                if cell.walls["left"]:
                    self._draw_box(x, 0.0, z, thick, wall_h, 1.0)
                if row == maze.rows - 1 and cell.walls["bottom"]:
                    self._draw_box(x, 0.0, z + 1.0 - thick, 1.0, wall_h, thick)
                if col == maze.cols - 1 and cell.walls["right"]:
                    self._draw_box(x + 1.0 - thick, 0.0, z, thick, wall_h, 1.0)

    def _draw_box(self, x: float, y: float, z: float, w: float, h: float, d: float) -> None:
        x2, y2, z2 = x + w, y + h, z + d

        glBegin(GL_QUADS)
        # Top face (y2)
        glNormal3f(0.0, 1.0, 0.0)
        glVertex3f(x, y2, z)
        glVertex3f(x2, y2, z)
        glVertex3f(x2, y2, z2)
        glVertex3f(x, y2, z2)

        # Bottom face (y)
        glNormal3f(0.0, -1.0, 0.0)
        glVertex3f(x, y, z)
        glVertex3f(x2, y, z)
        glVertex3f(x2, y, z2)
        glVertex3f(x, y, z2)

        # Front face (z)
        glNormal3f(0.0, 0.0, -1.0)
        glVertex3f(x, y, z)
        glVertex3f(x2, y, z)
        glVertex3f(x2, y2, z)
        glVertex3f(x, y2, z)

        # Back face (z2)
        glNormal3f(0.0, 0.0, 1.0)
        glVertex3f(x, y, z2)
        glVertex3f(x2, y, z2)
        glVertex3f(x2, y2, z2)
        glVertex3f(x, y2, z2)

        # Left face (x)
        glNormal3f(-1.0, 0.0, 0.0)
        glVertex3f(x, y, z)
        glVertex3f(x, y, z2)
        glVertex3f(x, y2, z2)
        glVertex3f(x, y2, z)

        # Right face (x2)
        glNormal3f(1.0, 0.0, 0.0)
        glVertex3f(x2, y, z)
        glVertex3f(x2, y, z2)
        glVertex3f(x2, y2, z2)
        glVertex3f(x2, y2, z)
        glEnd()

    def _draw_player_3d(self, maze: MazeGenerator, player: Player) -> None:
        glColor3f(*self.player_color)
        self._draw_box(float(player.col) + 0.25, 0.0, float(player.row) + 0.25, 0.5, 0.35, 0.5)

    def _draw_hud(self, hud: Dict[str, object]) -> None:
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, self.width, 0, self.height, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glColor3f(0.95, 0.95, 0.95)

        lines = hud.get("lines", [])
        if not isinstance(lines, list):
            lines = []

        y = self.height - 28
        for line in lines:
            if not isinstance(line, str):
                continue
            self._draw_text(12, y, line)
            y -= 24

        center_value = hud.get("center")
        center_line: Optional[str] = center_value if isinstance(center_value, str) else None
        if center_line:
            self._draw_text(max(10, self.width // 2 - 220), self.height // 2, center_line)

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

    def _draw_text(self, x: int, y: int, text: str) -> None:
        if _HUD_FONT is None:
            return
        glRasterPos2f(float(x), float(y))
        for ch in text:
            GLUT.glutBitmapCharacter(_HUD_FONT, ord(ch))
