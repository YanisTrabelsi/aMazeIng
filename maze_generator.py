from path import find
from mlx import Mlx
from draw import put_cell, put_path
import numpy as np
import numpy.typing as npt
import random as rd
import json


with open("data.json") as f:
    data = json.load(f)
    print(data)


rd.seed(data["SEED"])
# CONST VARIABLES
WIDTH = int(data["WIDTH"])
HEIGHT = int(data["HEIGHT"])
CELL_SIZE = int(data["CELL_SIZE"])
WIN_WIDTH = WIDTH * CELL_SIZE + 20
WIN_HEIGHT = HEIGHT * CELL_SIZE + 40
PADDING_X = 10
PADDING_Y = 7
IS_PERFECT = data["PERFECT"]
PATERN = np.array(
    [
        [0, 1, 0, 1, 0, 1, 1, 1],
        [0, 1, 0, 1, 0, 0, 0, 1],
        [0, 1, 1, 1, 0, 1, 1, 1],
        [0, 0, 0, 1, 0, 1, 0, 0],
        [0, 0, 0, 1, 0, 1, 1, 1],
    ]
)

PATERN_WIDTH = len(PATERN[0])
PATERN_HEIGHT = len(PATERN)

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
        self.is_fourty_two: bool = False
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
            if cell is not None
            and cell.get_id != self.get_id
            and not cell.is_fourty_two
        ]

    @staticmethod
    def sync():
        for line in cells:
            for cell in line:
                cell.go_north = None
                cell.go_south = None
                cell.go_east = None
                cell.go_west = None
                cell.step = -1
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
                    if (
                        subcell is not None
                        and subcell.get_id != cell.get_id
                        and not subcell.is_fourty_two
                    )
                ]

    @staticmethod
    def init_cells():
        for i, line in enumerate(layer_const):
            for j, id in enumerate(line):
                cells[i, j] = Cell(id)


Cell.init_cells()


def draw_path():
    target = next((cell for cell in cells.flat if cell.is_exit), None)

    if target is None:
        return

    put_path(
        mlx,
        win,
        target.y,
        target.x,
        int(data["GREEN"], 16),
    )

    while not target.is_entry:
        neighbours = [
            target.go_north,
            target.go_south,
            target.go_east,
            target.go_west,
        ]

        previous = next(
            (
                cell
                for cell in neighbours
                if cell is not None and cell.step == target.step - 1
            ),
            None,
        )

        if previous is None:
            raise RuntimeError(
                f"Impossible de remonter le chemin depuis "
                f"({target.x}, {target.y}), step={target.step}"
            )

        put_path(
            mlx,
            win,
            previous.y,
            previous.x,
            int(data["GREEN"], 16),
        )

        target = previous


def draw() -> None:
    matrix_init()

    draw_path()
    y: int = -1
    for v in layer_wall[:, :]:
        y += 1
        for i, v in enumerate(v):
            put_cell(
                mlx,
                win,
                i * CELL_SIZE + PADDING_X,
                y * CELL_SIZE + PADDING_Y,
                int(data["TURQUOISE"], 16),
                v,
            )
    for cell in cells.flat:
        if cell.is_fourty_two:
            put_path(mlx, win, cell.y, cell.x, int(data["VIOLET"], 16))
    m.mlx_string_put(mlx, win, 10, WIN_HEIGHT - 30, 0xFF0000FF, "[Q]: EXIT")
    m.mlx_string_put(mlx, win, 165, WIN_HEIGHT - 30, 0xFF0000FF, "[R]: RELOAD")


def loop(param) -> None:
    m.mlx_clear_window(mlx, win)
    draw()


def key_hook(keycode, param) -> None:
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
        Cell.sync()
        Cell.sync_valid()
        Cell.init_cells()
        run()


