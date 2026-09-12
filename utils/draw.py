from mlx import Mlx

m = Mlx()

CELL_SIZE = 30
WALL_SIZE = 5

def west(mlx, win, x: int, y: int, color: int):
    for i in range(CELL_SIZE):
        for j in range(WALL_SIZE):
            m.mlx_pixel_put(mlx, win, j + x, i + y, color) 

def north(mlx, win, x: int, y: int, color: int):
    for i in range(WALL_SIZE):
        for j in range(CELL_SIZE):
            m.mlx_pixel_put(mlx, win, j + x, i + y, color) 

def east(mlx, win, x: int, y: int, color: int):
    for i in range(CELL_SIZE):
        for j in range(WALL_SIZE):
            m.mlx_pixel_put(mlx, win, j + x + 25, i + y, color) 

def south(mlx, win, x: int, y: int, color: int):
    for i in range(WALL_SIZE):
        for j in range(CELL_SIZE):
            m.mlx_pixel_put(mlx, win, j + x, i + y + 25, color) 



def put_cell(mlx, win, x: int, y: int, color: int, hex: int) -> None:
    '''
        Put a cell, walls are defined by hex value
    '''

    if (hex == 0x1):
        north(mlx, win, x, y, color)
    if (hex == 0x2):
        east(mlx, win, x, y, color)
    if (hex == 0x3):
        north(mlx, win, x, y, color); east(mlx, win, x, y, color)
    if (hex == 0x4):
        south(mlx, win, x, y, color)
    if (hex == 0x5):
        south(mlx, win, x, y, color); north(mlx, win, x, y, color)
    if (hex == 0x6):
        south(mlx, win, x, y, color); east(mlx, win, x, y, color)
    if (hex == 0x7):
        south(mlx, win, x, y, color); east(mlx, win, x, y, color); north(mlx, win, x, y, color)
    if (hex == 0x8):
        west(mlx, win, x, y, color)
    if (hex == 0x9):
        west(mlx, win, x, y, color); north(mlx, win, x, y, color)
    if (hex == 0xa):
        west(mlx, win, x, y, color); east(mlx, win, x, y, color)
    if (hex == 0xb):
        north(mlx, win, x, y, color); west(mlx, win, x, y, color); east(mlx, win, x, y, color)
    if (hex == 0xc):
        south(mlx, win, x, y, color); west(mlx, win, x, y, color)
    if (hex == 0xd):
        south(mlx, win, x, y, color); west(mlx, win, x, y, color); north(mlx, win, x, y, color)
    if (hex == 0xe):
        south(mlx, win, x, y, color); east(mlx, win, x, y, color); west(mlx, win, x, y, color)
    if (hex == 0xf):
        south(mlx, win, x, y, color); east(mlx, win, x, y, color); west(mlx, win, x, y, color); north(mlx, win, x, y, color)
