import json
import numpy.typing as npt
import random as rd


with open("data.json") as f:
    data = json.load(f)

ENTRY = str(data["ENTRY"]).split(",")
EXIT = str(data["EXIT"]).split(",")


def init_cells(cells: npt.NDArray, Direction) -> tuple:
    entry_cell = None
    exit_cell = None
    for cell in cells.flat:
        wall: int = cell.get_wall
        if cell.x == int(ENTRY[0]) and cell.y == int(ENTRY[1]):
            cell.is_entry = True
            entry_cell = cell
        if cell.x == int(EXIT[0]) and cell.y == int(EXIT[1]):
            cell.is_exit = True
            exit_cell = cell

        if wall - Direction.Hex.WEST < 0:
            cell.go_west = cell.lcell
        else:
            wall -= Direction.Hex.WEST
        if wall - Direction.Hex.SOUTH < 0:
            cell.go_south = cell.bcell
        else:
            wall -= Direction.Hex.SOUTH
        if wall - Direction.Hex.EAST < 0:
            cell.go_east = cell.rcell
        else:
            wall -= Direction.Hex.EAST
        if wall - Direction.Hex.NORTH < 0:
            cell.go_north = cell.tcell
        else:
            wall -= Direction.Hex.NORTH

    return (entry_cell, exit_cell)


def find(cells: npt.NDArray, Direction):
    init_result = init_cells(cells, Direction)
    cell_entry = init_result[0]
    for cell in cells.flat:
        print(cell.go_south)

    step: int = 0
    next_targets: list = [cell_entry]
    target = next_targets[0]
    while not target.is_exit:
        target.visited = True

        neighbours: list = [
            cell
            for cell in (
                target.go_north,
                target.go_south,
                target.go_east,
                target.go_west,
            )
            if cell is not None and cell.visited is False
        ]
        print(neighbours)
        for cell in neighbours:
            cell.step = step + 1
        next_targets.remove(target)
        print(next_targets)
        if len(next_targets) == 0:
            step += 1
            next_targets = [
                cell
                for cell in cells.flat
                if cell.step == step and cell.visited is False
            ]
            for cell in cells.flat:
                print(cell.step)
            print(next_targets)
        target = rd.choice(next_targets)

    print("PATH FOUNDED")
