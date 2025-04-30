import random
import time

from cell import Cell


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._seed = seed

        if self._seed is not None:
            random.seed(self._seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)

    def _create_cells(self):
        self._cells = [
            [Cell(self._win) for row in range(self._num_rows)]
            for col in range(self._num_cols)
        ]
        for col in range(self._num_cols):
            for row in range(self._num_rows):
                self._draw_cell(col, row)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, col, row):
        self._cells[col][row].visited = True
        while True:
            next_index_list = []

            directions = [
                (-1, 0, "left"),  # left
                (1, 0, "right"),  # right
                (0, -1, "up"),  # up
                (0, 1, "down"),  # down
            ]

            for dx, dy, direction in directions:
                new_col, new_row = col + dx, row + dy
                if (
                    0 <= new_col < self._num_cols
                    and 0 <= new_row < self._num_rows
                    and not self._cells[new_col][new_row].visited
                ):
                    next_index_list.append((new_col, new_row, direction))

            if not next_index_list:
                self._draw_cell(col, row)
                return

            # Choose random direction and break walls
            next_cell = random.choice(next_index_list)
            new_col, new_row, direction = next_cell

            if direction == "right":
                self._cells[col][row].has_right_wall = False
                self._cells[new_col][new_row].has_left_wall = False
            elif direction == "left":
                self._cells[col][row].has_left_wall = False
                self._cells[new_col][new_row].has_right_wall = False
            elif direction == "down":
                self._cells[col][row].has_bottom_wall = False
                self._cells[new_col][new_row].has_top_wall = False
            else:  # up
                self._cells[col][row].has_top_wall = False
                self._cells[new_col][new_row].has_bottom_wall = False

            # Recursively visit the next cell
            self._break_walls_r(new_col, new_row)

    def _draw_cell(self, col, row):
        if self._win is None:
            return
        x1 = self._x1 + col * self._cell_size_x
        y1 = self._y1 + row * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[col][row].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.02)
