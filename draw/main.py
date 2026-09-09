from mlx import Mlx

m = Mlx()

def west(mlx, win, x: int, y: int, color: int):
    global m
    for i in range(30):
        for j in range(5):
            m.mlx_pixel_put(mlx, win, j + x, i + y, color) 

def north(mlx, win, x: int, y: int, color: int):
    global m
    for i in range(5):
        for j in range(30):
            m.mlx_pixel_put(mlx, win, j + x, i + y, color) 

def east(mlx, win, x: int, y: int, color: int):
    global m
    for i in range(30):
        for j in range(5):
            m.mlx_pixel_put(mlx, win, j + x + 25, i + y, color) 

def south(mlx, win, x: int, y: int, color: int):
    global m
    for i in range(5):
        for j in range(30):
            m.mlx_pixel_put(mlx, win, j + x, i + y + 25, color) 



def put_cell(mlx, win, x: int, y: int, color: int, hex: str) -> None:
    '''
        Put a cell, walls are defined by hex value
    '''

    if (hex == "1"):
        north(mlx, win, x, y, color)
    if (hex == "2"):
        east(mlx, win, x, y, color)
    if (hex == "3"):
        north(mlx, win, x, y, color); east(mlx, win, x, y, color)
    if (hex == "4"):
        south(mlx, win, x, y, color)
    if (hex == "5"):
        south(mlx, win, x, y, color); north(mlx, win, x, y, color)
    if (hex == "6"):
        south(mlx, win, x, y, color); east(mlx, win, x, y, color)
    if (hex == "7"):
        south(mlx, win, x, y, color); east(mlx, win, x, y, color); north(mlx, win, x, y, color)
    if (hex == "8"):
        west(mlx, win, x, y, color)
    if (hex == "9"):
        west(mlx, win, x, y, color); north(mlx, win, x, y, color)
    if (hex == "a"):
        west(mlx, win, x, y, color); east(mlx, win, x, y, color)
    if (hex == "b"):
        north(mlx, win, x, y, color); west(mlx, win, x, y, color); east(mlx, win, x, y, color)
    if (hex == "c"):
        south(mlx, win, x, y, color); west(mlx, win, x, y, color)
    if (hex == "d"):
        south(mlx, win, x, y, color); west(mlx, win, x, y, color); north(mlx, win, x, y, color)
    if (hex == "e"):
        south(mlx, win, x, y, color); east(mlx, win, x, y, color); west(mlx, win, x, y, color)
    if (hex == "f"):
        south(mlx, win, x, y, color); east(mlx, win, x, y, color); west(mlx, win, x, y, color); north(mlx, win, x, y, color)
