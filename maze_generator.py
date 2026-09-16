from mlx import Mlx
from draw import put_cell
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
        if not self.is_left:
            self.lcell = cells[self.x, self.y - 1]
        try:
            self.rcell = cells[self.x, self.y + 1]
        except IndexError:
            self.rcell = None
        if not self.is_top:
            self.tcell = cells[self.x - 1, self.y]
        try:
            self.bcell = cells[self.x + 1, self.y]
        except IndexError:
            self.bcell = None

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
                cell.valid_cells = cell.valid_cells = [
                    cell
                    for cell in (
                        cell.lcell,
                        cell.rcell,
                        cell.tcell,
                        cell.bcell,
                    )
                    if cell is not None and cell.get_id != cell.get_id
                ]


for i, line in enumerate(layer_const):
    for j, id in enumerate(line):
        cells[i, j] = Cell(id)
Cell.sync()


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
    else:
        m.mlx_clear_window(mlx, win)
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
            temp = Cell(cell.const)
            if len(temp.valid_cells) >= 1:
                valid_ids.append(temp)

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

    print(f"\n\n===  ID  ===\n{layer_id}")
    print(f"\n=== WALL ===\n{layer_wall}")
    print(f"\nCELL1| ({cell1.x}, {cell1.y})")
    print(f"CELL2| ({cell2.x}, {cell2.y})")

    for i, line in enumerate(layer_id):
        for j, id in enumerate(line):
            if id == cell2.get_id:
                layer_id[i, j] = cell1.get_id


if __name__ == "__main__":
    m.mlx_key_hook(win, key_hook, None)
    m.mlx_loop_hook(mlx, loop, None)
    m.mlx_loop(mlx)
    find(cells)

    with open(data["OUTPUT_FILE"], "w") as f:
        for line in layer_wall:
            for id in line:
                f.write(hex(int(id))[2:])
            f.write("\n")
