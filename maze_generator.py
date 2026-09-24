from mlx import Mlx
from draw import put_cell, put_path
import numpy as np
import numpy.typing as npt
import random as rd
import json
from path import find


with open("data.json") as f:
    data = json.load(f)


rd.seed(data["SEED"])
# CONST VARIABLES
WIDTH = int(data["WIDTH"])
HEIGHT = int(data["HEIGHT"])
CELL_SIZE = int(data["CELL_SIZE"])
WIN_WIDTH = WIDTH * CELL_SIZE + 20
WIN_HEIGHT = HEIGHT * CELL_SIZE + 40

m = Mlx()
mlx = m.mlx_init()
win = m.mlx_new_window(mlx, WIN_WIDTH, WIN_HEIGHT, "Test")


def matrix_init():
    grid: npt.NDArray = np.zeros((HEIGHT, WIDTH, 3))
    return grid


grid = matrix_init()
layer_id = grid[:, :, 0]
layer_const = grid[:, :, 1]
layer_wall = grid[:, :, 2]
layer_id = np.arange(0, WIDTH * HEIGHT).reshape(HEIGHT, WIDTH)
layer_const = np.arange(0, WIDTH * HEIGHT).reshape(HEIGHT, WIDTH)
layer_wall[:, :] = 0xF
cells: npt.NDArray = np.empty((HEIGHT, WIDTH), dtype=object)


class Direction:
    class Hex:
        NORTH = 1
        EAST = 2
        SOUTH = 4
        WEST = 8

    class Size:
        NORTH = -WIDTH
        EAST = 1
        SOUTH = WIDTH
        WEST = -1

    class Location:
        L = layer_const[:, :1]
        R = layer_const[:, -1:]
        T = layer_const[:1, :]
        B = layer_const[-1:, :]


class Cell:
    def __init__(self, id: int):
        self.const = id
        self.x: int = self.const // WIDTH
        self.y: int = self.const % WIDTH
        self.get_const = layer_const[self.x, self.y]
        self.get_wall = layer_wall[self.x, self.y]
        self.get_id = layer_id[self.x, self.y]
        self.is_top: bool = self.get_const in Direction.Location.T
        self.is_bottom: bool = self.get_const in Direction.Location.B
        self.is_left: bool = self.get_const in Direction.Location.L
        self.is_right: bool = self.get_const in Direction.Location.R
        self.lcell: Cell | None = None
        self.rcell: Cell | None = None
        self.tcell: Cell | None = None
        self.bcell: Cell | None = None
        self.is_entry: bool = False
        self.is_exit: bool = False
        self.step: int = -1
        self.visited: bool = False
        self.go_north: Cell | None = None
        self.go_south: Cell | None = None
        self.go_east: Cell | None = None
        self.go_west: Cell | None = None
        if not self.is_left:
            self.lcell = cells[self.x, self.y - 1]
        if not self.is_right:
            self.rcell = cells[self.x, self.y + 1]
        if not self.is_top:
            self.tcell = cells[self.x - 1, self.y]
        if not self.is_bottom:
            self.bcell = cells[self.x + 1, self.y]

        self.valid_cells: list[Cell | None] = [
            cell
            for cell in (
                self.lcell,
                self.rcell,
                self.tcell,
                self.bcell,
            )
            if cell is not None and cell.get_id != self.get_id
        ]

    @staticmethod
    def sync():
        for line in cells:
            for cell in line:
                cell.get_wall = layer_wall[cell.x, cell.y]
                cell.get_id = layer_id[cell.x, cell.y]
                if not cell.is_left:
                    cell.lcell = cells[cell.x, cell.y - 1]
                if not cell.is_right:
                    cell.rcell = cells[cell.x, cell.y + 1]
                if not cell.is_top:
                    cell.tcell = cells[cell.x - 1, cell.y]
                if not cell.is_bottom:
                    cell.bcell = cells[cell.x + 1, cell.y]

    @staticmethod
    def sync_valid():
        for line in cells:
            for cell in line:
                cell.valid_cells = [
                    subcell
                    for subcell in (
                        cell.lcell,
                        cell.rcell,
                        cell.tcell,
                        cell.bcell,
                    )
                    if subcell is not None and subcell.get_id != cell.get_id
                ]


for i, line in enumerate(layer_const):
    for j, id in enumerate(line):
        cells[i, j] = Cell(id)
Cell.sync()
Cell.sync_valid()


