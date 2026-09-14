from mlx import Mlx
from draw import put_cell
import numpy as np
import numpy.typing as npt
import random as rd
import json

with open('data.json') as f:
    data = json.load(f)


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
layer_wall = grid[:, :, 2]
layer_const = grid[:, :, 1]
layer_id = np.arange(0, WIDTH * HEIGHT).reshape(HEIGHT, WIDTH)
layer_const = np.arange(0, WIDTH * HEIGHT).reshape(HEIGHT, WIDTH)
layer_wall[:, :] = 0xf

class Direction():
    class Hex():
        NORTH = 1
        EAST = 2
        SOUTH = 4
        WEST = 8

    class Size():
        NORTH = -WIDTH
        EAST = 1
        SOUTH = WIDTH
        WEST = -1

    class Location():
        L = layer_const[:, 0]
        R = layer_const[:, -1]
        T = layer_const[0, :]
        B = layer_const[-1, :]

class Cell():
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
        self.lcell: tuple[int, int] | None = None
        self.rcell: tuple[int, int] | None = None
        self.tcell: tuple[int, int] | None = None
        self.bcell: tuple[int, int] | None = None
        try:
            self.lcell = (layer_id[self.x - 1, self.y], layer_const[self.x - 1, self.y])
        except IndexError:
            self.lcell = None
        try:
            self.rcell = (layer_id[self.x + 1, self.y], layer_const[self.x + 1, self.y])
        except IndexError:
            self.rcell = None
        try:
            self.tcell = (layer_id[self.x, self.y - 1], layer_const[self.x, self.y - 1])
        except IndexError:
            self.tcell = None
        try:
            self.bcell = (layer_id[self.x, self.y + 1], layer_const[self.x, self.y + 1])
        except IndexError:
            self.bcell = None

        self.valid_cells: list[tuple[int, int] | None] = [
            cell for cell in (
                self.lcell,
                self.rcell,
                self.tcell,
                self.bcell,
            )
            if cell is not None and cell[0] != self.get_id]


            
def draw() -> None:
    matrix_init()

    y: int = -1
    for v in layer_wall[:, :]:
        y += 1
        for i, v in enumerate(v):
            put_cell(mlx, win, i * CELL_SIZE + 10, y * CELL_SIZE + 7, int(data["TURQUOISE"], 16), v)
    m.mlx_string_put(mlx, win, 10, WIN_HEIGHT - 30, 0xff0000ff, "[Q]: EXIT")
    m.mlx_string_put(mlx, win, 165, WIN_HEIGHT - 30, 0xff0000ff, "[R]: RELOAD")

def loop(param):
    done = np.all(layer_id == layer_id.flat[0])
    if (not done):
        destroy_wall()
    else:
        m.mlx_clear_window(mlx, win)
        draw()

def key_hook(keycode, param):
    if (keycode == 113):
        m.mlx_loop_exit(mlx)
    if (keycode == 114):
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
        layer_wall[:, :] = 0xf



def choose_cell() -> tuple[Cell, Cell]:
    '''Instanciate two Cell with different ID from layer_id'''
    base_id = rd.choice(layer_const[:, :].ravel())
    cell1 = Cell(base_id)
    while (len(cell1.valid_cells) < 1):
        base_id = rd.choice(layer_const[:, :].ravel())
        cell1 = Cell(base_id)
    valid_cells: list[int] = [id[1] for id in cell1.valid_cells]
    cell2 = Cell(rd.choice(valid_cells))
    return (cell1, cell2)




def destroy_wall():
    cells: tuple[Cell, Cell] = choose_cell()
    cell1, cell2 = cells[0], cells[1]

    direction = cell2.const - cell1.const
    if (direction == Direction.Size.NORTH):
        layer_wall[cell1.x, cell1.y] -= Direction.Hex.NORTH
        layer_wall[cell2.x, cell2.y] -= Direction.Hex.SOUTH
    if (direction == Direction.Size.EAST):
        layer_wall[cell1.x, cell1.y] -= Direction.Hex.EAST
        layer_wall[cell2.x, cell2.y] -=Direction.Hex.WEST
    if (direction == Direction.Size.SOUTH):
        layer_wall[cell1.x, cell1.y] -= Direction.Hex.SOUTH
        layer_wall[cell2.x, cell2.y] -= Direction.Hex.NORTH
    if (direction == Direction.Size.WEST):
        layer_wall[cell1.x, cell1.y] -= Direction.Hex.WEST
        layer_wall[cell2.x, cell2.y] -= Direction.Hex.EAST

    for i, line in enumerate(layer_id):
        for j, id in enumerate(line):
            if (id == cell2.get_id):
                layer_id[i, j] = cell1.get_id


m.mlx_key_hook(win, key_hook, None)
m.mlx_loop_hook(mlx, loop, None)
m.mlx_loop(mlx)
