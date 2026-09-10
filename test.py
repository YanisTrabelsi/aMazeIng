from mlx import Mlx
from utils import put_cell
import numpy as np
import numpy.typing as npt
import random as rd
import time

BLACK = 0xFF000000
WHITE = 0xFFFFFFFF
RED   = 0xFFFF0000
GREEN = 0xFF00FF00
BLUE  = 0xFF0000FF

WIDTH = 4
HEIGHT = 5

class Direction():
    class Hex():
        NORTH = 1
        EAST = 2
        SOUTH = 4
        WEST = 8

    class Size():
        NORTH = -1
        EAST = HEIGHT
        SOUTH = 1
        WEST = -HEIGHT


def key_event(keycode, param):
    if keycode == 113:
        m.mlx_loop_exit(mlx)

m = Mlx()
mlx = m.mlx_init()
win = m.mlx_new_window(mlx, 700, 1000, "Test")

grid: npt.NDArray = np.zeros((WIDTH, HEIGHT, 2))
layer_id = grid[:, :, 0]
layer_wall = grid[:, :, 1]

layer_id = np.arange(0, WIDTH * HEIGHT).reshape(WIDTH, HEIGHT)
layer_wall[:, :] = 0xf

class Cell():
    def __init__(self, id: int):
        self.id = id
        self.x: int = id % WIDTH
        self.y: int = id // WIDTH
        self.wall: int = layer_wall[self.x, self.y]


def choose_cell() -> tuple[Cell, Cell]:
    '''Instanciate two Cell with different ID from layer_id'''
    direction: list[int] = [1, -1, HEIGHT, -HEIGHT]
    valid_cells: npt.NDArray = layer_id[1:-1, 1:-1].ravel()
    base_id = rd.choice(valid_cells)
    dir_choice = rd.choice(direction)
    print(f"direction__ : {dir_choice}")
    cell1 = Cell(base_id)
    cell2 = Cell(base_id + dir_choice)
    print(f"Cell 1 ID: {cell1.id}")
    print(f"Cell 2 ID: {cell2.id}")

    if (layer_id[cell1.x, cell1.y] == layer_id[cell2.x , cell2.y]):
        return choose_cell()
    return (cell1, cell2)

def destroy_wall():
    cells: tuple[Cell, Cell] = choose_cell()
    cell1, cell2 = cells[0], cells[1]
    cell2_id = cell2.id
    

    direction = cell2.id - cell1.id
    print(f"direction {direction}")
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
    print("#" * 10)
    for i, line in enumerate(layer_id):
        print(f"LINE {i}: {line}")
        for j, id in enumerate(line):
            if (id == cell2_id):
                layer_id[i, j] = cell1.id
        print("#" * 10)




for _ in range(300):
    destroy_wall()

y: int = -1
for v in layer_wall[:, :]:
    y += 1
    for i, v in enumerate(v):
        put_cell(mlx, win, i * 30, y * 30, RED, v)


m.mlx_key_hook(win, key_event, None)
m.mlx_loop(mlx)

