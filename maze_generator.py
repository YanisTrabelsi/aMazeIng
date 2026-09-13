from mlx import Mlx
from utils import put_cell
import numpy as np
import numpy.typing as npt
import random as rd
from parser import parser_tojson
import json

parser_tojson()
with open('data.json') as f:
    data = json.load(f)


# CONST VARIABLES
WIDTH = int(data["WIDTH"])
HEIGHT = int(data["HEIGHT"])
WIN_WIDTH = WIDTH * 30
WIN_HEIGHT = HEIGHT * 30 + 40

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

class Cell():
    def __init__(self, id: int):
        self.const = id
        self.x: int = self.const // WIDTH
        self.y: int = self.const % WIDTH
        self.wall: int = layer_wall[self.x, self.y]
        self.pos = layer_const[self.x, self.y]

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
        class Corner():
            TL = layer_const[0, 0]
            TR = layer_const[0, -1]
            BL = layer_const[-1, 0]
            BR = layer_const[-1, -1]

        class Border():
            L = layer_const[:, 0]
            R = layer_const[:, -1]
            T = layer_const[0, :]
            B = layer_const[-1, :]




def draw() -> None:
    matrix_init()
    m.mlx_clear_window(mlx, win)

    y: int = -1
    for v in layer_wall[:, :]:
        y += 1
        for i, v in enumerate(v):
            put_cell(mlx, win, i * 30, y * 30, int(data["TURQUOISE"], 16), v)
    m.mlx_string_put(mlx, win, 10, WIN_HEIGHT - 33, 0xff0000ff, "[Q]: EXIT")
    m.mlx_string_put(mlx, win, 165, WIN_HEIGHT - 33, 0xff0000ff, "[R]: RELOAD")


def loop(param):
    draw()
    done = np.all(layer_id == layer_id.flat[0])
    if (not done):
        destroy_wall()

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

    if (cell1.pos == Direction.Location.Corner.TL):
        direction: list[int] = [1, WIDTH]
    elif (cell1.pos == Direction.Location.Corner.TR):
        direction: list[int] = [-1, WIDTH]
    elif (cell1.pos == Direction.Location.Corner.BL):
        direction: list[int] = [1, -WIDTH]
    elif (cell1.pos == Direction.Location.Corner.BR):
        direction: list[int] = [-1, -WIDTH]
    elif (cell1.pos in Direction.Location.Border.T):
        direction: list[int] = [-1, 1, WIDTH]
    elif (cell1.pos in Direction.Location.Border.B):
        direction: list[int] = [-1, 1, -WIDTH]
    elif (cell1.pos in Direction.Location.Border.L):
        direction: list[int] = [1, WIDTH, -WIDTH]
    elif (cell1.pos in Direction.Location.Border.R):
        direction: list[int] = [-1, WIDTH, -WIDTH]
    else:
        direction: list[int] = [1, -1, WIDTH, -WIDTH]
    
    dir_choice = rd.choice(direction)
    cell2 = Cell(base_id + dir_choice)

    if (layer_id[cell1.x, cell1.y] == layer_id[cell2.x , cell2.y]):
        return choose_cell()
    return (cell1, cell2)




def destroy_wall():
    cells: tuple[Cell, Cell] = choose_cell()
    cell1, cell2 = cells[0], cells[1]
    

    direction = cell2.const - cell1.const
    ##print(f"direction {direction}")
    if (direction == Direction.Size.NORTH):
        layer_wall[cell1.x, cell1.y] = layer_wall[cell1.x, cell1.y] - Direction.Hex.NORTH
        layer_wall[cell2.x, cell2.y] = layer_wall[cell2.x, cell2.y] - Direction.Hex.SOUTH
    if (direction == Direction.Size.EAST):
        layer_wall[cell1.x, cell1.y] = layer_wall[cell1.x, cell1.y] - Direction.Hex.EAST
        layer_wall[cell2.x, cell2.y] = layer_wall[cell2.x, cell2.y] - Direction.Hex.WEST
    if (direction == Direction.Size.SOUTH):
        layer_wall[cell1.x, cell1.y] = layer_wall[cell1.x, cell1.y] - Direction.Hex.SOUTH
        layer_wall[cell2.x, cell2.y] = layer_wall[cell2.x, cell2.y] - Direction.Hex.NORTH
    if (direction == Direction.Size.WEST):
        layer_wall[cell1.x, cell1.y] = layer_wall[cell1.x, cell1.y] - Direction.Hex.WEST
        layer_wall[cell2.x, cell2.y] = layer_wall[cell2.x, cell2.y] - Direction.Hex.EAST
    id_to_remove = layer_id[cell2.x, cell2.y]
    for i, line in enumerate(layer_id):
        for j, id in enumerate(line):
            if (id == id_to_remove):
                layer_id[i, j] = layer_id[cell1.x, cell1.y]


m.mlx_key_hook(win, key_hook, None)
m.mlx_loop_hook(mlx, loop, None)
m.mlx_loop(mlx)
