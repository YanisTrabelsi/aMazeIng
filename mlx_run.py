from mlx import Mlx
import numpy.typing as npt
from mlx_draw import put_cell, put_path


class Mlx_handler:
    def __init__(
        self,
        width: int,
        height: int,
        cells: npt.NDArray,
        generator,
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = 40
        self.wall_size = 2
        self.win_width = width * self.cell_size + 50
        self.win_height = height * self.cell_size + 80
        self.color = 0xFF40E0D0

        self.m = Mlx()
        self.mlx = self.m.mlx_init()
        self.win = self.m.mlx_new_window(
            self.mlx,
            self.win_width,
            self.win_height,
            "Maze Generator",
        )

        def draw_path(color: int) -> None:
            cells = generator.cells
            target = next(
                (cell for cell in cells.flat if cell.is_exit),
                None,
            )

            if target is None or target.step < 0:
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
                    return

                put_path(
                    self.mlx,
                    self.win,
                    previous.y,
                    previous.x,
                    color,
                )
                target = previous

        def key_hook(keycode, param) -> None:
            if keycode == 48:  # 0
                self.m.mlx_loop_exit(self.mlx)

            elif keycode == 49:  # 1
                self.m.mlx_clear_window(self.mlx, self.win)
                generator.regenerate()

            elif keycode == 50:  # 2
                draw_path(0xFF00FF00)

            elif keycode == 51:  # 3
                draw_path(0xFF000000)

        def loop(params) -> None:
            for cell in generator.cells.flat:
                put_cell(
                    self.mlx,
                    self.win,
                    cell.y * self.cell_size + 25,
                    cell.x * self.cell_size + 25,
                    self.color,
                    cell.get_wall,
                )

            self.m.mlx_string_put(
                self.mlx,
                self.win,
                10,
                self.win_height - 40,
                0xFF0000FF,
                "[0]: EXIT",
            )
            self.m.mlx_string_put(
                self.mlx,
                self.win,
                150,
                self.win_height - 40,
                0xFF0000FF,
                "[1]: RELOAD",
            )
            self.m.mlx_string_put(
                self.mlx,
                self.win,
                300,
                self.win_height - 40,
                0xFF0000FF,
                "[2]: SHOW PATH",
            )
            self.m.mlx_string_put(
                self.mlx,
                self.win,
                470,
                self.win_height - 40,
                0xFF0000FF,
                "[3]: HIDE PATH",
            )

        self.m.mlx_key_hook(self.win, key_hook, self)
        self.m.mlx_loop_hook(self.mlx, loop, None)
        self.m.mlx_loop(self.mlx)
