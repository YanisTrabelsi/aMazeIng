from __future__ import annotations

import random as rd
import numpy as np
import numpy.typing as npt


class MazeGenerator:
    """Maze generator built from the original functions (no MLX)."""

    class Hex:
        NORTH = 1
        EAST = 2
        SOUTH = 4
        WEST = 8

    PATERN = np.array(
        [
            [1, 0, 1, 0, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1],
        ]
    )

    class Cell:
        def __init__(self, maze: MazeGenerator, id: int):
            self.maze = maze
            self.const = id
            self.x: int = self.const // maze.width
            self.y: int = self.const % maze.width
            self.get_const = maze.layer_const[self.x, self.y]
            self.get_wall = maze.layer_wall[self.x, self.y]
            self.get_id = maze.layer_id[self.x, self.y]
            self.is_top: bool = self.get_const in maze.layer_const[:1, :]
            self.is_bottom: bool = self.get_const in maze.layer_const[-1:, :]
            self.is_left: bool = self.get_const in maze.layer_const[:, :1]
            self.is_right: bool = self.get_const in maze.layer_const[:, -1:]
            self.lcell: MazeGenerator.Cell | None = None
            self.rcell: MazeGenerator.Cell | None = None
            self.tcell: MazeGenerator.Cell | None = None
            self.bcell: MazeGenerator.Cell | None = None
            self.is_entry: bool = False
            self.is_exit: bool = False
            self.step: int = -1
            self.visited: bool = False
            self.go_north: MazeGenerator.Cell | None = None
            self.go_south: MazeGenerator.Cell | None = None
            self.go_east: MazeGenerator.Cell | None = None
            self.go_west: MazeGenerator.Cell | None = None
            self.is_fourty_two: bool = False
            cells = maze.cells
            if not self.is_left:
                self.lcell = cells[self.x, self.y - 1]
            if not self.is_right:
                self.rcell = cells[self.x, self.y + 1]
            if not self.is_top:
                self.tcell = cells[self.x - 1, self.y]
            if not self.is_bottom:
                self.bcell = cells[self.x + 1, self.y]

            self.valid_cells: list = [
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

    def __init__(
        self,
        width: int,
        height: int,
        seed=None,
        perfect: bool = True,
        entry: tuple[int, int] = (0, 0),
        exit: tuple[int, int] | None = None,
    ):
        self.width = width
        self.height = height
        self.seed = seed
        self.perfect = perfect
        self.entry = entry
        self.exit = exit if exit is not None else (height - 1, width - 1)
        self.patern_width = len(self.PATERN[0])
        self.patern_height = len(self.PATERN)
        self.size_north = -width
        self.size_east = 1
        self.size_south = width
        self.size_west = -1
        rd.seed(self.seed)
        self.init_layers()

    def matrix_init(self):
        grid: npt.NDArray = np.zeros((self.height, self.width, 3))
        return grid

    def init_layers(self) -> None:
        self.grid = self.matrix_init()
        self.layer_id = self.grid[:, :, 0]
        self.layer_const = self.grid[:, :, 1]
        self.layer_wall = self.grid[:, :, 2]
        self.layer_id = np.arange(0, self.width * self.height).reshape(
            self.height, self.width
        )
        self.layer_const = np.arange(0, self.width * self.height).reshape(
            self.height, self.width
        )
        self.layer_wall[:, :] = 0xF
        self.cells: npt.NDArray = np.empty((self.height, self.width), dtype=object)
        self.init_cells

    def sync(self) -> None:
        cells = self.cells
        for line in cells:
            for cell in line:
                cell.go_north = None
                cell.go_south = None
                cell.go_east = None
                cell.go_west = None
                cell.step = -1
                cell.get_wall = self.layer_wall[cell.x, cell.y]
                cell.get_id = self.layer_id[cell.x, cell.y]
                if not cell.is_left:
                    cell.lcell = cells[cell.x, cell.y - 1]
                if not cell.is_right:
                    cell.rcell = cells[cell.x, cell.y + 1]
                if not cell.is_top:
                    cell.tcell = cells[cell.x - 1, cell.y]
                if not cell.is_bottom:
                    cell.bcell = cells[cell.x + 1, cell.y]

    def sync_valid(self) -> None:
        for line in self.cells:
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

    def init_cells(self) -> None:
        for i, line in enumerate(self.layer_const):
            for j, id in enumerate(line):
                self.cells[i, j] = self.Cell(self, id)

    def fourty_two(self) -> None:
        sliced_w: int = (len(self.cells[0]) - self.patern_width) // 2
        sliced_h: int = (len(self.cells) - self.patern_height) // 2
        center = self.cells[
            sliced_h : sliced_h + self.patern_height,
            sliced_w : sliced_w + self.patern_width,
        ]

        for cell in center[self.PATERN == 1]:
            cell.is_fourty_two = True

    def choose_cell(self) -> tuple:
        """Instanciate two Cell with different ID from layer_id"""
        valid_ids: list = []
        for line in self.cells:
            for cell in line:
                if len(cell.valid_cells) > 0 and not cell.is_fourty_two:
                    valid_ids.append(cell)

        cell1 = rd.choice(valid_ids)
        valid_cells_id: list[int] = [
            cell.get_const
            for cell in cell1.valid_cells
            if cell is not None and not cell.is_fourty_two
        ]
        cell2 = self.Cell(self, rd.choice(valid_cells_id))
        self.cells[cell1.x, cell1.y] = cell1
        self.cells[cell2.x, cell2.y] = cell2
        return (cell1, cell2)

    def destroy_wall(self) -> None:
        self.sync()
        self.sync_valid()
        cells: tuple = self.choose_cell()
        cell1, cell2 = cells[0], cells[1]

        direction = cell2.const - cell1.const
        if direction == self.size_north:
            self.layer_wall[cell1.x, cell1.y] -= self.Hex.NORTH
            self.layer_wall[cell2.x, cell2.y] -= self.Hex.SOUTH
        if direction == self.size_east:
            self.layer_wall[cell1.x, cell1.y] -= self.Hex.EAST
            self.layer_wall[cell2.x, cell2.y] -= self.Hex.WEST
        if direction == self.size_south:
            self.layer_wall[cell1.x, cell1.y] -= self.Hex.SOUTH
            self.layer_wall[cell2.x, cell2.y] -= self.Hex.NORTH
        if direction == self.size_west:
            self.layer_wall[cell1.x, cell1.y] -= self.Hex.WEST
            self.layer_wall[cell2.x, cell2.y] -= self.Hex.EAST

        for i, line in enumerate(self.layer_id):
            for j, id in enumerate(line):
                if id == cell2.get_id:
                    self.layer_id[i, j] = cell1.get_id

    def walls(self, cell) -> list:
        value = int(self.layer_wall[cell.x, cell.y])
        result = []
        if value & self.Hex.NORTH:
            result.append("NORTH")
        if value & self.Hex.EAST:
            result.append("EAST")
        if value & self.Hex.SOUTH:
            result.append("SOUTH")
        if value & self.Hex.WEST:
            result.append("WEST")
        return result

    def choose_cell_2(self, cell1) -> tuple | None:
        wall_of_cell = self.walls(cell1)
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

    def destroy_wall_2(self, cell_origin) -> None:
        self.sync()
        self.sync_valid()
        pair = self.choose_cell_2(cell_origin)
        if pair is None:
            return
        cell1, cell2 = pair[0], pair[1]

        direction = cell2.const - cell1.const
        if direction == self.size_north:
            self.layer_wall[cell1.x, cell1.y] -= self.Hex.NORTH
            self.layer_wall[cell2.x, cell2.y] -= self.Hex.SOUTH
        if direction == self.size_east:
            self.layer_wall[cell1.x, cell1.y] -= self.Hex.EAST
            self.layer_wall[cell2.x, cell2.y] -= self.Hex.WEST
        if direction == self.size_south:
            self.layer_wall[cell1.x, cell1.y] -= self.Hex.SOUTH
            self.layer_wall[cell2.x, cell2.y] -= self.Hex.NORTH
        if direction == self.size_west:
            self.layer_wall[cell1.x, cell1.y] -= self.Hex.WEST
            self.layer_wall[cell2.x, cell2.y] -= self.Hex.EAST

        for i, line in enumerate(self.layer_id):
            for j, id in enumerate(line):
                if id == cell2.get_id:
                    self.layer_id[i, j] = cell1.get_id

    def run(self) -> None:
        """Generate the maze, then compute the path (original run())."""
        self.fourty_two()
        done = False
        while not done:
            self.destroy_wall()

            ids = set()
            for cell in self.cells.flat:
                if not cell.is_fourty_two:
                    ids.add(self.layer_id[cell.x, cell.y])
            done = len(ids) == 1

        self.sync()
        self.sync_valid()
        if not self.perfect:
            for cell in self.cells.flat:
                if not cell.is_fourty_two:
                    self.destroy_wall_2(cell)
        self.sync()
        self.sync_valid()
        self.find()

    def regenerate(self) -> None:
        """What the 'R' key did in key_hook (no reseed, new maze)."""
        self.init_layers()
        self.sync()
        self.sync_valid()
        self.init_cells()
        self.run()

    def init_path_cells(self) -> tuple:
        entry_cell = None
        exit_cell = None
        for cell in self.cells.flat:
            wall: int = cell.get_wall
            if cell.x == int(self.entry[0]) and cell.y == int(self.entry[1]):
                cell.is_entry = True
                entry_cell = cell
                cell.step = 0
            if cell.x == int(self.exit[0]) and cell.y == int(self.exit[1]):
                cell.is_exit = True
                exit_cell = cell

            if wall - self.Hex.WEST < 0:
                cell.go_west = cell.lcell
            else:
                wall -= self.Hex.WEST
            if wall - self.Hex.SOUTH < 0:
                cell.go_south = cell.bcell
            else:
                wall -= self.Hex.SOUTH
            if wall - self.Hex.EAST < 0:
                cell.go_east = cell.rcell
            else:
                wall -= self.Hex.EAST
            if wall - self.Hex.NORTH < 0:
                cell.go_north = cell.tcell
            else:
                wall -= self.Hex.NORTH

        return (entry_cell, exit_cell)

    def find(self) -> None:
        init_result = self.init_path_cells()
        cell_entry = init_result[0]

        step: int = 0
        next_targets: list = [cell_entry]
        target = next_targets[0]

        while not target.is_exit:
            target.visited = True

            neighbours = [
                cell
                for cell in (
                    target.go_north,
                    target.go_south,
                    target.go_east,
                    target.go_west,
                )
                if cell is not None and not cell.visited and not cell.is_fourty_two
            ]

            for cell in neighbours:
                cell.step = step + 1

            next_targets.remove(target)

            if len(next_targets) == 0:
                step += 1
                next_targets = [
                    cell
                    for cell in self.cells.flat
                    if cell.step == step and not cell.visited and not cell.is_fourty_two
                ]

                if len(next_targets) == 0:
                    # Aucun chemin vers la sortie
                    return

            target = rd.choice(next_targets)

    def get_path(self) -> list:
        """Cells of the path, from the exit back to the entry."""
        target = next((cell for cell in self.cells.flat if cell.is_exit), None)

        if target is None:
            return []

        path = [target]
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

            path.append(previous)
            target = previous
        return path

    def write_output(self, path: str) -> None:
        with open(path, "w") as f:
            for line in self.layer_wall:
                for id in line:
                    f.write(hex(int(id))[2:])
                f.write("\n")


if __name__ == "__main__":
    maze = MazeGenerator(15, 15, 42, True, (0, 0), (14, 14))
    maze.run()
