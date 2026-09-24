from mlx import Mlx
import json
from parser import parser_tojson

parser_tojson()
with open("data.json") as f:
    data = json.load(f)

m = Mlx()

CELL_SIZE = int(data["CELL_SIZE"])
WALL_SIZE = int(data["WALL_SIZE"])
PADDING_X = 10
PADDING_Y = 7


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
            m.mlx_pixel_put(mlx, win, j + x + CELL_SIZE - WALL_SIZE, i + y, color)


def south(mlx, win, x: int, y: int, color: int):
    for i in range(WALL_SIZE):
        for j in range(CELL_SIZE):
            m.mlx_pixel_put(mlx, win, j + x, i + y + CELL_SIZE - WALL_SIZE, color)


def put_path(mlx, win, x: int, y: int, color: int):
    for i in range(CELL_SIZE):
        for j in range(CELL_SIZE):
            m.mlx_pixel_put(
                mlx,
                win,
                x * CELL_SIZE + i + PADDING_X,
                y * CELL_SIZE + j + PADDING_Y,
                color,
            )


def put_cell(mlx, win, x: int, y: int, color: int, hex: int) -> None:
    """
    Put a cell, walls are defined by hex value
    """

    if hex == 0x1:
        north(mlx, win, x, y, color)
    if hex == 0x2:
        east(mlx, win, x, y, color)
    if hex == 0x3:
        north(mlx, win, x, y, color)
        east(mlx, win, x, y, color)
    if hex == 0x4:
        south(mlx, win, x, y, color)
    if hex == 0x5:
        south(mlx, win, x, y, color)
        north(mlx, win, x, y, color)
    if hex == 0x6:
        south(mlx, win, x, y, color)
        east(mlx, win, x, y, color)
    if hex == 0x7:
        south(mlx, win, x, y, color)
        east(mlx, win, x, y, color)
        north(mlx, win, x, y, color)
    if hex == 0x8:
        west(mlx, win, x, y, color)
    if hex == 0x9:
        west(mlx, win, x, y, color)
        north(mlx, win, x, y, color)
    if hex == 0xA:
        west(mlx, win, x, y, color)
        east(mlx, win, x, y, color)
    if hex == 0xB:
        north(mlx, win, x, y, color)
        west(mlx, win, x, y, color)
        east(mlx, win, x, y, color)
    if hex == 0xC:
        south(mlx, win, x, y, color)
        west(mlx, win, x, y, color)
    if hex == 0xD:
        south(mlx, win, x, y, color)
        west(mlx, win, x, y, color)
        north(mlx, win, x, y, color)
    if hex == 0xE:
        south(mlx, win, x, y, color)
        east(mlx, win, x, y, color)
        west(mlx, win, x, y, color)
    if hex == 0xF:
        south(mlx, win, x, y, color)
        east(mlx, win, x, y, color)
        west(mlx, win, x, y, color)
        north(mlx, win, x, y, color)
