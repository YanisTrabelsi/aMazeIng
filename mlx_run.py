from mlx import Mlx
import numpy.typing as npt
from mlx_draw import put_cell, put_path


class Mlx_handler:
    def __init__(self, width: int, height: int, cells: npt.NDArray, generator) -> None:
        self.width: int = width
        self.height: int = height
        self.cell_size: int = 40
        self.wall_size: int = 2
        self.win_width: int = width * self.cell_size + 50
        self.win_height: int = height * self.cell_size + 50
        self.color: int = 0xFF40E0D0
        self.m = Mlx()
        self.mlx = self.m.mlx_init()
        self.win = self.m.mlx_new_window(
            self.mlx, self.win_width, self.win_height, "Test"
        )

        def draw_path(color: int):
            target = next((cell for cell in cells.flat if cell.is_exit), None)

            if target is None:
                return

            put_path(
                self.mlx,
                self.win,
                target.y,
                target.x,
                color,
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
                    self.mlx,
                    self.win,
                    previous.y,
                    previous.x,
                    color,
                )

                target = previous

        def key_hook(keycode, param) -> None:
            if keycode == 113:
                self.m.mlx_loop_exit(self.mlx)
            if keycode == 114:
                self.m.mlx_destroy_window(self.mlx, self.win)
                self.m.mlx_loop_exit(self.mlx)
                generator.matrix_init()
                generator.init_layers()
                generator.init_cells()
                generator.run()
            if keycode == 112:
                draw_path(0xFF00FF00)
            if keycode == 111:
                draw_path(0xFF000000)

        def loop(params):
            for cell in cells.flat:
                put_cell(
                    self.mlx,
                    self.win,
                    cell.y * self.cell_size + 25,
                    cell.x * self.cell_size + 25,
                    self.color,
                    cell.get_wall,
                )

        self.m.mlx_key_hook(self.win, key_hook, self)
        self.m.mlx_loop_hook(self.mlx, loop, None)
        self.m.mlx_loop(self.mlx)