def fourty_two():
    sliced_w: int = (len(cells[0]) - PATERN_WIDTH) // 2
    sliced_h: int = (len(cells) - PATERN_HEIGHT) // 2
    center = cells[
        sliced_h : sliced_h + PATERN_HEIGHT, sliced_w : sliced_w + PATERN_WIDTH
    ]

    for cell in center[PATERN == 1]:
        cell.is_fourty_two = True


def choose_cell() -> tuple[Cell, Cell]:
    """Instanciate two Cell with different ID from layer_id"""
    valid_ids: list[Cell] = []
    for line in cells:
        for cell in line:
            if len(cell.valid_cells) > 0 and not cell.is_fourty_two:
                valid_ids.append(cell)

    cell1 = rd.choice(valid_ids)
    valid_cells_id: list[int] = [
        cell.get_const
        for cell in cell1.valid_cells
        if cell is not None and not cell.is_fourty_two
    ]
    cell2 = Cell(rd.choice(valid_cells_id))
    cells[cell1.x, cell1.y] = cell1
    cells[cell2.x, cell2.y] = cell2
    return (cell1, cell2)


def destroy_wall():
    #print(f"\n\n{layer_id}")
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

    for i, line in enumerate(layer_id):
        for j, id in enumerate(line):
            if id == cell2.get_id:
                layer_id[i, j] = cell1.get_id


def walls(cell: Cell):
    value = int(layer_wall[cell.x, cell.y])
    result = []
    if value & Direction.Hex.NORTH:
        result.append("NORTH")
    if value & Direction.Hex.EAST:
        result.append("EAST")
    if value & Direction.Hex.SOUTH:
        result.append("SOUTH")
    if value & Direction.Hex.WEST:
        result.append("WEST")
    return result


def choose_cell_2(cell1: Cell) -> tuple[Cell, Cell] | None:
    wall_of_cell = walls(cell1)
    if len(wall_of_cell) <= 2:
        return None
    candidates = []
    for direction in wall_of_cell:
        if direction == "NORTH":
            if not cell1.is_top and not cell1.tcell.is_fourty_two:
                candidates.append(cell1.tcell)
        if direction == "SOUTH":
            if not cell1.is_bottom and not cell1.bcell.is_fourty_two:
                candidates.append(cell1.bcell)
        if direction == "EAST":
            if not cell1.is_right and not cell1.rcell.is_fourty_two:
                candidates.append(cell1.rcell)
        if direction == "WEST":
            if not cell1.is_left and not cell1.lcell.is_fourty_two:
                candidates.append(cell1.lcell)
    if not candidates:
        return None
    return (cell1, rd.choice(candidates))


def destroy_wall_2(cell_origin: Cell):
    Cell.sync()
    Cell.sync_valid()
    pair: tuple[Cell, Cell] | None = choose_cell_2(cell_origin)
    if pair is None:
        return
    cell1, cell2 = pair[0], pair[1]

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

    for i, line in enumerate(layer_id):
        for j, id in enumerate(line):
            if id == cell2.get_id:
                layer_id[i, j] = cell1.get_id


def run():
    fourty_two()
    done = False
    while not done:
        destroy_wall()

        ids = set()
        for cell in cells.flat:
            if not cell.is_fourty_two:
                ids.add(layer_id[cell.x, cell.y])
        done = len(ids) == 1

    Cell.sync()
    Cell.sync_valid()
    if IS_PERFECT == "False":
        half = False
        for cell in cells.flat:
            #if half:
                if not cell.is_fourty_two:
                    destroy_wall_2(cell)
                #half = False
            #else:
                #half = True
    Cell.sync()
    Cell.sync_valid()
    find(cells, Direction)


if __name__ == "__main__":
    run()
    m.mlx_key_hook(win, key_hook, None)
    m.mlx_loop_hook(mlx, loop, None)
    m.mlx_loop(mlx)

    with open(data["OUTPUT_FILE"], "w") as f:
        for line in layer_wall:
            for id in line:
                f.write(hex(int(id))[2:])
            f.write("\n")
