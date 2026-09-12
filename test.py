from mlx import Mlx
from utils import put_cell
import numpy as np
import numpy.typing as npt
import random as rd

BLACK = 0xFF000000
WHITE = 0xFFFFFFFF
RED   = 0xFFFF0000
GREEN = 0xFF00FF00
BLUE  = 0xFF0000FF

WIDTH = 15
HEIGHT = 20

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


m = Mlx()
mlx = m.mlx_init()
win = m.mlx_new_window(mlx, WIDTH * 30, HEIGHT * 30, "Test")

grid: npt.NDArray = np.zeros((HEIGHT, WIDTH, 3))
layer_id = grid[:, :, 0]
layer_wall = grid[:, :, 2]
layer_const = grid[:, :, 1]
layer_id = np.arange(0, WIDTH * HEIGHT).reshape(HEIGHT, WIDTH)
layer_const = np.arange(0, WIDTH * HEIGHT).reshape(HEIGHT, WIDTH)
layer_wall[:, :] = 0xf

def loop(param):
    draw()
    done = np.all(layer_id == layer_id.flat[0])
    if (not done):
        destroy_wall()

def key_hook(keycode, param):
    if (keycode == 113):
        m.mlx_loop_exit(mlx)

class Cell():
    def __init__(self, id: int):
        self.id = id
        self.x: int = self.id // WIDTH
        self.y: int = self.id % WIDTH
        self.wall: int = layer_wall[self.x, self.y]



def choose_cell() -> tuple[Cell, Cell]:
    '''Instanciate two Cell with different ID from layer_id'''
    print("===== LAYER_ID =====")
    print(layer_id)
    print("=====          =====")
    print("==== LAYER_CONST ===")
    print(layer_const)
    base_id = rd.choice(layer_const[:, :].ravel())
    print(base_id)
    cell1 = Cell(base_id)
    print(f"Cell 1 CONST: {cell1.id}   (x= {cell1.x}, y: {cell1.y})")

    if (cell1.x == 0 and cell1.y == 0):
        direction: list[int] = [1, WIDTH]
    elif (cell1.x == 0 and cell1.y == WIDTH - 1):
        direction: list[int] = [-1, WIDTH]
    elif (cell1.x == HEIGHT - 1 and cell1.y == 0):
        direction: list[int] = [1, -WIDTH]
    elif (cell1.x == HEIGHT - 1 and cell1.y == WIDTH - 1):
        direction: list[int] = [-1, -WIDTH]
    elif (cell1.x == 0):
        direction: list[int] = [-1, 1, WIDTH]
    elif (cell1.x == HEIGHT - 1):
        direction: list[int] = [-1, 1, -WIDTH]
    elif (cell1.y == 0):
        direction: list[int] = [1, WIDTH, -WIDTH]
    elif (cell1.y == WIDTH - 1):
        direction: list[int] = [-1, WIDTH, -WIDTH]
    else:
        direction: list[int] = [1, -1, WIDTH, -WIDTH]
    
    dir_choice = rd.choice(direction)
    print(f"direction : {dir_choice}")
    cell2 = Cell(base_id + dir_choice)
    print(f"Cell 2 ID: {cell2.id}   (x= {cell2.x}, y= {cell2.y})")

    if (layer_id[cell1.x, cell1.y] == layer_id[cell2.x , cell2.y]):
        return choose_cell()
    return (cell1, cell2)





def draw() -> None:
    m.mlx_clear_window(mlx, win)

    y: int = -1
    for v in layer_wall[:, :]:
        y += 1
        for i, v in enumerate(v):
            put_cell(mlx, win, i * 30, y * 30, RED, v)


def destroy_wall():
    cells: tuple[Cell, Cell] = choose_cell()
    cell1, cell2 = cells[0], cells[1]
    

    direction = cell2.id - cell1.id
    #print(f"direction {direction}")
    if (direction == Direction.Size.NORTH):
        print("REMOVE NORTH")
        layer_wall[cell1.x, cell1.y] = layer_wall[cell1.x, cell1.y] - Direction.Hex.NORTH
        layer_wall[cell2.x, cell2.y] = layer_wall[cell2.x, cell2.y] - Direction.Hex.SOUTH
    if (direction == Direction.Size.EAST):
        print("REMOVE EAST")
        layer_wall[cell1.x, cell1.y] = layer_wall[cell1.x, cell1.y] - Direction.Hex.EAST
        layer_wall[cell2.x, cell2.y] = layer_wall[cell2.x, cell2.y] - Direction.Hex.WEST
    if (direction == Direction.Size.SOUTH):
        print("REMOVE SOUTH")
        layer_wall[cell1.x, cell1.y] = layer_wall[cell1.x, cell1.y] - Direction.Hex.SOUTH
        layer_wall[cell2.x, cell2.y] = layer_wall[cell2.x, cell2.y] - Direction.Hex.NORTH
    if (direction == Direction.Size.WEST):
        print("REMOVE WEST")
        layer_wall[cell1.x, cell1.y] = layer_wall[cell1.x, cell1.y] - Direction.Hex.WEST
        layer_wall[cell2.x, cell2.y] = layer_wall[cell2.x, cell2.y] - Direction.Hex.EAST
    #print("#" * 10)
    id_to_remove = layer_id[cell2.x, cell2.y]
    for i, line in enumerate(layer_id):
        for j, id in enumerate(line):
            if (id == id_to_remove):
                layer_id[i, j] = layer_id[cell1.x, cell1.y]

    #print("#" * 10)

m.mlx_key_hook(win, key_hook, None)
m.mlx_loop_hook(mlx, loop, None)
m.mlx_loop(mlx)