def draw_path():
    target: Cell | None = None
    for cell in cells.flat:
        if cell.is_entry:
            target = cell

    i: int = 0
    next_target: list = [target]
    if (target is not None):
        while not target.is_exit:
            put_path(mlx, win, target.x + 10, target.y + 7, int(data["GREEN"], 16))
            next_target.remove(target)
            if len(next_target) == 0:
                i += 1
            for cell in [target.lcell, target.tcell, target.rcell, target.bcell]:
                if cell.step == i + 1:
                    next_target.append(cell)
            target = rd.choice(next_target)


def draw() -> None:
    matrix_init()

    y: int = -1
    for v in layer_wall[:, :]:
        y += 1
        for i, v in enumerate(v):
            put_cell(
                mlx,
                win,
                i * CELL_SIZE + 10,
                y * CELL_SIZE + 7,
                int(data["TURQUOISE"], 16),
                v,
            )
    m.mlx_string_put(mlx, win, 10, WIN_HEIGHT - 30, 0xFF0000FF, "[Q]: EXIT")
    m.mlx_string_put(mlx, win, 165, WIN_HEIGHT - 30, 0xFF0000FF, "[R]: RELOAD")


def loop(param):
    done = np.all(layer_id == layer_id.flat[0])
    if not done:
        destroy_wall()
        if np.all(layer_id == layer_id.flat[0]):
            Cell.sync()
            Cell.sync_valid()
            find(cells, Direction)
            draw_path()
    else:
        # m.mlx_clear_window(mlx, win)
        draw()


def key_hook(keycode, param):
    if keycode == 113:
        m.mlx_loop_exit(mlx)
    if keycode == 114:
        global grid
        global layer_id
        global layer_wall
        global layer_const
        grid = matrix_init()
        layer_id = grid[:, :, 0]
        layer_wall = grid[:, :, 2]
        layer_const = grid[:, :, 1]
        layer_id = np.arange(0, WIDTH * HEIGHT).reshape(HEIGHT, WIDTH)
        layer_const = np.arange(0, WIDTH * HEIGHT).reshape(HEIGHT, WIDTH)
        layer_wall[:, :] = 0xF


def choose_cell() -> tuple[Cell, Cell]:
    """Instanciate two Cell with different ID from layer_id"""
    valid_ids: list[Cell] = []
    for line in cells:
        for cell in line:
            if len(cell.valid_cells) > 0:
                valid_ids.append(cell)

    cell1 = rd.choice(valid_ids)
    valid_cells_id: list[int] = [
        cell.get_const for cell in cell1.valid_cells if cell is not None
    ]
    cell2 = Cell(rd.choice(valid_cells_id))
    cells[cell1.x, cell1.y] = cell1
    cells[cell2.x, cell2.y] = cell2
    return (cell1, cell2)


def destroy_wall():
    Cell.sync()
    Cell.sync_valid()
    cells: tuple[Cell, Cell] = choose_cell()
    cell1, cell2 = cells[0], cells[1]

    direction = cell2.const - cell1.const
    if direction == Direction.Size.NORTH:
        layer_wall[cell1.x, cell1.y] -= Direction.Hex.NORTH
        layer_wall[cell2.x, cell2.y] -= Direction.Hex.SOUTH
    if direction == Direction.Size.EAST:
        layer_wall[cell1.x, cell1.y] -= Direction.Hex.EAST
        layer_wall[cell2.x, cell2.y] -= Direction.Hex.WEST
    if direction == Direction.Size.SOUTH:
        layer_wall[cell1.x, cell1.y] -= Direction.Hex.SOUTH
        layer_wall[cell2.x, cell2.y] -= Direction.Hex.NORTH
    if direction == Direction.Size.WEST:
        layer_wall[cell1.x, cell1.y] -= Direction.Hex.WEST
        layer_wall[cell2.x, cell2.y] -= Direction.Hex.EAST

    # print(f"\n\n===  ID  ===\n{layer_id}")
    # print(f"\n=== WALL ===\n{layer_wall}")
    # print(f"\nCELL1| ({cell1.x}, {cell1.y})|| const= {cell1.const}")
    # print(cell1.valid_cells)
    valid_const = [cell.get_const for cell in cell1.valid_cells if cell is not None]
    # print(f"valid| {valid_const}")
    # print(f"CELL2| ({cell2.x}, {cell2.y})|| const= {cell2.const}")

    for i, line in enumerate(layer_id):
        for j, id in enumerate(line):
            if id == cell2.get_id:
                layer_id[i, j] = cell1.get_id


if __name__ == "__main__":
    m.mlx_key_hook(win, key_hook, None)
    m.mlx_loop_hook(mlx, loop, None)
    m.mlx_loop(mlx)

    with open(data["OUTPUT_FILE"], "w") as f:
        for line in layer_wall:
            for id in line:
                f.write(hex(int(id))[2:])
            f.write("\n")
